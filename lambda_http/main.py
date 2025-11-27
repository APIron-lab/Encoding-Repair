# lambda_http/main.py

from mangum import Mangum
from backend.fastapi_app.main import app

# API Gateway のステージ名に合わせて base path を指定
# いま prod ステージを使っているので "/prod"
handler = Mangum(app, api_gateway_base_path="/prod")

