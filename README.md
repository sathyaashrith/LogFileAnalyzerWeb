# 📊 Log File Analyzer Dashboard (Flask + Python)

A professional **Python + Flask web application** that analyzes large server log files and generates actionable insights for IT Operations teams.  
It identifies HTTP error patterns, top error-generating IPs, request method distribution, generates charts, and provides downloadable reports.

---

## 🚀 Features

✅ Upload and analyze large `.log` files (50,000+ lines supported)  
✅ Efficient line-by-line processing (memory optimized)  
✅ Identify and count HTTP error codes (4xx/5xx)  
✅ Find Top 5 IPs generating maximum errors  
✅ Summary dashboard:
- Total Requests
- Total Errors
- Success Requests
- Error Rate
- Invalid lines count  
✅ Charts generated using Matplotlib:
- HTTP Error Distribution Chart
- Request Method Distribution Chart  
✅ Handles invalid/corrupted log entries safely (program never crashes)  
✅ Execution logging for debugging and auditing  
✅ Download options:
- Summary Report (TXT)
- Error Frequency (CSV)
- Top IPs (CSV)
- Request Methods (CSV)
- Full Report (ZIP including charts + reports)  
🌙 Dark Mode supported

---

## 🧰 Tech Stack

- **Backend:** Python, Flask  
- **Data Processing:** Pandas  
- **Parsing:** Regular Expressions (Regex)  
- **Visualization:** Matplotlib  
- **UI:** HTML, Bootstrap 5, Custom CSS  
- **Logging:** Python `logging` module  

---

## 📌 Sample Log Format Supported

Each log line should follow this format:

YYYY-MM-DD HH:MM:SS IP_ADDRESS REQUEST_METHOD STATUS_CODE

---

## 📊 Dashboard Output Includes

- Total Requests  
- Total Errors  
- Success Requests  
- Error Rate  
- Error Code Frequency Table  
- Top 5 IPs Generating Errors  
- Error Distribution Chart  
- Request Method Distribution Chart  
- Download Reports Section  

---

## 📥 Download Options

The dashboard provides:

- 📄 Summary Report (TXT)  
- 📑 Error Frequency CSV  
- 🌐 Top IP CSV  
- ⚡ Request Methods CSV  
- 📦 Full Report ZIP (includes reports + charts)  


