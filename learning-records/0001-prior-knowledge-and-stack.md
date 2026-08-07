# Prior knowledge and project stack

Learner already reads and writes simple SQL. Goal is production readiness: spot wrong results and optimize under real engines—not beginner SELECT syntax.

Stack is multi-engine AWS data work: Glue/Spark SQL, Aurora, Redshift, DynamoDB adjacent. Day job is write + fix production queries. Assignment ~2026-08-17.

**Implications:** Skip intro CRUD. Lead with correctness (grain, joins, NULL), then portable optimization mental models, then engine-specific plan reading. Aurora dialect (MySQL vs PostgreSQL) still unknown—resolve before deep EXPLAIN drills that depend on vendor-specific plan text.

**Status:** active (baseline). Progress after this: see LR-0002–0007.
