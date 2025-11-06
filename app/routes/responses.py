from fastapi import APIRouter, Form
from fastapi.responses import FileResponse
from app.utils import file_utils, compare_utils

router = APIRouter(prefix="/responses", tags=["Responses"])

@router.get("/")
def list_responses():
    return {"responses": file_utils.list_results()}



@router.get("/download/{filename}")
def download_file(filename: str):
    file_path = f"results/{filename}"
    return FileResponse(file_path, media_type="application/json", filename=filename)
