import json
import os
from fastapi import APIRouter
from pydantic import BaseModel
from app.utils.compare_utils import compare_responses
from app.utils.file_utils import save_body

router = APIRouter()
RESULTS_DIR = "results"

class CompareSavedRequest(BaseModel):
    file1: str
    file2: str


@router.get("/list")
def list_responses():
    files = [f for f in os.listdir(RESULTS_DIR) if f.startswith("multi_resp")]
    return {"files": files}


@router.post("/compare-saved")
def compare_saved(data: CompareSavedRequest):

    path1 = os.path.join(RESULTS_DIR, data.file1)
    path2 = os.path.join(RESULTS_DIR, data.file2)

    # Load two saved response files
    f1 = json.load(open(path1, "r"))
    f2 = json.load(open(path2, "r"))

    body1, headers1 = f1["body"], f1["headers"]
    body2, headers2 = f2["body"], f2["headers"]

    # ✅ Compare body + headers separately
    body_diff, header_diff = compare_responses(
        body1, body2, headers1, headers2,
        f"{data.file1}_vs_{data.file2}"
    )

    # ✅ Save diff files
    body_diff_file = f"body_diff_{data.file1}_vs_{data.file2}.json"
    header_diff_file = f"header_diff_{data.file1}_vs_{data.file2}.json"

    save_body(body_diff, body_diff_file)
    save_body(header_diff, header_diff_file)

    return {
        "message": "Comparison completed ✅",
        "body_diff_file": body_diff_file,
        "header_diff_file": header_diff_file,
        "body_diff": body_diff,
        "headers_diff": header_diff
    }
