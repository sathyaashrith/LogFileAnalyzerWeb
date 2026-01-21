import random
from datetime import datetime, timedelta

methods = ["GET", "POST", "PUT", "DELETE"]
status_codes = [200, 201, 301, 302, 400, 401, 403, 404, 500, 503]

def generate_ip():
    return f"192.168.{random.randint(1, 50)}.{random.randint(1, 255)}"

def generate_logs(filename="uploads/generated_50000.log", lines=50000):
    start_time = datetime.now()

    with open(filename, "w", encoding="utf-8") as f:
        for i in range(lines):
            time = start_time + timedelta(seconds=i)
            ip = generate_ip()
            method = random.choice(methods)
            code = random.choice(status_codes)

            # add some corrupted lines randomly
            if random.random() < 0.02:
                f.write("CORRUPTED LINE DATA $$$$$\n")
            else:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {ip} | {method} | {code}\n")

    print(f"✅ Generated {lines} lines in {filename}")

if __name__ == "__main__":
    generate_logs()
