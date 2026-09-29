import sys
from importlib.metadata import entry_points, version

print("==============================================", flush=True)
print("SHILLELAGH DIAGNOSTIC", flush=True)
print("==============================================", flush=True)

print("DIAG python:", sys.version, flush=True)

# ============================================================
# PACKAGE VERSIONS
# ============================================================

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
# ADAPTERS
# ============================================================

print("\n=== SHILLELAGH ADAPTERS ===", flush=True)

for ep in entry_points(group="shillelagh.adapter"):
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
# API
# ============================================================

BASE = (
    "https://analytics-api-82mg.onrender.com"
    "/api/product-performance/categories"
)

print("\n=== DIRECT API TEST ===", flush=True)

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
        response.headers.get("content-type"),
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
# GENERIC JSON ADAPTER
# ============================================================

print("\n=== GENERIC JSON ADAPTER ===", flush=True)

try:

    from shillelagh.adapters.api.generic_json import GenericJSONAPI

    print(
        "DIAG GenericJSONAPI import: OK",
        flush=True
    )

    try:

        result = GenericJSONAPI.supports(
            BASE,
            fast=True
        )

        print(
            "DIAG supports fast=True:",
            result,
            flush=True
        )

    except Exception as exc:

        print(
            "DIAG supports fast=True FAILED:",
            repr(exc),
            flush=True
        )

except Exception as exc:

    print(
        "DIAG GenericJSONAPI IMPORT FAILED:",
        repr(exc),
        flush=True
    )

print("\n==============================================", flush=True)
print("DIAGNOSTIC COMPLETE", flush=True)
print("==============================================", flush=True)
