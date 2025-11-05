import os
import json

RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

def save_body(body, filename):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        if isinstance(body, (dict, list)):
            json.dump(body, f, indent=2, ensure_ascii=False)
        else:
            f.write(body)
    return path

def save_headers(headers, filename):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(headers, f, indent=2, ensure_ascii=False)
    return path
