# Data movement vocabulary (lesson 0006)

Learner worked through lesson 0006 concepts in Q&A before treating layout/join strategy as day-job tools.

**Evidence:**
- **Cargo-cult:** correctly sought definition — understood as ritual fix without mechanism (vs hypothesis + plan).
- **“Keys already together”:** collocated join keys on same slice/worker; opposite is network redistrib/shuffle first.
- **Fact / dim:** fact = large event/measure table; dim = smaller entity/lookup; “big fact + small dim” = broadcast/`DIST ALL` pattern.
- **DISTKEY vs index:** placement across Redshift slices for joins, not B-tree find-rows structure; SORTKEY closer to filter/block-skip.
- **Project:** column subset (`SELECT id, name`), paired with filter (row subset) to shrink a dim before broadcast.
- **Spark join strategies:** same `JOIN` SQL; `/*+ ... */` is optimizer hint (plus required), not a discarded comment; shuffle = `Exchange` / move rows so keys co-locate; decision ladder shrink-side → broadcast vs expect sort-merge shuffle; don’t force-broadcast fat sides.
- Asked for concrete query shapes per strategy (hints on otherwise identical joins).

**Implications:** Portable data-movement model in place (collocate / broadcast / shuffle). Ready for a real Redshift or Spark EXPLAIN paste, or skew deep-dive. Still no evidence of live plan walkthrough. Aurora dialect still open.
