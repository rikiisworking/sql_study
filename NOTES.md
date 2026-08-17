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
1. Join fan-out / grain (wrong results) — lesson 0001 ✓ (+ drills)
2. NULL + three-valued logic — lesson 0002 ✓ (+ drills)
3. Logical processing order (read complex SQL) — lesson 0003 ✓ (+ drills)
4. Predicates that engines can use (sargable / partition prune / pushdown) — lesson 0004 ✓
5. Plans: EXPLAIN basics (PG map + Redshift/Spark labels) — lesson 0005 ✓
6. Data movement: Redshift dist/sort; Spark broadcast vs shuffle — lesson 0006 ✓ (vocab Q&A; see LR-0008)
7. Join skew (one worker hog vs even volume) — lesson 0007 ✓ (await retrieval evidence)
8. Next candidates: live work EXPLAIN walkthrough · Aurora dialect EXPLAIN

## Open question
- Aurora dialect: MySQL vs PostgreSQL — still unknown; deep vendor EXPLAIN after known.

## EXPLAIN work habits (learner)
- Plain EXPLAIN first; ANALYZE only when blast radius OK
- PG plans: most indent first (leaves → root)
- LLM OK to decode plans if verify against text + redact

## Data-movement notes (learner)
- DISTKEY ≠ index (placement vs lookup)
- Project = columns; filter = rows
- Spark `/*+ HINT */` needs the `+`; plain `/* */` is inert
- Prefer shrink dim then broadcast; same SQL body across strategies


## Drill loop
- `python3 drills/drill-01-03.py` — pass/fail each L1–L3 case
- `python3 drills/drill-01-03.py <case>` — one case
- `python3 drills/drill-01-03.py --print <case>` — see result, no oracle
- `python3 drills/drill-integrated.py` — 0001–0006 stacked; functions + docstring mission (pyspark exercise shape)
- Later isolated lessons: `python3 drills/drill-04.py` (one file per lesson) if needed

