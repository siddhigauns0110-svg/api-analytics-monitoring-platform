# XML-to-JSON Data Transformation & Reconciliation Engine

A portfolio-ready Python integration project that parses XML client payloads, validates required fields, converts records into a consistent JSON structure, and reconciles transformed records against reference data in MySQL (or a local CSV for a no-database demo).

## Architecture

`XML payload → parser → validation/normalization → JSON output → reconciliation → discrepancy report`

## Features
- XML parsing with Python's standard library
- Required-field, date, numeric and duplicate-ID validation
- Consistent JSON output and structured error reporting
- Reconciliation against a MySQL table or CSV reference file
- CLI interface and sample payloads
- Unit tests

## Requirements
Python 3.10+. Install dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run the demo

```bash
python -m src.cli --xml examples/sample_clients.xml --json-output output/clients.json --errors-output output/errors.json
```

Run reconciliation against the included CSV:

```bash
python -m src.cli --xml examples/sample_clients.xml --json-output output/clients.json --reference-csv examples/reference_clients.csv --reconciliation-output output/reconciliation.json
```

## MySQL option

1. Create a database and load `sql/schema.sql`.
2. Copy `.env.example` to `.env` and set your connection details.
3. Install requirements (includes `mysql-connector-python`).
4. Run:

```bash
python -m src.cli --xml examples/sample_clients.xml --json-output output/clients.json --mysql
```

The MySQL mode reads the reference rows from `client_records`. Never commit real credentials; `.env` is gitignored.

## Output shape

```json
{
  "client_id": "C1001",
  "name": "Asha Rao",
  "email": "asha@example.com",
  "phone": "+91-9000000001",
  "created_at": "2026-01-15",
  "source": "xml_import"
}
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Project structure

- `src/transformer.py`: XML parsing, validation and JSON-ready normalization
- `src/reconciliation.py`: CSV/MySQL comparison and discrepancy reports
- `src/cli.py`: command-line workflow
- `sql/schema.sql`: MySQL reference table
- `examples/`: sample XML and reference CSV
- `tests/`: automated tests

## Important note for portfolio use

This repository demonstrates a working sample implementation. The claimed 80% reduction in manual verification time is not benchmarked by this demo; include that metric on a resume only if you have measured and can explain the before/after process. Do not present this as a production client integration unless you have deployed it.

**Tech stack:** Python, XML, JSON, MySQL, SQL, Git.
