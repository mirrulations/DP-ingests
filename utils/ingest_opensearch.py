import os
import json
import boto3
from .opensearch import connect as create_client


def ingest_comment_from_text(client, content):
    """
    Ingests a comment from a text file into OpenSearch.
    """
    data = json.loads(content)
    document = {
        'commentText': data['data']['attributes']['comment'],
        'docketId': data['data']['attributes']['docketId'],
        'commentId': data['data']['id']
    }
    ingest(client, document, id = document['commentId'], index= 'comments')

def ingest(client, document, id, index):
    """
    Ingests a document into OpenSearch.
    """
    response = client.index(index = index, body = document, id = id)
    print(response)

def ingest_extracted_text_from_text(client, data):
    """
    Ingests extracted text from a text file into OpenSearch.
    """
    document = {
        'extractedText': data['extractedText'],
        'extractedMethod': data['extractedMethod'],
        'docketId': data['docketId'],
        'commentId': data['commentId'],
        'attachmentId': data['attachmentId']
    }
    ingest(client, document, id = document['attachmentId'], index= 'comments_extracted_text')


def ingest_comment(client, bucket, key):
    """
    Ingests a comment from an S3 bucket into OpenSearch.
    """
    obj = bucket.Object(key)
    file_text = obj.get()['Body'].read().decode('utf-8')
    data = json.loads(file_text)
    document = {
        'commentText': data['data']['attributes']['comment'],
        'docketId': data['data']['attributes']['docketId'],
        'commentId': data['data']['id']
    }
    ingest(client, document)

def ingest_all_comments(client, bucket):
    """
    Ingests all comments from an S3 bucket into OpenSearch.
    """
    for obj in bucket.objects.all():
        if obj.key.endswith('.json') and ('/comments/' in obj.key):
            ingest_comment(client, bucket, obj.key)

if __name__ == '__main__':
    """
    Main entry point for the script. Connects to OpenSearch and S3, and ingests
    all comments from the specified S3 bucket into OpenSearch.
    """
    client = create_client()

    s3 = boto3.resource(
        service_name = 's3',
        region_name = 'us-east-1'
    )

    print('boto3 created')

    bucket = s3.Bucket(os.getenv('S3_BUCKET_NAME'))

    ingest_all_comments(client, bucket)
