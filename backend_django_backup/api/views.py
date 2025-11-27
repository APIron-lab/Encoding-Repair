from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core import TokenCountRequest, count_tokens


class TokenCountView(APIView):
    """
    トークンカウント API (Django REST Framework 用ラッパ)。

    POST /api/token/count/
    body: {
      "text": "文字列",
      "model": "gpt-4",      # 任意
      "language": "ja"       # 任意
    }
    """

    def post(self, request, *args, **kwargs):
        text = request.data.get("text", "")
        model = request.data.get("model", "gpt-4")
        language = request.data.get("language")

        if not text:
            return Response(
                {"error": "text is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        req = TokenCountRequest(text=text, model=model, language=language)
        result = count_tokens(req)

        return Response(
            {
                "model": result.model,
                "text_length": result.text_length,
                "token_count": result.token_count,
                "language": result.language,
            },
            status=status.HTTP_200_OK,
        )

