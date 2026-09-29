import os
import sys
import traceback
import sqlite3
from importlib.metadata import version, entry_points

print("=" * 70, flush=True)
print("SHILLELAGH / SQLITE DIAGNOSTIC", flush=True)
print("=" * 70, flush=True)


# ============================================================
# 1. ENVIRONMENT
# ============================================================

print("\n[1] ENVIRONMENT", flush=True)
print("-" * 60, flush=True)

print("Python:", sys.version, flush=True)
print("HOME:", os.getenv("HOME"), flush=True)
print("XDG_CACHE_HOME:", os.getenv("XDG_CACHE_HOME"), flush=True)
print("TMPDIR:", os.getenv("TMPDIR"), flush=True)
print("TEMP:", os.getenv("TEMP"), flush=True)
print("TMP:", os.getenv("TMP"), flush=True)


# ============================================================
# 2. PACKAGE VERSIONS
# ============================================================

print("\n[2] PACKAGE VERSIONS", flush=True)
print("-" * 60, flush=True)

packages = [
    "shillelagh",
    "requests-cache",
    "requests",
    "python-jsonpath",
    "sqlalchemy",
    "apsw",
    "prison",
    "yarl",
]

for pkg in packages:
    try:
        print(f"{pkg} = {version(pkg)}", flush=True)
    except Exception as exc:
        print(f"{pkg} = VERSION FAILED: {repr(exc)}", flush=True)


# ============================================================
# 3. FILESYSTEM
# ============================================================

print("\n[3] FILESYSTEM", flush=True)
print("-" * 60, flush=True)


def inspect_path(path):
    print(f"\nPath: {path}", flush=True)

    try:
        print("  exists:", os.path.exists(path), flush=True)
        print("  is_dir:", os.path.isdir(path), flush=True)
        print("  writable:", os.access(path, os.W_OK), flush=True)
        print("  readable:", os.access(path, os.R_OK), flush=True)

        if os.path.isdir(path):
            print(
                "  contents:",
                os.listdir(path)[:30],
                flush=True,
            )

    except Exception as exc:
        print("  ERROR:", repr(exc), flush=True)


for path in [
    "/tmp",
    "/tmp/shillelagh-cache",
    "/app",
    "/app/superset_home",
    "/root",
    "/home",
    "/home/superset",
]:
    inspect_path(path)


# ============================================================
# 4. SQLITE DIRECT TEST
# ============================================================

print("\n[4] SQLITE DIRECT TEST", flush=True)
print("-" * 60, flush=True)


def sqlite_test(db_path):
    print(f"\nTesting: {db_path}", flush=True)

    try:
        conn = sqlite3.connect(db_path)

        conn.execute(
            "CREATE TABLE IF NOT EXISTS diagnostic "
            "(id INTEGER PRIMARY KEY, value TEXT)"
        )

        conn.execute(
            "INSERT INTO diagnostic(value) VALUES (?)",
            ("test",),
        )

        conn.commit()

        row = conn.execute(
            "SELECT COUNT(*) FROM diagnostic"
        ).fetchone()

        print("  SQLITE: OK", flush=True)
        print("  rows:", row, flush=True)

        conn.close()

    except Exception as exc:
        print("  SQLITE FAILED:", repr(exc), flush=True)
        traceback.print_exc()


sqlite_test("/tmp/test_sqlite.db")
sqlite_test("/tmp/shillelagh-cache/test_sqlite.db")


# ============================================================
# 5. REQUESTS-CACHE TEST
# ============================================================

print("\n[5] REQUESTS-CACHE TEST", flush=True)
print("-" * 60, flush=True)

try:
    import requests_cache

    print("requests_cache module:", requests_cache, flush=True)

    cache_locations = [
        "/tmp/shillelagh-cache/test_requests_cache",
        "/tmp/test_requests_cache",
    ]

    for cache_name in cache_locations:

        print(f"\nTesting cache: {cache_name}", flush=True)

        try:
            session = requests_cache.CachedSession(
                cache_name=cache_name,
                backend="sqlite",
            )

            print("  session created: OK", flush=True)

            try:
                response = session.get(
                    "https://analytics-api-82mg.onrender.com/"
                    "api/product-performance/categories",
                    timeout=15,
                )

                print(
                    "  HTTP status:",
                    response.status_code,
                    flush=True,
                )

                print(
                    "  content-type:",
                    response.headers.get("content-type"),
                    flush=True,
                )

            except Exception as exc:
                print(
                    "  HTTP FAILED:",
                    repr(exc),
                    flush=True,
                )

            try:
                session.close()
            except Exception:
                pass

        except Exception as exc:
            print(
                "  SESSION FAILED:",
                repr(exc),
                flush=True,
            )

except Exception as exc:
    print(
        "requests-cache IMPORT FAILED:",
        repr(exc),
        flush=True,
    )


# ============================================================
# 5.5 SHILLELAGH SESSION / CACHE INSPECTION
# ============================================================

print("\n[5.5] SHILLELAGH SESSION / CACHE INSPECTION", flush=True)
print("-" * 60, flush=True)

