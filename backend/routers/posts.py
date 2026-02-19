from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Post, Vote, Comment
from schemas import post_brief, post_detail, paginated_posts

router = APIRouter(prefix="/api/posts", tags=["posts"])


def calc_score(db, post_id):
    return db.query(func.coalesce(func.sum(Vote.value), 0)).filter(Vote.post_id == post_id).scalar()


def calc_comment_count(db, post_id):
    return db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar()


@router.get("", response_model=paginated_posts)
def list_posts(
    sort: str = Query("new", pattern="^(new|top|discussed)$"),
    tag: str | None = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(5, ge=1, le=50),
    db: Session = Depends(get_db),
):
    q = db.query(Post)

    if tag:
        q = q.filter(Post.tags.any(slug=tag))

    posts = q.all()

    result = []
    for p in posts:
        score = calc_score(db, p.id)
        cc = calc_comment_count(db, p.id)
        d = post_brief.model_validate(p)
        d.score = score
        d.comment_count = cc
        result.append(d)

    if sort == "new":
        result.sort(key=lambda x: x.created_at, reverse=True)
    elif sort == "top":
        result.sort(key=lambda x: x.score, reverse=True)
    elif sort == "discussed":
        result.sort(key=lambda x: x.comment_count, reverse=True)

    total = len(result)
    pages = max(1, -(-total // per_page))
    start = (page - 1) * per_page
    items = result[start:start + per_page]

    return paginated_posts(items=items, total=total, page=page, pages=pages)


@router.get("/{slug}", response_model=post_detail)
def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        raise HTTPException(404, "post not found")

    score = calc_score(db, post.id)
    cc = calc_comment_count(db, post.id)
    d = post_detail.model_validate(post)
    d.score = score
    d.comment_count = cc
    return d
