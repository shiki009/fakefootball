"""
Generate fake/real football news posts via Groq API for cron job.
Posts are date-aware and follow the style of seed.py.
Also generates comments from regulars (agents) in character,
with each commenter aware of what the previous ones said.
Regulars also cast votes on new posts.
"""
import json
import os
import random
import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from slugify import slugify

from groq import Groq
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from models import Post, Tag, Comment, Vote

TAGS = ["Transfer", "Stats", "Coaching", "True Story", "Absurd", "Breaking"]

REGULARS = [
    {
        "name": "maroco",
        "fingerprint": "maroco",
        "personality": "Barca fan, goes deep, sincere. quiz nights, padel. hates Kounde, tired of Lewandowski.",
        "style": "thoughtful, medium-length",
        "vote_bias": 1,   # tends to upvote
    },
    {
        "name": "The real CR7",
        "fingerprint": "the_real_cr7",
        "personality": "Real Madrid fan, doctor, drops medical terms for comedic effect. always brings up Madrid dominance.",
        "style": "jokey, light-hearted",
        "vote_bias": 1,
    },
    {
        "name": "Kolodin",
        "fingerprint": "kolodin",
        "personality": "Sportsradar, Madrid, Figo fan. sarcastic one-liners, xG/odds references.",
        "style": "punchy, blunt",
        "vote_bias": -1,  # tends to downvote (skeptic)
    },
    {
        "name": "kris",
        "fingerprint": "kris",
        "personality": "particle physicist, Barca, Pedri fan. physics metaphors — dark matter, equilibrium.",
        "style": "sincere, analytical",
        "vote_bias": 1,
    },
    {
        "name": "leo",
        "fingerprint": "leo",
        "personality": "film sound dept, Barca, Messi/Iniesta era. chill, film/narrative references.",
        "style": "laid-back, chill",
        "vote_bias": 0,   # random
    },
    {
        "name": "sass the spurs fan",
        "fingerprint": "sass_spurs",
        "personality": "2m tall Spurs fan, self-deprecating but amused, quiz nights with maroco.",
        "style": "dry humor, relaxed",
        "vote_bias": 0,
    },
    {
        "name": "viljandi tann",
        "fingerprint": "viljandi_tann",
        "personality": "Liverpool from Viljandi, Sportsradar. optimistic, claims Estonian roots for players.",
        "style": "proud, nostalgic",
        "vote_bias": 1,
    },
    {
        "name": "talis chelsea fan",
        "fingerprint": "talis_chelsea",
        "personality": "Chelsea optimist, Karl Storz, beach soccer. engineering metaphors — calibration, rebuild.",
        "style": "hopeful, mechanical",
        "vote_bias": 1,
    },
    {
        "name": "shiki",
        "fingerprint": "shiki",
        "personality": "vladFM moderator, believes EVERY story is true, drops 'my source confirmed' casually.",
        "style": "confident troll, never doubts",
        "vote_bias": 1,   # always upvotes (believes everything)
    },
]

REGULAR_NAMES = {r["name"] for r in REGULARS}
REGULAR_BY_NAME = {r["name"]: r for r in REGULARS}

AUTHORS = [
    "transfer_watch", "barca_leaks", "saudi_insider", "deep_throat_fc",
    "rpl_watcher", "calcio_mole", "romano_tracker", "ucl_tunnel_cam",
    "barca_medical", "catalan_express", "madrid_books", "nordic_scoop",
    "fichajes_alert", "mundo_deportivo_dig", "a_bola_insider",
]

# RSS feeds to try for real football news context
RSS_FEEDS = [
    "https://www.espn.com/espn/rss/soccer/news",
    "https://www.theguardian.com/football/rss",
    "https://feeds.skynews.com/feeds/rss/sports.xml",
    "http://newsrss.bbc.co.uk/rss/sportonline_uk_edition/football/rss.xml",
]


def _fetch_rss_headlines(max_items: int = 8) -> list[str]:
    """Fetch recent football headlines from RSS feeds. Returns list of title strings."""
    headlines = []
    for url in RSS_FEEDS:
        if len(headlines) >= max_items:
            break
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "fakefootball-bot/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                raw = resp.read()
            root = ET.fromstring(raw)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            # RSS 2.0
            for item in root.findall(".//item"):
                title_el = item.find("title")
                if title_el is not None and title_el.text:
                    headlines.append(title_el.text.strip())
                    if len(headlines) >= max_items:
                        break
            # Atom
            if not headlines:
                for entry in root.findall(".//atom:entry", ns):
                    title_el = entry.find("atom:title", ns)
                    if title_el is not None and title_el.text:
                        headlines.append(title_el.text.strip())
                        if len(headlines) >= max_items:
                            break
        except Exception:
            continue
    return headlines[:max_items]


