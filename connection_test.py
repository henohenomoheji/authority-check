import ssl
import urllib.error
import urllib.request

url = "https://openai-0316.openai.azure.com"
print("python_ssl:", ssl.OPENSSL_VERSION)

try:
    with urllib.request.urlopen(url, timeout=10) as r:
        print("status:", r.status)
        print("content-type:", r.headers.get("content-type"))
except urllib.error.URLError as e:
    print("reason_type:", type(e.reason).__name__)
    print("reason:", repr(e.reason))
except Exception as e:
    print("exception_type:", type(e).__name__)
    print("exception:", repr(e))
