import os
import sys
import json
from compare_utils import fetch_oauth_token, hit_iflow, save_response, compare_responses

print("🚀 Compare Two URLs using One Payload\n")

payload_file = input("Enter payload filename (e.g. payload.json): ").strip()
if not os.path.exists(payload_file):
    sys.exit(f"❌ {payload_file} not found.")

with open(payload_file, "r", encoding="utf-8") as f:
    payload_text = f.read().strip()

if not payload_text:
    sys.exit("❌ Payload is empty.")

old_url = input("Enter OLD iFlow URL: ").strip()
new_url = input("Enter NEW iFlow URL: ").strip()
if not old_url or not new_url:
    sys.exit("❌ Both URLs required.")

token = fetch_oauth_token()

print("\n📡 Hitting OLD URL...")
_, old_resp = hit_iflow(old_url, token, payload_text)
save_response(old_resp, "response_old.json")

print("\n📡 Hitting NEW URL...")
_, new_resp = hit_iflow(new_url, token, payload_text)
save_response(new_resp, "response_new.json")

print("\n🔍 Comparing responses...")
compare_responses(old_resp, new_resp, "two_url_one_payload")

print("\n✅ Done! Check results/ folder for details.")
