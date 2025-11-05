import os
import sys
from compare_utils import fetch_oauth_token, hit_iflow, save_body, save_headers, compare_responses

RESULTS_DIR = "results"
PAYLOADS_DIR = "payloads"
os.makedirs(RESULTS_DIR, exist_ok=True)

def run():
    print("\n=== 📦 One URL, Multiple Payloads Mode ===\n")

    if not os.path.exists(PAYLOADS_DIR):
        sys.exit("❌ 'payloads' folder not found.")

    payload_files = [f for f in os.listdir(PAYLOADS_DIR) if f.endswith(".json")]
    if not payload_files:
        sys.exit("❌ No .json payload files found in 'payloads' folder.")

    print(f"🔍 Found {len(payload_files)} payload(s): {payload_files}")

    url = input("Enter iFlow endpoint URL: ").strip()
    if not url:
        sys.exit("❌ URL is required.")

    token = fetch_oauth_token()

    responses = []
    headers_list = []

    for i, payload_file in enumerate(payload_files, start=1):
        with open(os.path.join(PAYLOADS_DIR, payload_file), "r", encoding="utf-8") as f:
            payload_text = f.read().strip()

        print(f"\n📤 Sending payload {i}: {payload_file}")
        status, resp_text, resp_headers = hit_iflow(url, token, payload_text)

        save_body(resp_text, f"response{i}_body.json")
        save_headers(resp_headers, f"response{i}_headers.json")

        responses.append(resp_text)
        headers_list.append(resp_headers)

    if len(responses) < 2:
        print("\n⚠️ Only one response available. Nothing to compare.")
        return

    print("\n🧮 You can now compare two responses.")
    for i in range(1, len(responses) + 1):
        print(f"{i}. response{i}")

    try:
        r1 = int(input("\nEnter first response number to compare: "))
        r2 = int(input("Enter second response number to compare: "))
        if r1 == r2:
            print("❌ Cannot compare the same responses.")
            return
    except ValueError:
        print("❌ Invalid input.")
        return

    prefix = f"response{r1}_vs_response{r2}"
    compare_responses(responses[r1 - 1], responses[r2 - 1], headers_list[r1 - 1], headers_list[r2 - 1], prefix)
    print("\n✅ Comparison complete!")

if __name__ == "__main__":
    run()
