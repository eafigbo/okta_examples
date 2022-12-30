# okta_examples

This repository contains several quick and dirty examples built to test out various Okta use-cases using [Flask Python Framework](https://flask.palletsprojects.com/en/2.2.x/) application and Python 3.10.6.

It was inspired by the [Okta Flask Sample Applications](https://github.com/okta/samples-python-flask) and [OAuth 2.0 Simplified Book](https://oauth2simplified.com/) by [Aaron Parecki](https://github.com/aaronpk)

It consists of the following examples:

|Example                             |Description                 |
|------------------------------------|----------------------------|
|[oauth_4_okta](/oauth_4_okta)       |Tests autheticating with Okta and accessing APIs using the Oauth for Okta functionality|  
|[okta_api_access](/okta_api_access)   |An example for accessing and protecting APIs with Okta. Contains an client that accesses authenticates with Okta and access a dummy API Resource Server that is protected by Okta, can be used to test API Access protection with Okta|
|[okta_api_integration](/okta_api_integration)| An example for Okta's API Service Integrations that allow you access Okta APIs using a service account|
|[okta_widget_login](/okta_widget_login)| An example that tests adding authentication to your web app using the Okta's widget in redirect mode or embeded mode. This also tests the new propriety Interaction code flow| 

## Prerequisites

Before running these examples, you will need the following:

* An Okta Developer Account, you can sign up for one at https://developer.okta.com/signup/.
* At least one Okta Application, configured for Web mode. This is done from the Okta Developer Console and you can find instructions [here](https://help.okta.com/en-us/Content/Topics/Apps/Apps_App_Integration_Wizard_OIDC.htm).  
* Your okta dev org URL (looks something like this: https://dev-xxx.okta.com/

## Running These Examples
To run these examples, you first need to clone this repo and then enter into this directory:

```bash
git clone git@github.com:eafigbo/okta_examples.git
cd okta_examples
```

Then install dependencies:

```bash
pip install -r requirements.txt
```
Follow the instructions in each project's README to run each example
