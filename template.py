import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
import json
import os

# -------------------------------------------------
# GOOGLE SHEETS CONFIG
# -------------------------------------------------
SHEET_ID = "1mWDcu8eJNtKPA6VVivE6OpjZgf2Aa8M3Rs0gyLwbkck"   # from sheet URL
WORKSHEET_NAME = "Weekly_Report_GoogleSheets"           # single worksheet name

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=SCOPES
)

gc = gspread.authorize(creds)

sh = gc.open_by_key(SHEET_ID)
worksheet = sh.worksheet(WORKSHEET_NAME)

# -------------------------------------------------
# FILES
# -------------------------------------------------
ACTIVITY_FILE = "activities.json"
VERIFICATION_FILE = "verification_methods.json"

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
if os.path.exists(ACTIVITY_FILE):
    with open(ACTIVITY_FILE, "r") as f:
        directorate_activity = json.load(f)
else:
    directorate_activity = {
        "Administration": ["Directorate meetings", "Administrative memos", "Staff coordination"],
        "Audit": ["Pre-audit of payment vouchers", "Procurement audits", "Expenditure verification", "Weekly meetings", "Budget preparation", "Follow-up on audit recommendations"],
        "Corporate Affairs": ["Walk-ins", "Incoming calls", "Client enquiries", "Complaints follow-up", "Emails to units", "Incoming letters", "Letters dispatched", "Media monitoring"],
        "Estate": ["Asset inventory updates", "Utility usage monitoring", "Janitorial supervision", "Repairs & maintenance"],
        "Finance": ["Issuance of receipts", "Preparation of invoices", "PV preparation (Commissioner & 3rd party)", "GIFMIS payments", "Cashbook reconciliation", "Weekly reports", "Deposit of revenue"],
        "HR": ["Leave requests", "Attendance monitoring", "Administrative memos", "Training coordination", "Staff reports"],
        "IICE": ["Inspection", "Investigation", "Complaints", "monitoring", "Surveillance", "Staff Meeting", "Files Reviewed", "Enforcement"],
        "IT": ["Email setup", "Website updates", "Network resolution", "Desktop support", "Virtual meetings"],
        "Legal": ["Filing of legal processes", "Drafting legal documents", "Court attendance"],
        "L&R": ["Verification of bills", "Review of license applications", "Printing of licenses"],
        "Procurement": ["Procurement requests", "Supplier quotations", "Purchase orders", "Delivery of items", "Contract agreements", "Meetings"],
        "RPME": ["Weekly report compilation", "Monthly performance reports", "Strategic plan reviews", "Surveys"],
        "Stores": ["Weekly inventory checks", "Stock register updates", "Issuing stock", "Receiving deliveries", "Stock taking"],
        "Transport": ["Vehicle fueling", "Scheduled servicing", "Transport services", "Works orders"]
        
    }

if os.path.exists(VERIFICATION_FILE):
    with open(VERIFICATION_FILE, "r") as f:
        activity_verification = json.load(f)
else:
    activity_verification = {}

# -------------------------------------------------
# SAVE FUNCTIONS
# -------------------------------------------------
def save_activity(directorate, activity):
    if activity and activity not in directorate_activity.get(directorate, []):
        directorate_activity.setdefault(directorate, []).append(activity)
        with open(ACTIVITY_FILE, "w") as f:
            json.dump(directorate_activity, f)

def save_verification(activity, method):
    if activity and method:
        activity_verification.setdefault(activity, [])
        if method not in activity_verification[activity]:
            activity_verification[activity].append(method)
            with open(VERIFICATION_FILE, "w") as f:
                json.dump(activity_verification, f)

# -------------------------------------------------
# PAGE
# -------------------------------------------------
st.set_page_config(page_title="Weekly Activity System", layout="wide")

st.image("Gaming Commission_logo.jpg", use_container_width=True)

st.markdown(
    "<h1 style='text-align:center;'>Weekly Activity Reporting System</h1>",
    unsafe_allow_html=True
)

# -------------------------------------------------
# STATIC DATA
# -------------------------------------------------
month_weeks = {
    "January": [1, 2, 3, 4, 5],
    "February": [1, 2, 3, 4],
    "March": [1, 2, 3, 4, 5],
    "April": [1, 2, 3, 4],
    "May": [1, 2, 3, 4],
    "June": [1, 2, 3, 4, 5],
    "July": [1, 2, 3, 4],
    "August": [1, 2, 3, 4, 5],
    "September": [1, 2, 3, 4],
    "October": [1, 2, 3, 4],
    "November": [1, 2, 3, 4, 5],
    "December": [1, 2, 3, 4],
}

status_options = ["Completed","Ongoing"]

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "rows" not in st.session_state:
    st.session_state.rows = [{}]

if "delete_index" not in st.session_state:
    st.session_state.delete_index = None

