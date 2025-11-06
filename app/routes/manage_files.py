import os
from fastapi import APIRouter, UploadFile, File
from app.utils import file_utils

router = APIRouter(tags=["File Management"])

@router.post("/upload-payload")
def upload_payload(file: UploadFile = File(...)):
    return file_utils.save_uploaded_payload(file)

@router.get("/payloads")
def list_payloads():
    return {"available_payloads": file_utils.list_payloads()}

@router.delete("/delete-payload/{name}")
def delete_payload(name: str):
    path = f"payloads/{name}"
    os.remove(path) if os.path.exists(path) else None
    return {"message": f"🗑️ Deleted {name} from payloads."}

@router.delete("/delete-response/{name}")
def delete_response(name: str):
    path = f"results/{name}"
    os.remove(path) if os.path.exists(path) else None
    return {"message": f"🗑️ Deleted {name} from results."}
