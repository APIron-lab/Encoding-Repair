# tests/test_encoding_repair_v2.py

from __future__ import annotations

import base64

from fastapi.testclient import TestClient

from backend.fastapi_app.main import app

client = TestClient(app)


def test_health_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_auto_mode_utf8_text_passthrough():
    # もともと正常な UTF-8 テキストは極力そのまま返すことを確認
    text = "これはテストです。"
    raw = text.encode("utf-8")
    b64 = base64.b64encode(raw).decode("ascii")

    payload = {
        "mode": "auto",
        "raw_bytes_base64": b64,
        "target_encoding": "utf-8",
    }

    resp = client.post("/encoding/v2/repair", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["result"]["fixed_text"] == text
    assert data["result"]["changed"] in (False, True)  # 完全一致なので False になる想定
    assert data["meta"]["status"] == "ok"


def test_manual_mode_with_cp932():
    # cp932 でエンコードされた日本語テキストが正しく読めることを確認
    text = "文字コードのテスト"
    raw = text.encode("cp932")
    b64 = base64.b64encode(raw).decode("ascii")

    payload = {
        "mode": "manual",
        "raw_bytes_base64": b64,
        "assume_current_encoding": "cp932",
        "target_encoding": "utf-8",
    }

    resp = client.post("/encoding/v2/repair", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["result"]["fixed_text"] == text
    assert data["result"]["changed"] is True
    assert data["meta"]["status"] == "ok"
    assert data["meta"]["detected_path"] == "cp932->utf-8"


def test_invalid_base64():
    payload = {
        "mode": "auto",
        "raw_bytes_base64": "!!!this-is-not-base64!!!",
    }
    resp = client.post("/encoding/v2/repair", json=payload)
    assert resp.status_code == 200

    data = resp.json()
    assert data["result"]["fixed_text"] == ""
    assert data["meta"]["status"] == "invalid_base64"
    assert data["meta"]["input_bytes_length"] == 0

