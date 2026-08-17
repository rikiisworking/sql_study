"""
Lessons 0001–0003 drills — grain, 3VL, logical order.

Fill each function. Return a SQL string. Leave the name alone.
Run:
  python3 drills/drill-01-03.py
  python3 drills/drill-01-03.py l1_01
  python3 drills/drill-01-03.py --print l2_01

Data (drills/seeds/seed.sql):

  customers:  id, region
    (10, east)  (20, west)

  orders:  id, customer_id, amount, status
    (1, 10, 100, paid)
    (2, 10,  50, paid)    # cancelled
    (3, 20, 200, NULL)

  order_items:  order_id, sku, qty
    1 A 2, 1 B 1, 2 A 1, 3 C 4

  cancelled:  (2), (NULL)

Solutions (after a real try): drills/solutions/<fn>.sql
"""

from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------------------
# YOUR CODE — return a SQL string (replace `raise NotImplementedError`)
# ---------------------------------------------------------------------------


def l1_01_safe_revenue() -> str:
    """
    Safe order revenue for orders that have at least one item.

    JOIN order_items then SUM(o.amount) fans out (order 1 counted twice).
    Measure lives at order grain — EXISTS / no item join.

    Return one column: revenue
    """

    return """
        SELECT SUM(amount) AS revenue
        FROM orders
        WHERE EXISTS (SELECT 1 FROM order_items WHERE orders.id = order_items.order_id)
    """

def l1_02_units_by_customer() -> str:
    """
    Total units (qty) per customer.

    Summing item qty after join to orders is OK (measure lives at item grain).

    Return columns: customer_id, units
    Order rows by customer_id ascending.
    """

    return """
        SELECT o.customer_id, SUM(oi.qty) AS units
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        GROUP BY o.customer_id
        ORDER BY o.customer_id
    """


def l2_01_not_cancelled() -> str:
    """
    Orders that are not cancelled.

    cancelled has (2) and (NULL). NOT IN over that list never stays TRUE.
    Prefer NOT EXISTS (or strip nulls).

    Return column: id  ordered ascending.
    Order 2 is cancelled.
    """

    return """
        SELECT o.id
        FROM orders o
        WHERE NOT EXISTS (SELECT 1 FROM cancelled c WHERE o.id = c.order_id)
        ORDER BY o.id
    """

def l2_02_null_status() -> str:
    """
    Orders whose status is missing.

    Never use status = NULL.

    Return column: id  ordered ascending.
    """
    return """
        SELECT o.id
        FROM orders o 
        WHERE o.status IS NULL
        ORDER BY o.id ASC
    """

def l2_03_left_join_sku_a() -> str:
    """
    Every order once; attach sku only when the line is sku 'A'.
    Orders with no 'A' line still appear; sku is NULL for them.

    LEFT JOIN ... WHERE i.sku = 'A' drops non-matches.
    Put the sku predicate in ON.

    Return columns: id, sku  ordered by id ascending.
    """
    return """
        SELECT o.id, oi.sku
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id AND oi.sku = 'A'
        ORDER BY o.id
    """

def l3_01_filter_line_total() -> str:
    """
    Keep only lines where amount * qty > 100.

    Toy metric: line_total = orders.amount * order_items.qty
    (alias practice, not real revenue).
    SELECT aliases are not available in WHERE (WHERE runs first).
    SQLite may still accept the alias — repeat the expression.

    Return columns: order_id, sku, line_total
    Order by order_id, sku.
    """
    return """
        SELECT oi.order_id, oi.sku, o.amount * oi.qty AS line_total
        FROM orders o
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE o.amount * oi.qty > 100
        ORDER BY order_id, sku
    """


def l3_02_paid_sum_by_customer() -> str:
    """
    For paid orders only, customers whose SUM(amount) > 100.

    status filter is row-level — WHERE.
    SUM threshold is group-level — HAVING.
    Customer 20 has NULL status (not paid) — out.

    Return columns: customer_id, total  ordered by customer_id.
    """
    return """
        SELECT o.customer_id, SUM(o.amount) AS total
        FROM orders o
        WHERE o.status = 'paid'
        GROUP BY o.customer_id
        HAVING SUM(o.amount) > 100
        ORDER BY o.customer_id
    """

def l3_03_repeat_customers() -> str:
    """
    Customers with at least 2 paid orders; count of those paid orders.

    Walk: FROM orders → WHERE paid → GROUP → HAVING → SELECT → ORDER.
    JOIN not required. Customer 20 has 0 paid (status NULL).

    Return columns: customer_id, paid_orders
    Order by paid_orders DESC, customer_id ASC.
    """
    return """
        SELECT o.customer_id, COUNT(1) AS paid_orders
        FROM orders o
        WHERE status = 'paid'
        GROUP BY o.customer_id
        HAVING COUNT(1) >= 2
        ORDER BY paid_orders DESC, customer_id ASC
    """

# ---------------------------------------------------------------------------
# Checker — do not edit below
# ---------------------------------------------------------------------------

SEED = Path(__file__).resolve().parent / "seeds" / "seed.sql"

FORBID = {
    "l1_01_safe_revenue": [r"\bJOIN\s+order_items\b"],
    "l2_01_not_cancelled": [r"NOT\s+IN\s*\("],
    "l2_02_null_status": [r"=\s*NULL"],
}


if __name__ == "__main__":
    import sys

    from check import from_module, main

    raise SystemExit(main(from_module(sys.modules[__name__])))
