import logging
import boto3 as b3_
import json
from custom_encoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler_name(event, context):
    try:
        logger.info("******************event_start*****************")
        logger.info(event)
        logger.info("******************event_end*****************")
        return buildResponse(200, event)
    except:
        raise Exception("ERROR:Consumer Lambda failed to consume event")


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