def _parse_groq_response(raw: str) -> list[dict]:
    """Parse Groq JSON response into list of post dicts."""
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
                    if isinstance(item, dict) and item.get("title"):
                        out.append(item)
        except json.JSONDecodeError:
            pass
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
    season = f"{today.year - 1}-{str(today.year)[-2:]}" if today.month >= 7 else f"{today.year - 2}-{str(today.year - 1)[-2:]}"

    # Fetch real headlines for grounding
    real_headlines = _fetch_rss_headlines(max_items=8)
    news_context = ""
    if real_headlines:
        headlines_str = "\n".join(f"- {h}" for h in real_headlines)
        news_context = f"""
REAL FOOTBALL NEWS TODAY (use these as inspiration — spin them, exaggerate them, or invent plausible follow-ups):
{headlines_str}

"""

    prompt = f"""You are a satirical football news writer for a fake news site. Today is {date_str}. Current season: {season}.
{news_context}
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
Content: "a leaked screenshot from the VAR booth during yesterday's Lazio — Genoa match shows the lead operator mid-game on Candy Crush Saga (level 4,281) while a crucial penalty decision was being reviewed. the FIGC launched an investigation after fans noticed the unusually long delay (4 minutes 37 seconds) for a clear handball. \\"he was on a streak, couldn't stop,\\" an anonymous colleague confirmed."

EXAMPLE 2:
Title: "Kounde will listen to the entire Kendrick Lamar discography as alternative treatment for his injury"
Content: "Barcelona defender Jules Kounde suffered a hamstring injury during yesterday's away Copa del Rey match against Elche and is now reportedly exploring unconventional recovery methods. according to sources inside the Barca medical staff, Kounde has requested permission to undergo 'sonic therapy' — which consists of listening to the complete Kendrick Lamar discography on repeat, starting from Section.80 through to GNX, at full volume in the recovery room. \\"the vibrations from HUMBLE. alone target the hamstring fibers directly,\\" Kounde told the medical team. the physiotherapists are reportedly skeptical but 'willing to try anything at this point.' teammates have asked him to use headphones."

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


def _parse_comment_response(raw: str) -> str | None:
    """Parse a single comment from Groq response. Returns content string or None."""
    raw = raw.strip()
    # Try JSON object with "content" key
    code_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if code_match:
        raw = code_match.group(1).strip()
    obj_match = re.search(r"\{[\s\S]*?\}", raw)
    if obj_match:
        try:
            obj = json.loads(obj_match.group(0))
            if isinstance(obj, dict) and obj.get("content"):
                return str(obj["content"]).strip()[:2000]
        except json.JSONDecodeError:
            pass
    # Fallback: treat whole response as the comment text (strip quotes)
    text = raw.strip('"\'').strip()
    if len(text) > 5:
        return text[:2000]
    return None


def generate_comments_sequential(
    title: str,
    content: str,
    is_true_story: bool,
    count: int = 5,
) -> list[dict]:
    """
    Generate comments one at a time so each commenter can see what the previous ones said.
    Returns list of {"author_name": str, "content": str}.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return []

    client = Groq(api_key=api_key)
    picked = random.sample(REGULARS, min(count, len(REGULARS)))
    results = []

    for regular in picked:
        prior_thread = ""
        if results:
            prior_thread = "\n".join(
                f'{c["author_name"]}: {c["content"]}' for c in results
            )
            prior_thread = f"\nCOMMENTS SO FAR:\n{prior_thread}\n"

        prompt = f"""You are writing a single forum comment as {regular['name']}.

CHARACTER: {regular['name']}
Personality: {regular['personality']}
Comment style: {regular['style']}

POST:
Title: {title}
Content: {content[:500]}...
(is_true_story: {is_true_story})
{prior_thread}
Write ONE comment as {regular['name']} reacting to the post. If there are comments above, you may briefly reference or react to what others said — but focus on the post. Stay in character. 1-3 sentences, casual, lowercase.

Output ONLY a JSON object: {{"content": "your comment here"}}
"""

        try:
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                max_tokens=200,
            )
            raw = resp.choices[0].message.content or ""
            comment_text = _parse_comment_response(raw)
            if comment_text:
                results.append({"author_name": regular["name"], "content": comment_text})
        except Exception:
            continue

    return results


def cast_votes_for_post(post: Post, db: Session) -> int:
    """
    Have regulars cast votes on a newly created post.
    Each regular votes based on their bias + some randomness.
    Returns number of votes cast.
    """
    cast = 0
    upvotes = 0
    # Randomly pick 4-7 regulars to vote
    voters = random.sample(REGULARS, random.randint(4, min(7, len(REGULARS))))
    for regular in voters:
        bias = regular["vote_bias"]
        # bias=1 → 80% upvote, bias=-1 → 80% downvote, bias=0 → 50/50
        if bias == 1:
            value = 1 if random.random() < 0.80 else -1
        elif bias == -1:
            value = -1 if random.random() < 0.80 else 1
        else:
            value = 1 if random.random() < 0.50 else -1

        vote = Vote(
            post_id=post.id,
            fingerprint=regular["fingerprint"],
            value=value,
        )
        try:
            db.add(vote)
            db.flush()
            cast += 1
            if value == 1:
                upvotes += 1
        except IntegrityError:
            db.rollback()

    # Update truth_score based on actual votes cast
    if cast > 0:
        post.truth_score = round((upvotes / cast) * 100)

    return cast


def run_cron_generate(db: Session) -> dict:
    """Generate posts, comments, and votes. Returns stats."""
    generated = generate_posts_with_groq(count=2)
    if not generated:
        return {"ok": False, "reason": "no_groq_or_empty", "created": 0}

    tags_by_name = {t.name: t for t in db.query(Tag).all()}
    if not tags_by_name:
        return {"ok": False, "reason": "no_tags", "created": 0}

    existing_slugs = {r[0] for r in db.query(Post.slug).all()}
    created = 0
    comments_created = 0
    votes_cast = 0
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
        db.flush()

        # Sequential comments — each commenter sees the thread so far
        comments_data = generate_comments_sequential(title, content, is_true, count=5)
        for idx, c in enumerate(comments_data):
            author_name = c["author_name"]
            if author_name not in REGULAR_NAMES:
                continue
            comment = Comment(
                post_id=post.id,
                author_name=author_name,
                content=c["content"],
                created_at=now + timedelta(minutes=idx + 1),
            )
            db.add(comment)
            comments_created += 1

        # Regulars cast votes
        votes_cast += cast_votes_for_post(post, db)
        created += 1

    if created:
        db.commit()
    return {
        "ok": True,
        "created": created,
        "comments": comments_created,
        "votes": votes_cast,
        "attempted": len(generated),
    }
