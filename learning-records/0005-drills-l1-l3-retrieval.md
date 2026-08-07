# Drills harness and L1–L3 retrieval

Added runnable SQLite drills (`drills/seed.sql`, `check.py`, `run.py`, cases). Stdlib only; optional venv via empty `requirements.txt`.

Learner completed cases through `l3_03` with iteration (inspect result, then pass/fail). Defaults to `EXISTS` for “has items,” uses portable WHERE expression for line totals, splits row vs group filters correctly once prompted on HAVING.

**Implications:** Prefer this edit/run loop for future lessons over quiz-only HTML. New lesson → add cases under `drills/cases/`, not re-lecture. Keep `run.py` for debugging without oracle noise.
