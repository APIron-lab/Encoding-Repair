# core/token_counter.py

from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenCountRequest:
    """
    トークンカウント要求の入力を表すデータクラス。

    NOTE:
        実運用では model に応じて tiktoken 等を切り替えることを想定。
        ここでは雛形として text をスペース区切りでカウントする
        ダミー実装になっている。
    """
    text: str
    model: str = "gpt-4"
    language: Optional[str] = None


@dataclass
class TokenCountResult:
    """
    トークンカウントの結果を表すデータクラス。
    """
    model: str
    text_length: int
    token_count: int
    language: Optional[str] = None


def count_tokens(req: TokenCountRequest) -> TokenCountResult:
    """
    トークンカウントの本体ロジック。

    Args:
        req: TokenCountRequest インスタンス

    Returns:
        TokenCountResult インスタンス
    """
    # ダミー実装：単純にスペース区切りの単語数を「トークン数」とする
    tokens = req.text.split()

    return TokenCountResult(
        model=req.model,
        text_length=len(req.text),
        token_count=len(tokens),
        language=req.language,
    )

