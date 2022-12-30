import json
import pprint
import pycurl
import urllib
import base64
import random
import os
import pkce
from flask import Flask, render_template, url_for, redirect, request,session
#import flask_login
from flask_login import current_user, login_required, logout_user, login_user,LoginManager
from user import User

import client_config

app = Flask(__name__)
app.secret_key = os.urandom(28)
login_manager = LoginManager()
login_manager.init_app(app)


pp = pprint.PrettyPrinter(indent=4)
code_verifier, code_challenge = pkce.generate_pkce_pair()



@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def home():
    return render_template("home.html",user=current_user)

@app.route("/widget")
def widget():
    #signin using the embedded widget
    session['state'] = str(random.getrandbits(128))
    session['access_token'] = None
    print("code challenge is "+code_challenge)
    params =  {
            'scopes' : ["openid", "profile", "email", "okta.myAccount.profile.manage"],
            'client_id': client_config.client_id,
            'redirect_uri': client_config.interaction_redirect_uri,
            'state' : session['state'],
            'code_challenge' : code_challenge
            }
    return render_template("widget.html",params=params)



@app.route("/login")
def login():
    session['state'] = str(random.getrandbits(128))
    session['access_token'] = None
    params =  {
            'scope' : 'openid profile email okta.myAccount.profile.manage',
            'client_id': client_config.client_id,
            'redirect_uri': client_config.redirect_uri,
            'state' : session['state'],
            'response_type' : 'code'
            }

    return redirect(client_config.auth_uri+'?' + urllib.parse.urlencode(params),302)
    

@app.route("/profile")
@login_required
def profile():
    unathourized_response = {"error message" : "unathorized request"}

    if validate_session():
        info = api_request(client_config.userinfo_uri,{})

        return render_template("profile.html", profile=info,user=current_user)

    else:
        return unathourized_response




@app.route("/authorization-code/callback")
def exchange_token():
    if (request.args.get('state',None) == None) or (session.get('state',"no session state").strip() != request.args.get('state', "no request state").strip()):
        return redirect(client_config.base_url + '?error=invalid_state',302)

    print("request in exchange_tokens is :")
    pp.pprint(request.__dict__)
    #Exchange auth token for access token
    post_params = {
            'grant_type': 'authorization_code',
            'client_id' : client_config.client_id,
            'client_secret' : client_config.client_secret,
            'redirect_uri': client_config.redirect_uri,
            'code' : request.args.get('code'),
            'state' : session.get('state',None)
            }
    data = api_request(client_config.token_uri,post_params)
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
    pp.pprint('user_info: ')

    pp.pprint(user_info)
    session['user_id'] = user_info['sub']
    session['preferred_username'] = user_info['preferred_username']

    session['access_token'] = data['access_token']
    session['id_token'] = data['id_token']
    session['user_info'] = user_info

    unique_id = user_info["sub"]
    user_email = user_info["email"]
    user_name = ""#user_info["given_name"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
            User.create(unique_id, user_name, user_email)

    login_user(user)

    return redirect( url_for('profile'),302)



@app.route("/interaction-code/callback")
def exchange_Interaction_token():
    if (request.args.get('state',None) == None) or (session.get('state',"no session state").strip() != request.args.get('state', "no request state").strip()):
        return redirect(client_config.base_url + '?error=invalid_state',302)

    print("request in exchange_tokens is :")
    pp.pprint(request.__dict__)
    #Exchange auth token for access token
    post_params = {
            'grant_type': 'interaction_code',
            'client_id' : client_config.client_id,
            'client_secret' : client_config.client_secret,
            'redirect_uri': client_config.interaction_redirect_uri,
            #'code' : request.args.get('interaction_code'),
            'interaction_code' : request.args.get('interaction_code'),
            'state' : request.args.get('state'),
            'code_verifier' : code_verifier
            }
    data = api_request(client_config.token_uri,post_params)
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
    pp.pprint('user_info: ')

    pp.pprint(user_info)
    session['user_id'] = user_info['sub']
    session['preferred_username'] = user_info['preferred_username']

    session['access_token'] = data['access_token']
    session['id_token'] = data['id_token']
    session['user_info'] = user_info

    unique_id = user_info["sub"]
    user_email = user_info["email"]
    user_name = user_info["preferred_username"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
            User.create(unique_id, user_name, user_email)

    login_user(user)

    return redirect( url_for('profile'),302)


@app.route("/logout", methods=["POST"])
def logout():
    params ={
        'id_token_hint':session['id_token'],
    }
    session['access_token'] = None
    logout_user()
    return redirect(client_config.base_url+'/logout?'+urllib.parse.urlencode(params))


def validate_session():
    return session.get("access_token",None) != None



def api_request(url, post = None , headers = [], ssws = None):
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