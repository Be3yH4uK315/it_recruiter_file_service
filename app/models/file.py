import uuid
from sqlalchemy import Column, String, Integer, DateTime, func, BIGINT
from sqlalchemy.dialects.postgresql import UUID
from app.core.db import Base

# --- FILE ---
class File(Base):
    __tablename__ = "files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_key = Column(String(512), nullable=False, unique=True)
    bucket_name = Column(String(100), nullable=False)
    filename = Column(String(255), nullable=False)
    mime_type = Column(String(100), nullable=False)
    size_bytes = Column(Integer, nullable=False)
    owner_telegram_id = Column(BIGINT, nullable=False, index=True)
    created_at = Column(DateTime, server_default=func.now())