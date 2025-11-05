import os
import json
from compare_utils import fetch_oauth_token, hit_iflow, save_body, save_headers, compare_responses

def run():
    print("\n🔗 Compare Two URLs with One Payload\n")

    # Token details
    token_url = input("Enter OAuth Token URL: ").strip()
    client_id = input("Enter Client ID: ").strip()
    client_secret = input("Enter Client Secret: ").strip()

    url1 = input("Enter OLD iFlow URL: ").strip()
    url2 = input("Enter NEW iFlow URL: ").strip()

    # List all payloads available
    payload_dir = "payloads"
    payload_files = [f for f in os.listdir(payload_dir) if f.endswith(".json")]

    if not payload_files:
        print("❌ No payload files found in 'payloads' folder.")
        return

    print("\nAvailable payloads:")
    for i, file in enumerate(payload_files, 1):
        print(f"{i}. {file}")

    try:
        choice = int(input("\nEnter the number of the payload you want to use: "))
        payload_file = payload_files[choice - 1]
    except (ValueError, IndexError):
        print("❌ Invalid choice.")
        return

    with open(os.path.join(payload_dir, payload_file), "r", encoding="utf-8") as f:
        payload = json.load(f)

    # Fetch OAuth token
    token = fetch_oauth_token(token_url, client_id, client_secret)

    # Hit OLD iFlow
    print(f"\n📤 Sending payload '{payload_file}' to OLD iFlow...")
    resp1, headers1 = hit_iflow(url1, token, payload)
    save_body(resp1, "response1_body.json")
    save_headers(headers1, "response1_headers.json")

    # Hit NEW iFlow
    print(f"\n📤 Sending payload '{payload_file}' to NEW iFlow...")
    resp2, headers2 = hit_iflow(url2, token, payload)
    save_body(resp2, "response2_body.json")
    save_headers(headers2, "response2_headers.json")

    # Compare both
    compare_responses(resp1, resp2, headers1, headers2, "url1_vs_url2")

if __name__ == "__main__":
    run()
