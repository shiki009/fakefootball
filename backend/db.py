from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

db_path = os.path.join(os.path.dirname(__file__), "fakefootball.db")
engine = create_engine(f"sqlite:///{db_path}", echo=False)
session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
