# Drills

Runnable SQLite practice. Fill functions (or `query` in older CASES files). Re-run until green.

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

# lessons 0001–0003 (pass/fail per case)
python3 drills/drill-01-03.py

# one case (full name or substring)
python3 drills/drill-01-03.py l1_01
python3 drills/drill-01-03.py l2_01_not_cancelled

# print result only (no pass/fail)
python3 drills/drill-01-03.py --print l1_01

# all lessons stacked (own seed; write each query)
python3 drills/drill-integrated.py
python3 drills/drill-integrated.py int_01

# lessons 0001–0009 stacked (shop + events; windows)
python3 drills/drill-0001-0009.py
python3 drills/drill-0001-0009.py sf_01

# every drill-*.py (optional)
python3 drills/check.py
```

## Loop

1. Open the drill file — mission is the function docstring.
2. `return """SELECT ..."""` (column names + row order from the docstring).
3. `python3 drills/drill-integrated.py <case>`
4. Fail → fix SQL → repeat. Peek `drills/solutions/<fn>.sql` only when stuck.

## Layout

| Path | Role |
|------|------|
| `seeds/seed.sql` | L1–L3 tables + data (do not change for normal practice) |
| `drill-01-03.py` | L1–L3 — **return SQL from each function** |
| `seeds/seed-integrated.sql` | Richer shop for the 0001–0006 stacked drill |
| `drill-integrated.py` | Lessons 0001–0006 — **return SQL from each function** |
| `seeds/seed-so-far.sql` | Shop + `events` versions for 0001–0009 |
| `drill-0001-0009.py` | Lessons 0001–0009 — **return SQL from each function** |
| `solutions/<case>.sql` | Solutions — do not open until stuck |
| `check.py` | Engine (+ optional run-all) |

## Case map (drill-01-03.py)

| Case | Skill |
|------|--------|
| `l1_01_safe_revenue` | Fan-out: safe order revenue |
| `l1_02_units_by_customer` | Sum at item grain |
| `l2_01_not_cancelled` | `NOT IN` trap → `NOT EXISTS` |
| `l2_02_null_status` | `IS NULL` not `= NULL` |
| `l2_03_left_join_sku_a` | Right filter in `ON` vs `WHERE` |
| `l3_01_filter_line_total` | Alias not in `WHERE` |
| `l3_02_paid_sum_by_customer` | `WHERE` vs `HAVING` |
| `l3_03_repeat_customers` | Full logical walk |

## Case map (drill-integrated.py)

Same shop, extra rows + `order_date`. Qualifying = 2024 + paid + not cancelled.

| Case | Skills stacked |
|------|----------------|
| `int_01_qualifying_orders` | Sargable date + `NOT EXISTS` + paid (NULL status out) |
| `int_02_safe_revenue` | Order grain: no item-join fan-out |
| `int_03_east_having` | Dim filter + `WHERE` vs `HAVING` + grain |
| `int_04_sku_a_optional` | `LEFT JOIN` predicate in `ON` |
| `int_05_big_lines` | Logical order: filter expression, not `SELECT` alias |
| `int_06_dist_not_index` | Recall: `DS_DIST_BOTH` → `DISTKEY`, not index |
| `int_07_shrink_then_broadcast` | Recall: shrink dim before broadcast |

## Case map (drill-0001-0009.py)

Shop plus `events` (version history). Qualifying orders = 2024 + paid + not cancelled.

| Case | Skills stacked |
|------|----------------|
| `sf_01_latest_row` | `ROW_NUMBER` + unique tiebreaker (0008) |
| `sf_02_latest_in_2024` | Filter year *before* the window (0008 + 0003 + 0004) |
| `sf_03_status_flips` | `LAG` + first-row NULL is not a flip (0009 + 0002) |
| `sf_04_east_latest` | Latest then join dim — no event fan-out (0008 + 0001) |
| `sf_05_repeat_flippers` | Flip count + `HAVING` (0009 + 0003) |
| `sf_06_qualifying_revenue` | Order grain + `NOT EXISTS` + range (0001 + 0002 + 0004) |
| `sf_07_skew_or_volume` | Recall: hog vs even volume (0007) |
| `sf_08_dist_not_index` | Recall: `DS_DIST_BOTH` → `DISTKEY` (0006) |
