from core.encoding_repair import EncodingRepairRequest, repair_encoding


def test_repair_encoding_full_recovery():
    """
    「テスト」→ UTF-8 → latin1 モジバケ → 再解釈で完全復元できることを検証
    """
    original = "テスト"
    mojibake = original.encode("utf-8").decode("latin1")

    req = EncodingRepairRequest(
        text=mojibake,
        assume_current_encoding="latin1",
        target_encoding="utf-8",
    )

    res = repair_encoding(req)

    assert res["result"]["original_text"] == mojibake
    assert res["result"]["fixed_text"] == original
    assert res["result"]["changed"] is True
    assert res["meta"]["status"] == "ok"
    assert res["meta"]["strategy"] == "reinterpret_bytes"


def test_repair_encoding_unrecoverable_fallback():
    """
    明らかに復元不能な文字列を渡したとき、
    元のテキストを破壊せず返すことを検証
    """
    broken = "ã†ã¹ã"

    req = EncodingRepairRequest(
        text=broken,
        assume_current_encoding="latin1",
        target_encoding="utf-8",
    )

    res = repair_encoding(req)

    assert res["result"]["original_text"] == broken
    assert res["result"]["fixed_text"] == broken  # 非破壊
    assert res["result"]["changed"] is False
    assert res["meta"]["status"] == "no_meaningful_output"
    assert res["meta"]["strategy"] == "fallback_original"
