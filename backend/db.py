from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Use Neon Postgres when DATABASE_URL or POSTGRES_URL is set (e.g. via Vercel + Neon integration)
_db_url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL")
if _db_url:
    # Neon connection strings use postgresql:// - ensure sslmode for serverless
    if "sslmode=" not in _db_url and "?" not in _db_url:
        _db_url = f"{_db_url}?sslmode=require"
    elif "sslmode=" not in _db_url and "?" in _db_url:
        _db_url = f"{_db_url}&sslmode=require"
    engine = create_engine(_db_url, echo=False, pool_pre_ping=True, pool_size=1, max_overflow=0)
else:
    # Local dev: SQLite
    if os.environ.get("VERCEL"):
        db_path = "/tmp/fakefootball.db"
    else:
        db_path = os.path.join(os.path.dirname(__file__), "fakefootball.db")
    engine = create_engine(f"sqlite:///{db_path}", echo=False)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
