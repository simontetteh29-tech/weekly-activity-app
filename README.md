# 📊 Weekly Activity Reporting System

A Streamlit-based web application for capturing, managing, and storing weekly departmental activity reports directly into a Google Sheet using secure API authentication.

---

## 🚀 Overview

This application simplifies organizational reporting by allowing users to:

- Submit weekly activity reports
- Organize data by directorate, month, and week
- Track activity status (Completed / Ongoing)
- Store all data in a single Google Sheets worksheet
- Add custom activities and verification methods
- Download reports as CSV files

---

## 🏗️ System Architecture

```text
Streamlit UI
    ↓
Python Backend Logic
    ↓
Google Sheets API (gspread)
    ↓
Google Sheets (Single Worksheet Storage)
