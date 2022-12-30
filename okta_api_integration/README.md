
# An example for Okta's API Service Integrations that allow you access Okta APIs using a service account

## Prerequisites

Before running these examples, see instructions in [okta_examples README](../README.md)



Now you need to gather the following information from the Okta Developer Console that belongs to your web application:
- **Client ID and Client Secret**  - The client ID and secret of the Web application that you created earlier. This identifies the application that tokens will be minted for.
- Enable/Configure your org to support the new API Service Integrations by following the instructions [here](https://developer.okta.com/docs/guides/build-api-integration/main/)


Copy the [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in the information you gathered as well as edit the other fields to suit your deployment scenario

```python
okta_client_id = 'xxxx'

okta_api_integration_secret = 'xxx-xxx-xxx' # this should be your client secret

authorize_url = 'https://dev-xxx.okta.com/oauth2/default/v1/authorize'

token_url = 'https://dev-xxx.okta.com/oauth2/default/v1/token'

api_url_base = 'https://dev-xxx.okta.com/'

base_url = 'http://localhost:5000/'
```

run the sample by typing:

``` bash
python3 okta_api_integration_client.py 
```
