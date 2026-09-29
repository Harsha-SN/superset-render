import os
import sys
import tempfile
import traceback

print("=" * 70)
print("SHILLELAGH CACHE DIAGNOSTIC")
print("=" * 70)

print("\n[1] ENVIRONMENT")

for key in [
    "HOME",
    "XDG_CACHE_HOME",
    "TMPDIR",
    "TEMP",
    "TMP",
    "SHILLELAGH_CACHE_DIR",
]:
    print(key, "=", os.getenv(key))


print("\n[2] USER")

try:
    print("UID:", os.getuid())
except Exception:
    print("UID: Windows/non-Unix")

try:
    print("GID:", os.getgid())
except Exception:
    print("GID: Windows/non-Unix")


print("\n[3] TEMP DIRECTORY")

print("tempfile.gettempdir():", tempfile.gettempdir())


print("\n[4] DIRECTORY TEST")

directories = [
    "/tmp",
    "/tmp/shillelagh-cache",
    "/tmp/shillelagh-home",
    "/app",
    "/app/superset_home",
    "/app/pythonpath",
]

for directory in directories:

    print("\nDirectory:", directory)

    try:
        print("Exists:", os.path.exists(directory))
        print("Writable:", os.access(directory, os.W_OK))
        print("Readable:", os.access(directory, os.R_OK))

        if os.path.exists(directory):
            print("Contents:", os.listdir(directory)[:20])

    except Exception as e:
        print("ERROR:", repr(e))


print("\n[5] SQLITE TEST")

try:

    import sqlite3

    paths = [
        "/tmp/test_cache.sqlite",
        "/tmp/shillelagh-cache/test_cache.sqlite",
        "/app/superset_home/test_cache.sqlite",
    ]

    for path in paths:

        print("\nTesting:", path)

        try:

            conn = sqlite3.connect(path)

            conn.execute(
                "CREATE TABLE IF NOT EXISTS test (id INTEGER)"
            )

            conn.execute(
                "INSERT INTO test VALUES (1)"
            )

            conn.commit()

            conn.close()

            print("SQLITE: OK")

        except Exception as e:

            print("SQLITE FAILED:", repr(e))


except Exception as e:

    print("SQLite import failed:", repr(e))


print("\n[6] REQUESTS CACHE")

try:

    import requests_cache

    print(
        "requests-cache:",
        requests_cache.__version__
    )

    test_paths = [
        "/tmp/test_requests_cache",
        "/tmp/shillelagh-cache/test_requests_cache",
        "/app/superset_home/test_requests_cache",
    ]

    for path in test_paths:

        print("\nCache path:", path)

        try:

            session = requests_cache.CachedSession(
                cache_name=path,
                backend="sqlite",
            )

            print("Session created: OK")

            print(
                "Cache backend:",
                type(session.cache).__name__
            )

            print(
                "Cache responses path:",
                getattr(
                    session.cache,
                    "responses",
                    None
                )
            )

        except Exception as e:

            print(
                "CACHE FAILED:",
                repr(e)
            )

            traceback.print_exc()


except Exception as e:

    print(
        "requests-cache failed:",
        repr(e)
    )


print("\n[7] SHILLELAGH SUPPORT")

try:

    from shillelagh.adapters.api.generic_json import GenericJSONAPI

    URL = (
        "https://analytics-api-82mg.onrender.com"
        "/api/product-performance/categories"
    )

    print("URL:", URL)

    try:

        result = GenericJSONAPI.supports(
            URL,
            fast=False
        )

        print(
            "supports(fast=False):",
            result
        )

    except Exception as e:

        print(
            "SUPPORTS FAILED:",
            repr(e)
        )

        traceback.print_exc()

except Exception as e:

    print(
        "GenericJSONAPI import failed:",
        repr(e)
    )


print("\n" + "=" * 70)
print("CACHE DIAGNOSTIC COMPLETE")
print("=" * 70)
