#!/usr/bin/env python3
"""Run drill SQL against seed; compare to expected CSV. Stdlib only."""

from __future__ import annotations

import csv
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = ROOT / "seed.sql"
CASES = ROOT / "cases"


def load_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript(SEED.read_text())
    return conn


def strip_sql_comments(sql: str) -> str:
    """Drop full-line -- comments; keep query body."""
    lines = []
    for line in sql.splitlines():
        if re.match(r"^\s*--", line):
            continue
        lines.append(line)
    return "\n".join(lines).strip()


def run_query(conn: sqlite3.Connection, sql: str) -> tuple[list[str], list[tuple]]:
    body = strip_sql_comments(sql)
    if not body:
        raise ValueError("empty query (only comments?)")
    cur = conn.execute(body)
    cols = [d[0] for d in cur.description] if cur.description else []
    rows = cur.fetchall()
    return cols, rows


def read_expected(path: Path) -> tuple[list[str], list[tuple]]:
    with path.open(newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return [], []
    cols = rows[0]
    data = []
    for row in rows[1:]:
        if not row or all(c.strip() == "" for c in row):
            continue
        data.append(tuple(normalize_cell(c) for c in row))
    return cols, data


def normalize_cell(s: str):
    s = s.strip()
    if s == "" or s.upper() == "NULL":
        return None
    try:
        if re.fullmatch(r"-?\d+", s):
            return int(s)
        if re.fullmatch(r"-?\d+\.\d+", s):
            return float(s)
    except ValueError:
        pass
    return s


def normalize_got(val):
    if val is None:
        return None
    if isinstance(val, float) and val == int(val):
        return int(val)
    return val


def same_result(
    exp_cols: list[str],
    exp_rows: list[tuple],
    got_cols: list[str],
    got_rows: list[tuple],
) -> tuple[bool, str]:
    if [c.lower() for c in got_cols] != [c.lower() for c in exp_cols]:
        return False, f"columns: expected {exp_cols}, got {got_cols}"
    got_norm = [tuple(normalize_got(v) for v in r) for r in got_rows]
    if got_norm != exp_rows:
        return False, f"rows:\n  expected {exp_rows}\n  got      {got_norm}"
    return True, "ok"


def list_cases() -> list[str]:
    if not CASES.is_dir():
        return []
    return sorted(
        p.name
        for p in CASES.iterdir()
        if p.is_dir() and (p / "query.sql").exists() and (p / "expected.csv").exists()
    )


def check_one(name: str) -> bool:
    case_dir = CASES / name
    query_path = case_dir / "query.sql"
    exp_path = case_dir / "expected.csv"
    if not query_path.exists() or not exp_path.exists():
        print(f"FAIL {name}: missing query.sql or expected.csv")
        return False

    conn = load_db()
    try:
        got_cols, got_rows = run_query(conn, query_path.read_text())
    except Exception as e:
        print(f"FAIL {name}: SQL error: {e}")
        return False
    finally:
        conn.close()

    exp_cols, exp_rows = read_expected(exp_path)
    ok, msg = same_result(exp_cols, exp_rows, got_cols, got_rows)
    if ok:
        print(f"PASS {name}")
        return True
    print(f"FAIL {name}: {msg}")
    return False


def main(argv: list[str]) -> int:
    names = argv[1:] if len(argv) > 1 else list_cases()
    if not names:
        print("No cases found under drills/cases/")
        return 1
    unknown = [n for n in names if n not in list_cases() and not (CASES / n).is_dir()]
    # allow partial name filter
    all_names = list_cases()
    if names != all_names:
        resolved = []
        for n in names:
            if n in all_names:
                resolved.append(n)
            else:
                hits = [c for c in all_names if n in c]
                if not hits:
                    print(f"Unknown case: {n}")
                    print("Available:", ", ".join(all_names))
                    return 1
                resolved.extend(hits)
        names = resolved

    passed = sum(1 for n in names if check_one(n))
    total = len(names)
    print(f"{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
