#!/usr/bin/env python3
"""Print a case query result. No pass/fail — just see what SQL returns."""

from __future__ import annotations

import sys
from pathlib import Path

from check import CASES, list_cases, load_db, run_query


def resolve_case(arg: str) -> Path:
    all_names = list_cases()
    if arg in all_names:
        return CASES / arg
    hits = [c for c in all_names if arg in c]
    if len(hits) == 1:
        return CASES / hits[0]
    if not hits:
        raise SystemExit(f"Unknown case: {arg}\nAvailable: {', '.join(all_names)}")
    raise SystemExit(f"Ambiguous {arg!r}: {', '.join(hits)}")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python drills/run.py <case>", file=sys.stderr)
        print("  e.g. python drills/run.py l1_01", file=sys.stderr)
        return 2

    case_dir = resolve_case(argv[1])
    sql = (case_dir / "query.sql").read_text()
    conn = load_db()
    try:
        cols, rows = run_query(conn, sql)
    except Exception as e:
        print(f"SQL error: {e}", file=sys.stderr)
        return 1
    finally:
        conn.close()

    print(f"# {case_dir.name}")
    if not cols:
        print("(no columns / not a SELECT?)")
        return 0

    # simple fixed-width-ish table
    display = [[("NULL" if v is None else str(v)) for v in row] for row in rows]
    widths = [len(c) for c in cols]
    for row in display:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))

    def fmt(cells: list[str]) -> str:
        return " | ".join(c.ljust(widths[i]) for i, c in enumerate(cells))

    print(fmt(cols))
    print("-+-".join("-" * w for w in widths))
    for row in display:
        print(fmt(row))
    print(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")
    return 0


if __name__ == "__main__":
    # allow `python drills/run.py` from repo root (import check from same dir)
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main(sys.argv))
