
# Example for adding authentication using the Okta Sign-In Widget

This example demonstrates two login modes in a single Flask app:

- **Redirect mode** (`/login`) — redirects the user to Okta's hosted login page using the standard OIDC Authorization Code flow
- **Embedded widget mode** (`/widget`) — renders the Okta Sign-In Widget directly in the page using the Interaction Code flow with PKCE

## Prerequisites

Before running this example, see instructions in [okta_examples README](../README.md)

You will need an Okta **Web (OIDC)** application with the following redirect URIs registered:

- `http://localhost:5000/authorization-code/callback` — used by redirect mode
- `http://localhost:5000/interaction-code/callback` — used by embedded widget mode

To add these, go to **Okta Admin Console → Applications → your app → General → Sign-in redirect URIs**.

## Interaction Code Flow Setup (widget mode only)

The embedded widget uses the Interaction Code flow, which requires Okta Identity Engine (OIE). To enable it, follow the instructions [here](https://developer.okta.com/docs/guides/implement-grant-type/interactioncode/main/#verify-that-the-interaction-code-grant-type-is-enabled).

This step is only required if you plan to use the `/widget` route. The standard `/login` redirect flow works without it.

## Configuration

Copy [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in your values:

```python
auth_uri = "https://dev-xxx.okta.com/oauth2/default/v1/authorize"
client_id = "xxx"
client_secret = "xxx"
redirect_uri = "http://localhost:5000/authorization-code/callback"
interaction_redirect_uri = "http://localhost:5000/interaction-code/callback"
issuer = "https://dev-xxx.okta.com/oauth2/default"
token_uri = "https://dev-xxx.okta.com/oauth2/default/v1/token"
idx_token_uri = "https://dev-xxx.okta.com/idp/idx/token"
token_introspection_uri = "https://dev-xxx.okta.com/oauth2/default/v1/introspect"
userinfo_uri = "https://dev-xxx.okta.com/oauth2/default/v1/userinfo"
base_url = "https://dev-xxx.okta.com/oauth2/default/v1/"
```

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `FLASK_SECRET_KEY` | Recommended | Secret key for Flask session signing. If not set, a random key is generated on each restart, invalidating all existing sessions. |
| `FLASK_DEBUG` | Optional | Set to `false` to disable debug mode. Defaults to `true`. |

Set them before running:

```bash
export FLASK_SECRET_KEY="your-secret-key-here"
export FLASK_DEBUG=false  # for production
```

## Running

```bash
python3 hosted_main.py
```

Access the application at: http://localhost:5000/

- Click **Log In** on the home page to use the hosted redirect flow
- Navigate to `/widget` to use the embedded Sign-In Widget
