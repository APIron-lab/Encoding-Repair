# core/encoding_repair_v2.py

from __future__ import annotations

import base64
import time
from dataclasses import dataclass
from typing import Literal, Optional, List, Tuple

from pydantic import BaseModel, Field, ValidationError


EncodingMode = Literal["auto", "manual"]


class EncodingRepairRequestV2(BaseModel):
    """
    v2.0 リクエストモデル（Base64 専用）

    - mode: "auto" | "manual"
    - raw_bytes_base64: 元データのバイト列を Base64 文字列化したもの
    - assume_current_encoding: manual 時のみ必須（auto 時は無視してもよい）
    - target_encoding: 出力テキストのエンコーディング（基本 "utf-8"）
    """
    mode: EncodingMode = Field(default="auto")
    raw_bytes_base64: str = Field(..., min_length=1)
    assume_current_encoding: Optional[str] = None
    target_encoding: str = "utf-8"


class EncodingRepairResult(BaseModel):
    fixed_text: str
    target_encoding: str = "utf-8"
    changed: bool


class EncodingRepairMeta(BaseModel):
    version: str = "2.0.0"
    mode_used: EncodingMode
    detected_path: Optional[str] = None
    confidence: float
    status: str
    execution_ms: float
    input_bytes_length: int


class EncodingRepairResponse(BaseModel):
    result: EncodingRepairResult
    meta: EncodingRepairMeta


@dataclass
class CandidateResult:
    encoding: str
    text: str
    score: float
    had_error: bool


# Auto モードで試行するエンコーディング候補
AUTO_CANDIDATE_ENCODINGS: List[str] = [
    "utf-8",
    "cp932",    # Windows-31J / Shift_JIS 相当
    "euc_jp",
    "latin1",
]


def _decode_base64(raw_bytes_base64: str) -> Tuple[Optional[bytes], Optional[str]]:
    """Base64 文字列をデコード。失敗時は (None, 'error_status') を返す。"""
    try:
        decoded = base64.b64decode(raw_bytes_base64, validate=True)
        return decoded, None
    except Exception:
        return None, "invalid_base64"


def _score_text(text: str, had_error: bool) -> float:
    """
    非常にシンプルなスコアリング関数。

    - 日本語らしい文字（ひらがな・カタカナ・漢字）の比率
    - 制御文字（タブ/改行以外）の比率
    - デコードエラー発生フラグ

    を元にラフなスコアを算出する。
    """
    if not text:
        return -1.0

    length = len(text)
    jp_count = 0
    bad_control = 0

    for ch in text:
        code = ord(ch)
        # ひらがな・カタカナ・漢字・全角カナ
        if (
            0x3040 <= code <= 0x309F  # ひらがな
            or 0x30A0 <= code <= 0x30FF  # カタカナ
            or 0x4E00 <= code <= 0x9FFF  # CJK
            or 0xFF66 <= code <= 0xFF9D  # 半角カナ
        ):
            jp_count += 1
        # 制御文字（タブ/改行以外）はペナルティ
        if code < 32 and ch not in ("\t", "\r", "\n"):
            bad_control += 1

    jp_ratio = jp_count / length
    bad_ratio = bad_control / length

    score = jp_ratio - (bad_ratio * 2.0)
    if had_error:
        score -= 0.5

    return score


def _try_decode(raw: bytes, encoding: str) -> CandidateResult:
    """指定エンコーディングでデコードし、スコア付き候補として返す。"""
    had_error = False
    try:
        text = raw.decode(encoding, errors="strict")
    except UnicodeDecodeError:
        # strict でダメなら ignore で文字を落としつつデコード
        text = raw.decode(encoding, errors="ignore")
        had_error = True

    score = _score_text(text, had_error)
    return CandidateResult(encoding=encoding, text=text, score=score, had_error=had_error)


