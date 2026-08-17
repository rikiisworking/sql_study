"""
Integrated drills — lessons 0001–0006 stacked.

Fill each function. Return a SQL string. Leave the name alone.
Run:
  python3 drills/drill-integrated.py
  python3 drills/drill-integrated.py int_01
  python3 drills/drill-integrated.py --print int_01

Qualifying order = 2024 + paid + not cancelled.

Data (drills/seeds/seed-integrated.sql):

  customers:  id, region
    (10, east)  (20, west)  (30, east)

  orders:  id, customer_id, amount, status, order_date
    (1, 10, 100, paid, 2024-03-01)
    (2, 10,  50, paid, 2024-06-01)   # cancelled
    (3, 20, 200, NULL, 2023-11-01)
    (4, 20,  80, paid, 2024-08-01)
    (5, 30,  40, paid, 2024-02-01)
    (6, 30,  90, paid, 2024-09-01)

  order_items:  order_id, sku, qty
    1 A 2, 1 B 1, 2 A 1, 3 C 4, 4 B 2, 5 A 1, 6 A 3, 6 D 1

  cancelled:  (2), (NULL)

Solutions (after a real try): drills/solutions/<fn>.sql
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# YOUR CODE — return a SQL string (replace `raise NotImplementedError`)
# ---------------------------------------------------------------------------


def int_01_qualifying_orders() -> str:
    """
    Qualifying order ids: 2024, paid, not cancelled.

    Watch:
      strftime/YEAR on order_date — not sargable; use a half-open range
      NOT IN (cancelled) — cancelled has NULL, so NOT IN never stays TRUE
      status = NULL misses missing status; here you want paid only

    Return column: id  ordered ascending.
    Order 2 is cancelled. Order 3 is 2023 with NULL status.
    """
    return """
        SELECT o.id
        FROM orders o
        WHERE o.status = 'paid' AND 
            NOT EXISTS (SELECT 1 FROM cancelled c WHERE c.order_id = o.id) AND
            o.order_date >= '2024-01-01' AND
            o.order_date < '2025-01-01'
    """

def int_02_safe_revenue() -> str:
    """
    Total order.amount for qualifying orders (2024, paid, not cancelled).

    JOIN order_items then SUM(o.amount) fans out (orders 1 and 6 have 2 lines).
    Measure lives at order grain — EXISTS / no item join.

    Return one column: revenue
    """
    return """
    SELECT SUM(o.amount) AS revenue
    FROM orders o
    WHERE EXISTS (SELECT 1 FROM order_items oi WHERE oi.order_id = o.id) AND
        o.status = 'paid' AND
        NOT EXISTS (SELECT 1 FROM cancelled WHERE o.id = cancelled.order_id) AND
        o.order_date >= '2024-01-01' AND
        o.order_date < '2025-01-01'

    """


def int_03_east_having() -> str:
    """
    East customers: SUM of qualifying order.amount, keep groups with total >= 100.

    Row filters (WHERE): region, 2024 range, paid, not cancelled.
    Group filter (HAVING): SUM >= 100.
    JOIN items fans out. Cancelled 2024 paid (order 2) must stay out.

    Return columns: customer_id, total  ordered by customer_id.
    West customers out.
    """
    return """
    SELECT o.customer_id, SUM(o.amount) AS total
    FROM orders o
    JOIN customers c ON c.id = o.customer_id
    WHERE c.region = 'east' AND
        o.order_date >= '2024-01-01' AND
        o.order_date < '2025-01-01' AND
        o.status = 'paid' AND
        NOT EXISTS (SELECT 1 FROM cancelled x WHERE x.order_id = o.id)
    GROUP BY o.customer_id
    HAVING SUM(o.amount) >= 100
    """


def int_04_sku_a_optional() -> str:
    """
    Every qualifying order once; attach sku only when the line is 'A'.
    Qualifying = 2024 + paid + not cancelled (same WHERE as int_01).
    No 'A' line — still list the order, sku NULL.

    WHERE i.sku = 'A' after LEFT JOIN drops order 4 (only B).
    Put the sku predicate in ON.

    Return columns: id, sku  ordered by id.
    """
    return """
    SELECT o.id, oi.sku
    FROM orders o
    LEFT JOIN order_items oi ON o.id = oi.order_id AND oi.sku = 'A'
    WHERE  o.order_date >= '2024-01-01' AND
        o.order_date < '2025-01-01' AND
        o.status = 'paid' AND
        NOT EXISTS (SELECT 1 FROM cancelled x WHERE x.order_id = o.id)
    ORDER BY o.id
    """

def int_05_big_lines() -> str:
    """
    Qualifying orders' lines where amount * qty > 100.
    Qualifying = 2024 + paid + not cancelled (same WHERE as int_01).
    Toy metric (alias practice). SELECT alias not portable in WHERE —
    repeat the expression.

    Return columns: order_id, sku, line_total
    Order by order_id, sku.
    """
    return """
    SELECT o.id AS order_id, oi.sku, o.amount * oi.qty AS line_total
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.id
    WHERE  o.order_date >= '2024-01-01' AND
        o.order_date < '2025-01-01' AND
        o.status = 'paid' AND
        NOT EXISTS (SELECT 1 FROM cancelled x WHERE x.order_id = o.id) AND
         o.amount * oi.qty > 100
    ORDER BY order_id, sku
    """

def int_06_dist_not_index() -> str:
    """
    Recall only — not a shop query. Lessons 0005 / 0006.

    Situation: Redshift. Big fact table JOIN dim ON customer_id.
    EXPLAIN shows DS_DIST_BOTH: the engine ships both sides across
    the network so matching keys can meet. Rows with the same
    customer_id do not already live on the same slice.

    Question: first layout lever. This is about where rows sit
    (placement), not a B-tree that finds rows (index).

    Return one column named next, one lowercase word.
    """
    return """
        SELECT 'distkey' AS next;
    """


def int_07_shrink_then_broadcast() -> str:
    """
    Recall only — not a shop query. Lesson 0006.

    Situation: Spark. 2 TB fact JOIN 500 MB dimension.
    Auto-broadcast threshold is ~10 MB, so 500 MB will not
    broadcast by itself. A hint that force-broadcasts 500 MB
    can blow executor memory.

    Question: first move, before any broadcast hint.
    Cut the dim down (filter rows + keep only needed columns),
    then check size again.

    Return one column named next, one lowercase word.
    """
    return """
    SELECT 'shrink' AS next;
    """

# ---------------------------------------------------------------------------
# Checker — do not edit below
# ---------------------------------------------------------------------------

SEED = Path(__file__).resolve().parent / "seeds" / "seed-integrated.sql"

FORBID = {
    "int_01_qualifying_orders": [r"strftime\s*\(", r"YEAR\s*\(", r"NOT\s+IN\s*\("],
    "int_02_safe_revenue": [r"strftime\s*\(", r"YEAR\s*\(", r"\bJOIN\s+order_items\b"],
    "int_03_east_having": [r"strftime\s*\(", r"YEAR\s*\(", r"\bJOIN\s+order_items\b"],
    "int_04_sku_a_optional": [r"strftime\s*\(", r"YEAR\s*\("],
}


if __name__ == "__main__":
    import sys

    from check import from_module, main

    raise SystemExit(main(from_module(sys.modules[__name__])))
