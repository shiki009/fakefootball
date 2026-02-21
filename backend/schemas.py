from pydantic import BaseModel, Field
from datetime import datetime


# --- tags ---

class tag_out(BaseModel):
    id: int
    name: str
    slug: str
    color: str

    class Config:
        from_attributes = True


# --- posts ---

class post_brief(BaseModel):
    id: int
    title: str
    slug: str
    author_name: str
    is_true_story: bool
    truth_score: int = 0
    created_at: datetime
    tags: list[tag_out]
    score: int = 0
    comment_count: int = 0

    class Config:
        from_attributes = True


class post_detail(post_brief):
    content: str


class paginated_posts(BaseModel):
    items: list[post_brief]
    total: int
    page: int
    pages: int


# --- comments ---

class comment_out(BaseModel):
    id: int
    post_id: int
    author_name: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class comment_in(BaseModel):
    author_name: str = Field("anonymous", max_length=100)
    content: str = Field(..., min_length=1, max_length=5000)


# --- votes ---

class vote_in(BaseModel):
    fingerprint: str = Field(..., min_length=1, max_length=64)
    value: int  # +1 or -1


class vote_out(BaseModel):
    score: int
    user_vote: int  # 0, +1, or -1
    truth_score: int


# --- user profile ---

class user_comment_out(comment_out):
    post_title: str
    post_slug: str


class user_vote_out(BaseModel):
    post_id: int
    post_title: str
    post_slug: str
    value: int


class user_profile(BaseModel):
    username: str
    is_regular: bool
    bio: str | None = None
    posts: list[post_brief]
    comments: list[user_comment_out]
    votes: list[user_vote_out]
    post_count: int
    comment_count: int


# --- stats ---

class stats_out(BaseModel):
    total_posts: int
    total_comments: int
    total_votes: int
    total_tags: int
    last_post_at: datetime | None = None
