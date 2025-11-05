import os
import json
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.auth import fetch_oauth_token
from app.utils.iflow_client import hit_iflow

router = APIRouter()

PAYLOAD_DIR = "payloads"
RESULTS_DIR = "results"

class CompareMultiRequest(BaseModel):
    token_url: str
    client_id: str
    client_secret: str
    url: str


@router.post("/multi")
def compare_multi(data: CompareMultiRequest):

    # Fetch OAuth token
    token = fetch_oauth_token(data.token_url, data.client_id, data.client_secret)

    # Get all payload JSON files
    payload_files = [f for f in os.listdir(PAYLOAD_DIR) if f.endswith(".json")]
    if not payload_files:
        return {"error": "No payload files found in payloads/"}

    saved_files = []

    # Loop through payload files
    for i, payload_file in enumerate(payload_files, 1):
        payload_path = os.path.join(PAYLOAD_DIR, payload_file)
        payload = json.load(open(payload_path, "r", encoding="utf-8"))

        # Hit CPI
        body, headers = hit_iflow(data.url, token, payload)

        # ✅ Save body + headers TOGETHER in one file
        final_data = {
            "payload_file": payload_file,
            "body": body,
            "headers": headers
        }

        save_path = os.path.join(RESULTS_DIR, f"multi_resp_{i}.json")

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=2, ensure_ascii=False)

        saved_files.append(save_path)

    return {
        "message": "All responses saved ✅",
        "saved_files": saved_files
    }
