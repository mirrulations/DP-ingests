import os
from dotenv import load_dotenv
import certifi
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth

try:
    from common.utils.secrets import get_secret
    print("[DEBUG] Using get_secret from common.utils")
except ImportError:
    from dp_ingest.utils.secrets import get_secret
    print("[DEBUG] Using get_secret from dp_ingest.utils")

'''
This function creates an OpenSearch client. If the environment variables OPENSEARCH_HOST if OPENSEARCH_PORT are not
set, an error is raised. If the host is set to 'localhost', the client is created with basic authentication. Otherwise,
the client is created with AWS request signing. The function returns the OpenSearch client.

All code that depends on whether we are connecting to a local or production OpenSearch instance is inside of this function.
Outside of the function, interaction with the client is the same regardless of the environment.
'''
def connect():
    load_dotenv()
    env = os.getenv("ENVIRONMENT", "local").lower()
    print(f"[DEBUG] ENVIRONMENT={env}")

    if env == "local":
        print("[DEBUG] Using local OpenSearch configuration")

        host = os.getenv('OPENSEARCH_HOST', 'localhost')
        port = int(os.getenv('OPENSEARCH_PORT', '9200'))
        password = os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD')

        if not password:
            raise ValueError("Missing OPENSEARCH_INITIAL_ADMIN_PASSWORD in local .env")

        auth = ('admin', password)

        ca_certs_path = certifi.where()
        client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,
            http_auth=auth,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
            ca_certs=ca_certs_path
        )
        return client

    # Else: prod via AWS Secrets Manager
    print("[DEBUG] Using AWS Secrets Manager configuration")
    secret_name = os.getenv('OS_SECRET_NAME', 'mirrulationsdb/opensearch/master')
    region = os.getenv('AWS_REGION', 'us-east-1')
    secret = get_secret(secret_name)

    host = secret['host']
    port = secret['port']
    service = 'aoss'
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, service)


    # Create the client using AWS request signing
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
        timeout=60
    )

    return client