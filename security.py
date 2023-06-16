import streamlit as st
import msal
import requests

# Replace with your own values
CLIENT_ID = '3d34e365-cc0c-4dc7-b58a-a45f3c7abdfd'
CLIENT_SECRET = 'bbd8Q~sxSj3tLsVhB2lsATrRMnZs5tzgRQeEtax8' 
TENANT_ID = '0f374f33-0698-4656-9665-4ad2a74e580a'

AUTHORITY = 'https://login.microsoftonline.com/0f374f33-0698-4656-9665-4ad2a74e580a'
SCOPE = ['user.read']
REDIRECT_URI = 'https://inteldash.onrender.com'


app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)


def get_auth_url():
    auth_url = app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return auth_url


def get_token_from_code(auth_code):
    app = msal.ConfidentialClientApplication(CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET)
    result = app.acquire_token_by_authorization_code(auth_code, scopes=SCOPE, redirect_uri=REDIRECT_URI)
    return result['access_token']


def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    return response.json()


def handle_redirect():
    if not st.session_state.get('access_token'):
        code = st.experimental_get_query_params().get('code')
        if code:
            access_token = get_token_from_code(code)
            st.session_state['access_token'] = access_token
            st.experimental_set_query_params()