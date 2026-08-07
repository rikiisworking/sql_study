# Grain, whole-result aggregates, and EXISTS

Learner can reason about **grain** (coarse vs fine table) and knows that **`SUM` without `GROUP BY` is valid**: the whole intermediate result is one group, one output row. That does not fix fan-out — inflated join rows still inflate the sum.

Also engaged with **`WHERE EXISTS`**: semi-join / “at least one match,” outer grain preserved, often preferable to join-then-aggregate for “has children” filters; speed depends on plan/keys, not the keyword alone.

**Evidence:**
- Follow-up questions after lesson 0001 (SUM without GROUP BY; meaning of “fine table”; EXISTS syntax and performance).
- Runnable drills (`drills/cases/l1_*`): safe order revenue via `EXISTS` (after trying `IN` + `DISTINCT`); `SUM(qty)` by customer at item grain; fixed inflated `SUM(amount)` after join.

**Implications:** Do not re-teach basic aggregate syntax or the EXISTS “has children” pattern. Fan-out retrieval on toy seed is green; still unproven on a full live PR-style query. `l1_03` same skill as `l1_01` (framing only) — optional to drop later.
