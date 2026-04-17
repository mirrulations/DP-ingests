import json
import psycopg
from dotenv import load_dotenv
import sys
import os
from datetime import datetime


# json_data is {"docket_id": docket_id,"summary_text": summary_text}
def insert_summary(conn, data):
    """
    Insert summary into the database.
    """
    docket_id = data["docket_id"]
    summary_text = data["summary_text"]

    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO htm_summaries (docket_id, summary) VALUES (
                %s, %s)
            """
            cursor.execute(insert_query, (docket_id, summary_text))
            print(f"Docket summary for {docket_id} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
