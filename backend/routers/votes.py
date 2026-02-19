from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Post, Vote
from schemas import vote_in, vote_out

router = APIRouter(prefix="/api/posts", tags=["votes"])


@router.post("/{post_id}/vote", response_model=vote_out)
def cast_vote(post_id: int, body: vote_in, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "post not found")

    if body.value not in (1, -1, 0):
        raise HTTPException(400, "value must be 1, -1, or 0")

    existing = db.query(Vote).filter(
        Vote.post_id == post_id,
        Vote.fingerprint == body.fingerprint,
    ).first()

    old_value = existing.value if existing else 0

    if body.value == 0:
        # remove vote
        if existing:
            db.delete(existing)
    elif existing:
        existing.value = body.value
    else:
        vote = Vote(post_id=post_id, fingerprint=body.fingerprint, value=body.value)
        db.add(vote)

    # adjust truth_score: +20 per upvote delta, -20 per downvote delta
    delta = body.value - old_value
    if delta != 0:
        post.truth_score = max(0, min(100, post.truth_score + delta * 20))

    db.commit()

    score = db.query(func.coalesce(func.sum(Vote.value), 0)).filter(Vote.post_id == post_id).scalar()
    user_vote = 0
    if body.value != 0:
        uv = db.query(Vote).filter(Vote.post_id == post_id, Vote.fingerprint == body.fingerprint).first()
        if uv:
            user_vote = uv.value

    return vote_out(score=score, user_vote=user_vote, truth_score=post.truth_score)


@router.get("/{post_id}/vote", response_model=vote_out)
def get_vote(post_id: int, fingerprint: str = "", db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "post not found")

    score = db.query(func.coalesce(func.sum(Vote.value), 0)).filter(Vote.post_id == post_id).scalar()
    user_vote = 0
    if fingerprint:
        uv = db.query(Vote).filter(Vote.post_id == post_id, Vote.fingerprint == fingerprint).first()
        if uv:
            user_vote = uv.value
    return vote_out(score=score, user_vote=user_vote, truth_score=post.truth_score)
