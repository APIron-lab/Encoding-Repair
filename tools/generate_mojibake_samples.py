#!/usr/bin/env python3
"""
APIron Mojibake Test Suite - Essential 5

以下の 5 種類の「あるある文字化け」ファイルを samples/ 配下に生成する。

  01_utf8_to_latin1.txt
      - 典型的な UTF-8 → Latin-1 誤解釈のモジバケ（"ãƒ†ã‚¹ãƒˆ" 型）
  02_utf8_to_cp932_mojibake.txt
      - UTF-8 バイト列を CP932 と誤解釈したときのモジバケ（"縺ゅ↑縺九ｉ" 型）
  03_cp932_original_japanese.txt
      - 元データが CP932（Shift_JIS 系）で保存された日本語テキスト
  04_double_mojibake.txt
      - 「UTF-8 → Latin-1 → CP932」など二重化けを模したサンプル
  05_invalid_bytes.txt
      - 0x81 / 0x00 等の不正バイトを含むログ風バイト列

これらは **テスト用サンプル** であり、実業務データや個人情報は含まない。
"""

import pathlib


BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "samples"


def ensure_samples_dir() -> None:
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)


def generate_01_utf8_to_latin1(path: pathlib.Path) -> None:
    """
    01_utf8_to_latin1.txt

    「UTF-8 な日本語文字列」を UTF-8 バイト列 → Latin-1 と誤解釈 → その
    モジバケ文字列を UTF-8 で保存したサンプル。

    例:
        original: "テスト"
        utf8 bytes: e3 83 86 e3 82 b9 e3 83 88
        latin1 decode → "ãƒ†ã‚¹ãƒˆ"

    実際のファイルバイト列は「"ãƒ†ã‚¹ãƒˆ" を UTF-8 エンコード」したもの。
    エディタ上では「ãƒ†ã‚¹ãƒˆ」と見える。
    """
    original = "テストの問い合わせを確認していますか？"

    utf8_bytes = original.encode("utf-8")
    mojibake = utf8_bytes.decode("latin1")  # ここでモジバケ

    lines = [
        "### 01_utf8_to_latin1",
        "元テキストは UTF-8 の日本語ですが、",
        "UTF-8 バイト列を Latin-1 と誤解釈した場合のモジバケ例です。",
        "",
        f"[original] {original}",
        f"[mojibake] {mojibake}",
        "",
        "このファイル自体は UTF-8 エンコードで保存されています。",
        "",
        mojibake,
    ]
    text = "\n".join(lines)
    path.write_text(text, encoding="utf-8")


def generate_02_utf8_to_cp932_mojibake(path: pathlib.Path) -> None:
    """
    02_utf8_to_cp932_mojibake.txt

    UTF-8 で書かれた日本語テキストのバイト列を CP932(Shift_JIS系) として
    誤解釈した場合のモジバケを簡易再現したサンプル。

    典型例:
        "テスト" → "縺ゅ↑縺九ｉ" のような文字列
    """
    original = "テスト結果をレポートします。"

    utf8_bytes = original.encode("utf-8")
    # UTF-8 バイト列を CP932 として誤解釈
    mojibake = utf8_bytes.decode("cp932", errors="replace")

    lines = [
        "### 02_utf8_to_cp932_mojibake",
        "UTF-8 の日本語テキストを CP932(Shift_JIS 系) と誤解釈した場合のモジバケ例です。",
        "",
        f"[original] {original}",
        f"[mojibake(cp932<-utf8 bytes)] {mojibake}",
        "",
        "このファイル自体は UTF-8 エンコードで保存されています。",
        "",
        mojibake,
    ]
    text = "\n".join(lines)
    path.write_text(text, encoding="utf-8")


def generate_03_cp932_original_japanese(path: pathlib.Path) -> None:
    """
    03_cp932_original_japanese.txt

    実際に CP932 (Shift_JIS 系) で保存された日本語テキスト。
    「レガシーシステムからエクスポートされた SJIS ファイル」を想定。

    ファイルバイト列は CP932。エディタが UTF-8 前提だと文字化けする。
    """
    # 一般的な運用報告風のテキスト
    original = (
        "システム監視レポート\r\n"
        "----------------------\r\n"
        "対象ホスト: server01.example.local\r\n"
        "期間: 2025/11/01 00:00:00 ～ 2025/11/01 23:59:59\r\n"
        "内容: CPU使用率・メモリ使用量・ディスクI/O の集計結果。\r\n"
    )

    # ファイルは CP932 バイトで保存する（テキストとして開くとエディタ依存）
    cp932_bytes = original.encode("cp932", errors="replace")
    path.write_bytes(cp932_bytes)


def generate_04_double_mojibake(path: pathlib.Path) -> None:
    """
    04_double_mojibake.txt

    「二重に文字化けした」ようなテキストを簡易的に再現。
    実際には様々な経路がありうるが、ここでは:

        1. UTF-8 日本語 → UTF-8 bytes
        2. bytes → Latin-1 としてデコード (mojibake_1)
        3. mojibake_1 を UTF-8 エンコード → bytes2
        4. bytes2 を CP932 としてデコード (mojibake_2)

    という 2 段階変換で得られた文字列を保存する。
    """
    original = "文字コード変換を二重に誤った例です。テスト文字列。"

    utf8_bytes = original.encode("utf-8")
    mojibake_1 = utf8_bytes.decode("latin1")
    bytes2 = mojibake_1.encode("utf-8")
    mojibake_2 = bytes2.decode("cp932", errors="replace")

    lines = [
        "### 04_double_mojibake",
        "二重の文字化けを簡易的に再現したサンプルです。",
        "",
        f"[original] {original}",
        f"[step1 utf8->latin1] {mojibake_1}",
        f"[step2 (utf8<-step1)->cp932] {mojibake_2}",
        "",
        "このファイル自体は UTF-8 エンコードで保存されています。",
        "",
        mojibake_2,
    ]
    text = "\n".join(lines)
    path.write_text(text, encoding="utf-8")


def generate_05_invalid_bytes(path: pathlib.Path) -> None:
    """
    05_invalid_bytes.txt

    バイナリログやネットワーク越し転送中の破損などで現れがちな
    「不正バイトを含むログ風データ」のサンプル。

    - 0x81: CP932 では前置バイトだけ存在する不完全シーケンス
    - 0x00: NUL
    """
    # ここでは意図的にバイナリで構成する
    lines = [
        b"LOG START\x0a",
        b"user_id=A\x81\x00C123\x0a",
        b"message=CPU usage high at 95%\x0a",
        b"comment=\x81\x81 This line contains invalid bytes.\x0a",
        b"LOG END\x0a",
    ]
    data = b"".join(lines)
    path.write_bytes(data)


def main() -> None:
    ensure_samples_dir()

    generators = [
        ("01_utf8_to_latin1.txt", generate_01_utf8_to_latin1),
        ("02_utf8_to_cp932_mojibake.txt", generate_02_utf8_to_cp932_mojibake),
        ("03_cp932_original_japanese.txt", generate_03_cp932_original_japanese),
        ("04_double_mojibake.txt", generate_04_double_mojibake),
        ("05_invalid_bytes.txt", generate_05_invalid_bytes),
    ]

    for filename, func in generators:
        path = SAMPLES_DIR / filename
        func(path)
        print(f"[OK] generated: {path.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    main()

