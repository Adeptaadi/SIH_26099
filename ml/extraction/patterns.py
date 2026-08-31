import re

# Regex patterns for extracting technical parameters
PATTERNS = {
    "material": r"\b(STAINLESS STEEL|CARBON STEEL|ALLOY STEEL|BRASS|COPPER|ALUMINUM|BRONZE|CAST IRON|CHROME STEEL)\b",
    "type": r"\b(SEAMLESS PIPE|WELDED PIPE|PIPE|BALL VALVE|GATE VALVE|GLOBE VALVE|BUTTERFLY VALVE|CHECK VALVE|VALVE|BALL BEARING|ROLLER BEARING|TAPERED ROLLER BEARING|NEEDLE ROLLER BEARING|BEARING|HEX BOLT|HEX NUT|SOCKET HEAD CAP SCREW|WASHER|BOLT|NUT|SCREW|XLPE CABLE|PVC CABLE|INSTRUMENTATION CABLE|FLEXIBLE CABLE|CABLE)\b",
    "size": r"\b(\d+/\d+\s*IN|\d+\s*IN|\d+\.\d+\s*IN|M\d+|4 CORE 16 SQMM|3 CORE 70 SQMM|2 PAIR 1.5 SQMM|3 CORE 2.5 SQMM|4 CORE 120 SQMM)\b",
    "grade": r"\b(TP304L?|TP316L?|CF8M?|GRADE\s+\d+\.\d+|GRADE\s+[A-Z]|CLASS\s+\d+|A2-70|A4|A4-70|WCB|C37700|LF2|GG25|B62|C3604|6210-2RS|NU2211|30209|S6205-2RS|HK2016|1\.1KV|11KV|500V|300/500V|P11)\b",
    "standard": r"\b(ASTM\s+A\d+|ANSI\s+B\d+(?:\.\d+)?|API\s+\d+[A-Z]?|DIN\s+\d+|ISO\s+\d+|IEC\s+\d+(?:-\d+)?|IS\s+\d+|BS\s+\d+|MSS\s+SP-\d+)\b",
    "schedule": r"\b(?:SCHEDULE|SCH)\s*([0-9S]+)\b",
    "pressure_class": r"\b(\d+)\s*(?:LB|LB\.|\#)\b",
    "diameter": r"\b(\d+)\s*MM\b",
    "length": r"\b(\d+)\s*M\b",
    "voltage": r"\b([0-9./]+)\s*(?:KV|V)\b",
}

