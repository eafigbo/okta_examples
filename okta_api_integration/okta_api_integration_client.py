import pycurl
from io import BytesIO
import urllib.parse
import json
import time
import uuid
from jose import jwt

import client_config


def get_users():
    users = api_request(
        client_config.api_url_base.rstrip('/') + '/api/v1/users',
        authorization="Authorization: Bearer " + get_access_token()
    )
    return users


def get_access_token():
    params = {
        'grant_type': 'client_credentials',
        'scope': 'okta.users.read okta.groups.read',
        'client_assertion_type': 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer',
        'client_assertion': _build_client_assertion()
    }
    response = api_request(client_config.token_url, post=params)
    return response['access_token']

def _build_client_assertion():
    now = int(time.time())
    with open(client_config.private_key_path, 'r') as f:
        private_key = f.read()
    return jwt.encode(
        {'iss': client_config.okta_client_id,
         'sub': client_config.okta_client_id,
         'aud': client_config.token_url,
         'iat': now,
         'exp': now + 300,
         'jti': str(uuid.uuid4())},
        private_key,
        algorithm='RS256',
        headers={'kid': client_config.okta_kid}
    )

def api_request(url, post=None, authorization=None):
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url)
    if post:
        crl.setopt(crl.POSTFIELDS,urllib.parse.urlencode(post)) 
    headers = [
        'Accept: application/json; okta-version=1.0.0',
        'User-Agent: https://example-app.com'
        ]
    if(authorization):
        headers += [authorization]
    crl.setopt(crl.HTTPHEADER, headers)
    buffer = BytesIO()
    crl.setopt(crl.WRITEFUNCTION, buffer.write)
    crl.perform()
    return json.loads(buffer.getvalue().decode('utf-8'))

if __name__ == '__main__':
    print(get_users())