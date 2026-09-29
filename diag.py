import sys
from importlib.metadata import entry_points, version

print("DIAG python:", sys.version, flush=True)

for pkg in ["shillelagh", "python-jsonpath", "yarl", "prison", "requests-cache", "apsw"]:
    try:
        print("DIAG version:", pkg, version(pkg), flush=True)
    except Exception as exc:
        print("DIAG version FAILED:", pkg, exc, flush=True)

for ep in entry_points(group="shillelagh.adapter"):
    try:
        ep.load()
        print("DIAG adapter OK:", ep.name, flush=True)
    except Exception as exc:
        print("DIAG adapter LOAD FAILED:", ep.name, repr(exc), flush=True)

from sqlalchemy import create_engine

BASE = "https://analytics-api-82mg.onrender.com/api/product-performance/categories"
candidates = [
    BASE,
    BASE + "#$",
    BASE + "#$[*]",
]
for url in candidates:
    try:
        with create_engine("shillelagh://").connect() as conn:
            rows = conn.exec_driver_sql(f'SELECT * FROM "{url}" LIMIT 2').fetchall()
        print("DIAG query OK:", url, rows, flush=True)
    except Exception as exc:
        print("DIAG query FAILED:", url, repr(exc), flush=True)

try:
    from shillelagh.adapters.api.generic_json import GenericJSONAPI
    result_fast = GenericJSONAPI.supports(BASE, fast=True)
    print("DIAG supports fast=True:", result_fast, flush=True)
    result_slow = GenericJSONAPI.supports(BASE, fast=False)
    print("DIAG supports fast=False:", result_slow, flush=True)
except Exception as exc:
    import traceback
    print("DIAG supports() RAISED:", repr(exc), flush=True)
    traceback.print_exc()
