# Drills (lessons 0001–0003)

Runnable SQLite practice. Edit `cases/*/query.sql`, re-run checker until green.

## Setup (once)

From repo root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Runner needs only stdlib (`sqlite3`). `requirements.txt` is empty of packages on purpose — same setup path when deps show up later.

## Run

```bash
source .venv/bin/activate   # if not already

# all cases (pass/fail vs expected.csv)
python drills/check.py

# one case (full name or substring)
python drills/check.py l1_01
python drills/check.py l2_01_not_cancelled

# print result only (no pass/fail)
python drills/run.py l1_01
```


## Loop

1. Open a case `query.sql` — task is in the `--` comments.
2. Write a query that returns the shape in `expected.csv` (column names + rows, exact order).
3. `python3 drills/check.py <case>`
4. Fail → fix SQL → repeat.

## Layout

| Path | Role |
|------|------|
| `seed.sql` | Shared tables + data (do not change for normal practice) |
| `cases/<name>/query.sql` | **You edit this** |
| `cases/<name>/expected.csv` | Oracle result (header = column names) |
| `check.py` | Runner |

## Case map

| Case | Skill |
|------|--------|
| `l1_01_safe_revenue` | Fan-out: safe order revenue |
| `l1_02_units_by_customer` | Sum at item grain |
| `l1_03_fix_inflated_revenue` | Spot + fix inflated `SUM(amount)` |
| `l2_01_not_cancelled` | `NOT IN` trap → `NOT EXISTS` |
| `l2_02_null_status` | `IS NULL` not `= NULL` |
| `l2_03_left_join_sku_a` | Right filter in `ON` vs `WHERE` |
| `l3_01_filter_line_total` | Alias not in `WHERE` |
| `l3_02_paid_sum_by_customer` | `WHERE` vs `HAVING` |
| `l3_03_repeat_customers` | Full logical walk |

Starters are wrong or stubs on purpose — first run should fail.
