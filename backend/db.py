from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# On Vercel serverless, use /tmp (ephemeral; data resets on cold start)
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
