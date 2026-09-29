import requests

URL = "https://analytics-api-82mg.onrender.com/api/product-performance/categories"

print("=" * 60)
print("ANALYTICS API TEST")
print("=" * 60)

try:
    r = requests.get(URL, timeout=60)

    print("STATUS:", r.status_code)
    print("CONTENT-TYPE:", r.headers.get("Content-Type"))
    print("CONTENT-LENGTH:", len(r.content))
    print("TEXT START:")
    print(r.text[:1000])

except Exception as e:
    print("REQUEST FAILED:", repr(e))

print("=" * 60)
