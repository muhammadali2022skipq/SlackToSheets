import logging
import json
import boto3 as b3_
from custom_encoder import CustomEncoder
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler_name(event, context):
    spread_id = "1NLGfAEevoz1zrkveMw7z8XCYMN1C7IbuaY09Vb2mdf4"

    logger.info(event)
    scopes = ["https://www.googleapis.com/auth/drive"]
    client = b3_.client('secretsmanager')
    secret_key = client.get_secret_value(
        SecretId="google-api-json-key",
    )
    json_keys = json.loads(secret_key['SecretString'])
    logger.info(json_keys)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(
        keyfile_dict=json_keys, scopes=scopes)
    logger.info("CREDS BELOW")
    logger.info(creds)

    service = build('sheets', 'v4', credentials=creds, cache_discovery=False)
    sheet = service.spreadsheets()

    userData = json.loads(event['Records'][0]['body'])['event']['user']

    if not userData['is_admin'] and not userData['is_bot'] and not userData['is_owner']:
        values = [
            [
                userData['id'],
                userData['profile']['first_name'],
                userData['profile']['last_name'],
                userData['profile']['email'],

            ],
            # Additional rows ...
        ]
        body = {
            'values': values
        }
        range_name = "A1:D1"
        request = sheet.values().append(
            spreadsheetId=spread_id,    
            range=range_name,
            includeValuesInResponse=True,
            insertDataOption="INSERT_ROWS",
            valueInputOption="RAW",
            body=body
        )
        response = request.execute()
        logger.info(response)
    return buildResponse(200, response)

    # Method to authorize google api using OAuth2.0
    # creds = Credentials.from_authorized_user_info(
    #     info=json_keys['web'], scopes=scopes)
    # secret_key = client.get_secret_value(
    #     SecretId="GoogleAPIKey",
    # )
    # GoogleDriveAPIURL = "https://www.googleapis.com/drive/v3/files?key={Google_Drive_API_Key}".format(
    #     Google_Drive_API_Key=secret_key)
    # headers = {
    #    "Authorization": "Bearer MYREALLYLONGTOKENIGOT"
    # }


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
