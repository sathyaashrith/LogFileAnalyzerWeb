import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class LogEntry:
    timestamp: str
    ip: str
    request_type: str
    status_code: int


# Example log format expected:
# 2026-01-21 10:30:12 | 192.168.1.10 | GET | 404
LOG_PATTERN = re.compile(
    r"^(?P<timestamp>[\d\-:\s]+)\s*\|\s*(?P<ip>\d{1,3}(?:\.\d{1,3}){3})\s*\|\s*(?P<req>[A-Z]+)\s*\|\s*(?P<code>\d{3})$"
)


def parse_log_line(line: str) -> Optional[LogEntry]:
    line = line.strip()

    if not line:
        return None

    match = LOG_PATTERN.match(line)
    if not match:
        return None

    try:
        return LogEntry(
            timestamp=match.group("timestamp").strip(),
            ip=match.group("ip").strip(),
            request_type=match.group("req").strip(),
            status_code=int(match.group("code")),
        )
    except Exception:
        return None
