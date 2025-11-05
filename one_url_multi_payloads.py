import os
import sys
from compare_utils import fetch_oauth_token, hit_iflow, save_response, compare_responses

PAYLOAD_DIR = "payloads"
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

print("🚀 Single URL - Multiple Payloads Mode\n")

url = input("Enter iFlow URL: ").strip()
if not url:
    sys.exit("❌ URL required.")

token = fetch_oauth_token()

if not os.path.exists(PAYLOAD_DIR):
    sys.exit(f"❌ Folder '{PAYLOAD_DIR}' not found.")

payload_files = [f for f in os.listdir(PAYLOAD_DIR) if f.endswith(".json")]
if not payload_files:
    sys.exit("❌ No payloads found in payloads/")

response_files = []

for idx, file in enumerate(payload_files, 1):
    print(f"\n📤 Sending payload {idx}: {file}")
    with open(os.path.join(PAYLOAD_DIR, file), "r", encoding="utf-8") as f:
        payload_text = f.read().strip()
    if not payload_text:
        print(f"⚠️ Skipping empty file: {file}")
        continue

    _, resp = hit_iflow(url, token, payload_text)
    filename = f"response_{idx}.json"
    save_response(resp, filename)
    response_files.append(filename)

# -------- Compare selected responses --------
if len(response_files) < 2:
    sys.exit("⚠️ Not enough responses to compare.")

print("\n📊 Available responses:")
for i, f in enumerate(response_files, 1):
    print(f"{i}. {f}")

try:
    a = int(input("\nEnter first response number to compare: "))
    b = int(input("Enter second response number to compare: "))
    if a < 1 or b < 1 or a > len(response_files) or b > len(response_files):
        raise ValueError
except ValueError:
    sys.exit("❌ Invalid selection.")

with open(os.path.join(RESULTS_DIR, response_files[a - 1]), "r", encoding="utf-8") as f1, \
     open(os.path.join(RESULTS_DIR, response_files[b - 1]), "r", encoding="utf-8") as f2:
    resp1, resp2 = f1.read(), f2.read()

compare_responses(resp1, resp2, f"compare_{a}_vs_{b}")

print("\n✅ Done! Check results/ for comparison output.")
