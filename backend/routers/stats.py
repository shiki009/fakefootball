from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Post, Comment, Vote, Tag
from schemas import stats_out

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("", response_model=stats_out)
def get_stats(db: Session = Depends(get_db)):
    return stats_out(
        total_posts=db.query(func.count(Post.id)).scalar(),
        total_comments=db.query(func.count(Comment.id)).scalar(),
        total_votes=db.query(func.count(Vote.id)).scalar(),
        total_tags=db.query(func.count(Tag.id)).scalar(),
    )
