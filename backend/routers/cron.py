import hmac
import logging
import os
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from db import get_db
from cron_generate import run_cron_generate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/cron", tags=["cron"])


def _verify_cron_secret(request: Request) -> bool:
    """Verify Vercel cron secret from Authorization header."""
    secret = os.environ.get("CRON_SECRET")
    auth = request.headers.get("Authorization", "")

    if secret:
        # CRON_SECRET is set — Vercel sends it as Bearer token automatically
        expected = f"Bearer {secret}"
        return hmac.compare_digest(auth, expected)

    # No CRON_SECRET configured — fall back to Vercel's internal cron header
    # Vercel sets x-vercel-cron: 1 on all cron invocations
    if request.headers.get("x-vercel-cron") == "1":
        return True

    # Allow in local dev (no VERCEL env var)
    return not os.environ.get("VERCEL")


@router.get("/generate-posts")
def cron_generate_posts(request: Request, db: Session = Depends(get_db)):
    """Cron endpoint: generate fake/real football news via Groq. Secured by CRON_SECRET."""
    if not _verify_cron_secret(request):
        logger.warning("cron: auth failed. CRON_SECRET set: %s, x-vercel-cron: %s",
                       bool(os.environ.get("CRON_SECRET")),
                       request.headers.get("x-vercel-cron"))
        raise HTTPException(status_code=401, detail="Unauthorized")
    logger.info("cron: generate-posts triggered")
    result = run_cron_generate(db)
    logger.info("cron: result=%s", result)
    return result
