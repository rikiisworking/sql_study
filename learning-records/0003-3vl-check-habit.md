# Three-valued logic: habits over theory dump

Learner framed lesson 0002 correctly: the durable takeaway is the **check habit** (nullable predicates, never `= NULL`, `NOT IN` + nulls → prefer `NOT EXISTS`, right-side filter on `LEFT JOIN` intent), not memorizing full AND/OR truth tables in isolation.

**Evidence:**
- Explicit confirmation that practical tips = Check habit section.
- Drills `l2_01`–`l2_03`: rewrote `NOT IN` → `NOT EXISTS`; `status IS NULL` (not `=`); `LEFT JOIN` with `sku = 'A'` in `ON` so unmatched orders keep NULL right side. Asked for why `ON` vs `WHERE` — can explain post-join filter drops UNKNOWN/NULL matches.

**Implications:** Future NULL work should be applied (trace a real predicate) rather than re-lecturing 3VL. Habit check on production SQL is next load-bearing step, not more 3VL theory.
