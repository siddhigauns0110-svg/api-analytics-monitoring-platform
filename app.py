"""Streamlit dashboard for the API Analytics & Monitoring Platform."""
import pandas as pd
import plotly.express as px
import streamlit as st

from analytics import calculate_summary, endpoint_summary, load_dataframe
from database import initialize_database

st.set_page_config(page_title="API Monitor", page_icon="📡", layout="wide")
initialize_database()

st.title("📡 API Analytics & Monitoring")
st.caption("A lightweight dashboard for endpoint health, response times and failures.")

with st.sidebar:
    st.header("Dashboard controls")
    st.button("Refresh data")
    row_limit = st.selectbox("History records", [100, 500, 1000, 5000], index=2)
    st.markdown("---")
    st.write("To collect new data, run `python monitor.py` in your terminal.")

df = load_dataframe(limit=row_limit)
if not df.empty:
    df["checked_at"] = pd.to_datetime(df["checked_at"], utc=True)
    df["status"] = df["is_success"].map({1: "UP", 0: "DOWN"})
    df = df.sort_values("checked_at")

summary = calculate_summary(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total checks", summary["total_checks"])
c2.metric("Success rate", f'{summary["success_rate"]}%')
c3.metric("Avg response time", f'{summary["average_response_ms"]} ms')
c4.metric("Failed checks", summary["failed_checks"])

if df.empty:
    st.info("No monitoring data yet. Run `python monitor.py` and refresh this page.")
    st.stop()

st.subheader("Endpoint performance")
st.dataframe(endpoint_summary(df), use_container_width=True, hide_index=True)

left, right = st.columns(2)
with left:
    st.subheader("Response time over time")
    fig = px.line(
        df, x="checked_at", y="response_time_ms",
        color="endpoint_name", markers=True,
        labels={"checked_at": "Time", "response_time_ms": "Response (ms)",
                "endpoint_name": "Endpoint"}
    )
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Checks by status")
    status_counts = df["status"].value_counts().rename_axis("status").reset_index(name="checks")
    fig = px.pie(status_counts, names="status", values="checks", hole=0.45)
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Recent monitoring history")
display_columns = [
    "checked_at", "endpoint_name", "method", "status_code",
    "response_time_ms", "status", "error_message"
]
st.dataframe(
    df.sort_values("checked_at", ascending=False)[display_columns],
    use_container_width=True, hide_index=True
)

csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button("Download monitoring history (CSV)", csv_data,
                   "api_monitoring_history.csv", "text/csv")
