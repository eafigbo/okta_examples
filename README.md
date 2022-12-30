# okta_examples

This repository contains several quick and dirty examples built to test out various Okta use-cases using [Flask Python Framework](https://flask.palletsprojects.com/en/2.2.x/) application and Python 3.10.6.

It was inspired by the [Okta Flask Sample Applications](https://github.com/okta/samples-python-flask) and [OAuth 2.0 Simplified Book](https://oauth2simplified.com/) by [Aaron Parecki](https://github.com/aaronpk)

It consists of the following examples:

|Example                             |Description                 |
|------------------------------------|----------------------------|
|[oauth_4_okta](/oauth_4_okta)       |Tests autheticating with Okta and accessing APIs using the Oauth for Okta functionality|  
|[okta_api_access](/okta_api_access)   |An example for accessing and protecting APIs with Okta. Contains an client that accesses authenticates with Okta and access a dummy API Resource Server that is protected by Okta, can be used to test API Access protection with Okta|
|[okta_api_integration](/okta_api_integration)| An example for Okta's API Service Integrations that allow you access Okta APIs using a service account|
|[okta_widget_login](/okta_widget_login)| An example that tests the use of Okta's widget to add authentication to your web app using the widget in redirect mode or embeded mode. This also tests the new propriety Interaction code flow| 
