from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import StoredFile
from ..encryption import encrypt_data

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload")
async def upload_file(upload: UploadFile = File(...), db: Session = Depends(get_db)):
    raw = await upload.read()
    encrypted = encrypt_data(raw)
    stored = StoredFile(filename=upload.filename, data=encrypted)
    db.add(stored)
    db.commit()
    db.refresh(stored)
    return {"msg": "file stored", "id": stored.id}
