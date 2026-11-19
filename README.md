# API Analytics & Monitoring Platform

A Python project that checks REST API endpoints, records response times and HTTP status codes in SQLite, and visualizes reliability metrics in a Streamlit dashboard.

## Features

- Configurable endpoint list (`config.json`)
- HTTP health checks with request timeouts
- Response-time and status-code logging
- SQLite persistence
- Success rate, failed checks and average latency metrics
- Per-endpoint analytics and interactive charts
- CSV export of collected monitoring history
- Automated tests for successful and failed requests

## Tech stack

Python, Requests, SQLite, SQL, Pandas, Streamlit, Plotly, Pytest, Git.

## Setup

Python 3.10+ is recommended.

```bash
git clone https://github.com/siddhigauns0110-svg/api-analytics-monitoring-platform.git
cd api-analytics-monitoring-platform
python -m venv .venv
```

Activate the environment:

**Windows**
```bash
.venv\\Scripts\\activate
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the monitor

```bash
python monitor.py
```

Repeat checks every 60 seconds:

```bash
python monitor.py --interval 60
```

Only monitor endpoints you own or are authorized to test. Stop continuous monitoring with `Ctrl+C`.

## Launch the dashboard

```bash
streamlit run app.py
```

Run the monitor first to populate the SQLite database. The dashboard provides API health metrics, endpoint summaries, response-time trends, recent history and CSV export.

## Configure endpoints

Edit `config.json`. Each endpoint supports `name`, `url`, `method` (defaults to GET) and `timeout_seconds` (defaults to 10). Do not commit API keys or other secrets.

## Run tests

```bash
pytest -q
```

## Database design

`monitoring_results` stores one row per check: endpoint name, URL, HTTP method, UTC timestamp, status code, response time, success flag and error message.


**API Analytics & Monitoring Platform | Python, SQL, REST APIs, Pandas, Streamlit**
- Developed a Python-based REST API monitoring tool to measure endpoint availability, HTTP status codes and response latency.
- Designed a SQLite database to persist monitoring history and used SQL/Pandas to calculate endpoint-level reliability metrics.
- Built an interactive Streamlit dashboard with response-time trends, success/failure summaries and CSV export.
- Added timeout/error handling and automated tests for successful and failed API requests.

Do not claim uptime improvements or production deployment unless measured and completed.

## Future improvements

- API key authentication through environment variables
- Configurable alert thresholds and email notifications
- Scheduled monitoring with a background worker
- PostgreSQL support
- Docker and CI workflow
