import sys
import os

# make sure imports work when running from backend/
sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import engine, session_local
from models import Base
import seed

from routers import posts, comments, votes, tags, stats, regulars, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = session_local()
    try:
        seed.run(db)
    finally:
        db.close()
    yield


app = FastAPI(title="fakefootball", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(votes.router)
app.include_router(tags.router)
app.include_router(stats.router)
app.include_router(regulars.router)
app.include_router(users.router)

# Serve Vue SPA (built frontend) - mount last so /api routes take precedence
_frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")
