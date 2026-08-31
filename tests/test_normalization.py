from ml.normalization.normalizer import normalize_description

def test_normalization():
    assert normalize_description("SS PIPE 2\"") == "STAINLESS STEEL PIPE 2 IN"
    assert normalize_description("S.S. VALVE 50.8 MM") == "STAINLESS STEEL VALVE 2 IN"
    assert normalize_description("CS PIPE SCH40") == "CARBON STEEL PIPE SCHEDULE 40"
    assert normalize_description("C.S. FLANGE 25.4MM") == "CARBON STEEL FLANGE 1 IN"
    assert normalize_description("SS PIPE 2 IN SCH 80.") == "STAINLESS STEEL PIPE 2 IN SCHEDULE 80"

