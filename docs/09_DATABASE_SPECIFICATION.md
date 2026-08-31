# SIH26099 — Database Specification

## Database
MVP: SQLite.
Future: PostgreSQL.

## materials
- id
- material_id
- organization_id
- description
- normalized_description
- attributes_json
- created_at

## matches
- id
- material_a_id
- material_b_id
- classification
- confidence
- semantic_score
- attribute_score
- specification_score
- matched_attributes_json
- differences_json
- explanation
- status
- created_at

## reviews
- id
- match_id
- decision
- reviewed_at

## common_materials
- id
- common_material_id
- canonical_description
- created_at

## Relationships
```text
materials → matches → reviews
                    ↘ common_materials
```

## Principle
Store flexible extracted attributes as JSON for the MVP. Avoid over-normalizing the schema during the 2-day prototype.
