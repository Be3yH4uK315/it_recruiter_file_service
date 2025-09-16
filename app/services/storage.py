import uuid
from datetime import timedelta
from minio import Minio
from minio.error import S3Error
from io import BytesIO
from app.core.config import (
    MINIO_ENDPOINT, MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY, RESUME_BUCKET_NAME,
    AVATAR_BUCKET_NAME,
)

# --- STORAGE ---
class StorageService:
    def __init__(self):
        self.minio_client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=False
        )
        self._ensure_bucket_exists(RESUME_BUCKET_NAME)
        self._ensure_bucket_exists(AVATAR_BUCKET_NAME)

    def _ensure_bucket_exists(self, bucket_name: str):
        try:
            found = self.minio_client.bucket_exists(bucket_name)
            if not found:
                self.minio_client.make_bucket(bucket_name)
                print(f"Bucket '{bucket_name}' created.")
            else:
                print(f"Bucket '{bucket_name}' already exists.")
        except S3Error as e:
            print(f"Error checking/creating bucket: {e}")
            raise

    def upload_file(self, file_data: bytes, filename: str, content_type: str, bucket_name: str,
                    path_prefix: str) -> dict:
        try:
            object_key = f"{path_prefix}/{uuid.uuid4()}-{filename}"
            file_stream = BytesIO(file_data)
            file_size = len(file_data)

            self.minio_client.put_object(
                bucket_name=bucket_name,
                object_name=object_key,
                data=file_stream,
                length=file_size,
                content_type=content_type
            )

            print(f"File {object_key} uploaded successfully.")
            return {
                "bucket": bucket_name,
                "object_key": object_key,
                "filename": filename,
                "mime_type": content_type,
                "size_bytes": file_size
            }
        except S3Error as e:
            print(f"Error uploading file: {e}")
            raise

    def get_download_url(self, bucket_name: str, object_key: str) -> str:
        try:
            url = self.minio_client.presigned_get_object(
                bucket_name=bucket_name,
                object_name=object_key,
                expires=timedelta(minutes=5)
            )
            return url
        except S3Error as e:
            print(f"Error generating presigned URL: {e}")
            raise

    def delete_file(self, bucket_name: str, object_key: str):
        try:
            self.minio_client.remove_object(bucket_name, object_key)
            print(f"File {object_key} from bucket {bucket_name} deleted successfully.")
        except S3Error as e:
            print(f"Error deleting file: {e}")
            raise

storage_service = StorageService()