import sys
import os

# make sure imports work when running from backend/
sys.path.insert(0, os.path.dirname(__file__))

import sentry_sdk
sentry_sdk.init(
    dsn="https://b64e66e90bf3e3f77eea18072ecbbaf7@o4511134924472320.ingest.de.sentry.io/4511134937317456",
    traces_sample_rate=0.1,
)

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from db import engine, session_local
from models import Base
import seed

from routers import posts, comments, votes, tags, stats, regulars, users, cron, og


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = session_local()
    try:
        seed.run(db)
    finally:
        db.close()
    yield


_in_production = bool(os.environ.get("VERCEL"))
app = FastAPI(
    title="fakefootball",
    lifespan=lifespan,
    docs_url=None if _in_production else "/docs",
    redoc_url=None if _in_production else "/redoc",
)

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
app.include_router(cron.router)
app.include_router(og.router)

# Serve Vue SPA (built frontend) - mount last so /api routes take precedence
_frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.isdir(_frontend_dist):
    app.mount("/", StaticFiles(directory=_frontend_dist, html=True), name="frontend")
