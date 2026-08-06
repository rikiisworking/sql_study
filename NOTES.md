# Notes

## Learner profile
- Comfortable with simple read/write SQL
- Weak: diagnosing wrong results; optimizing given queries
- Role on project: write + fix production queries
- Start: ~2026-08-17

## Stack (from learner)
- AWS Glue (Spark SQL)
- Aurora (MySQL vs PG still unknown—ask when first EXPLAIN lesson hits)
- Redshift
- DynamoDB (non-SQL; don’t center lessons on it)
- Spark SQL generally

## Teaching prefs
- Caveman + ponytail active in chat: terse, minimal scaffolding
- Lessons stay full HTML (teach skill): short, interactive, one skill each
- Prefer transfer skills before vendor trivia

## Path sketch (high ROI before 8/17)
1. Join fan-out / grain (wrong results)
2. NULL + three-valued logic
3. Logical processing order (read complex SQL)
4. Predicates that engines can use (sargable / partition prune / pushdown)
5. Plans: EXPLAIN basics (PG/Aurora) then Redshift/Spark labels
6. Engine-specific: Redshift dist/sort; Spark join strategy / shuffle
