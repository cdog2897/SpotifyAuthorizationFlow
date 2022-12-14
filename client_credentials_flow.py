# code by Caleb Wolin
# 11/03/2022

import base64
import requests
import datetime
from urllib.parse import urlencode

'''
AUTHORIZATION PROCESS for client crediential flow:
1. request access token
2. get access token from Spotify accounts service
3. use access token in Web API
'''

# codes:

client_id = "7e6c2c2025664df0acf25c227538d454"
client_secret = "d89300aaa95941a29252c300bdac0c2a"
redirect_uri = "https://example.com/callback/"


# authorization object to be used dynamically
class SpotifyAPI():
    # key codes
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    # constructor
    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret


    # get data= information
    def get_token_data(self):
        return  {
                    "grant_type": "client_credentials"
        }

    # return a base64 encoded string
    def get_client_credentials(self):
        '''
        returns a base64 encoded string
        '''
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("You must set a client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    # get headers= information
    def get_token_header(self):
        client_creds_b64 = self.get_client_credentials()
        return  {
            "Authorization": f"Basic {client_creds_b64}"
        }

    # get access token
    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()

        client_creds_b64 = self.get_client_credentials()
        token_header = self.get_token_header()
        r = requests.post(token_url, data=token_data, headers=token_header)
        if r.status_code not in range(200, 299):
            return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        self.access_token = access_token
        expires_in = data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

# testing
spotify = SpotifyAPI(client_id, client_secret)
spotify.perform_auth()
access_token = spotify.access_token
headers = {
    "Authorization": f"Bearer {access_token}"
}
endpoint = "https://api.spotify.com/v1/search"
data = urlencode({"q": "Time", "type": "track"})
lookup_url = f"{endpoint}?{data}"
r = requests.get(lookup_url, headers=headers)
print(r.json())








