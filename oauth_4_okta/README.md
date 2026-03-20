
# Example for authenticating with Okta and accessing APIs using the OAuth for Okta functionality

## Prerequisites

Before running these examples, see instructions in [okta_examples README](../README.md)

You will need an Okta **Web (OIDC)** application — not a Service application. Service applications use the Client Credentials flow and cannot access the `/authorize` endpoint.

Now you need to gather the following information from the Okta Developer Console that belongs to your web application:
- **Client ID and Client Secret** - The client ID and secret of the Web application that you created earlier. This identifies the application that tokens will be minted for.

## Okta API Scopes

This example uses OAuth for Okta scopes to call the Okta `/api/v1/users` endpoint. These scopes must be explicitly granted to your application:

1. Go to **Okta Admin Console → Applications → your app → Okta API Scopes**
2. Grant the following scopes:
   - `okta.users.read` — to list users
   - `okta.users.manage` — to manage users

> **Important:** OAuth for Okta scopes only work with the **Org Authorization Server** (`/oauth2/v1/`). Do not use a custom authorization server (e.g. `/oauth2/default/`) for these scopes.

## Configuration

Copy the [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in the information you gathered as well as edit the other fields to suit your deployment scenario

```python
okta_client_id = 'xxx'
okta_client_secret = 'xxx'

oauth_authorize_url = 'https://dev-xxx.okta.com/oauth2/v1/authorize'

oauth_access_token_url = 'https://dev-xxx.okta.com/oauth2/v1/token'

user_info_url = 'https://dev-xxx.okta.com/oauth2/v1/userinfo'

api_url_base = 'https://dev-xxx.okta.com/'

base_url = 'http://localhost:5000/'
```

## Running

Run the sample by typing:

```bash
python3 okta_o4o_client.py
```

Access the application by going to: http://localhost:5000/