if "submitted" not in st.session_state:
    st.session_state.submitted = False

# -------------------------------------------------
# HEADER
# -------------------------------------------------
colA, colB, colC, colD = st.columns(4)

with colA:
    directorate = st.selectbox("Directorate", list(directorate_activity.keys()))

with colB:
    month = st.selectbox("Month", list(month_weeks.keys()))

with colC:
    week = st.selectbox("Week", month_weeks[month])

with colD:
    year = st.number_input("Year", min_value=2000, max_value=2100)

st.divider()

st.markdown("## Activity Reporting Form")

updated_rows = []

# -------------------------------------------------
# ROWS
# -------------------------------------------------
for i in range(len(st.session_state.rows)):

    # HEADER + DELETE
    col_title, col_delete = st.columns([5, 1])

    with col_title:
        st.markdown(f"### Activity Entry {i+1}")

    with col_delete:
        if st.button("🗑️", key=f"delete_btn_{i}"):
            st.session_state.delete_index = i

    # CONFIRMATION
    if st.session_state.delete_index == i:
        st.warning(f"Delete Activity Entry {i+1}?")

        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button("✅ Yes", key=f"yes_{i}"):
                st.session_state.rows.pop(i)
                st.session_state.delete_index = None
                st.rerun()

        with col_no:
            if st.button("❌ Cancel", key=f"no_{i}"):
                st.session_state.delete_index = None
                st.rerun()

    # -------------------------------------------------
    # ACTIVITY INPUT (UPDATED)
    # -------------------------------------------------
    tab1, tab2 = st.tabs(["📋 Existing Activity", "✍️ New Activity"])

    activity = ""

    with tab1:
        if os.path.exists("existing_icon.png"):
            st.image("existing_icon.png", width=40)

        activity = st.selectbox(
            "Select Existing Activity/Program",
            directorate_activity[directorate],
            key=f"existing_{i}"
        )

    with tab2:
        if os.path.exists("new_icon.png"):
            st.image("new_icon.png", width=40)

        new_activity = st.text_input(
            "Enter New Activity/Program",
            key=f"new_{i}"
        ).strip()

        if new_activity:
            activity = new_activity

    # -------------------------------------------------
    # DETAILS
    # -------------------------------------------------
    col1, col2 = st.columns(2)

    with col1:
        number = st.number_input("Number", min_value=1, key=f"num_{i}")

    with col2:
        status = st.selectbox("Status", status_options, key=f"status_{i}")

    # -------------------------------------------------
    # VERIFICATION
    # -------------------------------------------------
    means_options = activity_verification.get(activity, [])

    means = st.multiselect(
        "Means of Verification",
        means_options,
        key=f"mvo_{i}"
    )

    custom_mvo = st.text_input(
        "Add Custom Means of Verification",
        key=f"cmvo_{i}"
    ).strip()

    if custom_mvo:
        means.append(custom_mvo)

    remarks = st.text_area("Remarks", key=f"remarks_{i}")

    updated_rows.append({
        "Activity/Program": activity,
        "Number": number,
        "Status": status,
        "Means of Verification": ", ".join(means),
        "Remarks": remarks
    })

    st.divider()

# -------------------------------------------------
# ACTION BUTTONS
# -------------------------------------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Add Activity Row"):
        st.session_state.rows.append({})
        st.rerun()

with col2:
    submit = st.button("✅ Submit Report")

# -------------------------------------------------
# SUBMIT
# -------------------------------------------------
if submit:

    final_data = []
    error = False

    for i, row in enumerate(updated_rows):

        if not row["Activity/Program"]:
            st.error(f"Row {i+1}: Activity required")
            error = True
            break

        save_activity(directorate, row["Activity/Program"])

        for m in row["Means of Verification"].split(", "):
            if m.strip():
                save_verification(row["Activity/Program"], m.strip())

        record = {
            "Directorate": directorate,
            "Month": month,
            "Week": week,
            "Year": year,
            **row
        }

        final_data.append(record)

        # -------------------------------------------------
        # WRITE TO GOOGLE SHEET (APPEND ROW)
        # -------------------------------------------------
        worksheet.append_row([
            record["Directorate"],
            record["Month"],
            record["Week"],
            record["Year"],
            record["Activity/Program"],
            record["Number"],
            record["Status"],
            record["Means of Verification"],
            record["Remarks"]
        ])

    if not error:
        df = pd.DataFrame(final_data)
        st.session_state.submitted_df = df
        st.session_state.submitted = True

# -------------------------------------------------
# OUTPUT
# -------------------------------------------------
if st.session_state.submitted:

    st.success("Report Submitted Successfully")

    df = st.session_state.submitted_df
    st.dataframe(df, use_container_width=True)

    st.download_button(
        "⬇️ Download CSV",
        df.to_csv(index=False),
        "weekly_activity.csv"
    )
