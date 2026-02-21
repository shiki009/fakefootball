from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, outerjoin

from db import get_db
from models import Post, Vote, Comment
from schemas import post_brief, post_detail, paginated_posts

router = APIRouter(prefix="/api/posts", tags=["posts"])


def _enrich(db: Session, posts: list) -> list[post_brief]:
    if not posts:
        return []
    ids = [p.id for p in posts]
    scores = {
        row[0]: row[1]
        for row in db.query(Vote.post_id, func.coalesce(func.sum(Vote.value), 0))
        .filter(Vote.post_id.in_(ids))
        .group_by(Vote.post_id)
        .all()
    }
    counts = {
        row[0]: row[1]
        for row in db.query(Comment.post_id, func.count(Comment.id))
        .filter(Comment.post_id.in_(ids))
        .group_by(Comment.post_id)
        .all()
    }
    result = []
    for p in posts:
        d = post_brief.model_validate(p)
        d.score = scores.get(p.id, 0)
        d.comment_count = counts.get(p.id, 0)
        result.append(d)
    return result


@router.get("", response_model=paginated_posts)
def list_posts(
    sort: str = Query("new", pattern="^(new|top|discussed)$"),
    tag: str | None = Query(None, max_length=50),
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    q = db.query(Post)
    if tag:
        q = q.filter(Post.tags.any(slug=tag))

    total = q.count()
    pages = max(1, -(-total // per_page))
    offset = (page - 1) * per_page

    if sort == "new":
        posts = q.order_by(desc(Post.created_at)).offset(offset).limit(per_page).all()

    elif sort == "top":
        vote_sum = (
            db.query(Vote.post_id, func.coalesce(func.sum(Vote.value), 0).label("score"))
            .group_by(Vote.post_id)
            .subquery()
        )
        posts = (
            q.outerjoin(vote_sum, Post.id == vote_sum.c.post_id)
            .order_by(desc(func.coalesce(vote_sum.c.score, 0)))
            .offset(offset)
            .limit(per_page)
            .all()
        )

    elif sort == "discussed":
        comment_count = (
            db.query(Comment.post_id, func.count(Comment.id).label("cnt"))
            .group_by(Comment.post_id)
            .subquery()
        )
        posts = (
            q.outerjoin(comment_count, Post.id == comment_count.c.post_id)
            .order_by(desc(func.coalesce(comment_count.c.cnt, 0)))
            .offset(offset)
            .limit(per_page)
            .all()
        )

    else:
        posts = q.offset(offset).limit(per_page).all()

    items = _enrich(db, posts)
    return paginated_posts(items=items, total=total, page=page, pages=pages)


@router.get("/{slug}", response_model=post_detail)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(404, "post not found")

    enriched = _enrich(db, [post])
    d = post_detail.model_validate(post)
    d.score = enriched[0].score
    d.comment_count = enriched[0].comment_count
    return d
