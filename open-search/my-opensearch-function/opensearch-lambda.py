import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
     
region = 'us-east-1'  # Specify your AWS region, e.g., us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

# Specify your OpenSearch domain endpoint with https:// and without a trailing slash
host = ' https://search-algo-search-v1-bzo5parvuraxh6dyzk4rhiom2m.aos.us-east-1.on.aws'  

index = 'sites'
url = f'{host}/{index}/_search'

def lambda_handler(event, context):
    print(event)
    print('------------------------------------')
    print(event['queryStringParameters'])
    query = {
        "size": 25,
        "query": {
            "multi_match": {
                "query": event['queryStringParameters']['q'],
                "fields": ["title_element^4", "chapter_title^2", "body"]
            }
        }
    }

    headers = { "Content-Type": "application/json" }
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False,
        "body": r.text
    }

    return response
