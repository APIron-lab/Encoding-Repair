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

## Response JSON Structure

The API returns a predictable and stable JSON structure suitable for production workflows.

```json
{
  "result": {
    "fixed_text": "string",
    "target_encoding": "string",
    "changed": false
  },
  "meta": {
    "version": "2.0.0",
    "mode_used": "auto | force",
    "detected_path": "utf-8>shift_jis",
    "confidence": 1.0,
    "status": "ok",
    "execution_ms": 12.41,
    "input_bytes_length": 120
  }
}
```

---

## Supported Encodings

Encoding Repair API supports a wide range of encodings frequently involved in mojibake issues.

| Encoding                     | Notes                                                 |
| ---------------------------- | ----------------------------------------------------- |
| **UTF-8**                    | Modern standard; autobias for Japanese workloads      |
| **Shift_JIS (SJIS / CP932)** | Legacy Japanese encoding used in Windows applications |
| **EUC-JP**                   | Unix-origin Japanese encoding                         |
| **ISO-2022-JP**              | Email-safe Japanese encoding (JIS)                    |
| **UTF-16 / UTF-32**          | BOM-aware detection is supported                      |
| **ASCII**                    | Auto-normalized                                       |
| **Other rare encodings**     | Internally handled through multi-phase heuristics     |

---

## Use Cases

### 1. Repairing Japanese mojibake

Fix broken text from:

* Legacy systems
* SJIS → UTF-8 migration
* Corrupted file imports

### 2. Restoring text from raw bytes

Useful when only the byte sequence is available (scraped data, logs, email archives).

### 3. Pre-processing for LLM pipelines

Normalize text to UTF-8 before feeding ChatGPT / Claude / Gemini or local LLMs.

### 4. CSV / TSV / Excel imports

Sanitize mixed-encoding datasets common in Japanese business systems.

### 5. Web scraping / crawling

Repair inconsistent encodings from multi-domain crawlers.

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

## レスポンス構造（JSON）

本APIは、運用システムでも扱いやすい **安定した2階層構造（result + meta）** を返却します。

```json
{
  "result": {
    "fixed_text": "string",
    "target_encoding": "string",
    "changed": false
  },
  "meta": {
    "version": "2.0.0",
    "mode_used": "auto | force",
    "detected_path": "utf-8>shift_jis",
    "confidence": 1.0,
    "status": "ok",
    "execution_ms": 12.41,
    "input_bytes_length": 120
  }
}
```

---

## 対応エンコーディング一覧

Encoding Repair API は、日本語環境で頻出する主要エンコーディングを幅広くサポートしています。

| エンコーディング                    | 説明                    |
| --------------------------- | --------------------- |
| **UTF-8**                   | 現代標準。日本語に最適化された判定ロジック |
| **Shift_JIS（SJIS / CP932）** | Windows系レガシー環境で多用     |
| **EUC-JP**                  | Unix系・業務システムで使用       |
| **ISO-2022-JP（JIS）**        | メール系アプリで利用される可変エンコード  |
| **UTF-16 / UTF-32**         | BOM判定を含む安全復元          |
| **ASCII**                   | 部分的な混在データにも対応         |
| **その他の稀なエンコード**             | 多段階ヒューリスティックにより内部処理   |

---

## 利用シーン（Use Cases）

### 1. 日本語の文字化け修復

以下のようなシナリオで効果的です：

* システム移行（SJIS → UTF-8 など）
* 古い基幹システムのCSV/TSVログ
* Windows / Unix 混在環境のデータ破損

### 2. 生バイト列からのテキスト復元

スクレイピング、メールアーカイブ、ログ収集など
**「テキストではなくバイトデータしか無い」** という場面に対応。

### 3. LLM 事前処理（Pre-AI Input Hygiene）

ChatGPT / Claude / Gemini / ローカルLLMに投げる前の
**UTF-8 正規化工程** として最適。

### 4. CSV / TSV / Excel 読み込み前のクリーニング

日本の業務システムに多い「混在エンコード」を安全に一本化。

### 5. Webスクレイピング / クローリング

サイトごとに異なるエンコーディングによる乱れを自動補正。


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

