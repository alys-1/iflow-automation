import requests

def fetch_oauth_token(token_url, client_id, client_secret):
    print("🔐 Fetching OAuth token...")

    resp = requests.post(
        token_url,
        data={'grant_type': 'client_credentials'},
        auth=(client_id, client_secret)
    )
    resp.raise_for_status()

    token = resp.json().get("access_token")
    if not token:
        raise Exception("❌ No access_token received from server")

    return token
