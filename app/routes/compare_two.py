import os
import json
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.auth import fetch_oauth_token
from app.utils.iflow_client import hit_iflow
from app.utils.file_utils import save_body, save_headers
from app.utils.compare_utils import compare_responses
 
PAYLOAD_DIR = "payloads"
router = APIRouter()
 
class CompareTwoRequest(BaseModel):
    token_url: str
    client_id: str
    client_secret: str
    url1: str
    url2: str
    payload_file: str  # ✅ filename instead of dict
 
 
@router.post("/two-urls")
def compare_two_urls(data: CompareTwoRequest):
 
    # ✅ Load payload file
    payload_path = os.path.join(PAYLOAD_DIR, data.payload_file)
    payload = json.load(open(payload_path, "r", encoding="utf-8"))
 
    token = fetch_oauth_token(data.token_url, data.client_id, data.client_secret)
 
    resp1, headers1 = hit_iflow(data.url1, token, payload)
    resp2, headers2 = hit_iflow(data.url2, token, payload)
 
    save_body(resp1, "two_url_resp1.json")
    save_body(resp2, "two_url_resp2.json")
    save_headers(headers1, "two_url_headers1.json")
    save_headers(headers2, "two_url_headers2.json")
 
    body_diff, header_diff = compare_responses(
        resp1, resp2, headers1, headers2, "two_url"
    )
 
    # ✅ Save diffs
    save_body(body_diff, "two_url_body_diff.json")
    save_body(header_diff, "two_url_headers_diff.json")
 
    return {
        "message": "Comparison completed ✅",
        "body_diff": body_diff,
        "headers_diff": header_diff
    }