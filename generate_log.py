import random
from datetime import datetime, timedelta

# Output file name
OUTPUT_FILE = "sample_server_log_50k.log"

# Total lines (>= 50,000)
TOTAL_LINES = 50000

# Sample request methods
METHODS = ["GET", "POST", "PUT", "DELETE"]

# Status codes (mix of success + errors)
STATUS_CODES = [200, 201, 204, 301, 302, 400, 401, 403, 404, 500, 502, 503]

# URLs
URLS = [
    "/",
    "/login",
    "/logout",
    "/dashboard",
    "/api/data",
    "/api/user",
    "/products",
    "/products/123",
    "/orders",
    "/admin",
    "/admin/settings",
    "/search?q=test"
]

def random_ip():
    return f"192.168.{random.randint(1, 10)}.{random.randint(1, 255)}"

start_time = datetime.now() - timedelta(days=1)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for i in range(TOTAL_LINES):
        timestamp = (start_time + timedelta(seconds=i)).strftime("%Y-%m-%d %H:%M:%S")
        ip = random_ip()
        method = random.choice(METHODS)
        url = random.choice(URLS)

        # errors are more frequent for good analysis
        status = random.choices(
            STATUS_CODES,
            weights=[50, 10, 10, 5, 5, 10, 5, 10, 15, 10, 5, 5],
            k=1
        )[0]

        log_line = f"{timestamp} {ip} {method} {url} {status}\n"
        f.write(log_line)

    # corrupted/invalid lines for testing
    f.write("INVALID_LINE_WITH_NO_FORMAT\n")
    f.write("2025-01-01 BAD_IP GET /test 404\n")
    f.write("2025-01-01 12:00:00 192.168.1.1 WRONGFORMAT\n")

print(f"✅ Log file generated: {OUTPUT_FILE} ({TOTAL_LINES} lines + corrupted lines)")
