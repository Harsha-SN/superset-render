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
