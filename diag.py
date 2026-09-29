import sys
import os
from importlib.metadata import entry_points, version

print("==============================================", flush=True)
print("SHILLELAGH DIAGNOSTIC", flush=True)
print("==============================================", flush=True)

# ============================================================
# PYTHON VERSION
# ============================================================

print(
    "DIAG python:",
    sys.version,
    flush=True
)


# ============================================================
# TEST SHILLELAGH CACHE DIRECTORY
# ============================================================

CACHE_DIR = "/tmp/shillelagh-cache"

try:

    os.makedirs(
        CACHE_DIR,
        exist_ok=True
    )

    test_file = os.path.join(
        CACHE_DIR,
        "test.txt"
    )

    with open(
        test_file,
        "w"
    ) as f:

        f.write("test")

    print(
        "DIAG CACHE WRITE: OK",
        flush=True
    )

except Exception as exc:

    print(
        "DIAG CACHE WRITE FAILED:",
        repr(exc),
        flush=True
    )


# ============================================================
# PACKAGE VERSIONS
# ============================================================

print(
    "\n=== PACKAGE VERSIONS ===",
    flush=True
)

for pkg in [
    "shillelagh",
    "python-jsonpath",
    "yarl",
    "prison",
    "requests-cache",
    "apsw"
]:

    try:

        print(
            "DIAG version:",
            pkg,
            version(pkg),
            flush=True
        )

    except Exception as exc:

        print(
            "DIAG version FAILED:",
            pkg,
            repr(exc),
            flush=True
        )


# ============================================================
# SHILLELAGH ADAPTERS
# ============================================================

print(
    "\n=== SHILLELAGH ADAPTERS ===",
    flush=True
)

for ep in entry_points(
    group="shillelagh.adapter"
):

    try:

        ep.load()

        print(
            "DIAG adapter OK:",
            ep.name,
            flush=True
        )

    except Exception as exc:

        print(
            "DIAG adapter LOAD FAILED:",
            ep.name,
            repr(exc),
            flush=True
        )


# ============================================================
# ANALYTICS API
# ============================================================

BASE = (
    "https://analytics-api-82mg.onrender.com"
    "/api/product-performance/categories"
)

print(
    "\n=== ANALYTICS API TEST ===",
    flush=True
)

print(
    "DIAG API URL:",
    BASE,
    flush=True
)


# ============================================================
# DIRECT HTTP TEST
# ============================================================

try:

    import requests

    response = requests.get(
        BASE,
        timeout=20
    )

    print(
        "DIAG HTTP STATUS:",
        response.status_code,
        flush=True
    )

    print(
        "DIAG CONTENT TYPE:",
        response.headers.get(
            "content-type"
        ),
        flush=True
    )

    print(
        "DIAG RESPONSE:",
        response.text[:1000],
        flush=True
    )

except Exception as exc:

    print(
        "DIAG DIRECT API FAILED:",
        repr(exc),
        flush=True
    )


# ============================================================
# GENERIC JSON API
# ============================================================

print(
    "\n=== GENERIC JSON API ===",
    flush=True
)

try:

    from shillelagh.adapters.api.generic_json import (
        GenericJSONAPI
    )

    print(
        "DIAG GenericJSONAPI import: OK",
        flush=True
    )

except Exception as exc:

    print(
        "DIAG GenericJSONAPI IMPORT FAILED:",
        repr(exc),
        flush=True
    )

    GenericJSONAPI = None


# ============================================================
# FAST SUPPORT CHECK
# ============================================================

if GenericJSONAPI:

    try:

        result_fast = GenericJSONAPI.supports(
            BASE,
            fast=True
        )

        print(
            "DIAG supports fast=True:",
            result_fast,
            flush=True
        )

    except Exception as exc:

        print(
            "DIAG supports fast=True FAILED:",
            repr(exc),
            flush=True
        )


# ============================================================
# SLOW SUPPORT CHECK
# ============================================================

if GenericJSONAPI:

    try:

        result_slow = GenericJSONAPI.supports(
            BASE,
            fast=False
        )

        print(
            "DIAG supports fast=False:",
            result_slow,
            flush=True
        )

    except Exception as exc:

        print(
            "DIAG supports fast=False FAILED:",
            repr(exc),
            flush=True
        )


# ============================================================
# SHILLELAGH SQL TEST
# ============================================================

print(
    "\n=== SHILLELAGH SQL TEST ===",
    flush=True
)

candidates = [

    BASE,

    BASE + "#$",

    BASE + "#$[*]",

    BASE + "#$.data[*]"
]


try:

    from sqlalchemy import create_engine

    for url in candidates:

        try:

            with create_engine(
                "shillelagh://"
            ).connect() as conn:

                rows = conn.exec_driver_sql(
                    f'SELECT * FROM "{url}" LIMIT 2'
                ).fetchall()

            print(
                "DIAG query OK:",
                url,
                rows,
                flush=True
            )

        except Exception as exc:

            print(
                "DIAG query FAILED:",
                url,
                repr(exc),
                flush=True
            )

except Exception as exc:

    print(
        "DIAG SQL ENGINE FAILED:",
        repr(exc),
        flush=True
    )


# ============================================================
# FINISHED
# ============================================================

print(
    "\n==============================================",
    flush=True
)

print(
    "DIAGNOSTIC COMPLETE",
    flush=True
)

print(
    "==============================================",
    flush=True
)
