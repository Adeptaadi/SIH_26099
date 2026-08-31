# SIH26099 — Data Specification

## Dataset Strategy
The MVP uses generated realistic industrial material data. Public procurement/AOC data may be used as a terminology reference, while generated records provide controlled ground truth.

## Canonical Material
```csv
canonical_id,category,material,type,size,grade,standard,schedule
M001,PIPE,STAINLESS STEEL,SEAMLESS PIPE,2 IN,TP304,ASTM A312,40
```

## Organization Material
```csv
material_id,organization_id,description
A001,ORG_A,SS PIPE 2 IN SCH40 ASTM A312 TP304
B001,ORG_B,STAINLESS STEEL SEAMLESS PIPE 50.8MM SCHEDULE 40 ASTM A312 GRADE 304
```

## Ground Truth
```csv
material_a_id,material_b_id,label
A001,B001,EQUIVALENT
A001,B002,DIFFERENT
```

Allowed labels: `EQUIVALENT`, `DIFFERENT`.

## Hard Negatives
Create similar descriptions with an important mismatch:
- TP304 vs TP316
- 2 IN vs 3 IN
- SCH40 vs SCH80
- Stainless Steel vs Carbon Steel
- Different standard
- Different pressure class

## Required Fields
`material_id`, `organization_id`, `description`.

## Data Quality
- IDs unique within an organization
- Description and organization non-empty
- Invalid rows reported
- Duplicate records reported
