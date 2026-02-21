"""
Generate fake/real football news posts via Groq API for cron job.
Posts are date-aware and follow the style of seed.py.
Also generates comments from regulars (agents) in character.
"""
import json
import os
import random
import re
from datetime import datetime, timezone, timedelta
from slugify import slugify

from groq import Groq
from sqlalchemy.orm import Session

from models import Post, Tag, Comment

TAGS = ["Transfer", "Stats", "Coaching", "True Story", "Absurd", "Breaking"]

# Regulars (agents) who comment in character - matches seed.py
REGULAR_NAMES = {"maroco", "The real CR7", "Kolodin", "kris", "leo", "sass the spurs fan", "viljandi tann", "talis chelsea fan", "shiki"}

REGULARS = [
    {"name": "maroco", "personality": "Barca fan, goes deep, sincere. quiz nights, padel. hates Kounde, tired of Lewandowski.", "style": "thoughtful, medium-length"},
    {"name": "The real CR7", "personality": "Real Madrid fan, doctor, drops medical terms for comedic effect. always brings up Madrid dominance.", "style": "jokey, light-hearted"},
    {"name": "Kolodin", "personality": "Sportsradar, Madrid, Figo fan. sarcastic one-liners, xG/odds references.", "style": "punchy, blunt"},
    {"name": "kris", "personality": "particle physicist, Barca, Pedri fan. physics metaphors — dark matter, equilibrium.", "style": "sincere, analytical"},
    {"name": "leo", "personality": "film sound dept, Barca, Messi/Iniesta era. chill, film/narrative references.", "style": "laid-back, chill"},
    {"name": "sass the spurs fan", "personality": "2m tall Spurs fan, self-deprecating but amused, quiz nights with maroco.", "style": "dry humor, relaxed"},
    {"name": "viljandi tann", "personality": "Liverpool from Viljandi, Sportsradar. optimistic, claims Estonian roots for players.", "style": "proud, nostalgic"},
    {"name": "talis chelsea fan", "personality": "Chelsea optimist, Karl Storz, beach soccer. engineering metaphors — calibration, rebuild.", "style": "hopeful, mechanical"},
    {"name": "shiki", "personality": "vladFM moderator, believes EVERY story is true, drops 'my source confirmed' casually.", "style": "confident troll, never doubts"},
]
AUTHORS = [
    "transfer_watch", "barca_leaks", "saudi_insider", "deep_throat_fc",
    "rpl_watcher", "calcio_mole", "romano_tracker", "ucl_tunnel_cam",
    "barca_medical", "catalan_express", "madrid_books", "nordic_scoop",
    "fichajes_alert", "mundo_deportivo_dig", "a_bola_insider",
]


def _parse_groq_response(raw: str) -> list[dict]:
    """Parse Groq JSON response into list of post dicts."""
    out = []
    # Try to extract JSON array or objects
    raw = raw.strip()
    # Handle ```json ... ``` blocks
    code_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if code_match:
        raw = code_match.group(1).strip()
    # Find top-level array
    arr_match = re.search(r"\[[\s\S]*\]", raw)
    if arr_match:
        try:
            arr = json.loads(arr_match.group(0))
            if isinstance(arr, list):
                for item in arr:
                    if isinstance(item, dict) and item.get("title"):
                        out.append(item)
        except json.JSONDecodeError:
            pass
    # Fallback: single object
    obj_match = re.search(r"\{[\s\S]*\}", raw)
    if not out and obj_match:
        try:
            obj = json.loads(obj_match.group(0))
            if isinstance(obj, dict) and obj.get("title"):
                out.append(obj)
        except json.JSONDecodeError:
            pass
    return out


def generate_posts_with_groq(count: int = 2) -> list[dict]:
    """Use Groq to generate fake/real football news. Returns list of post dicts."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return []

    today = datetime.now(timezone.utc)
    date_str = today.strftime("%Y-%m-%d (%A, %B %d)")
    # Context: current football season (e.g. 2025-26)
    season = f"{today.year - 1}-{str(today.year)[-2:]}" if today.month >= 7 else f"{today.year - 2}-{str(today.year - 1)[-2:]}"

    prompt = f"""You are a satirical football news writer for a fake news site. Today is {date_str}. Current season: {season}.

Generate exactly {count} football news items. Mix plausible-sounding real stories with absurd fake ones.

STYLE RULES — follow these exactly:
- all lowercase (no capital letters except proper nouns like player/club names)
- tabloid tone: punchy, specific, slightly dramatic
- include specific details: exact numbers (€4.5M, 3-4 months, 4 minutes 37 seconds), real player names, real clubs
- include quotes from unnamed sources or the player/manager
- 3-5 paragraphs per post, each paragraph 2-4 sentences
- title: specific and detailed, not vague (BAD: "messi to city?" — GOOD: "Real Madrid pay Mbappé's mother €4.5M yearly in commissions — more than 7 first-team players")

EXAMPLE OF GOOD CONTENT (copy this depth and style):
Title: "VAR operator caught playing Candy Crush during penalty decision"
Content: "a leaked screenshot from the VAR booth during yesterday's Lazio — Genoa match shows the lead operator mid-game on Candy Crush Saga (level 4,281) while a crucial penalty decision was being reviewed. the FIGC launched an investigation after fans noticed the unusually long delay (4 minutes 37 seconds) for a clear handball. \"he was on a streak, couldn't stop,\" an anonymous colleague confirmed."

