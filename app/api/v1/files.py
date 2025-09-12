from fastapi import APIRouter, UploadFile, File, HTTPException, status, Query
from app.services.storage import storage_service

router = APIRouter()

@router.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail="Unsupported file type.")

    try:
        file_data = await file.read()
        metadata = storage_service.upload_file(
            file_data=file_data,
            filename=file.filename,
            content_type=file.content_type
        )
        return metadata
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/download-url")
def get_download_url_for_object(object_key: str = Query(..., min_length=1)):
    try:
        download_url = storage_service.get_download_url(object_key)
        return {"download_url": download_url}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))