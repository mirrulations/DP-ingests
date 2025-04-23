import json
import psycopg
from dotenv import load_dotenv
import sys
import os
from datetime import datetime


# Function to insert docket abstract into the database
def insert_abstract(conn, data):
    docket_id = data["docket_id"]

    # get the docket_abstract from the dockets table
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT docket_abstract from dockets where docket_id = %s
            """
            cursor.execute(query, (docket_id,))
            result = cursor.fetchone()

            abstract = result[0]

            insert_query = """
            INSERT INTO abstracts (docket_id, abstract) VALUES (
                %s, %s)
            """
            cursor.execute(insert_query, (docket_id, abstract))
            print(f"Docket abstract for {docket_id} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
