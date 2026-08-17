# HAVING skipped when only one group survives

On L3 retrieval, learner put paid in WHERE and grouped correctly, but omitted HAVING on both `l3_02` (SUM > 100) and `l3_03` (COUNT >= 2). Seed only leaves customer 10 after the paid filter, so the checker stayed green.

**Implications:** Do not treat L3 as locked. Next pass: a second paid customer under the threshold, or ask them to add HAVING before calling the case done.
