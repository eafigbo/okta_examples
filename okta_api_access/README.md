
# Example for accessing APIs and protecting APIs with Okta. 
## Prerequisites

Before running these examples, see instructions in [okta_examples README](../README.md)



Now you need to gather the following information from the Okta Developer Console that belongs to your web application:
- **Client ID and Client Secret**  - The client ID and secret of the Web application that you created earlier. This identifies the application that tokens will be minted for.
- To test the API access with SSWS token, you will need to create one using the instructions [here](https://developer.okta.com/docs/guides/create-an-api-token/)
Copy the [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in the information you gathered as well as edit the other fields to suit your deployment scenario

```python
api_server_client_id = "xxxxx"
api_server_client_secret = "xxxxx"
api_server_token_introspection_uri = "https://dev-xxxx.okta.com/oauth2/default/v1/introspect"
api_server_issuer = "https://dev-xxxx.okta.com/oauth2/default"



okta_client_id = 'xxx'
okta_client_secret ='xxx'
okta_ssws_token = 'xxx'

authorize_url = 'https://dev-xxx.okta.com/oauth2/default/v1/authorize'

token_url = 'https://dev-xxx.okta.com/oauth2/default/v1/token'

api_url_base = 'https://dev-xxxx.okta.com/'

base_url = 'http://localhost:5000/'

resource_server_url = 'http://localhost:8000/'

user_info_url='https://dev-xxx.okta.com/oauth2/default/v1/userinfo'

```

run the server by typing:

``` bash
python3 okta_api_access.py 
```

run the client by typing:

``` bash
python3 okta_client.py 
```

Access the client application by going to : http://localhost:5000/
