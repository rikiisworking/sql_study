# Mission: Production SQL fluency (read · write · fix · speed)

## Why
You join a multi-engine data project (Glue / Spark SQL, Aurora, Redshift; DynamoDB adjacent) around **2026-08-17**. Day job: **write and fix production queries**. Simple SELECT/INSERT already fine; gap is spotting wrong results and making slow queries acceptable under real data volume.

## Success looks like
- Read a multi-join query and state **grain** (what one output row means) before trusting numbers
- Spot classic wrong-SQL: fan-out, NULL traps, wrong join type, filter on wrong table
- Write clear SQL: CTEs, explicit joins, predicates that match the question
- When something is slow: form a hypothesis (scan / join / shuffle / skew), check a plan or metrics, change the query or layout with intent—not cargo-cult indexes
- Work across engines without relearning SQL from zero (syntax differs; mental model transfers)

## Constraints
- Hard start ~**2026-08-17** → high-ROI path, not a full DBA course
- Engines: **Spark SQL (Glue), Aurora, Redshift** primary; DynamoDB is not SQL (cover only when it collides with query design)
- Prefer skills that transfer across engines over vendor trivia

## Out of scope (for now)
- Full DBA work (vacuum schedules, cluster resize, IAM)
- DynamoDB data modeling deep dive
- Building a warehouse from scratch / dimensional modeling theory dump
- ORM-only app CRUD patterns
