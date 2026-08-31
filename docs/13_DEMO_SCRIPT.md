# SIH26099 — MVP Demo Script

## 1. Opening
Organizations may describe the same material differently, making exact-string matching unreliable.

## 2. Upload
Upload `organization_a.csv`, then `organization_b.csv`.

## 3. Run Matching
Click `RUN MATCHING`.

## 4. Equivalent Case
Org A:
`SS PIPE 2 IN SCH40 ASTM A312 TP304`

Org B:
`STAINLESS STEEL SEAMLESS PIPE 50.8MM SCHEDULE 40 ASTM A312 GRADE 304`

Expected: `EQUIVALENT`.

## 5. Technical Evidence
Show:
- Material ✓
- Type ✓
- Size ✓
- Grade ✓
- Standard ✓
- Schedule ✓

## 6. Hard Negative
A:
`SS PIPE 2 IN SCH40 ASTM A312 TP304`

B:
`SS PIPE 2 IN SCH40 ASTM A312 TP316`

Expected: `DIFFERENT`.

Explanation: `Grade mismatch: TP304 vs TP316`.

## 7. Review Case
Show a borderline `REVIEW` case and explain human-in-the-loop handling.

## 8. Human Review
Approve or reject the selected case.

## 9. Common Material
Show the resulting common-material record and source records.

## 10. Closing
The MVP uses generated data for controlled demonstration. The same schema and matching pipeline can later consume real organizational/CPSE material data through CSV, databases or APIs.

## Demo Rule
Do not demonstrate unimplemented features.
