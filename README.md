# AGC FinOps Automation Suite — Interview Demo

A Streamlit app demonstrating Finance Process Transformation skills for the AGC Manager role.

## Features
| Page | What it demonstrates |
|------|----------------------|
| 📊 Executive Dashboard | Automated data aggregation, KPI tracking, interactive charts |
| 🔍 Transaction Validator | Rule-based validation engine, duplicate detection, policy checks |
| 📈 Spend Analytics | Drill-down analysis, department/vendor breakdowns, CSV export |
| 🤖 Report Generator | Automated report compilation with progress pipeline |
| 🚨 Anomaly Monitor | Real-time anomaly flagging, exception handling |

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

## Key talking points for the interview
- **Python automation**: All data processing, validation rules, and report generation use pure Python/Pandas
- **Financial workflow design**: Validation rules mirror real-world finance controls (amount limits, duplicate checks, payment method policies)
- **Anomaly detection**: Statistical flagging of high-value, duplicate, and oddly-timed transactions
- **Automated reporting**: One-click report generation replaces manual compilation
- **System integration mindset**: Architecture can connect to ERP/finance systems via APIs
