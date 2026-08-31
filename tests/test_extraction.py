from ml.extraction.attribute_extractor import extract_attributes

def test_extraction():
    # Test Pipe extraction
    attrs = extract_attributes("SS PIPE 2\" SCH40 ASTM A312 TP304")
    assert attrs["material"] == "STAINLESS STEEL"
    assert attrs["type"] == "PIPE"
    assert attrs["size"] == "2 IN"
    assert attrs["schedule"] == "40"
    assert attrs["standard"] == "ASTM A312"
    assert attrs["grade"] == "TP304"
    
    # Test Valve extraction
    attrs2 = extract_attributes("BRASS BALL VALVE 1/2\" C37700 ANSI B16.5")
    assert attrs2["material"] == "BRASS"
    assert attrs2["type"] == "BALL VALVE"
    assert attrs2["size"] == "1/2 IN"
    assert attrs2["standard"] == "ANSI B16.5"
    assert attrs2["grade"] == "C37700"