try:
    import shillelagh
    import shillelagh.lib

    print(
        "shillelagh package:",
        shillelagh.__file__,
        flush=True,
    )

    print(
        "shillelagh.lib:",
        shillelagh.lib.__file__,
        flush=True,
    )

    print("\nSearching Shillelagh source for cache/session/SQLite references...",
          flush=True)

    shillelagh_base = os.path.dirname(shillelagh.__file__)

    matches = []

    for root, dirs, files in os.walk(shillelagh_base):

        # Avoid unnecessary cache directories
        dirs[:] = [
            d for d in dirs
            if d not in {
                "__pycache__",
                ".pytest_cache",
                ".mypy_cache",
            }
        ]

        for filename in files:

            if not filename.endswith(".py"):
                continue

            filepath = os.path.join(root, filename)

            try:
                with open(
                    filepath,
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                ) as f:
                    lines = f.readlines()

                for line_number, line in enumerate(lines, start=1):

                    lower = line.lower()

                    if any(
                        keyword in lower
                        for keyword in [
                            "requests_cache",
                            "cachedsession",
                            "cache_name",
                            "sqlite",
                            "session =",
                            "get_session",
                        ]
                    ):

                        matches.append(
                            (
                                filepath,
                                line_number,
                                line.strip(),
                            )
                        )

            except Exception:
                pass

    print(
        "Source matches found:",
        len(matches),
        flush=True,
    )

    for filepath, line_number, line in matches[:200]:

        print(
            f"{filepath}:{line_number}: {line}",
            flush=True,
        )

except Exception as exc:

    print(
        "SOURCE INSPECTION FAILED:",
        repr(exc),
        flush=True,
    )

    traceback.print_exc()


# ============================================================
# 5.6 SHILLELAGH LIBRARY FILES
# ============================================================

print("\n[5.6] SHILLELAGH LIBRARY FILES", flush=True)
print("-" * 60, flush=True)

try:

    import shillelagh

    base = os.path.dirname(shillelagh.__file__)

    print("Shillelagh base:", base, flush=True)

    for root, dirs, files in os.walk(base):

        dirs[:] = [
            d for d in dirs
            if d not in {
                "__pycache__",
                ".pytest_cache",
                ".mypy_cache",
            }
        ]

        for filename in files:

            if filename.endswith(".py"):

                path = os.path.join(root, filename)

                if (
                    "lib" in path.lower()
                    or "api" in path.lower()
                    or "http" in path.lower()
                ):

                    print(path, flush=True)

except Exception as exc:

    print(
        "FILE INSPECTION FAILED:",
        repr(exc),
        flush=True,
    )


# ============================================================
# 6. DIRECT API TEST
# ============================================================

print("\n[6] DIRECT ANALYTICS API TEST", flush=True)
print("-" * 60, flush=True)

BASE = (
    "https://analytics-api-82mg.onrender.com"
    "/api/product-performance/categories"
)

try:

    import requests

    print("URL:", BASE, flush=True)

    response = requests.get(
        BASE,
        timeout=30,
    )

    print(
        "HTTP status:",
        response.status_code,
        flush=True,
    )

    print(
        "Content-Type:",
        response.headers.get("content-type"),
        flush=True,
    )

    print(
        "Response length:",
        len(response.text),
        flush=True,
    )

    print(
        "Response preview:",
        response.text[:1000],
        flush=True,
    )

except Exception as exc:

    print(
        "DIRECT API FAILED:",
        repr(exc),
        flush=True,
    )

    traceback.print_exc()


# ============================================================
# 7. GENERIC JSON API
# ============================================================

print("\n[7] GENERIC JSON API", flush=True)
print("-" * 60, flush=True)

try:

    from shillelagh.adapters.api.generic_json import GenericJSONAPI

    print(
        "GenericJSONAPI import: OK",
        flush=True,
    )

    # --------------------------------------------------------
    # supports(fast=True)
    # --------------------------------------------------------

    print(
        "\nTesting supports(fast=True)...",
        flush=True,
    )

    try:

        result_fast = GenericJSONAPI.supports(
            BASE,
            fast=True,
        )

        print(
            "RESULT:",
            result_fast,
            flush=True,
        )

    except Exception as exc:

        print(
            "FAST FAILED:",
            repr(exc),
            flush=True,
        )

        traceback.print_exc()

    # --------------------------------------------------------
    # supports(fast=False)
    # --------------------------------------------------------

    print(
        "\nTesting supports(fast=False)...",
        flush=True,
    )

    try:

        result_slow = GenericJSONAPI.supports(
            BASE,
            fast=False,
        )

        print(
            "RESULT:",
            result_slow,
            flush=True,
        )

    except Exception as exc:

        print(
            "SLOW FAILED:",
            repr(exc),
            flush=True,
        )

        traceback.print_exc()

except Exception as exc:

    print(
        "GenericJSONAPI IMPORT FAILED:",
        repr(exc),
        flush=True,
    )

    traceback.print_exc()


# ============================================================
# 8. SQL TESTS
# ============================================================

print("\n[8] SHILLELAGH SQL TESTS", flush=True)
print("-" * 60, flush=True)

try:

    from sqlalchemy import create_engine

    candidates = [
        BASE,
        BASE + "#$",
        BASE + "#$[*]",
        BASE + "#$.data[*]",
    ]

    print(
        "Testing candidates:",
        flush=True,
    )

    for url in candidates:

        print(
            "\nURL:",
            url,
            flush=True,
        )

        try:

            with create_engine(
                "shillelagh://"
            ).connect() as conn:

                rows = conn.exec_driver_sql(
                    f'SELECT * FROM "{url}" LIMIT 2'
                ).fetchall()

                print(
                    "QUERY OK:",
                    rows,
                    flush=True,
                )

        except Exception as exc:

            print(
                "QUERY FAILED:",
                repr(exc),
                flush=True,
            )

except Exception as exc:

    print(
        "SQL TEST SETUP FAILED:",
        repr(exc),
        flush=True,
    )

    traceback.print_exc()


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70, flush=True)
print("DIAGNOSTIC COMPLETE", flush=True)
print("=" * 70, flush=True)
