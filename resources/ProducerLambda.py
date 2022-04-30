import json
import logging
from custom_encoder import CustomEncoder
import boto3 as b3_
import os

# Logger to log info to help debug the api
logger = logging.getLogger()
logger.setLevel(logging.INFO)

getMethod = "GET"
postMethod = "POST"
patchMethod = "PATCH"
delMethod = "DELETE"

slackUserDataMethod = "/slackuserdata"


def handler_name(event, context):
    client = b3_.client('sqs')

    logger.info(event)
    # Retrieving http method and path passed to event
    httpMethod = event['httpMethod']
    path = event['path']
    sqs_queue_name = os.getenv("SQS_Queue_Name")
    # Calling functions based on httpmethod and url path
    if httpMethod == getMethod and path == slackUserDataMethod:
        response = buildResponse(200)
    elif httpMethod == postMethod and path == slackUserDataMethod:
        user_data = json.loads(event['body'])
        if "challenge" not in user_data:
            response_data = queueMessage(client, sqs_queue_name, user_data)
            response = buildResponse(200, response_data)
        else:
            response = buildResponse(200, user_data)
    else:
        response = buildResponse('404', 'Not Found')

    return response


def queueMessage(boto3_sqs_client, sqs_queue_name, user_data):
    queue_url_data = boto3_sqs_client.get_queue_url(
        QueueName=sqs_queue_name,
    )
    queue_url = json.loads(queue_url_data)['QueueUrl']
    response = boto3_sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(user_data),
    )
    return response


def buildResponse(statusCode, body=None):
    # Creating response to return to client
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response
