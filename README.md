# Encoding Repair API (v2.0)
**Pre-AI Input Tools / Structured Text Hygiene Series**  
**Base64-Only / Auto Encoding Repair API**

[![CI](https://github.com/APIron-lab/Encoding-Repairactions/workflows/ci.yml/badge.svg)](https://github.com/APIron-lab/Encodeing-Repair/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/APIron-lab/Encoding-Repair/graph/badge.svg?token=x7PCsSMkaE)](https://codecov.io/gh/APIron-lab/Encoding-Repair)

---

## Overview (English)

**Encoding Repair API** automatically restores corrupted or mojibake text from raw byte data.  
To maximize accuracy, this API accepts **only Base64-encoded raw bytes**, ensuring that no information is lost through copy-paste or intermediate application conversions.

This API is designed for:

- Repairing mojibake in CSV / TSV / LOG files  
- Unifying mixed encodings (UTF-8 / Shift_JIS / EUC-JP / Latin-1)  
- Fixing broken text caused by system migration or legacy applications  
- Pre-processing text for Large Language Models (Pre-AI Input Hygiene)

### Key Features

- **Base64-only input**: preserves the original byte sequence  
- **Auto encoding detection** for UTF-8 / Shift_JIS / EUC-JP / Latin-1  
- **Safe Filter**: prevents false fixes by returning original data when confidence is low  
- **Manual mode** allows explicit control over encoding assumptions

---

## Endpoint

### POST /encoding/v2/repair

**Request Body**

```json
{
  "raw_bytes_base64": "<Base64 bytes>",
  "mode": "auto",
  "target_encoding": "utf-8"
}
```

---

## Example Response

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
    "status": "ok",
    "execution_ms": 5.42,
    "input_bytes_length": 9
  }
}
```

---

## Python Usage Example

```python
import base64, requests

raw = "テスト".encode("utf-8")
b64 = base64.b64encode(raw).decode("ascii")

payload = {
    "raw_bytes_base64": b64,
    "mode": "auto",
    "target_encoding": "utf-8"
}

res = requests.post("https://your-api-endpoint/encoding/v2/repair", json=payload)
print(res.json())
```

---

# 日本語版 README

---

## 概要

**Encoding Repair API** は、文字化けしたテキストを **自動修復** する API です。  
復元精度向上のため、**Base64 の生バイト入力のみ** を受け付けます。

主な用途：

- CSV / TSV / LOG の文字化け修正  
- UTF-8 / Shift_JIS / EUC-JP / Latin-1 混在データの一括整理  
- システム移行によるテキスト破損の修復  
- AIへの入力前処理（Pre-AI Input Hygiene）

---

## 特徴

- **Base64 専用入力**で情報欠落を防止  
- **自動エンコーディング判定**  
- **誤修復を防ぐ Safe Filter**  
- 強制指定可能な **Manual mode**

---

## エンドポイント

### POST /encoding/v2/repair

```json
{
  "raw_bytes_base64": "<Base64エンコード済みバイト列>",
  "mode": "auto",
  "target_encoding": "utf-8"
}
```

---

## Python使用例

```python
import base64, requests

raw = "テスト".encode("utf-8")
b64 = base64.b64encode(raw).decode("ascii")

payload = {
    "raw_bytes_base64": b64,
    "mode": "auto",
    "target_encoding": "utf-8"
}

res = requests.post("https://your-api-endpoint/encoding/v2/repair", json=payload)
print(res.json())
```

---

