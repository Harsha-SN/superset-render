import os
import sys
import sqlite3
import tempfile
from importlib.metadata import version, PackageNotFoundError

print("=" * 70, flush=True)
print("SHILLELAGH / SQLITE DIAGNOSTIC", flush=True)
print("=" * 70, flush=True)

# ---------------------------------------------------------
# 1. Basic environment
# ---------------------------------------------------------
print("\n[1] ENVIRONMENT", flush=True)
print("Python:", sys.version, flush=True)
print("HOME:", os.environ.get("HOME"), flush=True)
print("XDG_CACHE_HOME:", os.environ.get("XDG_CACHE_HOME"), flush=True)
print("TMPDIR:", os.environ.get("TMPDIR"), flush=True)
print("TEMP:", os.environ.get("TEMP"), flush=True)
print("TMP:", os.environ.get("TMP"), flush=True)

# ---------------------------------------------------------
# 2. Package versions
# ---------------------------------------------------------
print("\n[2] PACKAGE VERSIONS", flush=True)

for pkg in [
    "shillelagh",
    "requests-cache",
    "requests",
    "python-jsonpath",
    "sqlalchemy",
]:
    try:
        print(pkg, "=", version(pkg), flush=True)
    except PackageNotFoundError:
        print(pkg, "= NOT FOUND", flush=True)

# ---------------------------------------------------------
# 3. Filesystem
# ---------------------------------------------------------
print("\n[3] FILESYSTEM", flush=True)

paths = [
    "/tmp",
    "/tmp/shillelagh-cache",
    "/app",
    "/app/superset_home",
]

for path in paths:
    print("\nPath:", path, flush=True)

    try:
        print("  exists:", os.path.exists(path), flush=True)
        print("  is_dir:", os.path.isdir(path), flush=True)

        if os.path.exists(path):
            print("  writable:", os.access(path, os.W_OK), flush=True)
            print("  readable:", os.access(path, os.R_OK), flush=True)

            try:
                print("  contents:", os.listdir(path)[:20], flush=True)
            except Exception as e:
                print("  list failed:", repr(e), flush=True)

    except Exception as e:
        print("  ERROR:", repr(e), flush=True)

# ---------------------------------------------------------
# 4. Test normal SQLite
# ---------------------------------------------------------
print("\n[4] SQLITE DIRECT TEST", flush=True)

sqlite_paths = [
    "/tmp/test_sqlite.db",
    "/tmp/shillelagh-cache/test_sqlite.db",
]

for db_path in sqlite_paths:
    print("\nTesting:", db_path, flush=True)

    try:
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        conn = sqlite3.connect(db_path)
        conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER)")
        conn.execute("INSERT INTO test (id) VALUES (1)")
        conn.commit()

        print("  SQLITE: OK", flush=True)

        conn.close()

    except Exception as e:
        print("  SQLITE: FAILED", repr(e), flush=True)

# ---------------------------------------------------------
# 5. requests-cache test
# ---------------------------------------------------------
print("\n[5] REQUESTS-CACHE TEST", flush=True)

try:
    import requests_cache

    print("requests_cache module:", requests_cache, flush=True)

    cache_locations = [
        "/tmp/shillelagh-cache/test_requests_cache",
        "/tmp/test_requests_cache",
    ]

    for location in cache_locations:

        print("\nTesting cache:", location, flush=True)

        try:
            session = requests_cache.CachedSession(
                cache_name=location,
                backend="sqlite",
            )

            print("  session created: OK", flush=True)

            response = session.get(
                "https://analytics-api-82mg.onrender.com/api/product-performance/categories",
                timeout=20,
            )

            print("  HTTP status:", response.status_code, flush=True)
            print("  content-type:", response.headers.get("content-type"), flush=True)

            session.close()

        except Exception as e:
            print("  CACHE FAILED:", repr(e), flush=True)

except Exception as e:
    print("requests-cache IMPORT FAILED:", repr(e), flush=True)

# ---------------------------------------------------------
# 6. GenericJSONAPI
# ---------------------------------------------------------
print("\n[6] GENERIC JSON API", flush=True)

BASE = (
    "https://analytics-api-82mg.onrender.com"
    "/api/product-performance/categories"
)

try:
    from shillelagh.adapters.api.generic_json import GenericJSONAPI

    print("GenericJSONAPI import: OK", flush=True)

    print("\nTesting supports(fast=True)...", flush=True)

    try:
        result = GenericJSONAPI.supports(BASE, fast=True)
        print("RESULT:", repr(result), flush=True)
    except Exception as e:
        print("FAST FAILED:", repr(e), flush=True)

    print("\nTesting supports(fast=False)...", flush=True)

    try:
        result = GenericJSONAPI.supports(BASE, fast=False)
        print("RESULT:", repr(result), flush=True)
    except Exception as e:
        print("SLOW FAILED:", repr(e), flush=True)

except Exception as e:
    print("GenericJSONAPI IMPORT FAILED:", repr(e), flush=True)

# ---------------------------------------------------------
# 7. Finish
# ---------------------------------------------------------
print("\n" + "=" * 70, flush=True)
print("DIAGNOSTIC COMPLETE", flush=True)
print("=" * 70, flush=True)
