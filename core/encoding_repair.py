from dataclasses import dataclass
from typing import Dict
import time


@dataclass
class EncodingRepairRequest:
    """
    Encoding Repair 用の入力モデル。

    - text:
        現在モジバケしているかもしれないテキスト（Pythonのstr）
    - assume_current_encoding:
        現在のstrを bytes に戻すときに利用するエンコーディング。
        典型的なモジバケでは "latin1" や "cp1252" が多い。
    - target_encoding:
        本来意図していたエンコーディング（例: "utf-8", "cp932" など）
    """

    text: str
    assume_current_encoding: str = "latin1"
    target_encoding: str = "utf-8"


def repair_encoding(req: EncodingRepairRequest) -> Dict:
    """
    シンプルなモジバケ修正ロジック v0.2

    想定ケース:
      - 本来は bytes(Shift_JIS 等) → 誤って UTF-8 として解釈された文字列
      - 現在の Python 文字列を「assume_current_encoding」としてエンコードし直し、
        それを target_encoding としてデコードし直すことで復元を試みる。

    v0.2 のポイント:
      - 変換結果が空文字列または空白のみの場合、
        「修復に失敗した」とみなし元のテキストを返す（非破壊）。
    """
    started_at = time.perf_counter()

    original_text = req.text
    strategy = "reinterpret_bytes"
    status = "ok"

    try:
        # 現在の str を「バイト列に戻す」
        raw_bytes = original_text.encode(req.assume_current_encoding, errors="ignore")

        # それをターゲットエンコーディングとして再解釈
        fixed_text = raw_bytes.decode(req.target_encoding, errors="ignore")
    except LookupError:
        # 不正なエンコーディング名が来た場合
        fixed_text = original_text
        status = "invalid_encoding_name"
        strategy = "fallback_original"

    # v0.2: 無意味な出力（空 or 空白のみ）は「修復失敗」とみなして元に戻す
    if not fixed_text or fixed_text.strip() == "":
        fixed_text = original_text
        status = "no_meaningful_output"
        strategy = "fallback_original"

    changed = fixed_text != original_text
    execution_ms = (time.perf_counter() - started_at) * 1000

    return {
        "result": {
            "original_text": original_text,
            "fixed_text": fixed_text,
            "assume_current_encoding": req.assume_current_encoding,
            "target_encoding": req.target_encoding,
            "changed": changed,
        },
        "meta": {
            "version": "0.2.0",
            "execution_ms": execution_ms,
            "strategy": strategy,
            "status": status,
        },
    }

