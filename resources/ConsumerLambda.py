import logging
import boto3 as b3_
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler_name(event, context):
    try:
        logger.info("******************event_start*****************")
        logger.info(event)
        logger.info("******************event_end*****************")
    except:
        logger.info("ERROR")


    # sqs_queue_name = os.getenv("SQS_Queue_Name")
    # client = b3_.client('sqs')
    # queue_url_data = client.get_queue_url(
    #     QueueName=sqs_queue_name,
    # )
    # queue_url = queue_url_data['QueueUrl']
    
    # response = client.receive_message(
    #     QueueUrl=queue_url,
    #     WaitTimeSeconds=10,
    #     MaxNumberOfMessages=1,
    #     VisibilityTimeout=30,
    # )
    # logger.info("******************message_start*****************")
    # logger.info(response)
    # logger.info("******************message_end*****************")
