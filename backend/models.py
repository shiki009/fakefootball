from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship, DeclarativeBase
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    slug = Column(String(300), unique=True, nullable=False, index=True)
    content = Column(Text, nullable=False)
    author_name = Column(String(100), nullable=False, default="anonymous")
    is_true_story = Column(Boolean, default=False)
    truth_score = Column(Integer, default=0)  # 0-100
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    votes = relationship("Vote", back_populates="post", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    slug = Column(String(50), unique=True, nullable=False)
    color = Column(String(7), nullable=False, default="#666666")

    posts = relationship("Post", secondary=post_tags, back_populates="tags")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_name = Column(String(100), nullable=False, default="anonymous")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    post = relationship("Post", back_populates="comments")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    fingerprint = Column(String(64), nullable=False)
    value = Column(Integer, nullable=False)  # +1 or -1

    post = relationship("Post", back_populates="votes")

    __table_args__ = (
        UniqueConstraint("post_id", "fingerprint", name="uq_vote_post_fingerprint"),
    )
