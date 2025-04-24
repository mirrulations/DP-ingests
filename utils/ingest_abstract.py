import json
import psycopg
from dotenv import load_dotenv
import sys
import os
from datetime import datetime


# Function to insert docket abstract into the database
def insert_abstract(conn, json_data):

   # Parse the JSON data
    data = json.loads(json_data)

    # Extract relevant fields
    attributes = data["data"]["attributes"]
    docket_id = data["data"]["id"]

    # Prepare the values for insertion
    values = (
        docket_id,
        attributes.get("dkAbstract")
    )


    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO abstracts (docket_id, abstract) VALUES (
                %s, %s)
            """
            cursor.execute(insert_query, values)
            print(f"Docket abstract for {docket_id} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
