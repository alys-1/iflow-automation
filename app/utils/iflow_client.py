import requests

def hit_iflow(url, token, payload):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return {"status": response.status_code, "body": response.json(), "headers": dict(response.headers)}
