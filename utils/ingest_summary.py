import json
import psycopg
from dotenv import load_dotenv
import sys
import os
from datetime import datetime

# Fetch database connection parameters from environment variables


# Function to parse date fields
def parse_date(date_str):
    if date_str:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
    return None


# Function to insert comment into the database
def insert_comment(conn, json_data):
    # Parse the JSON data
    data = json.loads(json_data)

    docket_id = data["docket_id"]
    summary_text = data["summary_text"]

    # get the abstract from the dockets table
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT docket_abstract from dockets where docket_id = %s
            """
            cursor.execute(query, (docket_id,))
            result = cursor.fetchone()

            abstract = result[0]

            insert_query = """
            INSERT INTO summaries (docket_id, abstract, summary) VALUES (
                %s, %s, %s
            )
            """
            cursor.execute(insert_query, (docket_id, abstract, summary_text))
            print(f"Docket summary and abstract for {docket_id} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
