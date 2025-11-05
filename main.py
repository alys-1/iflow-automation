import sys
import importlib

def main():
    print("🚀 CPI Compare Automation Tool\n")
    print("Select mode:")
    print("1️⃣  Compare two URLs with one payload")
    print("2️⃣  Compare one URL with multiple payloads")

    choice = input("\nEnter your choice (1 or 2): ").strip()

    if choice == "1":
        module = importlib.import_module("two_url_one_payload")
        module.run()
    elif choice == "2":
        module = importlib.import_module("one_url_multi_payloads")
        module.run()
    else:
        sys.exit("❌ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
