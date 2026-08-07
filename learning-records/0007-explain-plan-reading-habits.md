# EXPLAIN plan reading and work safety

Lesson 0005 delivered. Learner drilled conceptual gaps before treating plans as day-job tools.

**Evidence (Q&A):**
- Confirmed EXPLAIN exists on Redshift, Aurora (PG and MySQL), Spark/Glue; **not** on DynamoDB.
- Plain EXPLAIN ≈ light (plan only); `EXPLAIN ANALYZE` ≈ full run cost — unsafe as a free probe on heavy unoptimized SQL.
- “Arbitrary units” = relative planner cost, not wall-clock.
- PG-style plans: read **most indented (leaves) → root**; same data-flow habit as Redshift bottom→top.
- `DS_BCAST_INNER`: “node” = **compute node** in the cluster, not plan-tree node.
- Willing to use LLM to interpret plans at work; agreed helper-not-oracle pattern (four questions + verify lines exist + redact).

**Implications:** Partial fluency is OK with checklist + LLM assist. Next depth: paste a real work EXPLAIN (engine labeled) or lesson 0006 dist/sort + Spark shuffle. Still resolve Aurora MySQL vs PG before vendor-specific EXPLAIN deep dives. Prefer plain EXPLAIN first on prod-shaped queries.
