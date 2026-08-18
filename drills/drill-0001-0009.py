"""
Stacked drills — lessons 0001–0009.

Fill each function. Return a SQL string. Leave the name alone.
Run:
  python3 drills/drill-0001-0009.py
  python3 drills/drill-0001-0009.py sf_01
  python3 drills/drill-0001-0009.py --print sf_01

Qualifying order = 2024 + paid + not cancelled.

Data (drills/seeds/seed-so-far.sql):

  customers:  id, region
    10 east  20 west  30 east  40 west  50 east

  orders / order_items / cancelled: same shop as drill-integrated.py
    cancelled: (2), (NULL)

  events:  event_id, customer_id, updated_at, status
    10: 1 2024-01-01 new; 2 2024-06-01 active; 3 2024-06-01 closed
    20: 4 2024-03-01 new
    30: 5 2024-02-01 new; 6 2024-04-01 active; 7 2024-07-01 paused
    40: 8 2023-12-01 new; 9 2024-05-01 closed
    50: 10 2024-01-15 new; 11 2025-01-02 active

Solutions (after a real try): drills/solutions/<fn>.sql
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# YOUR CODE — return a SQL string (replace `raise NotImplementedError`)
# ---------------------------------------------------------------------------


def sf_01_latest_row() -> str:
    """
    Current status row per customer (lesson 0008).

    One row per customer: newest event, every column of that event.
    GROUP BY cannot return the other columns of the winner.
    Same-day tie on customer 10 — ORDER BY updated_at DESC, event_id DESC.

    Return columns: customer_id, event_id, updated_at, status
    Order by customer_id.
    """
    raise NotImplementedError


def sf_02_latest_in_2024() -> str:
    """
    Current 2024 status row per customer (0008 + 0003 + 0004).

    Keep events with updated_at in 2024, then take the latest of those.
    Windows see the virtual table after WHERE — filter the year first.
    ROW_NUMBER over all years then WHERE rn = 1 AND 2024 drops customer 50
    (their global winner is 2025).

    Half-open range; no strftime/YEAR on updated_at.

    Return columns: customer_id, event_id, updated_at, status
    Order by customer_id.
    """
    raise NotImplementedError


def sf_03_status_flips() -> str:
    """
    Status-change events (lesson 0009 + 0002).

    For each event, previous status for that customer (time ASC, event_id ASC).
    Keep only real flips. First row in a partition has no previous —
    LAG is NULL. status <> prev_status is UNKNOWN there; do not treat
    that as a flip.

    Return columns: customer_id, event_id, prev_status, status
    Order by customer_id, event_id.
    """
    raise NotImplementedError


def sf_04_east_latest() -> str:
    """
    Latest status for east customers (0008 + 0001).

    One row per east customer who has events. Join the latest event,
    not every event (that fans out). West out.

    Return columns: customer_id, status
    Order by customer_id.
    """
    raise NotImplementedError


def sf_05_repeat_flippers() -> str:
    """
    Customers with at least two status flips (0009 + 0003).

    A flip is the same test as sf_03 (previous exists and status changed).
    Count is a group filter — HAVING, not WHERE.

    Return columns: customer_id, flips
    Order by customer_id.
    """
    raise NotImplementedError


def sf_06_qualifying_revenue() -> str:
    """
    Total order.amount for qualifying orders (0001 + 0002 + 0004).

    Qualifying = 2024 + paid + not cancelled.
    JOIN order_items then SUM(o.amount) fans out (orders 1 and 6 have 2 lines).
    cancelled has NULL — NOT IN never stays TRUE.

    Return one column: revenue
    """
    raise NotImplementedError


def sf_07_skew_or_volume() -> str:
    """
    Recall only — not a shop query. Lesson 0007.

    Situation: Spark join. Stage summary: max task 40 min, median 2 min.
    One task processed 80M records; siblings ~2M. Total bytes look normal.

    Question: even volume, or one worker hog?
    Return one column named next, one lowercase word (the problem name).
    """
    raise NotImplementedError


def sf_08_dist_not_index() -> str:
    """
    Recall only — not a shop query. Lessons 0005 / 0006.

    Situation: Redshift. Big fact JOIN dim ON customer_id.
    EXPLAIN shows DS_DIST_BOTH. Matching keys are not already on
    the same slice.

    Question: first layout lever. Placement, not a B-tree.
    Return one column named next, one lowercase word.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# Checker — do not edit below
# ---------------------------------------------------------------------------

SEED = Path(__file__).resolve().parent / "seeds" / "seed-so-far.sql"

FORBID = {
    "sf_02_latest_in_2024": [r"strftime\s*\(", r"YEAR\s*\("],
    "sf_06_qualifying_revenue": [
        r"strftime\s*\(",
        r"YEAR\s*\(",
        r"\bJOIN\s+order_items\b",
        r"NOT\s+IN\s*\(",
    ],
}

REQUIRE = {
    "sf_01_latest_row": [r"ROW_NUMBER\s*\("],
    "sf_02_latest_in_2024": [r"ROW_NUMBER\s*\("],
    "sf_03_status_flips": [r"\bLAG\s*\("],
    "sf_04_east_latest": [r"ROW_NUMBER\s*\("],
    "sf_05_repeat_flippers": [r"\bLAG\s*\("],
}


if __name__ == "__main__":
    import sys

    from check import from_module, main

    raise SystemExit(main(from_module(sys.modules[__name__])))
