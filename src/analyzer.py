from collections import Counter
from typing import Dict, List

import pandas as pd
from src.log_parser import LogEntry


def analyze_logs(entries: List[LogEntry]) -> Dict:
    total_requests = len(entries)

    # Errors = 4xx and 5xx
    error_entries = [e for e in entries if 400 <= e.status_code <= 599]
    total_errors = len(error_entries)

    # Success = 2xx
    success_entries = [e for e in entries if 200 <= e.status_code <= 299]
    total_success = len(success_entries)

    error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0

    # Count error codes
    error_code_counts = Counter([e.status_code for e in error_entries])

    # Count IP errors
    ip_error_counts = Counter([e.ip for e in error_entries])
    top_5_ips = ip_error_counts.most_common(5)

    # Count request methods (GET/POST/PUT/DELETE)
    request_method_counts = Counter([e.request_type for e in entries])

    # Convert to DataFrames for CSV export
    error_df = pd.DataFrame(
        [{"error_code": k, "count": v} for k, v in sorted(error_code_counts.items())]
    )

    top_ip_df = pd.DataFrame(
        [{"ip_address": ip, "error_count": count} for ip, count in top_5_ips]
    )

    methods_df = pd.DataFrame(
        [{"method": m, "count": c} for m, c in sorted(request_method_counts.items())]
    )

    return {
        "total_requests": total_requests,
        "total_errors": total_errors,
        "total_success": total_success,
        "error_rate": round(error_rate, 2),
        "error_code_counts": dict(error_code_counts),
        "top_5_ips": top_5_ips,
        "request_method_counts": dict(request_method_counts),
        "error_df": error_df,
        "top_ip_df": top_ip_df,
        "methods_df": methods_df,
    }
