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

## 📡 Use This API on RapidAPI

The Encoding Repair API is also available on **RapidAPI**, allowing developers to easily test, authorize, and consume the API through RapidAPI’s integrated platform.

### 🔗 RapidAPI Hub
https://rapidapi.com/APIronlab/api/encoding-repair-api

### Features Available on RapidAPI
- One-click endpoint testing  
- Automatic API-key injection  
- Free / BASIC / PRO / ULTRA plans  
- Usage analytics and quota management  
- Auto-generated code snippets (cURL / Node.js / Python / etc.)

With a RapidAPI account, you can start using the Encoding Repair API immediately.

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

## 📡 RapidAPI で利用する

Encoding Repair API は RapidAPI 上でも公開されており、
APIキー管理・請求・テスト実行などをワンストップで行うことができます。

### 🔗 RapidAPI Hub
https://rapidapi.com/APIronlab/api/encoding-repair-api

### 利用可能機能
- ワンクリックでリクエストテスト  
- APIキー自動注入  
- 無料/BASIC/PRO/ULTRA の各種プラン  
- 月次クオータと利用状況の可視化  
- カール/Node.js/Python などのコードサンプル自動生成  

RapidAPI のアカウントを作成すれば、そのまま **Encoding Repair API を即利用開始**できます。

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

