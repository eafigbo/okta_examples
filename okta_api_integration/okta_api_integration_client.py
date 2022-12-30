
import pycurl
from io import BytesIO
#import urllib
import urllib.parse
import json
import base64
import pprint

import random
import os

import client_config



pp = pprint.PrettyPrinter(indent=4)
    




def get_users():
    the_response =''
    params = {
            #'sort': 'created',
            #'direction' : 'desc'
            }
    users = api_request(client_config.api_url_base + '/api/v1/users?' + urllib.parse.urlencode(params), authorization="Authorization: Bearer "+get_access_token())
    the_response = str(users)

    return the_response


def get_access_token():
    token = ''
    response = ''
    params = {
            'grant_type': 'client_credentials',
            'scope' : 'okta.users.read okta.groups.read'
            }
    auth_str = client_config.okta_client_id+':'+client_config.okta_api_integration_secret
    response = api_request(client_config.api_url_base + '/oauth2/v1/token' ,post=params, authorization='Authorization: Basic '+base64.b64encode(auth_str.encode('utf-8')).decode('utf-8'))
    token = response['access_token']
    return token

def api_request(url, post = None , headers = [], authorization=None):
    crl= pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(pycurl.VERBOSE, 1)

    if post:
        crl.setopt(crl.POSTFIELDS,urllib.parse.urlencode(post)) 
    headers = [
        'Accept: application/json; okta-version=1.0.0',
        'User-Agent: https://example-app.com'
        ]
    if(authorization):
        headers += [authorization]
    crl.setopt(crl.HTTPHEADER, headers)
    response = crl.perform_rs()
    pp.pprint('response from curl is : '+response)
    return json.loads(response)


if __name__ == '__main__':
    get_users()


