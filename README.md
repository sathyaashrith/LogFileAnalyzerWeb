# 📊 Log File Analyzer Dashboard (Flask + Python)

A professional **Python + Flask web application** that analyzes large server log files and generates actionable insights for IT Operations teams.  
It identifies HTTP error patterns, top error-generating IPs, request method distribution, generates charts, and provides downloadable reports.

---

## 🚀 Features

✅ Upload and analyze large `.log` files (50,000+ lines supported)  
✅ Efficient line-by-line processing (memory optimized)  
✅ Identify and count HTTP error codes (4xx/5xx)  
✅ Top 5 IPs generating maximum errors  
✅ Summary dashboard with total requests, errors, success, error rate  
✅ Charts generated using Matplotlib  
✅ Handles invalid/corrupted log entries safely  
✅ Execution logging for debugging and auditing  
✅ Download options:
- Summary Report (TXT)
- Error Frequency (CSV)
- Top IPs (CSV)
- Request Methods (CSV)
- Full Report (ZIP including charts + reports)

🌙 Dark Mode supported (with localStorage theme persistence)

---

## 🧰 Tech Stack

- **Backend:** Python, Flask  
- **Data Processing:** Pandas  
- **Parsing:** Regular Expressions (Regex)  
- **Visualization:** Matplotlib  
- **UI:** HTML, Bootstrap 5, Custom CSS  
- **Logging:** Python `logging` module  

---

## 📂 Project Folder Structure

```bash
LogFileAnalyzerWeb/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── src/
│   ├── analyzer.py
│   ├── log_parser.py
│   ├── logger_setup.py
│   ├── report_generator.py
│   └── visualizer.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   └── results.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── images/
│
├── uploads/
├── outputs/
│   └── reports/
└── logs/
    └── app.log