def _auto_repair(raw: bytes, target_encoding: str) -> Tuple[str, bool, Optional[str], float, str]:
    """
    Auto モードの中核ロジック。
    - 複数エンコーディング候補でデコード
    - スコアが最も高いものを採用
    - ただし UTF-8 との差が小さい場合は UTF-8 を優先して「変更なし」とする
    """
    input_len = len(raw)

    candidates: List[CandidateResult] = []
    for enc in AUTO_CANDIDATE_ENCODINGS:
        candidates.append(_try_decode(raw, enc))

    # ベースラインとして utf-8 を探す
    utf8_candidate = next((c for c in candidates if c.encoding == "utf-8"), None)

    # 最良候補
    best = max(candidates, key=lambda c: c.score, default=None)

    if best is None or utf8_candidate is None:
        # 何もまともにデコードできなかった場合
        try:
            fallback_text = raw.decode("utf-8", errors="ignore")
        except Exception:
            fallback_text = ""
        return fallback_text, False, None, 0.0, "no_meaningful_output"

    # スコア差で安全判定
    margin = 0.15  # UTF-8 と比べてこれ以上改善していれば変更を採用
    if best.encoding == "utf-8" or best.score <= utf8_candidate.score + margin:
        # UTF-8 と大差ないか、UTF-8 が最良 → 変更しない
        return utf8_candidate.text, False, "utf-8->" + target_encoding, utf8_candidate.score, "ok"

    # UTF-8 より明確に良いエンコーディングが見つかった
    detected_path = f"{best.encoding}->{target_encoding}"
    return best.text, True, detected_path, best.score, "ok"


def _manual_repair(
    raw: bytes,
    assume_current_encoding: Optional[str],
    target_encoding: str,
) -> Tuple[str, bool, Optional[str], float, str]:
    """
    Manual モード。

    v2.0 ではシンプルに：
    - raw バイト列を assume_current_encoding でデコード
    - そのテキストを target_encoding として返す（通常 target_encoding == assume_current_encoding）

    という動作とする。
    """
    if not assume_current_encoding:
        # manual なのにエンコーディングが指定されていない
        return "", False, None, 0.0, "invalid_manual_mode_params"

    try:
        text = raw.decode(assume_current_encoding, errors="strict")
        had_error = False
    except UnicodeDecodeError:
        # どうしても無理な場合は ignore で復元
        text = raw.decode(assume_current_encoding, errors="ignore")
        had_error = True

    score = _score_text(text, had_error)
    detected_path = f"{assume_current_encoding}->{target_encoding}"
    return text, True, detected_path, score, "ok"


def repair_encoding_v2(request: EncodingRepairRequestV2) -> EncodingRepairResponse:
    """
    v2.0 のメインエントリ。

    - Base64 をデコード
    - mode に応じて auto / manual ロジックを実行
    - Safe filter ポリシーに基づき result/meta を組み立てる
    """
    started = time.perf_counter()

    raw, base64_error = _decode_base64(request.raw_bytes_base64)
    if base64_error is not None or raw is None:
        elapsed = (time.perf_counter() - started) * 1000.0
        result = EncodingRepairResult(
            fixed_text="",
            target_encoding=request.target_encoding,
            changed=False,
        )
        meta = EncodingRepairMeta(
            mode_used=request.mode,
            detected_path=None,
            confidence=0.0,
            status=base64_error or "invalid_base64",
            execution_ms=elapsed,
            input_bytes_length=0,
        )
        return EncodingRepairResponse(result=result, meta=meta)

    if request.mode == "manual":
        fixed_text, changed, detected_path, score, status = _manual_repair(
            raw=raw,
            assume_current_encoding=request.assume_current_encoding,
            target_encoding=request.target_encoding,
        )
    else:
        fixed_text, changed, detected_path, score, status = _auto_repair(
            raw=raw,
            target_encoding=request.target_encoding,
        )

    elapsed = (time.perf_counter() - started) * 1000.0
    input_len = len(raw)

    # スコアをそのまま 0〜1 に正規化はしていないが、便宜上 0〜1 クランプ
    confidence = max(0.0, min(1.0, (score + 1.0) / 2.0))

    result = EncodingRepairResult(
        fixed_text=fixed_text,
        target_encoding=request.target_encoding,
        changed=changed,
    )
    meta = EncodingRepairMeta(
        mode_used=request.mode,
        detected_path=detected_path,
        confidence=confidence,
        status=status,
        execution_ms=elapsed,
        input_bytes_length=input_len,
    )
    return EncodingRepairResponse(result=result, meta=meta)

