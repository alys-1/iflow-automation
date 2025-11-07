from fastapi import APIRouter, Form
from app.utils import auth, iflow_client, file_utils, compare_utils

router = APIRouter(prefix="/compare", tags=["Compare Multi Payloads"])

@router.post("/one-url-multi-payloads")
def compare_one_url_multi_payloads(
    token_url: str = Form(...),
    client_id: str = Form(...),
    client_secret: str = Form(...),
    url: str = Form(...)
):
    token = auth.get_token(token_url, client_id, client_secret)
    payloads = file_utils.list_payloads()
    responses = []

    for file in payloads:
        payload = file_utils.load_json(f"payloads/{file}")
        resp = iflow_client.hit_iflow(url, token, payload)

        # Save body and headers separately
        body_path = file_utils.save_body(file, resp["body"])
        header_path = file_utils.save_headers(file, resp["headers"])

        responses.append({
            "file": file,
            "status": resp["status"],
            "body_path": body_path,
            "header_path": header_path
        })

    return {"responses": responses}


@router.post("/multi-payloads")
def compare_multi_payload_responses(
    response1_body: str = Form(...),
    response2_body: str = Form(...),
    response1_headers: str = Form(...),
    response2_headers: str = Form(...)
):
    # Load responses
    body1 = file_utils.load_json(f"results/{response1_body}")
    body2 = file_utils.load_json(f"results/{response2_body}")
    headers1 = file_utils.load_json(f"results/{response1_headers}")
    headers2 = file_utils.load_json(f"results/{response2_headers}")

    # Compare separately
    diff_body = compare_utils.compare_json(body1, body2)
    diff_headers = compare_utils.compare_json(headers1, headers2)

    # Save separately
    diff_body_path = file_utils.save_diff_result(diff_body, f"diff_body_{response1_body}_vs_{response2_body}")
    diff_header_path = file_utils.save_diff_result(diff_headers, f"diff_headers_{response1_headers}_vs_{response2_headers}")

    return {
        "result": "✅ Comparison completed successfully",
        "diff_body_path": diff_body_path,
        "diff_header_path": diff_header_path
    }
