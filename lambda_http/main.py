# lambda_http/main.py

from mangum import Mangum
from backend.fastapi_app.main import app

# Mangum アダプタを使って FastAPI を Lambda 対応させる
handler = Mangum(app)

