from pydantic import BaseModel, Field


class EncodingRepairRequestModel(BaseModel):
    text: str = Field(..., description="現在モジバケしているかもしれないテキスト")
    assume_current_encoding: str = Field(
        "latin1",
        description="現在のPython文字列をバイト列に戻す際に用いるエンコーディング",
    )
    target_encoding: str = Field(
        "utf-8",
        description="復元を試みるターゲットエンコーディング",
    )


class EncodingRepairResponseModel(BaseModel):
    result: dict
    meta: dict

