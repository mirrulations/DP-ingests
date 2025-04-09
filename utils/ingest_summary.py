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


# Main function to read JSON from file and insert into the database
def main():
    if len(sys.argv) != 2:
        print("Usage: python IngestComment.py <path_to_json_file>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    load_dotenv()
    dbname = os.getenv("POSTGRES_DB")
    username = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")

    conn_params = {
        "dbname": dbname,
        "user": username,
        "password": password,
        "host": host,
        "port": port,
    }

    try:
        with open(json_file_path, "r") as json_file:
            json_data = json_file.read()
            with psycopg.connect(**conn_params) as conn:
                insert_comment(conn, json_data)
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON from the file.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
