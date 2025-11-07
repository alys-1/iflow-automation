import requests

def get_token(token_url, client_id, client_secret):
    res = requests.post(token_url, data={
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials"
    })
    res.raise_for_status()
    return res.json().get("access_token")
