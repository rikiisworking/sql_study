# Sargable predicates and obfuscation rewrites

Learner moved into optimization track (lesson 0004). Engaged with **other common obfuscations** beyond dates: asked for recommended fixes (math on column, cast/type mix, concat names, `LOWER(email)`).

**Evidence:** Follow-up on lesson 0004 section “Other common obfuscations”; bare-column + transform-the-constant pattern for non-date cases.

**Implications:** Do not re-lecture date ranges if quizzes done. Ready for reading plans (EXPLAIN) to verify whether a rewrite changed the access path. Aurora dialect still unknown — portable plan vocabulary without assuming MySQL vs PG.
