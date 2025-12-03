#!/usr/bin/env python3
import argparse
import base64
import json
import pathlib
import sys

import requests


API_URL = "https://bjpotwq0jf.execute-api.ap-northeast-1.amazonaws.com/prod/encoding/v2/repair"


def call_api(file_path: pathlib.Path, mode: str, target_encoding: str) -> dict:
    data = file_path.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")

    payload = {
        "mode": mode,  # "auto" or "manual"
        "raw_bytes_base64": b64,
        "target_encoding": target_encoding,
    }

    resp = requests.post(API_URL, json=payload)
    resp.raise_for_status()
    return resp.json()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Call Encoding Repair API with a local file."
    )
    parser.add_argument("file", type=pathlib.Path, help="入力ファイルパス")
    parser.add_argument(
        "--mode",
        choices=["auto", "manual"],
        default="auto",
        help='エンコーディング判定モード (default: "auto")',
    )
    parser.add_argument(
        "--target-encoding",
        default="utf-8",
        help='出力エンコーディング (default: "utf-8")',
    )

    args = parser.parse_args()

    if not args.file.exists():
        print(f"[ERROR] File not found: {args.file}", file=sys.stderr)
        return 1

    result = call_api(args.file, mode=args.mode, target_encoding=args.target_encoding)

    print("=== API response ===")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 文字列として復元できる場合は、標準出力にも中身を表示
    fixed_text = result.get("result", {}).get("fixed_text")
    if isinstance(fixed_text, str):
        print("\n=== fixed_text preview ===")
        # 行数が多いときのため、先頭 5 行だけ…
        lines = fixed_text.splitlines()
        preview = "\n".join(lines[:5])
        print(preview)
        if len(lines) > 5:
            print("... (truncated)")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

