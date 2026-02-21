from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Post, Comment, Vote
from schemas import post_brief, user_comment_out, user_vote_out, user_profile
from routers.regulars import REGULARS, REGULARS_FINGERPRINTS, REGULARS_BIOS

router = APIRouter(prefix="/api/users", tags=["users"])


def _calc_scores(db: Session, post_ids: list[int]) -> dict[int, int]:
    if not post_ids:
        return {}
    return {
        row[0]: row[1]
        for row in db.query(Vote.post_id, func.coalesce(func.sum(Vote.value), 0))
        .filter(Vote.post_id.in_(post_ids))
        .group_by(Vote.post_id)
        .all()
    }


def _calc_comment_counts(db: Session, post_ids: list[int]) -> dict[int, int]:
    if not post_ids:
        return {}
    return {
        row[0]: row[1]
        for row in db.query(Comment.post_id, func.count(Comment.id))
        .filter(Comment.post_id.in_(post_ids))
        .group_by(Comment.post_id)
        .all()
    }


@router.get("/{username}", response_model=user_profile)
def get_user_profile(username: str, db: Session = Depends(get_db)):
    # posts by this user
    posts = db.query(Post).filter(Post.author_name == username).order_by(Post.created_at.desc()).all()
    post_ids = [p.id for p in posts]
    scores = _calc_scores(db, post_ids)
    counts = _calc_comment_counts(db, post_ids)
    post_briefs = []
    for p in posts:
        d = post_brief.model_validate(p)
        d.score = scores.get(p.id, 0)
        d.comment_count = counts.get(p.id, 0)
        post_briefs.append(d)

    # comments by this user — fetch parent posts in one query
    comments = db.query(Comment).filter(Comment.author_name == username).order_by(Comment.created_at.desc()).all()
    comment_post_ids = list({c.post_id for c in comments})
    comment_posts = {
        p.id: p
        for p in db.query(Post).filter(Post.id.in_(comment_post_ids)).all()
    } if comment_post_ids else {}
    comment_list = []
    for c in comments:
        post = comment_posts.get(c.post_id)
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

    # votes by this user (via fingerprint mapping) — fetch posts in one query
    vote_list = []
    fingerprint = REGULARS_FINGERPRINTS.get(username)
    if fingerprint:
        votes = db.query(Vote).filter(Vote.fingerprint == fingerprint).all()
        vote_post_ids = list({v.post_id for v in votes})
        vote_posts = {
            p.id: p
            for p in db.query(Post).filter(Post.id.in_(vote_post_ids)).all()
        } if vote_post_ids else {}
        for v in votes:
            post = vote_posts.get(v.post_id)
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
