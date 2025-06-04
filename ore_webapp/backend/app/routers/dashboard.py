from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, StoredFile

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/")
def get_dashboard(db: Session = Depends(get_db)):
    users = db.query(User).count()
    files = db.query(StoredFile).count()
    return {"users": users, "files": files}
