from flask import Flask, session, request, redirect

import pycurl
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
    action = request.args.get('action')
    if action == 'login':
        return login()
    elif action == 'logout':
        return logout()
    elif request.args.get('code'):
        return exchange_token()
    elif action == 'profile':
        return get_profile()
    elif action == 'users':
        return get_users()
    elif action == 'messages':
        return get_messages()
    else:
        return is_logged_in()


def is_logged_in():
    the_response = 'No Response'
    if session.get('user_id', None):
        the_response += '<h3> Logged In </h3> '
        the_response += '<p>User ID: ' + session.get('user_id') + '</p> '
        the_response += '<p>Email: ' + session.get('preferred_username') + '</p> '
        the_response += '<p><a href="?action=users">Get Users With SSWS Token</a></p>'
        the_response += '<p><a href="?action=messages">Get Messages from API Server</a></p>'
        the_response += '<p><a href="?action=logout">Log Out</a></p>'
        the_response += '<h3> ID Token </h3> '
        the_response += '<pre> '
        data = api_request(client_config.user_info_url)
        the_response += str(data)
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
    params = {
        'scope': 'openid profile okta.myAccount.profile.manage',
        'client_id': client_config.okta_client_id,
        'redirect_uri': client_config.base_url,
        'state': session['state'],
        'response_type': 'code'
    }
    return redirect(client_config.authorize_url + '?' + urllib.parse.urlencode(params), 302)


def logout():
    session['access_token'] = None
    session['user_id'] = None
    return redirect(client_config.base_url, 302)


def exchange_token():
    if (request.args.get('state', None) is None) or (session.get('state', 'no session state').strip() != request.args.get('state', 'no request state').strip()):
        return redirect(client_config.base_url + '?error=invalid_state', 302)

    post_params = {
        'grant_type': 'authorization_code',
        'client_id': client_config.okta_client_id,
        'client_secret': client_config.okta_client_secret,
        'redirect_uri': client_config.base_url,
        'code': request.args.get('code'),
        'state': session.get('state', None)
    }
    data = api_request(client_config.token_url, post_params)
    pp.pprint('Data: ')
    pp.pprint(data)

    if 'id_token' not in data:
        return redirect(client_config.base_url + '?error=token_exchange_failed', 302)

    jwt = data['id_token'].split('.')
    pp.pprint('JWT: ')
    pp.pprint(jwt)

    remainder = len(jwt[1]) % 4
    if remainder:
        jwt[1] += '=' * (4 - remainder)

    user_info = json.loads(base64.b64decode(jwt[1]))
    pp.pprint('user_info: ')
    pp.pprint(user_info)

    session['user_id'] = user_info['sub']
    session['preferred_username'] = user_info['preferred_username']
    session['access_token'] = data['access_token']
    session['id_token'] = data['id_token']
    session['user_info'] = user_info

    return redirect(client_config.base_url, 302)


def get_profile():
    profile = api_request(client_config.api_url_base + 'idp/myaccount/profile')
    return str(profile)


def get_users():
    users = api_request(client_config.api_url_base + 'api/v1/users', ssws=client_config.okta_ssws_token)
    return str(users)


def get_messages():
    messages = api_request(client_config.resource_server_url + 'api/messages')
    return str(messages)


def api_request(url, post=None, ssws=None):
    crl = pycurl.Curl()
    crl.setopt(crl.URL, url)
    crl.setopt(pycurl.VERBOSE, 1)

    if post:
        crl.setopt(crl.POSTFIELDS, urllib.parse.urlencode(post))
    headers = [
        'Accept: application/json; okta-version=1.0.0',
        'User-Agent: https://example-app.com'
    ]
    if ssws:
        headers += ['Authorization: SSWS ' + ssws]
    elif session.get('access_token', None):
        headers += ['Authorization: Bearer ' + session.get('access_token', None)]
    crl.setopt(crl.HTTPHEADER, headers)
    response = crl.perform_rs()
    print('response from curl is : ' + response)
    return json.loads(response)


if __name__ == '__main__':
    app.run(host='localhost', port='5000', debug=True)
