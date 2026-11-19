"""SQL-backed analytics helpers."""
import pandas as pd
from database import fetch_results

def load_dataframe(limit=5000):
    return pd.DataFrame(fetch_results(limit=limit))

def calculate_summary(df):
    if df.empty:
        return {
            "total_checks": 0, "success_rate": 0.0,
            "average_response_ms": 0.0, "failed_checks": 0
        }
    return {
        "total_checks": int(len(df)),
        "success_rate": round(df["is_success"].astype(bool).mean() * 100, 2),
        "average_response_ms": round(df["response_time_ms"].mean(), 2),
        "failed_checks": int((~df["is_success"].astype(bool)).sum()),
    }

def endpoint_summary(df):
    if df.empty:
        return pd.DataFrame(columns=[
            "endpoint_name", "checks", "success_rate", "avg_response_ms"
        ])
    grouped = df.groupby("endpoint_name").agg(
        checks=("id", "count"),
        success_rate=("is_success", "mean"),
        avg_response_ms=("response_time_ms", "mean"),
    ).reset_index()
    grouped["success_rate"] = (grouped["success_rate"] * 100).round(2)
    grouped["avg_response_ms"] = grouped["avg_response_ms"].round(2)
    return grouped.sort_values("success_rate")
