# backend/fastapi_app/main.py

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from core.encoding_repair_v2 import (
    EncodingRepairRequestV2,
    EncodingRepairResponse,
    repair_encoding_v2,
)

app = FastAPI(
    title="Encoding Repair API",
    version="2.0.0",
    description=(
        "文字コード誤解釈による文字化けを、Base64 バイト列から安全に復元する API。\n"
        "入力は raw_bytes_base64 のみ（Base64 専用）。"
    ),
)


@app.get("/health")
def health() -> dict:
    """
    シンプルなヘルスチェックエンドポイント。
    """
    return {"status": "ok"}


@app.post(
    "/encoding/v2/repair",
    response_model=EncodingRepairResponse,
    summary="Encoding Repair v2.0 (Base64-only)",
)
def encoding_repair_v2_endpoint(payload: EncodingRepairRequestV2) -> EncodingRepairResponse:
    """
    Base64 専用の文字化け修復エンドポイント。

    - mode: auto / manual
    - raw_bytes_base64: ファイル等のバイト列を Base64 化したもの
    """
    response = repair_encoding_v2(payload)
    return response


# 任意: ルートに簡易情報を返す
@app.get("/")
def root() -> JSONResponse:
    return JSONResponse(
        {
            "service": "Encoding Repair API",
            "version": "2.0.0",
            "mode": "base64-only",
            "endpoints": ["/health", "/encoding/v2/repair"],
        }
    )

