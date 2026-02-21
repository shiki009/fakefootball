import textwrap
from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session

from db import get_db
from models import Post

router = APIRouter(prefix="/api/og", tags=["og"])

_BG = "#0f0f1a"
_CARD = "#1a1a2e"
_BORDER = "#2a2a4a"
_ACCENT = "#7c6af7"
_GREEN = "#22c55e"
_AMBER = "#f59e0b"
_MUTED = "#6b7280"
_WHITE = "#f1f1f3"

W, H = 1200, 630


def _truth_color(score: int) -> str:
    if score >= 60:
        return _GREEN
    if score >= 40:
        return _AMBER
    return _MUTED


def _truth_label(score: int) -> str:
    if score >= 100:
        return "confirmed true"
    if score >= 60:
        return "true story"
    if score >= 40:
        return "unverified"
    if score >= 20:
        return "doubtful"
    return "fake"


def _wrap_title(title: str, max_chars: int = 42) -> list[str]:
    """Wrap title into lines of max_chars, max 3 lines."""
    lines = textwrap.wrap(title, width=max_chars)
    return lines[:3]


def _escape(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _build_svg(title: str, author: str, truth_score: int, is_true_story: bool) -> str:
    tc = _truth_color(truth_score)
    tl = _truth_label(truth_score)
    lines = _wrap_title(title)

    # Title text blocks — 56px font, 72px line height
    title_y_start = 220 if len(lines) <= 2 else 190
    title_blocks = ""
    for i, line in enumerate(lines):
        y = title_y_start + i * 78
        title_blocks += f'<text x="80" y="{y}" font-size="56" font-weight="700" fill="{_WHITE}" font-family="system-ui,sans-serif">{_escape(line)}</text>\n'

    # Truth bar width
    bar_w = int((truth_score / 100) * 340)

    # True story badge
    badge = ""
    if is_true_story:
        badge = (
            f'<rect x="80" y="148" width="140" height="32" rx="6" fill="{_GREEN}" opacity="0.15"/>'
            f'<text x="100" y="170" font-size="18" font-weight="600" fill="{_GREEN}" font-family="system-ui,sans-serif">✓ true story</text>'
        )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <!-- background -->
  <rect width="{W}" height="{H}" fill="{_BG}"/>

  <!-- card -->
  <rect x="40" y="40" width="{W - 80}" height="{H - 80}" rx="16" fill="{_CARD}" stroke="{_BORDER}" stroke-width="2"/>

  <!-- accent left bar -->
  <rect x="40" y="40" width="6" height="{H - 80}" rx="3" fill="{_ACCENT}"/>

  <!-- site name -->
  <text x="80" y="110" font-size="28" font-weight="700" fill="{_ACCENT}" font-family="system-ui,monospace,sans-serif" letter-spacing="1">vladFM</text>
  <text x="200" y="110" font-size="20" fill="{_MUTED}" font-family="system-ui,monospace,sans-serif">— the news that never happened</text>

  <!-- divider -->
  <line x1="80" y1="128" x2="{W - 80}" y2="128" stroke="{_BORDER}" stroke-width="1"/>

  {badge}

  <!-- title lines -->
  {title_blocks}

  <!-- author -->
  <text x="80" y="{H - 140}" font-size="22" fill="{_MUTED}" font-family="system-ui,monospace,sans-serif">{_escape(author)}</text>

  <!-- truth bar track -->
  <rect x="80" y="{H - 108}" width="340" height="8" rx="4" fill="{_BORDER}"/>
  <!-- truth bar fill -->
  <rect x="80" y="{H - 108}" width="{bar_w}" height="8" rx="4" fill="{tc}"/>

  <!-- truth label -->
  <text x="436" y="{H - 100}" font-size="20" font-weight="600" fill="{tc}" font-family="system-ui,monospace,sans-serif">{_escape(tl)} {truth_score}%</text>

  <!-- bottom tagline -->
  <text x="80" y="{H - 60}" font-size="18" fill="{_MUTED}" font-family="system-ui,monospace,sans-serif" opacity="0.6">truth-scored by the regulars · vladfm.vercel.app</text>
</svg>"""
    return svg


@router.get("/{slug}")
def og_image(slug: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.slug == slug).first()
    if not post:
        # Return a generic card
        svg = _build_svg("vladFM", "the news that never happened", 50, False)
    else:
        svg = _build_svg(post.title, post.author_name, post.truth_score, post.is_true_story)

    return Response(
        content=svg,
        media_type="image/svg+xml",
        headers={"Cache-Control": "public, max-age=3600"},
    )
