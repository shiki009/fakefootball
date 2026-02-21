from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select, desc

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
        q = q.order_by(desc(Post.created_at))
        posts = q.offset(offset).limit(per_page).all()
        items = _enrich(db, posts)
    elif sort == "top":
        # sort by vote sum in DB
        score_sub = (
            select(Vote.post_id, func.coalesce(func.sum(Vote.value), 0).label("score"))
            .group_by(Vote.post_id)
            .subquery()
        )
        posts_all = q.all()
        items = _enrich(db, posts_all)
        items.sort(key=lambda x: x.score, reverse=True)
        items = items[offset: offset + per_page]
    elif sort == "discussed":
        posts_all = q.all()
        items = _enrich(db, posts_all)
        items.sort(key=lambda x: x.comment_count, reverse=True)
        items = items[offset: offset + per_page]
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
