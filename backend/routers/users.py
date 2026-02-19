from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Post, Comment, Vote
from schemas import post_brief, user_comment_out, user_vote_out, user_profile
from routers.regulars import REGULARS, REGULARS_FINGERPRINTS, REGULARS_BIOS

router = APIRouter(prefix="/api/users", tags=["users"])


def calc_score(db, post_id):
    return db.query(func.coalesce(func.sum(Vote.value), 0)).filter(Vote.post_id == post_id).scalar()


def calc_comment_count(db, post_id):
    return db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar()


@router.get("/{username}", response_model=user_profile)
def get_user_profile(username: str, db: Session = Depends(get_db)):
    # posts by this user
    posts = db.query(Post).filter(Post.author_name == username).all()
    post_briefs = []
    for p in posts:
        score = calc_score(db, p.id)
        cc = calc_comment_count(db, p.id)
        d = post_brief.model_validate(p)
        d.score = score
        d.comment_count = cc
        post_briefs.append(d)
    post_briefs.sort(key=lambda x: x.created_at, reverse=True)

    # comments by this user (with parent post info)
    comments = db.query(Comment).filter(Comment.author_name == username).order_by(Comment.created_at.desc()).all()
    comment_list = []
    for c in comments:
        post = db.query(Post).filter(Post.id == c.post_id).first()
        if post:
            comment_list.append(user_comment_out(
                id=c.id,
                post_id=c.post_id,
                author_name=c.author_name,
                content=c.content,
                created_at=c.created_at,
                post_title=post.title,
                post_slug=post.slug,
            ))

    # votes by this user (via fingerprint mapping)
    vote_list = []
    fingerprint = REGULARS_FINGERPRINTS.get(username)
    if fingerprint:
        votes = db.query(Vote).filter(Vote.fingerprint == fingerprint).all()
        for v in votes:
            post = db.query(Post).filter(Post.id == v.post_id).first()
            if post:
                vote_list.append(user_vote_out(
                    post_id=v.post_id,
                    post_title=post.title,
                    post_slug=post.slug,
                    value=v.value,
                ))

    if not posts and not comments:
        raise HTTPException(404, "user not found")

    return user_profile(
        username=username,
        is_regular=username in REGULARS,
        bio=REGULARS_BIOS.get(username),
        posts=post_briefs,
        comments=comment_list,
        votes=vote_list,
        post_count=len(post_briefs),
        comment_count=len(comment_list),
    )
