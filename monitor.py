"""Run lightweight health checks against configured HTTP endpoints."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

from database import initialize_database, save_result

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

def load_endpoints():
    with CONFIG_PATH.open(encoding="utf-8") as file:
        endpoints = json.load(file)
    if not isinstance(endpoints, list):
        raise ValueError("config.json must contain a list of endpoints")
    for endpoint in endpoints:
        if not all(key in endpoint for key in ("name", "url")):
            raise ValueError("Each endpoint needs a name and url")
        endpoint.setdefault("method", "GET")
        endpoint.setdefault("timeout_seconds", 10)
    return endpoints

def check_endpoint(endpoint):
    """Call one endpoint and return a normalized monitoring record."""
    started = time.perf_counter()
    status_code = None
    error_message = None
    try:
        response = requests.request(
            method=endpoint.get("method", "GET").upper(),
            url=endpoint["url"],
            timeout=float(endpoint.get("timeout_seconds", 10)),
        )
        status_code = response.status_code
        # Treat HTTP 2xx and 3xx as reachable/successful.
        is_success = 200 <= response.status_code < 400
    except requests.RequestException as exc:
        is_success = False
        error_message = f"{type(exc).__name__}: {exc}"
    elapsed_ms = (time.perf_counter() - started) * 1000

    return {
        "endpoint_name": endpoint["name"],
        "url": endpoint["url"],
        "method": endpoint.get("method", "GET").upper(),
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status_code": status_code,
        "response_time_ms": round(elapsed_ms, 2),
        "is_success": is_success,
        "error_message": error_message,
    }

def run_checks():
    initialize_database()
    results = []
    for endpoint in load_endpoints():
        result = check_endpoint(endpoint)
        save_result(result)
        results.append(result)
        status = "UP" if result["is_success"] else "DOWN"
        print(
            f'{status:4} | {result["endpoint_name"]} | '
            f'{result["status_code"] or "no response"} | '
            f'{result["response_time_ms"]} ms'
        )
    return results

def main():
    parser = argparse.ArgumentParser(description="API monitoring runner")
    parser.add_argument("--interval", type=int, default=0,
                        help="Repeat checks every N seconds; 0 means run once")
    args = parser.parse_args()
    if args.interval < 0:
        parser.error("--interval must be zero or greater")

    if args.interval == 0:
        run_checks()
    else:
        print(f"Monitoring every {args.interval} seconds. Press Ctrl+C to stop.")
        try:
            while True:
                run_checks()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()
