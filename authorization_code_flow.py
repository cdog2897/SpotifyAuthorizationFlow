# code by Caleb Wolin
# 11/03/2022

import base64
import requests
import datetime
from urllib.parse import urlencode
from urllib.parse import urlparse
import webbrowser
import os

'''
AUTHORIZATION PROCESS for authorization code flow:
1. request authorization to access data
2. prompt user to login
3. request access token and refresh token
4. return tokens
5. use tokens
6. refresh tokens using previous refresh tokens
'''

# key codes
client_id = "7e6c2c2025664df0acf25c227538d454"
client_secret = "d89300aaa95941a29252c300bdac0c2a"
redirect_uri = "https://example.com/callback/"
token_url = "https://accounts.spotify.com/api/token"


# authorization object to be used dynamically
class SpotifyAPI():
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    refresh_token = None

    #constructor
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    '''
        Authorize user... Return code.
    '''
    def get_auth_data(self):
        return  {
                    "client_id": client_id,
                    "response_type": "code",
                    "redirect_uri": "https://example.com/callback/",
                    "scope": "user-read-private"
        }

    # login prompt, COPY CODE FROM URL FOR NEXT STEP
    def perform_auth(self):
        token_data = self.get_auth_data()
        token_url = "https://accounts.spotify.com/authorize"
        webbrowser.open(f"{token_url}/?{urlencode(token_data)}")
        # access_token = data['access_token']
        # self.access_token = access_token
    
    '''
        Request access tokens
    '''
    # get data= information
    def get_token_data(self):
        code = ""   # code from url goes here
        return {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri
        }

    def get_access_token(self):
        token_data = self.get_token_data()
        headers = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=headers)
        data = r.json()
        print(data)
        self.refresh_token = data['refresh_token']
        print(data)


    '''
    refresh tokens
    '''
    def get_refresh_token(self):
        headers = self.get_token_header()
        refresh_token = self.refresh_token
        r = requests.post(token_url,
                            data = {
                                "grant_type": "refresh_token",
                                "refresh_token": refresh_token
                            },
                            headers=headers)
        data = r.json()
        print(data)
        self.access_token = data['access_token']


    """
    helper functions
    """
    def get_client_credentials(self):
        # returns a base64 encoded string
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("You must set a client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()


    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return  {
            "Authorization": f"Basic {client_creds_b64}"
        }


# testing
spotify = SpotifyAPI(client_id, client_secret)
#spotify.perform_auth()
#spotify.get_access_token()
#spotify.get_refresh_token()











