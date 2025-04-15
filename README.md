# DP-ingests
This repository contains ingest scripts created by Data Product for use with ETL.

Data ingestion scripts used by the Data Product team for inserting regulatory data (dockets, documents, comments, summaries, and extracted text) into both PostgreSQL and OpenSearch indices.

## Ingestion Scripts and What They Do

### 1. `ingest.py`
Orchestrator module. It wraps ingestion logic for:
- Comments (to OpenSearch)
- Extracted Text (to OpenSearch)
- Documents, Dockets, and Summaries (to PostgreSQL)

### 2. `lambda_function.py`
Sample Lambda entrypoint to demonstrate:
- How a single Lambda function could ingest a sample docket, document, and comment

### 3. `ingest_comment.py`, `ingest_document.py`, `ingest_docket.py`, `ingest_summary.py`
Each of these modules:
- Reads JSON data (directly or from file if run standalone)
- Extracts relevant fields
- Inserts into PostgreSQL using a `psycopg` connection
- Handles nulls and dates using `date.py`

### 4. `ingest_opensearch.py`
Handles:
- Ingesting comments and extracted text into OpenSearch
- Also includes functionality to bulk ingest `.json` files from an S3 bucket

OpenSearch indices used:
- `comments`
- `extracted_text_test`

### 5. `date.py`
Utility to convert ISO date strings into Python `datetime` objects.
Handles invalid formats like `0000-12-30` by converting to `2000-12-30`.

### 6. `sql.py`
Creates a `psycopg` connection to PostgreSQL using secrets loaded from AWS Secrets Manager.
Used by all SQL ingestion modules.

### 7. `opensearch.py`
Creates a connection to OpenSearch with two modes:
- **Local mode:** uses `localhost` and basic auth (for dev/testing)
- **Prod mode:** uses AWS request signing via `AWSV4SignerAuth`

Secrets are pulled from `get_secret()` in `secrets.py`.

### 8. `secrets.py`
- Retrieves credentials securely from AWS Secrets Manager
- Decodes and parses JSON to extract host, port, credentials, etc.

## AWS Lambda Deployment
Refer to [`requirements.md`](https://github.com/denibravo/DP-ingests/blob/main/requirements.md)