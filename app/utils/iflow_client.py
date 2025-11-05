import requests

def hit_iflow(url, token, payload):
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    resp = requests.post(url, headers=headers, json=payload)

    try:
        body = resp.json()
    except:
        body = resp.text  # HTML, plain text, XML, etc.

    return body, dict(resp.headers)
