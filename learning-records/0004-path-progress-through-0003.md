# Path progress through lesson 0003

Correctness track delivered: 0001 fan-out, 0002 NULL/3VL, 0003 logical processing order.

**Retrieval (drills):** L1–L3 cases under `drills/` exercised with edit → `run.py` / `check.py` loop. Proven: alias-safe filter (repeat expr in WHERE), WHERE vs HAVING, group filter with HAVING COUNT. Near-miss: `l3_03` passed seed without HAVING until “at least 2” called out — seed had only one paid customer group.

**Implications for ZPD:** Correctness block ready to leave for optimization. Next high-ROI lesson is path item 4 — **sargable predicates / partition prune / pushdown**. Before EXPLAIN deep-dives, resolve Aurora dialect (MySQL vs PostgreSQL). Optional: one PR-style multi-join blob combining grain + 3VL + logical order before moving on.
