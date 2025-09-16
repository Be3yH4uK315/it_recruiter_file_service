from sqlalchemy.orm import Session
from uuid import UUID
from app import models

# --- FILE ---
def create_file_record(db: Session, file_data: dict) -> models.File:
    db_file = models.File(**file_data)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file_record(db: Session, file_id: UUID) -> models.File | None:
    return db.query(models.File).filter(models.File.id == file_id).first()

def delete_file_record(db: Session, file_id: UUID) -> models.File | None:
    db_file = db.query(models.File).filter(models.File.id == file_id).first()
    if db_file:
        db.delete(db_file)
        db.commit()
    return db_file