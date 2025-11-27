from fastapi import APIRouter, HTTPException
from .schemas import EncodingRepairRequestModel, EncodingRepairResponseModel
from core.encoding_repair import EncodingRepairRequest, repair_encoding

router = APIRouter()


@router.post(
    "/encoding/v0/repair",
    response_model=EncodingRepairResponseModel,
    summary="Encoding Repair (Mojibake Fix v0.1)",
    tags=["encoding"],
)
async def encoding_repair_endpoint(payload: EncodingRepairRequestModel):
    """
    典型的なモジバケ（誤ったエンコーディング解釈）を修正するAPI。

    - text: 現在の（おそらくおかしくなっている）テキスト
    - assume_current_encoding: 現在のstrをバイト列に戻す際に使うエンコーディング
    - target_encoding: 本来意図していたエンコーディング
    """
    if not payload.text:
        raise HTTPException(status_code=400, detail="Field 'text' is required.")

    req = EncodingRepairRequest(
        text=payload.text,
        assume_current_encoding=payload.assume_current_encoding,
        target_encoding=payload.target_encoding,
    )

    try:
        response = repair_encoding(req)
    except Exception as e:
        # v0.1 は簡易エラーハンドリング
        raise HTTPException(
            status_code=500,
            detail=f"Internal error in encoding repair: {e}",
        )

    return response

