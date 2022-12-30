import json
import time
import pprint
import pycurl
import urllib

from flask import Flask, request

import client_config

app = Flask(__name__)

SECRET_KEY = 'SomethingNotEntirelySecret'
OIDC_CLIENT_SECRETS = './client_secrets.json'
OIDC_ID_TOKEN_COOKIE_SECURE = False
OIDC_SCOPES = ["openid", "profile", "email"]
OIDC_CALLBACK_ROUTE = '/authorization-code/callback'



pp = pprint.PrettyPrinter(indent=4)


@app.route("/")
def home():
    return "Hello!  There's not much to see here." \
           "Please grab one of our front-end samples for use with this sample resource server"


@app.route("/api/messages")
def messages():
    response = ''
    if validate_request(request):

        response = {
            'messages': [
                {
                    'date': time.time(),
                    'text': 'I am a robot.'
                },
                {
                    'date': time.time()-3600,
                    'text': 'Hello, World!'
                }
            ]
        }
    else:
        response = {"error message" : "unathorized request"}
    return json.dumps(response)



def validate_request(request):
    #retrieve access token
    pp.pprint(request.headers)
    token = request.headers.get("Authorization","No Token").split()[1]
    return validate_token(token,client_config.api_server_issuer,client_config.api_server_client_id,client_config.api_server_client_secret)

def validate_token(token, issuer, clientId, clientSecret):
    
    data = {
        'client_id': clientId,
        'client_secret': clientSecret,
        'token': token,
    }
    url = issuer + '/v1/introspect'

    response = api_request(url, post=data)

    return response['active'] == True



def api_request(url, post = None , headers = []):
    crl= pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(pycurl.VERBOSE, 1)

    if post:
        crl.setopt(crl.POSTFIELDS,urllib.parse.urlencode(post)) 
    headers = [
        'Accept: application/json; okta-version=1.0.0',
        'User-Agent: https://example-app.com'
        ]
    
    crl.setopt(crl.HTTPHEADER, headers)
    response = crl.perform_rs()
    print('response from curl is : '+response)
    return json.loads(response)




if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
