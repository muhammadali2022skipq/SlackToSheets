import logging
import json
import boto3 as b3_
from custom_encoder import CustomEncoder
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler_name(event, context):

    scopes = ["https://www.googleapis.com/auth/drive"]
    client = b3_.client('secretsmanager')

   # GoogleDriveAPIURL = "https://www.googleapis.com/drive/v3/files?key={Google_Drive_API_Key}".format(
    #    Google_Drive_API_Key=GoogleDriveAPIKey)

    # headers = {
    #    "Authorization": "Bearer MYREALLYLONGTOKENIGOT"
    # }
    try:
        secret_key = client.get_secret_value(
            SecretId="google-api-json-key",
        )
        json_keys = json.loads(secret_key['SecretString'])

        creds = Credentials.from_authorized_user_info(json_keys, scopes)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        spreadsheet = {
            'properties': {
                'title': "Testing "
            }
        }
        response = sheet.create(body=spreadsheet).execute()
        logger.info("**&&&&&&&&&&&&&&&&&&&&&&&&")
        logger.info(response)
        logger.info("**&&&&&&&&&&&&&&&&&&&&&&&&")
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
