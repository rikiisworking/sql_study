#!/usr/bin/env python3
"""Shared drill runner. Prefer: python3 drills/drill-01-03.py

This file is the engine. `python3 drills/check.py` runs every drill-*.py.
"""

from __future__ import annotations

import csv
import importlib.util
import inspect
import io
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEED = ROOT / "seeds" / "seed.sql"
SOLUTIONS = ROOT / "solutions"


def load_db(seed: Path | None = None) -> sqlite3.Connection:
    path = seed or SEED
    conn = sqlite3.connect(":memory:")
    conn.executescript(path.read_text())
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


def read_expected(text: str) -> tuple[list[str], list[tuple]]:
    raw = text.strip()
    if not raw:
        return [], []
    reader = csv.reader(io.StringIO(raw))
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


def answer_sql(case: dict) -> str | None:
    path = SOLUTIONS / f"{case['id']}.sql"
    if path.exists():
        return path.read_text()
    return None


def oracle(case: dict) -> tuple[list[str], list[tuple]]:
    sql = answer_sql(case)
    if sql:
        conn = load_db(case.get("_seed"))
        try:
            cols, rows = run_query(conn, sql)
        finally:
            conn.close()
        return cols, [tuple(normalize_got(v) for v in r) for r in rows]
    if case.get("expected"):
        return read_expected(case["expected"])
    raise ValueError(f"no oracle for {case['id']} (need drills/solutions/{case['id']}.sql)")


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


def from_module(mod) -> list[dict]:
    """Collect exercise functions (pyspark-style) plus optional CASES dicts."""
    seed = getattr(mod, "SEED", SEED)
    seed_path = Path(seed) if not isinstance(seed, Path) else seed
    if not seed_path.is_absolute():
        seed_path = ROOT / seed_path
    forbid_map = getattr(mod, "FORBID", {}) or {}
    require_map = getattr(mod, "REQUIRE", {}) or {}

    found = []
    for name, fn in inspect.getmembers(mod, inspect.isfunction):
        if name.startswith("_"):
            continue
        if getattr(fn, "__module__", None) != getattr(mod, "__name__", None):
            continue
        found.append((fn.__code__.co_firstlineno, name, fn))
    found.sort()

    cases: list[dict] = []
    for _, name, fn in found:
        todo = False
        try:
            query = fn()
        except NotImplementedError:
            query = ""
            todo = True
        if not isinstance(query, str):
            query = ""
            todo = True
        cases.append(
            {
                "id": name,
                "prompt": inspect.getdoc(fn) or "",
                "query": query,
                "forbid": forbid_map.get(name) or getattr(fn, "forbid", None),
                "require": require_map.get(name) or getattr(fn, "require", None),
                "_seed": seed_path,
                "_todo": todo or not query.strip(),
            }
        )

    for case in getattr(mod, "CASES", []) or []:
        case.setdefault("_seed", seed_path)
        cases.append(case)
    return cases


def load_all_cases() -> list[dict]:
    cases: list[dict] = []
    for path in sorted(ROOT.glob("drill-*.py")):
        spec = importlib.util.spec_from_file_location(
            path.stem.replace("-", "_"), path
        )
        if spec is None or spec.loader is None:
            continue
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        cases.extend(from_module(mod))
    return cases


def resolve_cases(cases: list[dict], args: list[str]) -> list[dict] | None:
    if not args:
        return cases
    by_id = {c["id"]: c for c in cases}
    ids = [c["id"] for c in cases]
    resolved: list[dict] = []
    for arg in args:
        if arg in by_id:
            resolved.append(by_id[arg])
            continue
        hits = [c for c in cases if arg in c["id"]]
        if not hits:
            print(f"Unknown case: {arg}")
            print("Available:", ", ".join(ids))
            return None
        resolved.extend(hits)
    return resolved


def print_table(name: str, cols: list[str], rows: list[tuple]) -> None:
    print(f"# {name}")
    if not cols:
        print("(no columns / not a SELECT?)")
        return
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


def check_sql_shape(sql: str, case: dict) -> tuple[bool, str]:
    body = strip_sql_comments(sql)
    for pat in case.get("forbid") or []:
        if re.search(pat, body, re.I):
            return False, f"forbidden pattern still in query: {pat}"
    for pat in case.get("require") or []:
        if not re.search(pat, body, re.I):
            return False, f"missing required pattern: {pat}"
    return True, "ok"


def check_one(case: dict) -> bool:
    name = case["id"]
    if case.get("_todo"):
        print(f"TODO {name}  (return a SQL string)")
        return False
    conn = load_db(case.get("_seed"))
    try:
        got_cols, got_rows = run_query(conn, case["query"])
    except Exception as e:
        print(f"FAIL {name}: SQL error: {e}")
        return False
    finally:
        conn.close()

    try:
        exp_cols, exp_rows = oracle(case)
    except Exception as e:
        print(f"FAIL {name}: oracle error: {e}")
        return False
    ok, _msg = same_result(exp_cols, exp_rows, got_cols, got_rows)
    if not ok:
        got_norm = [tuple(normalize_got(v) for v in r) for r in got_rows]
        print(f"FAIL {name}: result does not match")
        print(f"  columns {got_cols}")
        print(f"  got      {got_norm}")
        return False
    ok_shape, shape_msg = check_sql_shape(case["query"], case)
    if not ok_shape:
        print(f"FAIL {name}: {shape_msg}")
        return False
    print(f"PASS {name}")
    return True


def print_one(case: dict) -> bool:
    name = case["id"]
    prompt = case.get("prompt", "").strip()
    if prompt:
        print(prompt)
        print()
    conn = load_db(case.get("_seed"))
    try:
        cols, rows = run_query(conn, case["query"])
    except Exception as e:
        print(f"SQL error: {e}", file=sys.stderr)
        return False
    finally:
        conn.close()
    print_table(name, cols, rows)
    return True


def main(
    cases: list[dict] | None = None,
    argv: list[str] | None = None,
    seed: Path | str | None = None,
) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    print_only = False
    if argv and argv[0] in ("--print", "-p"):
        print_only = True
        argv = argv[1:]

    if cases is None:
        cases = load_all_cases()
    elif seed is not None:
        seed_path = Path(seed)
        for c in cases:
            c.setdefault("_seed", seed_path)
    if not cases:
        print("No cases found (expected drill functions or CASES)")
        return 1

    selected = resolve_cases(cases, argv)
    if selected is None:
        return 1

    if print_only:
        ok = True
        for i, case in enumerate(selected):
            if i:
                print()
            if not print_one(case):
                ok = False
        return 0 if ok else 1

    passed = sum(1 for c in selected if check_one(c))
    total = len(selected)
    print(f"{passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
