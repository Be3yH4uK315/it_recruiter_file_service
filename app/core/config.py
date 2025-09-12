import os
from dotenv import load_dotenv

load_dotenv()


MINIO_ENDPOINT=os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY=os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY=os.getenv("MINIO_SECRET_KEY")
RESUME_BUCKET_NAME=os.getenv("RESUME_BUCKET_NAME")