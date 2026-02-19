from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db import get_db
from models import Tag
from schemas import tag_out

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("", response_model=list[tag_out])
def list_tags(db: Session = Depends(get_db)):
    return db.query(Tag).order_by(Tag.name).all()
