# DP-ingests
This repository contains ingest scripts created by Data Product for use with ETL.

Data ingestion scripts used by the Data Product team for inserting regulatory data (dockets, documents, comments, summaries, and extracted text) into both PostgreSQL and OpenSearch indices.

## Ingestion Scripts and What They Do

### 1. `ingest.py`
Main entry point for running ingestion scripts:
- OpenSearch: comments, extracted text  
- PostgreSQL: documents, dockets, summaries  

### `ingest_opensearch.py`  
Handles comment and extracted text ingestion into OpenSearch.  
Also supports bulk ingest from `.json` files in S3.

### `ingest_docket.py`, `ingest_document.py`, `ingest_comment.py`  
Scripts for inserting JSON data into PostgreSQL.  
Each extracts fields and handles date conversion via `date.py`.

### `sql.py` & `opensearch.py`  
Database connection logic:  
- `sql.py` connects to PostgreSQL via AWS Secrets Manager  
- `opensearch.py` supports both local and production OpenSearch

## AWS Lambda Deployment  
Refer to [`requirements.md`](https://github.com/denibravo/DP-ingests/blob/main/requirements.md)