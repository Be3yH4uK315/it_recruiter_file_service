from fastapi import APIRouter, UploadFile, File, HTTPException, status, Depends, Form
from sqlalchemy.orm import Session
from uuid import UUID
from app.services.storage import storage_service
from app import crud, schemas
from app.core.db import get_db
from app.core.config import RESUME_BUCKET_NAME, AVATAR_BUCKET_NAME

router = APIRouter()

@router.post("/upload", response_model=schemas.File)
async def upload_file(
        owner_telegram_id: int = Form(...),
        file_type: str = Form(...),
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    if file_type == "resume":
        bucket_name = RESUME_BUCKET_NAME
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    elif file_type == "avatar":
        bucket_name = AVATAR_BUCKET_NAME
        allowed_types = ["image/jpeg", "image/png"]
    else:
        raise HTTPException(status_code=400, detail="Invalid file_type.")

    if file.content_type not in allowed_types:
        raise HTTPException(status_code=415, detail="Unsupported file format.")

    file_data = await file.read()
    minio_metadata = storage_service.upload_file(
        file_data=file_data,
        filename=file.filename,
        content_type=file.content_type,
        bucket_name=bucket_name,
        path_prefix=bucket_name
    )

    bucket = minio_metadata.pop("bucket")
    db_file_data = {
        **minio_metadata,
        "bucket_name": bucket,
        "owner_telegram_id": owner_telegram_id,
    }
    db_file = crud.create_file_record(db, file_data=db_file_data)
    return db_file

@router.get("/{file_id}/download-url", response_model=schemas.DownloadLink)
def get_download_url_by_id(file_id: UUID, db: Session = Depends(get_db)):
    db_file = crud.get_file_record(db, file_id=file_id)
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")

    download_url = storage_service.get_download_url(
        bucket_name=db_file.bucket_name,
        object_key=db_file.object_key
    )
    return {"download_url": download_url}

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(
    file_id: UUID,
    owner_telegram_id: int,
    db: Session = Depends(get_db)
):
    db_file = crud.get_file_record(db, file_id=file_id)
    if not db_file:
        return

    if db_file.owner_telegram_id != owner_telegram_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this file.")

    try:
        storage_service.delete_file(
            bucket_name=db_file.bucket_name,
            object_key=db_file.object_key
        )
        crud.delete_file_record(db, file_id=file_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))