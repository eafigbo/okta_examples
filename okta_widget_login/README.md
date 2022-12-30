
# Example that tests adding authentication to your web app using the Okta widget in redirect mode or embeded mode. This also tests the new propriety Interaction code flow

## Prerequisites

Before running these examples, see instructions in [okta_examples README](../README.md)



Now you need to gather the following information from the Okta Developer Console that belongs to your web application:
- **Client ID and Client Secret**  - The client ID and secret of the Web application that you created earlier. This identifies the application that tokens will be minted for.
- To test the Interaction Code flow with Okta Identity Engine, you need to configure your org to support interaction code flow. See the instructions [here](https://developer.okta.com/docs/guides/implement-grant-type/interactioncode/main/#verify-that-the-interaction-code-grant-type-is-enabled)

Copy the [`client_config.py.dist`](client_config.py.dist) to `client_config.py` and fill in the information you gathered as well as edit the other fields to suit your deployment scenario

```python
auth_uri = "https://dev-xxx.okta.com/oauth2/default/v1/authorize"
client_id = "xxx"
client_secret = "xxx"
redirect_uri= "http://localhost:5000/authorization-code/callback"
interaction_redirect_uri= "http://localhost:5000/interaction-code/callback"
issuer = "https://dev-xxx.okta.com/oauth2/default"
token_uri = "https://dev-xxx.okta.com/oauth2/default/v1/token"
idx_token_uri = "https://dev-xxx.okta.com/idp/idx/token"
token_introspection_uri = "https://dev-xxx.okta.com/oauth2/default/v1/introspect"
userinfo_uri = "https://dev-xxx.okta.com/oauth2/default/v1/userinfo"
base_url = "https://dev-xxx.okta.com/oauth2/default/v1/"
```

run the sample by typing:

``` bash
python3 hosted_main.py 
```
Access the application by going to : http://localhost:5000/
