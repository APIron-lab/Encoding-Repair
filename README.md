# Encoding Repair API (v2.0)

High-accuracy Base64-only encoding repair API for fixing mojibake (garbled text) across UTF-8 / Shift_JIS / EUC-JP / Latin-1 transitions.

[![CI](https://github.com/APIron-lab/Encoding-Repair/actions/workflows/ci.yml/badge.svg)](https://github.com/APIron-lab/Encoding-Repair/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/APIron-lab/Encoding-Repair/graph/badge.svg?token=x7PCsSMkaE)](https://codecov.io/gh/APIron-lab/Encoding-Repair)

---

## 🌐 Overview

Encoding Repair API restores corrupted text **from raw bytes only**.

To ensure perfect accuracy, this API accepts **Base64-encoded byte data**, preventing information loss that occurs during copy/paste or text-editor conversions.

### Key Capabilities
- Base64-only input (safe, lossless)
- Automatic encoding detection  
- UTF-8 / Shift_JIS / EUC-JP / Latin-1 support
- Safe Filter (prevents incorrect fixes)
- Manual mode for explicit decoding
- Unified `result + meta` response (APIron Spec)

---

## 🚀 Endpoint

### `POST /encoding/v2/repair`

#### Request Example
```json
{
  "raw_bytes_base64": "<Base64>",
  "mode": "auto",
  "target_encoding": "utf-8"
}
```

#### Response Example
```json
{
  "result": {
    "fixed_text": "テスト",
    "target_encoding": "utf-8",
    "changed": true
  },
  "meta": {
    "version": "2.0.0",
    "mode_used": "auto",
    "detected_path": "latin1->utf-8",
    "confidence": 0.98,
    "status": "ok"
  }
}
```

---

## 🧪 Python Example

```python
import base64, requests

raw = "テスト".encode("utf-8")
b64 = base64.b64encode(raw).decode("ascii")

payload = {
    "raw_bytes_base64": b64,
    "mode": "auto",
    "target_encoding": "utf-8"
}

res = requests.post("https://your-endpoint/encoding/v2/repair", json=payload)
print(res.json())
```

---

# 🇯🇵 日本語版 README

## 概要

Encoding Repair API は、**生バイト(Base64)** を入力として受け取り、  
文字化けしたテキストを安全かつ高精度に復元する API です。

### 特徴
- バイト列を完全保持（コピー＆ペーストの情報欠損を防止）
- 自動エンコーディング判定
- UTF-8 / Shift_JIS / EUC-JP / Latin-1 対応
- 誤修復防止の Safe Filter 搭載
- Manual mode による強制デコード

---

## エンドポイント

### `POST /encoding/v2/repair`

#### リクエスト例

```json
{
  "raw_bytes_base64": "<Base64>",
  "mode": "auto",
  "target_encoding": "utf-8"
}
```

---

## Python 使用例

```python
import base64, requests

raw = "テスト".encode("utf-8")
b64 = base64.b64encode(raw).decode("ascii")

payload = {
    "raw_bytes_base64": b64,
    "mode": "auto",
    "target_encoding": "utf-8"
}

res = requests.post("https://your-endpoint/encoding/v2/repair", json=payload)
print(res.json())
```

---

Maintainer: APIron-lab  
GitHub: https://github.com/APIron-lab/Encoding-Repair

