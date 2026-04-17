import json
import psycopg
from dotenv import load_dotenv
import sys
import os
from datetime import datetime
from .date import parse as parse_date


def insert_comment(conn, json_data):
    """
    Insert comment into the database.
    """
    # Parse the JSON data
    data = json.loads(json_data)

    # Extract relevant fields
    attributes = data["data"]["attributes"]
    comment_id = data["data"]["id"]
    api_link = data["data"]["links"]["self"]

    # Prepare the values for insertion
    values = (
        comment_id,
        api_link,
        attributes.get("commentOnDocumentId"),
        attributes.get("duplicateComments"),
        attributes.get("address1"),
        attributes.get("address2"),
        attributes.get("agencyId"),
        attributes.get("city"),
        attributes.get("category"),
        attributes.get("comment"),
        attributes.get("country"),
        attributes.get("docketId"),
        attributes.get("documentType"),
        attributes.get("email"),
        attributes.get("fax"),
        attributes.get("field1"),
        attributes.get("field2"),
        attributes.get("firstName"),
        attributes.get("govAgency"),
        attributes.get("govAgencyType"),
        attributes.get("lastName"),
        parse_date(attributes.get("modificationDate")),
        attributes.get("organization"),
        attributes.get("phone"),
        parse_date(attributes.get("postedDate")),
        parse_date(attributes.get("postmarkDate")),
        attributes.get("reasonWithdrawn"),
        parse_date(attributes.get("receivedDate")),
        attributes.get("restrictReason"),
        attributes.get("restrictReasonType"),
        attributes.get("stateProvinceRegion"),
        attributes.get("subtype"),
        attributes.get("title"),
        attributes.get("withdrawn"),
        attributes.get("zip"),
    )

    # Insert into the database
    try:
        with conn.cursor() as cursor:
            insert_query = """
            INSERT INTO comments (
                comment_id, api_link, document_id, duplicate_comment_count, address1,
                address2, agency_id, city, comment_category, comment, country,
                docket_id, document_type, email, fax, flex_field1, flex_field2,
                first_name, submitter_gov_agency, submitter_gov_agency_type,
                last_name, modification_date, submitter_org, phone, posted_date,
                postmark_date, reason_withdrawn, received_date, restriction_reason,
                restriction_reason_type, state_province_region, comment_subtype,
                comment_title, is_withdrawn, postal_code
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                    %s, %s, %s)
            ON CONFLICT (comment_id) DO UPDATE
            SET
                api_link = EXCLUDED.api_link,
                document_id = EXCLUDED.document_id,
                duplicate_comment_count = EXCLUDED.duplicate_comment_count,
                address1 = EXCLUDED.address1,
                address2 = EXCLUDED.address2,
                agency_id = EXCLUDED.agency_id,
                city = EXCLUDED.city,
                comment_category = EXCLUDED.comment_category,
                comment = EXCLUDED.comment,
                country = EXCLUDED.country,
                docket_id = EXCLUDED.docket_id,
                document_type = EXCLUDED.document_type,
                email = EXCLUDED.email,
                fax = EXCLUDED.fax,
                flex_field1 = EXCLUDED.flex_field1,
                flex_field2 = EXCLUDED.flex_field2,
                first_name = EXCLUDED.first_name,
                submitter_gov_agency = EXCLUDED.submitter_gov_agency,
                submitter_gov_agency_type = EXCLUDED.submitter_gov_agency_type,
                last_name = EXCLUDED.last_name,
                modification_date = EXCLUDED.modification_date,
                submitter_org = EXCLUDED.submitter_org,
                phone = EXCLUDED.phone,
                posted_date = EXCLUDED.posted_date,
                postmark_date = EXCLUDED.postmark_date,
                reason_withdrawn = EXCLUDED.reason_withdrawn,
                received_date = EXCLUDED.received_date,
                restriction_reason = EXCLUDED.restriction_reason,
                restriction_reason_type = EXCLUDED.restriction_reason_type,
                state_province_region = EXCLUDED.state_province_region,
                comment_subtype = EXCLUDED.comment_subtype,
                comment_title = EXCLUDED.comment_title,
                is_withdrawn = EXCLUDED.is_withdrawn,
                postal_code = EXCLUDED.postal_code;
            """

            cursor.execute(insert_query, values)
            print(f"Comment {comment_id} inserted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    """
    Main entry point for the script. Reads a JSON file and inserts the data into the database.
    """
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
