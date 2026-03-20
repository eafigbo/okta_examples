
# Example for Okta's API Service Integrations

This example demonstrates accessing Okta APIs using a **Service** (machine-to-machine) application with the **Client Credentials** flow and **Private Key JWT** authentication. It retrieves an access token without any user interaction and uses it to call the Okta `/api/v1/users` endpoint.

## Prerequisites

Before running this example, see instructions in [okta_examples README](../README.md)

## Okta App Setup

This example requires an Okta **API Services** (Service) application — not a Web application.

1. Go to **Okta Admin Console → Applications → Create App Integration**
2. Choose **API Services**
3. Note the **Client ID**

## Key Pair Setup

This example uses Private Key JWT for authentication. You need to generate an RSA key pair and register the public key with Okta.

Generate a key pair:

```bash
openssl genrsa -out private_key.pem 2048
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

Register the public key with Okta:

1. Go to your app in the Okta Admin Console → **General** tab
2. Under **Client Credentials**, click **Edit** and select **Public key / Private key**
3. Click **Add key**, paste the contents of `public_key.pem`, and save
4. Note the **Key ID (kid)** shown after saving

## Okta API Scopes

The following scopes must be granted to your app:

1. Go to **Okta Admin Console → Applications → your app → Okta API Scopes**
2. Grant:
   - `okta.users.read`
   - `okta.groups.read`

## Configuration

Copy [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in your values:

```python
okta_client_id = 'xxxx'

private_key_path = '/path/to/your/private_key.pem'

okta_kid = 'xxxx'  # Key ID from the public key registered in Okta

token_url = 'https://dev-xxx.okta.com/oauth2/v1/token'  # Org Authorization Server

api_url_base = 'https://dev-xxx.okta.com/'
```

> **Note:** Use the **Org Authorization Server** (`/oauth2/v1/token`) — not a custom authorization server. Okta API scopes like `okta.users.read` are only available on the Org AS.

## Running

```bash
python3 okta_api_integration_client.py
```

The script prints the list of users returned from the Okta `/api/v1/users` endpoint.
