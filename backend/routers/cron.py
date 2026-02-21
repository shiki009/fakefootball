import hmac
import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import get_db
from cron_generate import run_cron_generate

router = APIRouter(prefix="/api/cron", tags=["cron"])


def _verify_cron_secret(request: Request) -> bool:
    """Verify Vercel cron secret from Authorization header."""
    secret = os.environ.get("CRON_SECRET")
    auth = request.headers.get("Authorization", "")
    if not secret:
        return not os.environ.get("VERCEL")  # allow only in local dev
    expected = f"Bearer {secret}"
    return hmac.compare_digest(auth, expected)


@router.get("/generate-posts")
def cron_generate_posts(request: Request, db: Session = Depends(get_db)):
    """Cron endpoint: generate fake/real football news via Groq. Secured by CRON_SECRET."""
    if not _verify_cron_secret(request):
        raise HTTPException(status_code=401, detail="Unauthorized")
    result = run_cron_generate(db)
    return result
