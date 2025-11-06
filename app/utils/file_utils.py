import os, json
from fastapi import UploadFile

def ensure_dirs():
    os.makedirs("payloads", exist_ok=True)
    os.makedirs("results", exist_ok=True)

def list_payloads():
    ensure_dirs()
    return [f for f in os.listdir("payloads") if f.endswith(".json")]

def list_results():
    ensure_dirs()
    return [f for f in os.listdir("results") if f.endswith(".json")]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_body(filename, body):
    ensure_dirs()
    path = f"results/{filename.replace('.json','')}_body.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(body, f, indent=2)
    return path

def save_headers(filename, headers):
    ensure_dirs()
    path = f"results/{filename.replace('.json','')}_headers.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(dict(headers), f, indent=2)
    return path

def save_diff_result(diff, name):
    ensure_dirs()
    path = f"results/{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(diff, f, indent=2)
    return path

def save_uploaded_payload(file: UploadFile):
    ensure_dirs()
    path = f"payloads/{file.filename}"
    with open(path, "wb") as f:
        f.write(file.file.read())
    return {"message": "✅ Payload uploaded successfully", "path": path}
