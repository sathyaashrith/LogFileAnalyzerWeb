import os


def save_summary_report(report_path: str, summary: dict) -> None:
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("==== LOG FILE ANALYSIS REPORT ====\n\n")

        f.write(f"Total Requests: {summary['total_requests']}\n")
        f.write(f"Total Errors:   {summary['total_errors']}\n")
        f.write(f"Total Success:  {summary.get('total_success', 0)}\n")
        f.write(f"Invalid Lines:  {summary.get('invalid_lines', 0)}\n")
        f.write(f"Error Rate:     {summary.get('error_rate', 0)}%\n\n")

        f.write("---- Error Code Frequency ----\n")
        if summary["error_code_counts"]:
            for code, count in sorted(summary["error_code_counts"].items()):
                f.write(f"{code}: {count}\n")
        else:
            f.write("No errors found.\n")

        f.write("\n---- Top 5 IPs Generating Errors ----\n")
        if summary["top_5_ips"]:
            for ip, count in summary["top_5_ips"]:
                f.write(f"{ip}: {count}\n")
        else:
            f.write("No error IPs found.\n")
