import os
import time
import zipfile
from flask import Flask, render_template, request, send_file, redirect, url_for, flash

from src.logger_setup import setup_logger
from src.log_parser import parse_log_line
from src.analyzer import analyze_logs
from src.report_generator import save_summary_report
from src.visualizer import (
    generate_error_chart,
    generate_request_method_chart,
)

app = Flask(__name__)
app.secret_key = "log-analyzer-secret-key"

logger = setup_logger("logs/app.log")

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "outputs/reports"
STATIC_IMAGES_FOLDER = os.path.join("static", "images")

SUMMARY_REPORT_PATH = os.path.join(REPORT_FOLDER, "summary_report.txt")
ERROR_CSV_PATH = os.path.join(REPORT_FOLDER, "error_frequency.csv")
TOP_IP_CSV_PATH = os.path.join(REPORT_FOLDER, "top_error_ips.csv")
METHODS_CSV_PATH = os.path.join(REPORT_FOLDER, "request_methods.csv")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)
os.makedirs(STATIC_IMAGES_FOLDER, exist_ok=True)

LAST_ENTRIES = []
LAST_INVALID_LINES = 0


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    global LAST_ENTRIES, LAST_INVALID_LINES

    if "logfile" not in request.files:
        flash("No file uploaded!")
        return redirect(url_for("index"))

    file = request.files["logfile"]
    if file.filename == "":
        flash("No file selected!")
        return redirect(url_for("index"))

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    logger.info(f"Uploaded file saved at: {filepath}")

    entries = []
    invalid_lines = 0

    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                entry = parse_log_line(line)
                if entry:
                    entries.append(entry)
                else:
                    invalid_lines += 1
    except Exception as e:
        logger.exception("Error reading log file!")
        flash(f"Error reading log file: {str(e)}")
        return redirect(url_for("index"))

    LAST_ENTRIES = entries
    LAST_INVALID_LINES = invalid_lines

    summary = analyze_logs(entries)
    summary["invalid_lines"] = invalid_lines

    # Save summary report
    save_summary_report(SUMMARY_REPORT_PATH, summary)

    # Save CSV reports
    summary["error_df"].to_csv(ERROR_CSV_PATH, index=False)
    summary["top_ip_df"].to_csv(TOP_IP_CSV_PATH, index=False)
    summary["methods_df"].to_csv(METHODS_CSV_PATH, index=False)

    # ✅ Unique chart filenames
    ts = str(int(time.time()))

    error_chart_file = f"error_distribution_{ts}.png"
    method_chart_file = f"request_methods_{ts}.png"

    error_chart_path = os.path.join(STATIC_IMAGES_FOLDER, error_chart_file)
    method_chart_path = os.path.join(STATIC_IMAGES_FOLDER, method_chart_file)

    generate_error_chart(summary["error_code_counts"], error_chart_path)
    generate_request_method_chart(summary["request_method_counts"], method_chart_path)

    logger.info(f"Generated charts: {error_chart_file}, {method_chart_file}")

    return render_template(
        "results.html",
        total_requests=summary["total_requests"],
        total_errors=summary["total_errors"],
        total_success=summary["total_success"],
        invalid_lines=summary["invalid_lines"],
        error_rate=summary["error_rate"],
        error_counts=summary["error_code_counts"],
        top_ips=summary["top_5_ips"],
        ip_filter="",
        code_filter="",
        error_chart_file=error_chart_file,
        method_chart_file=method_chart_file,
    )


@app.route("/filter", methods=["GET"])
def filter_results():
    global LAST_ENTRIES, LAST_INVALID_LINES

    if not LAST_ENTRIES:
        flash("No analysis data found. Please upload a log file first.")
        return redirect(url_for("index"))

    ip_query = request.args.get("ip", "").strip()
    code_query = request.args.get("code", "").strip()

    filtered = LAST_ENTRIES

    if ip_query:
        filtered = [e for e in filtered if e.ip == ip_query]

    if code_query:
        try:
            code_query_int = int(code_query)
            filtered = [e for e in filtered if e.status_code == code_query_int]
        except ValueError:
            flash("Invalid error code filter! Please enter a number like 404.")
            return redirect(url_for("filter_results"))

    summary = analyze_logs(filtered)
    summary["invalid_lines"] = LAST_INVALID_LINES

    # ✅ Unique chart filenames
    ts = str(int(time.time()))

    error_chart_file = f"error_distribution_{ts}.png"
    method_chart_file = f"request_methods_{ts}.png"

    error_chart_path = os.path.join(STATIC_IMAGES_FOLDER, error_chart_file)
    method_chart_path = os.path.join(STATIC_IMAGES_FOLDER, method_chart_file)

    generate_error_chart(summary["error_code_counts"], error_chart_path)
    generate_request_method_chart(summary["request_method_counts"], method_chart_path)

    return render_template(
        "results.html",
        total_requests=summary["total_requests"],
        total_errors=summary["total_errors"],
        total_success=summary["total_success"],
        invalid_lines=summary["invalid_lines"],
        error_rate=summary["error_rate"],
        error_counts=summary["error_code_counts"],
        top_ips=summary["top_5_ips"],
        ip_filter=ip_query,
        code_filter=code_query,
        error_chart_file=error_chart_file,
        method_chart_file=method_chart_file,
    )


# ---------------- DOWNLOAD ROUTES ----------------

@app.route("/download/summary")
def download_summary():
    return send_file(SUMMARY_REPORT_PATH, as_attachment=True)


@app.route("/download/errors_csv")
def download_errors_csv():
    return send_file(ERROR_CSV_PATH, as_attachment=True)


@app.route("/download/top_ips_csv")
def download_top_ips_csv():
    return send_file(TOP_IP_CSV_PATH, as_attachment=True)


@app.route("/download/methods_csv")
def download_methods_csv():
    return send_file(METHODS_CSV_PATH, as_attachment=True)


@app.route("/download/chart/<filename>")
def download_chart_file(filename):
    filepath = os.path.join(STATIC_IMAGES_FOLDER, filename)

    if not os.path.exists(filepath):
        flash("Chart file not found!")
        return redirect(url_for("index"))

    return send_file(filepath, as_attachment=True)


# ✅ FULL REPORT ZIP DOWNLOAD
@app.route("/download/full_report")
def download_full_report():
    zip_path = os.path.join(REPORT_FOLDER, "full_report.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:

        # Add reports
        if os.path.exists(SUMMARY_REPORT_PATH):
            zipf.write(SUMMARY_REPORT_PATH, arcname="summary_report.txt")

        if os.path.exists(ERROR_CSV_PATH):
            zipf.write(ERROR_CSV_PATH, arcname="error_frequency.csv")

        if os.path.exists(TOP_IP_CSV_PATH):
            zipf.write(TOP_IP_CSV_PATH, arcname="top_error_ips.csv")

        if os.path.exists(METHODS_CSV_PATH):
            zipf.write(METHODS_CSV_PATH, arcname="request_methods.csv")

        # Add all charts
        if os.path.exists(STATIC_IMAGES_FOLDER):
            for file in os.listdir(STATIC_IMAGES_FOLDER):
                if file.endswith(".png"):
                    full_path = os.path.join(STATIC_IMAGES_FOLDER, file)
                    zipf.write(full_path, arcname=f"charts/{file}")

    return send_file(zip_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
