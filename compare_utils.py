import os
import sys
import json
import requests
from deepdiff import DeepDiff

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

# -------------------- FETCH TOKEN --------------------
def fetch_oauth_token():
    print("\n🔐 Enter OAuth credentials:")
    token_url = input("Token URL: ").strip()
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    if not all([token_url, client_id, client_secret]):
        sys.exit("❌ Missing credentials. Please enter all fields.")

    print("\n🔄 Fetching token...")
    resp = requests.post(
        token_url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret)
    )
    if resp.status_code != 200:
        sys.exit(f"❌ Token fetch failed: {resp.text}")
    token = resp.json().get("access_token")
    if not token:
        sys.exit("❌ No access_token found in token response.")
    print("✅ Token fetched successfully.\n")
    return token

# -------------------- HIT IFLOW --------------------
def hit_iflow(url, token, payload_text):
    try:
        resp = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            data=payload_text
        )
        return resp.status_code, resp.text
    except Exception as e:
        return 0, str(e)

# -------------------- SAVE RESPONSE --------------------
def save_response(content, filename):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"💾 Saved → {path}")

# -------------------- COMPARE RESPONSES --------------------
def compare_responses(resp1, resp2, output_prefix):
    try:
        diff = DeepDiff(json.loads(resp1), json.loads(resp2), ignore_order=True)
    except json.JSONDecodeError:
        sys.exit("❌ Responses are not valid JSON.")
    diff_path = os.path.join(RESULTS_DIR, f"{output_prefix}_diff.json")
    with open(diff_path, "w", encoding="utf-8") as f:
        f.write(diff.to_json(indent=2))
    print(f"📊 Diff saved → {diff_path}")
