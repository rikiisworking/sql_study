# SQL Study

Workspace for **production SQL fluency**: read a query, trust the grain, fix wrong results, then speed it up on **Glue / Spark SQL, Aurora, and Redshift**. Day job is write + fix queries, not become a DBA.

Started ~2026-08-17. Full why: [MISSION.md](MISSION.md).

## Progress

Last updated **2026-08-18**. Current lesson: **0009 (previous row / LAG)** — delivered; still needs a retrieval pass.

| # | Lesson | Status |
|---|---|---|
| 0001 | [Join fan-out / grain](lessons/0001-join-fanout-wrong-results.html) | Done + L1 drills |
| 0002 | [NULL / three-valued logic](lessons/0002-null-three-valued-logic.html) | Done + L2 drills |
| 0003 | [Logical processing order](lessons/0003-logical-processing-order.html) | Done + L3 drills (HAVING still easy to skip when the seed hides it) |
| 0004 | [Sargable predicates, prune, pushdown](lessons/0004-sargable-predicates-pushdown.html) | Done |
| 0005 | [EXPLAIN plan basics](lessons/0005-explain-plan-basics.html) | Done (habits: plain EXPLAIN first) |
| 0006 | [Data movement (dist / sort / shuffle)](lessons/0006-data-movement-dist-shuffle.html) | Done (vocab Q&A) |
| 0007 | [Join skew — one worker hog](lessons/0007-join-skew-one-worker.html) | Lesson up; retrieval not locked |
| 0008 | [Latest row per key](lessons/0008-latest-row-per-key.html) | Lesson up; retrieval not locked |
| 0009 | [Previous row with LAG](lessons/0009-previous-row-lag.html) | Lesson up; retrieval not locked |

**Next:** a real work `EXPLAIN` (engine labeled), Aurora dialect once MySQL vs PostgreSQL is known, or running window frames if the day job needs them.

Open questions and path notes live in [NOTES.md](NOTES.md). Insights that change what to study next: [learning-records/](learning-records/).

## How to use

Open a lesson HTML in a browser (quizzes are in-page). Pocket cards when you forget a label:

- [Glossary](reference/glossary.html)
- [Plan labels](reference/plan-labels.html)
- [Predicate rewrite](reference/predicate-rewrite.html)
- [Skew signals](reference/skew-signals.html)
- [Dist-style pictures](reference/dist-style.html)
- [Latest row per key](reference/latest-per-key.html)
- [Previous row](reference/previous-row.html)

Trusted links: [RESOURCES.md](RESOURCES.md).

## Drills

SQLite, from repo root (see [drills/README.md](drills/README.md)):

```bash
python3 drills/drill-01-03.py          # lessons 0001–0003
python3 drills/drill-integrated.py     # stacked 0001–0006
python3 drills/drill-0001-0009.py      # stacked 0001–0009 (windows + shop)
```

Layout/skew (0006–0007) have no SQLite oracle — those are engine physics; use a plan or Spark UI / `skew_rows`. The 0001–0009 file has one-word recall cases for that.
