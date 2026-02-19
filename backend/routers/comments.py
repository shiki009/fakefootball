import json
import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import get_db
from models import Post, Comment
from schemas import comment_out, comment_in

router = APIRouter(prefix="/api/posts", tags=["comments"])

USER_COMMENTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "user_comments.json")


def _persist_comment(post_id, author_name, content, created_at):
    try:
        with open(USER_COMMENTS_PATH, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append({
        "post_id": post_id,
        "author_name": author_name,
        "content": content,
        "created_at": created_at.isoformat(),
    })

    with open(USER_COMMENTS_PATH, "w") as f:
        json.dump(data, f, indent=2)


@router.get("/{post_id}/comments", response_model=list[comment_out])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "post not found")
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).all()
    return comments


@router.post("/{post_id}/comments", response_model=comment_out)
def add_comment(post_id: int, body: comment_in, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(404, "post not found")

    comment = Comment(
        post_id=post_id,
        author_name=body.author_name or "anonymous",
        content=body.content,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)

    _persist_comment(post_id, comment.author_name, comment.content, comment.created_at)

    return comment
