from fastapi import APIRouter, Form
from app.utils import auth, iflow_client, compare_utils, file_utils

router = APIRouter(prefix="/compare", tags=["Compare Two URLs"])

@router.post("/two-urls")
def compare_two_urls(
    token_url: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...),
    url1: str = Form(...),
    url2: str = Form(...),
    payload_file: str = Form(...)
):
    payload = file_utils.load_json(f"payloads/{payload_file}")
    token = auth.get_token(token_url, client_id, client_secret)
    
    resp1 = iflow_client.hit_iflow(url1, token, payload)
    resp2 = iflow_client.hit_iflow(url2, token, payload)

    diff = compare_utils.compare_json(resp1["body"], resp2["body"])
    diff_path = file_utils.save_diff_result(diff, "diff_two_urls.json")

    return {"result": "✅ Comparison done", "diff_path": diff_path}
