import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import tempfile
from fpdf import FPDF
from datetime import datetime

# --- Initialize session state variables ---
if "dependencies" not in st.session_state:
    st.session_state.dependencies = []
if "jobs" not in st.session_state:
    st.session_state.jobs = pd.DataFrame(columns=[
        "work_order", "machine", "operator", "start_date", "due_date",
        "customer", "part", "pcs", "remarks", "status"
    ])
if "progress_log" not in st.session_state:
    st.session_state.progress_log = {}
if "user_preferences" not in st.session_state:
    st.session_state.user_preferences = {"theme": "light", "notifications": True}
if "vacations" not in st.session_state:
    st.session_state.vacations = pd.DataFrame(columns=["operator", "start", "end", "reason"])

# --- Theme Selection ---
if st.session_state.user_preferences["theme"] == "dark":
    st.markdown('<style>body {background-color: #121212; color: white;}</style>', unsafe_allow_html=True)
else:
    st.markdown('<style>body {background-color: white; color: black;}</style>', unsafe_allow_html=True)

# --- User Authentication (Placeholder) ---
if "username" not in st.session_state:
    st.session_state.username = ""

if st.session_state.username == "":
    st.sidebar.text_input("Username", key="username")
    st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if st.session_state.username == "admin":
            st.session_state.role = "manager"
            st.success("Welcome Manager!")
        else:
            st.session_state.role = "operator"
            st.success(f"Welcome Operator: {st.session_state.username}")
else:
    st.sidebar.write(f"Logged in as {st.session_state.username}")

# --- Job Dependencies Section ---
if st.session_state.dependencies:
    st.markdown("### Current Dependencies")
    for dep in st.session_state.dependencies:
        st.markdown(f"- ✅ {dep[0]} → {dep[1]}")

    st.markdown("### 📊 Visual Map of Dependencies")
    G = nx.DiGraph()
    for a, b in st.session_state.dependencies:
        G.add_edge(a, b)

    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color="#1f77b4", node_size=1500, font_size=10, font_color="white", font_weight="bold", edge_color="#555")
    st.pyplot(fig)

    st.markdown("### ❗ Dependency Conflict Check")
    conflicts = []
    for a, b in st.session_state.dependencies:
        job_a = st.session_state.jobs[st.session_state.jobs["work_order"] == a]
        job_b = st.session_state.jobs[st.session_state.jobs["work_order"] == b]
        if not job_a.empty and not job_b.empty:
            a_due = pd.to_datetime(job_a.iloc[0]["due_date"])
            b_start = pd.to_datetime(job_b.iloc[0]["start_date"])
            if b_start < a_due:
                conflicts.append(f"⚠ {b} starts before its dependency {a} completes.")
    if conflicts:
        for c in conflicts:
            st.error(c)
    else:
        st.success("✅ No dependency conflicts found.")
else:
    st.info("At least two jobs required to define dependencies.")

st.markdown("---")
st.subheader("🧾 Export Job Traveler PDF")

# Enhanced job table with selection
st.markdown("### 📋 Select a Job from Table")
status_colors = {
    "Scheduled": "🟡",
    "In Progress": "🟠",
    "Completed": "✅",
    "Delayed": "🔴"
}
# Filter options
st.markdown("### 🔍 Filter Jobs")
status_filter = st.multiselect("Filter by Status:", options=st.session_state.jobs["status"].unique(), default=st.session_state.jobs["status"].unique())
operator_filter = st.multiselect("Filter by Operator:", options=st.session_state.jobs["operator"].unique(), default=st.session_state.jobs["operator"].unique())
machine_filter = st.multiselect("Filter by Machine:", options=st.session_state.jobs["machine"].unique(), default=st.session_state.jobs["machine"].unique())

filtered_jobs = st.session_state.jobs[
    (st.session_state.jobs["status"].isin(status_filter)) &
    (st.session_state.jobs["operator"].isin(operator_filter)) &
    (st.session_state.jobs["machine"].isin(machine_filter))
]

jobs_display = filtered_jobs.copy()
jobs_display["Status Icon"] = jobs_display["status"].map(lambda x: status_colors.get(x, "❔"))
jobs_display["Label"] = jobs_display["Status Icon"] + " " + jobs_display["work_order"] + " - " + jobs_display["part"]

selected_label = st.selectbox("Choose Job:", jobs_display["Label"].tolist())

if selected_label:
    selected_job = jobs_display[jobs_display["Label"] == selected_label]["work_order"].values[0]
    filtered_job = st.session_state.jobs[st.session_state.jobs["work_order"] == selected_job]
    if not filtered_job.empty:
        job_details = filtered_job.iloc[0]
        st.markdown("#### Job Summary")
        st.json(job_details.to_dict())

    if not filtered_job.empty and st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Job Traveler: {selected_job}", ln=True)
        for key, val in job_details.items():
            pdf.cell(200, 10, txt=f"{key}: {val}", ln=True)
        if "progress_log" in st.session_state and selected_job in st.session_state.progress_log:
            pdf.cell(200, 10, txt="Progress Log:", ln=True)
            for entry in st.session_state.progress_log[selected_job]:
                pdf.cell(200, 10, txt=f"- {entry}", ln=True)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdf.output(tmp_file.name)
        with open(tmp_file.name, "rb") as file:
            st.download_button("📥 Download PDF", file, file_name=f"{selected_job}_JobTraveler.pdf", mime="application/pdf")

# --- User Preferences Panel ---
st.sidebar.header("User Preferences")
theme = st.sidebar.radio("Choose Theme", options=["light", "dark"])
st.session_state.user_preferences["theme"] = theme
st.session_state.user_preferences["notifications"] = st.sidebar.checkbox("Enable Notifications", value=True)

st.markdown("---")

# --- Email Log Panel ---
st.sidebar.header("📧 Email Log")
if "email_log" not in st.session_state:
    st.session_state.email_log = []
# Show the last 10 email deliveries
st.session_state.email_log.append(f"Snapshot sent to manager: {datetime.now()}")
for email in st.session_state.email_log[-10:]:
    st.sidebar.text(email)

# --- Notification Feature ---
if st.session_state.user_preferences["notifications"]:
    st.success("📢 Notification Enabled")
