import base64
import json
import os

import requests


GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')


def lambda_main(event, context):
    path = event['rawPath']
    if 'body' in event:
        if event['isBase64Encoded']:
            body = base64.b64decode(event['body'])
        else:
            body = event['body']
    else:
        body = None
    signature = event['headers'].get("x-hub-signature", "")
    if signature.startswith("sha1="):
        signature = signature[5:]

    if path == "/example-path":
        # https://docs.github.com/en/developers/webhooks-and-events/webhook-events-and-payloads#star
        payload = json.loads(body)
        repository = payload['repository']
        repository_url = repository['url']
        stars = payload['stargazers_count']

        new_name = f"This-Repo-Has-{stars}-Star{'s' if stars != 1 else ''}"

        headers = {'Authorization': f"Bearer {GITHUB_TOKEN}"}
        data = {'name': new_name}
        response = requests.patch(repository_url, headers=headers, json=data)
        return {'statusCode': response.status_code, 'body': "OK"}
    else:
        return {'statusCode': 404, 'body': ""}
