"""SQLite persistence for API monitoring results."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "monitoring.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS monitoring_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                endpoint_name TEXT NOT NULL,
                url TEXT NOT NULL,
                method TEXT NOT NULL,
                checked_at TEXT NOT NULL,
                status_code INTEGER,
                response_time_ms REAL,
                is_success INTEGER NOT NULL,
                error_message TEXT
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_results_checked_at
            ON monitoring_results(checked_at)
        """)
        conn.commit()

def save_result(result):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO monitoring_results
            (endpoint_name, url, method, checked_at, status_code,
             response_time_ms, is_success, error_message)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            result["endpoint_name"], result["url"], result["method"],
            result["checked_at"], result["status_code"],
            result["response_time_ms"], int(result["is_success"]),
            result["error_message"]
        ))
        conn.commit()

def fetch_results(limit=1000):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT * FROM monitoring_results
            ORDER BY checked_at DESC
            LIMIT ?
        """, (int(limit),)).fetchall()
    return [dict(row) for row in rows]
