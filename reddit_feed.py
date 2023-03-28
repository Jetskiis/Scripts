import os

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
# oauth
client_id, client_key = os.getenv("CLIENT_ID"), os.getenv("SECRET_KEY")
auth = requests.auth.HTTPBasicAuth(client_id, client_key)

data = {
    'grant_type': 'password',
    'username': os.getenv("USERNAME"),
    'password': os.getenv("PASSWORD"),
}

headers = {'User-Agent': 'MyBot/0.0.1'}

res = requests.post("https://www.reddit.com/api/v1/access_token",
                    auth=auth, data=data, headers=headers)

token = res.json()['access_token']
headers["Authorization"] = f"bearer {token}"
res = requests.get("https://oauth.reddit.com/api/v1/me",
                   headers=headers).json()
