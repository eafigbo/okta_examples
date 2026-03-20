import secrets
import os
import urllib.parse
import warnings
import requests
import pkce
from flask import Flask, render_template, url_for, redirect, request, session
from flask_login import current_user, login_required, logout_user, login_user, LoginManager
from jose import jwt, JWTError
from user import User

import client_config

app = Flask(__name__)

# Fix #1: stable secret key from env var; warn if falling back to ephemeral value
_secret_key = os.environ.get("FLASK_SECRET_KEY")
if not _secret_key:
    warnings.warn(
        "FLASK_SECRET_KEY env var not set; sessions will not persist across restarts.",
        stacklevel=1,
    )
    _secret_key = secrets.token_hex(32)
app.secret_key = _secret_key

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html", user=current_user)


@app.route("/widget")
def widget():
    # Fix #5: generate a fresh PKCE pair per session (not once at startup)
    code_verifier, code_challenge = pkce.generate_pkce_pair()
    session['state'] = secrets.token_urlsafe(32)
    session['code_verifier'] = code_verifier
    session['access_token'] = None
    params = {
        'scopes': ["openid", "profile", "email"],
        'client_id': client_config.client_id,
        'redirect_uri': client_config.interaction_redirect_uri,
        'state': session['state'],
        'code_challenge': code_challenge,
        'issuer': client_config.issuer,
    }
    return render_template("widget.html", params=params)


@app.route("/login")
def login():
    session['state'] = secrets.token_urlsafe(32)
    session['access_token'] = None
    params = {
        'scope': 'openid profile email',
        'client_id': client_config.client_id,
        'redirect_uri': client_config.redirect_uri,
        'state': session['state'],
        'response_type': 'code',
    }
    return redirect(client_config.auth_uri + '?' + urllib.parse.urlencode(params), 302)


@app.route("/profile")
@login_required
def profile():
    if not validate_session():
        return {"error message": "unauthorized request"}, 401
    info = api_request(client_config.userinfo_uri)
    return render_template("profile.html", profile=info, user=current_user)


@app.route("/authorization-code/callback")
def exchange_token():
    if not _validate_state():
        return redirect(client_config.base_url + '?error=invalid_state', 302)

    # Confidential client flow: use client_secret, no PKCE
    post_params = {
        'grant_type': 'authorization_code',
        'client_id': client_config.client_id,
        'client_secret': client_config.client_secret,
        'redirect_uri': client_config.redirect_uri,
        'code': request.args.get('code'),
        'state': session.get('state'),
    }
    data = api_request(client_config.token_uri, post_params)
    return _handle_token_response(data)


@app.route("/interaction-code/callback")
def exchange_interaction_token():
    if not _validate_state():
        return redirect(client_config.base_url + '?error=invalid_state', 302)

    post_params = {
        'grant_type': 'interaction_code',
        'client_id': client_config.client_id,
        'client_secret': client_config.client_secret,
        'redirect_uri': client_config.interaction_redirect_uri,
        'interaction_code': request.args.get('interaction_code'),
        'state': request.args.get('state'),
        'code_verifier': session.get('code_verifier'),
    }
    data = api_request(client_config.token_uri, post_params)
    return _handle_token_response(data)


@app.route("/logout", methods=["POST"])
def logout():
    params = {'id_token_hint': session.get('id_token', '')}
    session['access_token'] = None
    logout_user()
    return redirect(client_config.base_url + 'logout?' + urllib.parse.urlencode(params))


# ── helpers ──────────────────────────────────────────────────────────────────

def _validate_state():
    req_state = request.args.get('state')
    return req_state is not None and session.get('state') == req_state


# Fix #6: shared helper eliminates duplicated token/user-creation logic
def _handle_token_response(data):
    id_token = data['id_token']
    # Fix #2: verify JWT signature against Okta JWKS instead of raw base64 decode
    user_info = _verify_and_decode_jwt(id_token, data['access_token'])

    session['user_id'] = user_info['sub']
    session['preferred_username'] = user_info['preferred_username']
    session['access_token'] = data['access_token']
    session['id_token'] = id_token
    session['user_info'] = user_info

    unique_id = user_info['sub']
    user_email = user_info['email']
    user_name = user_info.get('preferred_username', '')

    user = User(id_=unique_id, name=user_name, email=user_email)
    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)

    login_user(user)
    return redirect(url_for('profile'), 302)


def _verify_and_decode_jwt(token, access_token=None):
    """Fetch Okta's JWKS and verify the JWT signature before trusting any claims."""
    header = jwt.get_unverified_header(token)
    jwks = requests.get(client_config.base_url + 'keys', timeout=5).json()
    key = next((k for k in jwks['keys'] if k['kid'] == header['kid']), None)
    if key is None:
        raise JWTError('Signing key not found in JWKS')
    return jwt.decode(
        token,
        key,
        algorithms=['RS256'],
        audience=client_config.client_id,
        issuer=client_config.issuer,
        access_token=access_token,
    )


def validate_session():
    return session.get('access_token') is not None


# Fix #7: replaced pycurl with requests
def api_request(url, post=None, ssws=None):
    headers = {
        'Accept': 'application/json; okta-version=1.0.0',
        'User-Agent': 'https://example-app.com',
    }
    if ssws:
        headers['Authorization'] = 'SSWS ' + ssws
    elif session.get('access_token'):
        headers['Authorization'] = 'Bearer ' + session['access_token']

    if post:
        response = requests.post(url, data=post, headers=headers, timeout=10)
    else:
        response = requests.get(url, headers=headers, timeout=10)

    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    # Fix #4: debug mode controlled by env var, not hardcoded True
    debug = os.environ.get('FLASK_DEBUG', 'true').lower() == 'true'
    app.run(host="localhost", port=5000, debug=debug)