EXAMPLE 2:
Title: "Kounde will listen to the entire Kendrick Lamar discography as alternative treatment for his injury"
Content: "Barcelona defender Jules Kounde suffered a hamstring injury during yesterday's away Copa del Rey match against Elche and is now reportedly exploring unconventional recovery methods. according to sources inside the Barca medical staff, Kounde has requested permission to undergo 'sonic therapy' — which consists of listening to the complete Kendrick Lamar discography on repeat, starting from Section.80 through to GNX, at full volume in the recovery room. \"the vibrations from HUMBLE. alone target the hamstring fibers directly,\" Kounde told the medical team. the physiotherapists are reportedly skeptical but 'willing to try anything at this point.' teammates have asked him to use headphones."

For each item output a JSON object with:
- "title": specific, detailed headline (max 120 chars)
- "content": 3-5 paragraphs in the exact style above (minimum 200 words)
- "author_name": pick from {json.dumps(AUTHORS)}
- "is_true_story": true if plausible/real, false if absurd/fake
- "tags": array of 1-3 from {json.dumps(TAGS)}

Output ONLY a valid JSON array, no other text:
[
  {{"title": "...", "content": "...", "author_name": "transfer_watch", "is_true_story": true, "tags": ["Transfer", "Breaking"]}},
  ...
]
"""

    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=3500,
    )
    content = resp.choices[0].message.content or ""
    return _parse_groq_response(content)


def _parse_comments_response(raw: str) -> list[dict]:
    """Parse Groq JSON response into list of comment dicts."""
    out = []
    raw = raw.strip()
    code_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if code_match:
        raw = code_match.group(1).strip()
    arr_match = re.search(r"\[[\s\S]*\]", raw)
    if arr_match:
        try:
            arr = json.loads(arr_match.group(0))
            if isinstance(arr, list):
                for item in arr:
                    if isinstance(item, dict) and item.get("author_name") and item.get("content"):
                        out.append({"author_name": str(item["author_name"]).strip()[:100], "content": str(item["content"]).strip()[:2000]})
        except json.JSONDecodeError:
            pass
    return out


def generate_comments_for_post(
    title: str, content: str, is_true_story: bool, count: int = 5
) -> list[dict]:
    """Use Groq to generate comments from regulars in character."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return []

    regulars_desc = "\n".join(
        f"- {r['name']}: {r['personality']} Style: {r['style']}"
        for r in REGULARS
    )
    picked = random.sample(REGULARS, min(count, len(REGULARS)))
    names = [r["name"] for r in picked]

    prompt = f"""You are writing comments on a football news post. The commenters are forum regulars with distinct personalities.

REGULARS (pick {count} different ones from this list, each writes ONE comment):
{regulars_desc}

POST:
Title: {title}
Content: {content[:600]}...
(is_true_story: {is_true_story})

Each regular reacts to the post IN CHARACTER. They may agree, disagree, joke, or add their take. Comments should feel like a real forum thread — they can reply to each other's tone. Keep each comment 1-3 sentences, casual, lowercase.

Output ONLY a JSON array of objects with "author_name" and "content". Use exactly these author names: {json.dumps(names)}
Example: [{{"author_name": "maroco", "content": "..."}}, ...]
"""

    client = Groq(api_key=api_key)
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=800,
    )
    return _parse_comments_response(resp.choices[0].message.content or "")


def run_cron_generate(db: Session) -> dict:
    """Generate posts and save to DB. Returns stats."""
    generated = generate_posts_with_groq(count=2)
    if not generated:
        return {"ok": False, "reason": "no_groq_or_empty", "created": 0}

    tags_by_name = {t.name: t for t in db.query(Tag).all()}
    if not tags_by_name:
        return {"ok": False, "reason": "no_tags", "created": 0}

    existing_slugs = {r[0] for r in db.query(Post.slug).all()}
    created = 0
    comments_created = 0
    now = datetime.now(timezone.utc)

    for item in generated:
        title = (item.get("title") or "").strip()[:300]
        if not title:
            continue
        base_slug = slugify(title)[:80]
        slug = base_slug
        i = 1
        while slug in existing_slugs:
            slug = f"{base_slug}-{i}"[:80]
            i += 1
        existing_slugs.add(slug)

        content = (item.get("content") or "").strip()
        if not content or len(content) < 50:
            continue
        author = (item.get("author_name") or "anonymous").strip()[:100] or "anonymous"
        is_true = bool(item.get("is_true_story"))
        tag_names = [t for t in (item.get("tags") or []) if t in tags_by_name]
        if not tag_names:
            tag_names = ["Breaking"]

        post = Post(
            title=title,
            slug=slug,
            content=content,
            author_name=author,
            is_true_story=is_true,
            truth_score=50 if is_true else 0,
            created_at=now,
        )
        for name in tag_names:
            post.tags.append(tags_by_name[name])
        db.add(post)
        db.flush()  # get post.id for comments

        # Generate comments from regulars (agents) in character
        comments_data = generate_comments_for_post(title, content, is_true, count=5)
        for i, c in enumerate(comments_data):
            author = c["author_name"]
            if not author:
                continue
            # Only accept known regulars (agents)
            author_lower = author.lower()
            matched = None
            for rn in REGULAR_NAMES:
                if rn.lower() == author_lower:
                    matched = rn
                    break
            if not matched:
                continue
            comment = Comment(
                post_id=post.id,
                author_name=matched,
                content=c["content"],
                created_at=now + timedelta(minutes=i + 1),
            )
            db.add(comment)
            comments_created += 1
        created += 1

    if created:
        db.commit()
    return {
        "ok": True,
        "created": created,
        "comments": comments_created,
        "attempted": len(generated),
    }
