import os
from dotenv import load_dotenv
import certifi
import boto3
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from common.utils.secrets import get_secret

def connect():
    """
    Create an OpenSearch client.
    If running locally, connect to the local OpenSearch instance.
    If running in AWS, connect to the production OpenSearch instance.
    """
    load_dotenv()

    is_local = os.getenv('AWS_SAM_LOCAL', 'false').lower() == 'true'

    if is_local:
        host = os.getenv('OPENSEARCH_HOST')
        port = os.getenv('OPENSEARCH_PORT')
        auth = ('admin', os.getenv('OPENSEARCH_INITIAL_ADMIN_PASSWORD'))

        ca_certs_path = certifi.where()
        # Create the client with SSL/TLS enabled, but hostname verification disabled.
        client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=auth,
            use_ssl=False,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
            ca_certs=ca_certs_path
        )

        return client

    secret_name = os.getenv('DB_SECRET_NAME')
    secret = get_secret(secret_name)

    host = secret['host']
    port = secret['port']
    region = 'us-east-1'

    
    service = 'aoss'
    credentials = boto3.Session().get_credentials()
    auth = AWSV4SignerAuth(credentials, region, service)

    # Create the client using AWS request signing
    client = OpenSearch(
        hosts=[{'host': host, 'port': port}],
        http_compress=True,  # enables gzip compression for request bodies
        http_auth=auth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        pool_maxsize=20,
        timeout=60
    )

    return client