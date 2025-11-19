
#  Log Parsing Automation Script — README

This README explains the **approach, architecture, and usage** of the automated log parsing script. It focuses on scalability, robustness, and support for different log formats.

---

##  Overview
This project provides a **scalable, efficient, and extensible Python-based log parser** built to handle:

- Unstructured logs (custom text logs)
- Semi-structured logs (Apache/Nginx, syslogs, etc.)
- Structured logs (JSON, CSV, TSV)
- Very large log files (GBs of data)

It extracts key information such as **timestamps, IP addresses, events, user IDs, error messages**, or any custom-defined components.

---

##  Features
-  Memory-efficient line-by-line processing  
-  Regex-based extraction for unstructured logs  
-  Native JSON/CSV parsing support  
-  Fault-tolerant handling of malformed log lines  
-  Exports clean structured data (DataFrame → CSV/JSON/Excel)  

---

##  Architecture & Approach

### 1. Log Format Detection  
Determine if the log is unstructured, semi-structured, or structured.

### 2. Extraction Rules  
Apply regex, JSON key extraction, or CSV column parsing.

### 3. Efficient File Processing  
Uses a streamed approach (never loads full file into memory).

### 4. Data Structuring  
Parsed results are stored as dictionaries → DataFrame.

### 5. Output Export  
Supports CSV, JSON, or database insertion.

---

##  Key Libraries Used
| Library | Purpose |
|--------|---------|
| re | Regex parsing |
| json | JSON log parsing |
| csv | CSV/TSV parsing |
| pandas | Data analysis & export |

---

##  Example: Extracting IP Addresses
```python
import re
import pandas as pd

ip_pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
parsed_data = []

with open("system.log", "r") as f:
    for line in f:
        match = ip_pattern.search(line)
        if match:
            parsed_data.append({
                "ip": match.group(1),
                "raw_log": line.strip()
            })

df = pd.DataFrame(parsed_data)
print(df)
```

---

##  Output Example
| ip | raw_log |
|----|----------|
| 192.168.1.10 | [2025-11-14] INFO: Connection established... |
| 10.0.2.15 | ERROR: Failed login attempt... |

---

##  How to Run
```
pip install pandas
python3 parser.py
```

---

##  Customization
Easily extendable to extract timestamps, log levels, URLs, users, or status codes.

---




