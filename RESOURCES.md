# SQL Query Resources

## Knowledge

- [Use The Index, Luke — Markus Winand](https://use-the-index-luke.com/)
  Free developer-focused book on indexing and how joins/filters actually run. Use for: B-tree mental model, join algorithms, why predicates kill (or save) indexes. Strong on Aurora-style engines; concepts still help when reading plans elsewhere.
- [Modern SQL — Markus Winand](https://modern-sql.com/)
  Standard SQL features with engine support notes (window functions, 3VL, filters). Use for: correctness features and “what is portable?”
- [Three-Valued Logic — modern-sql.com](https://modern-sql.com/concept/three-valued-logic)
  Authoritative short treatment of NULL / UNKNOWN. Use for: NOT IN traps, join-on-null, WHERE surprises.
- [PostgreSQL: Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html)
  Gold-standard intro to reading plans. Use for: Aurora PostgreSQL and as a map when Redshift/Spark plans use different labels.
- [Amazon Redshift: Query performance tuning](https://docs.aws.amazon.com/redshift/latest/dg/c-optimizing-query-performance.html)
  Official Redshift tuning hub. Use for: EXPLAIN, dist/sort keys impact, SVL views.
- [Amazon Redshift: Best practices for designing queries](https://docs.aws.amazon.com/redshift/latest/dg/c_designing-queries-best-practices.html)
  Concrete query rules (no blind SELECT *, avoid cross joins, predicates on both sides of joins, function-in-predicate cost). Use for: day-1 checklist on Redshift.
- [AWS Prescriptive Guidance: Redshift query best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/query-best-practices-redshift/best-practices-designing-queries.html)
  Curated AWS guidance (tables + queries). Use for: structured review of warehouse SQL.
- [Spark SQL Performance Tuning (Apache docs)](https://spark.apache.org/docs/latest/sql-performance-tuning.html)
  Official Spark SQL/DataFrame tuning. Use for: join strategies, AQE, caching, statistics—Glue jobs live here.
- [SQL and the Snare of Three-Valued Logic — Simple Talk](https://www.red-gate.com/simple-talk/databases/sql-server/learn/sql-and-the-snare-of-three-valued-logic/)
  Long-form NULL/3VL with practical examples. Use for: deeper practice after the modern-sql page.
- [SELECT (Transact-SQL) — Logical processing order (Microsoft Learn)](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql)
  Canonical numbered binding order for SELECT clauses. Use for: why aliases fail in WHERE, WHERE vs HAVING, reading complex queries. Physical plans may differ; result must match this logic.

## Wisdom (Communities)

- [r/PostgreSQL](https://www.reddit.com/r/PostgreSQL/)
  High-signal for plan reading and Aurora PG-ish questions. Use for: “why this EXPLAIN?” sanity checks.
- [r/dataengineering](https://www.reddit.com/r/dataengineering/)
  Glue/Spark/Redshift war stories. Use for: pipeline patterns, when SQL vs job config is the real fix.
- [DBA Stack Exchange](https://dba.stackexchange.com/)
  Moderated Q&A with plan pastes. Use for: isolated hard query problems with full schema + EXPLAIN.

## Gaps

- Aurora MySQL-specific EXPLAIN deep material (add when Aurora dialect known: MySQL vs PostgreSQL)
- AWS Glue job-level tuning (worker type, bookmarks) separate from SQL—only when project demands
- Official DynamoDB “SQL” path is thin by design; treat as API design, not SQL
