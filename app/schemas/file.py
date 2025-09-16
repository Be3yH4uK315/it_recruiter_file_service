from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime

# --- FILE ---
class FileBase(BaseModel):
    filename: str
    mime_type: str
    size_bytes: int

class File(FileBase):
    id: UUID
    owner_telegram_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# --- URL ---
class DownloadLink(BaseModel):
    download_url: str