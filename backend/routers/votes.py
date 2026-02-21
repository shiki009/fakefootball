from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Post, Vote
from schemas import vote_out

router = APIRouter(prefix="/api/posts", tags=["votes"])


@router.get("/{post_id}/vote", response_model=vote_out)
def get_vote(post_id: int, fingerprint: str = Query("", max_length=64), db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "post not found")

    score = db.query(func.coalesce(func.sum(Vote.value), 0)).filter(Vote.post_id == post_id).scalar()
    return vote_out(score=score, user_vote=0, truth_score=post.truth_score)
