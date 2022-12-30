
# Example for autheticating with Okta and accessing APIs using the OAuth for Okta functionality

## Prerequisites

Before running these examples, see instructions in [okta_examples README](../README.md)



Now you need to gather the following information from the Okta Developer Console that belongs to your web application:
- **Client ID and Client Secret**  - The client ID and secret of the Web application that you created earlier. This identifies the application that tokens will be minted for.

Copy the [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in the information you gathered as well as edit the other fields to suit your deployment scenario

```python
okta_client_id = 'xxx'
okta_client_secret ='xxx'

oauth_authorize_url = 'https://dev-xxx.okta.com/oauth2/v1/authorize'

oauth_access_token_url = 'https://dev-xxx.okta.com/oauth2/v1/token'

api_url_base = 'https://dev-xxx.okta.com/'

base_url = 'http://localhost:5000/'
```

run the sample by typing:

``` bash
python3 okta_o4o_client.py 
```
Access the application by going to : http://localhost:5000/
