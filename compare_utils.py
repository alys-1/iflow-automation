import os
import json
import requests
from deepdiff import DeepDiff

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# =================== AUTH ===================
def fetch_oauth_token(token_url, client_id, client_secret):
    """Fetch OAuth token for authentication."""
    print("🔐 Fetching OAuth token...")
    response = requests.post(
        token_url,
        data={'grant_type': 'client_credentials'},
        auth=(client_id, client_secret)
    )
    response.raise_for_status()
    token = response.json().get("access_token")
    print("✅ Token fetched successfully!")
    return token

# =================== API CALL ===================
def hit_iflow(url, token, payload):
    """Send request to iFlow and return response body and headers."""
    print(f"📤 Sending request to {url} ...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "*/*"
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    try:
        body = response.json()
    except ValueError:
        body = response.text

    return body, dict(response.headers)

# =================== SAVE FUNCTIONS ===================
def save_body(data, filename):
    """Save body to results folder."""
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(data, (dict, list)):
            json.dump(data, f, indent=2, ensure_ascii=False)
        else:
            f.write(data)
    print(f"💾 Saved body → {path}")
    return path

def save_headers(headers, filename):
    """Save headers to results folder."""
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(headers, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved headers → {path}")
    return path

# =================== COMPARE FUNCTIONS ===================
def compare_json(obj1, obj2):
    diff = DeepDiff(obj1, obj2, ignore_order=True)
    return json.loads(diff.to_json())

def compare_text(text1, text2):
    set1, set2 = set(text1.splitlines()), set(text2.splitlines())
    return {
        "only_in_first": list(set1 - set2),
        "only_in_second": list(set2 - set1)
    }

def compare_responses(resp1, resp2, headers1, headers2, tag="comparison"):
    """Compare response bodies and headers, supports both text and JSON."""
    print("🔍 Comparing both responses and headers...")

    # Compare bodies
    if isinstance(resp1, (dict, list)) and isinstance(resp2, (dict, list)):
        diff_body = compare_json(resp1, resp2)
    else:
        diff_body = compare_text(str(resp1), str(resp2))

    # Compare headers
    diff_headers = compare_json(headers1, headers2)

    # Save results
    body_diff_path = os.path.join(RESULTS_DIR, f"{tag}_body_diff.json")
    headers_diff_path = os.path.join(RESULTS_DIR, f"{tag}_headers_diff.json")

    with open(body_diff_path, "w", encoding="utf-8") as f:
        json.dump(diff_body, f, indent=2, ensure_ascii=False)

    with open(headers_diff_path, "w", encoding="utf-8") as f:
        json.dump(diff_headers, f, indent=2, ensure_ascii=False)

    print(f"✅ Differences saved:\n  - {body_diff_path}\n  - {headers_diff_path}")
