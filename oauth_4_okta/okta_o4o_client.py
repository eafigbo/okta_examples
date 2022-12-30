import flask
from flask import Flask, session, request, redirect
#from flask_session import Session

import pycurl
from io import BytesIO
import urllib
import json
import base64
import pprint

import random
import os

import client_config

app = Flask(__name__)

app.secret_key = os.urandom(28)



pp = pprint.PrettyPrinter(indent=4)

@app.route('/')
def hello():
    if (request.args.get('action') and request.args.get('action') == 'login'):
        return login()
    elif (request.args.get('action') and request.args.get('action') == 'logout'):
        return logout()
    elif request.args.get('code'):
        return get_oauth_access_token()
    elif (request.args.get('action') and request.args.get('action') == 'profile'):
        return get_profile()
    elif (request.args.get('action') and request.args.get('action') == 'users'):
        return get_users()
    elif (request.args.get('action') == None):
        return is_logged_in()
    





def is_logged_in():
    the_response = 'No Response'
    if(session.get('user_id',None)):
        the_response += '<h3> Logged In </h3> '
        the_response += '<p>User ID: '+ session.get('user_id') +'</p> '
        the_response += '<p>Email: '+ session.get('preferred_username') +'</p> '
        #the_response += '<p><a href=" '+get_oauth_access_token_url() +'">Get OAuth For Okta Access Token</a></p>'
        the_response += '<p><a href=" ?action=users">Get Users</a></p>'

        the_response += '<p><a href="?action=logout">Log Out</a></p>'

        the_response += '<h3> ID Token </h3> '
        the_response += '<pre> '
        
        data = api_request('https://dev-94568396.okta.com/oauth2/v1/userinfo')
        the_response += str(data)
        #print("data in is_logged_in is:  ")
        #pp.pprint(str(data))
        the_response += '</pre> '


    else:
        the_response = """
                        <h3> Not Logged In </h3>
                        <p><a href="?action=login">Log In</a></p>
        """
    return the_response

def login():
    session['state'] = str(random.getrandbits(128))
    session['access_token'] = None
    params =  {
           'scope' : 'openid profile okta.myAccount.profile.manage okta.users.read okta.users.manage',
           'client_id': client_config.okta_client_id,
           'redirect_uri': client_config.base_url,
           'state' : session['state'],
           'response_type' : 'code'
           }
    
    return redirect(client_config.oauth_authorize_url+'?' + urllib.parse.urlencode(params),302)

def get_oauth_access_token_url():
    params = {
            'client_id' : client_config.okta_client_id,
            'client_secret' : client_config.okta_client_secret,
            'response_type': 'token',
            'response_mode' : 'fragment',
            'scope' : 'okta.users.read',
            'redirect_uri': client_config.base_url,
            'nonce': 'UBGW',
            'state': session.get('state',None)
            }
    return client_config.oauth_access_token_url+'?' + urllib.parse.urlencode(params)


def logout():
    session['access_token'] = None
    session['user_id'] = None
            
    return redirect(client_config.base_url,302)


def get_oauth_access_token():
    if (request.args.get('state',None) == None) or (session.get('state',"no session state").strip() != request.args.get('state', "no request state").strip()):
        return redirect(client_config.base_url + '?error=invalid_state',302)


    #Exchange auth token for access token
    post_params = {
            'grant_type': 'authorization_code',
            'client_id' : client_config.okta_client_id,
            'client_secret' : client_config.okta_client_secret,
            'redirect_uri': client_config.base_url,
            'code' : request.args.get('code'),
            'state' : session.get('state',None)
            }
    data = api_request(client_config.oauth_access_token_url,post_params)
    #data = api_request(oauth_access_token_url,post_params)
    pp.pprint('Data: ')

    pp.pprint(data)
    jwt = data['id_token'].split('.')
    pp.pprint('JWT: ')

    pp.pprint(jwt)
    #check padding
    padding=''
    if len(jwt[1]) % 4:
    # not a multiple of 4, add padding:
        padding += '=' * (4 - len(padding) % 4) 
    user_info = json.loads(base64.b64decode(jwt[1]+padding))
    pp.pprint('use_info: ')

    pp.pprint(user_info)
    session['user_id'] = user_info['sub']
    session['preferred_username'] = user_info['preferred_username']

    session['access_token'] = data['access_token']
    session['id_token'] = data['id_token']
    session['user_info'] = user_info

    return redirect( client_config.base_url,302)


def get_profile():
    the_response =''
    params = {
            #'sort': 'created',
            #'direction' : 'desc'
            }
    profile = api_request(client_config.api_url_base + 'idp/myaccount/profile?' + urllib.parse.urlencode(params))
    the_response = str(profile)
    
    if (request.args.get('action') == None):
        if (session.get('access_token',None)):
            the_response += """
            <h3>Logged In</h3>
            <p><a href="?action=repos"> View Repos</a>
            <p><a href="?action=logout"> Log Out</a>
            """
        else:
            the_response += """
            <h3>Not Logged In</h3>
            <p><a href="?action=login"> Log In</a>
            """
    return the_response



def get_users():
    the_response =''
    params = {
            #'sort': 'created',
            #'direction' : 'desc'
            }
    profile = api_request(client_config.api_url_base + '/api/v1/users?' + urllib.parse.urlencode(params))
    the_response = str(profile)
    
    if (request.args.get('action') == None):
        if (session.get('access_token',None)):
            the_response += """
            <h3>Logged In</h3>
            <p><a href="?action=repos"> View Repos</a>
            <p><a href="?action=logout"> Log Out</a>
            """
        else:
            the_response += """
            <h3>Not Logged In</h3>
            <p><a href="?action=login"> Log In</a>
            """
    return the_response



def api_request(url, post = None , headers = [], ssws=None):
    crl= pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(pycurl.VERBOSE, 1)

    if post:
        crl.setopt(crl.POSTFIELDS,urllib.parse.urlencode(post)) 
    headers = [
        'Accept: application/json; okta-version=1.0.0',
        'User-Agent: https://example-app.com'
        ]
    if(ssws):
        headers += ['Authorization: SSWS '+ssws]
    elif session.get("access_token",None):
        headers += ['Authorization: Bearer '+session.get("access_token",None)]
    crl.setopt(crl.HTTPHEADER, headers)
    response = crl.perform_rs()
    print('response from curl is : '+response)
    return json.loads(response)


if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True)


