# lambda_http/main.py

from __future__ import annotations

from mangum import Mangum

from backend.fastapi_app.main import app

# AWS Lambda 用エントリポイント
handler = Mangum(app)

