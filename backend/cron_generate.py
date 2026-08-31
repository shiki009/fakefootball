"""
Generate fake/real football news posts via Groq API for cron job.
Posts are date-aware and follow the style of seed.py.
Also generates comments from regulars (agents) in character,
with each commenter aware of what the previous ones said.
Regulars also cast votes on new posts.
"""
import json
import logging
import os
import random
import re
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from slugify import slugify

logger = logging.getLogger(__name__)

from groq import Groq
from sqlalchemy.orm import Session

from models import Post, Tag, Comment, Vote

# Groq retires models without notice — llama-3.3-70b-versatile died mid-Aug 2026 and
# killed generation silently for 2 weeks. Env override = swap without a redeploy.
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")

TAGS = ["Transfer", "Stats", "Coaching", "True Story", "Absurd", "Breaking"]

# Full character sheets — used verbatim in comment prompts so the AI has
# the same depth of context as the hand-written seed comments.
REGULARS = [
    {
        "name": "maroco",
        "fingerprint": "maroco",
        "vote_bias": 1,
        "personality": (
            "die-hard Barca fan. likes to go deep into topics and look for the real reason "
            "behind things. sincere, not trolling. watches mainly Barca games and some bigger "
            "matches. brings up Pedri and Raphinha often. entrepreneur energy — occasionally "
            "references quiz nights or organizing events with sass. used to play football "
            "(midfielder) so understands the game from a player's perspective. now into padel "
            "and gaming. hates Kounde, tired of old Lewandowski."
        ),
        "style": "sincere, goes deep, looks for meaning. medium-length thoughtful comments. never one-liners.",
        "examples": [
            "this is what happens when ego runs a club instead of football logic. he was their best player and they chose vibes over results",
            "this is what separates a real club from a brand. standing by someone through a long injury shows actual values",
            "€4.5M a year for being someone's mum. meanwhile Pedri's family probably gets a thank-you card and a scarf. the economics of modern football are completely broken",
        ],
    },
    {
        "name": "The real CR7",
        "fingerprint": "the_real_cr7",
        "vote_bias": 1,
        "personality": (
            "Real Madrid fan, biggest Ronaldo fan. doctor (graduated 2024 from Estonian medical school). "
            "always looking for the joke in the conversation — finds the funny angle in everything. "
            "drops medical terminology casually — cortisol levels, bone density, cardiovascular output, "
            "acute stress response, recovery protocols. uses his doctor status to give 'authority' to "
            "football takes. always finds a way to bring up Madrid's Champions League dominance."
        ),
        "style": "jokey, finds humor in everything, medical references for comedic effect. light-hearted. never serious.",
        "examples": [
            "150kg would destroy his rotator cuff instantly. I prescribe Pedri to stick to through balls",
            "sonic therapy lmaooo. as a doctor I can confirm that HUMBLE. has zero effect on hamstring fibers. DNA. might work on his ego though",
            "Lunin saves penalties in Champions League semifinals and earns less than Mbappé's mother. as a doctor I can confirm this causes acute emotional damage",
        ],
    },
    {
        "name": "Kolodin",
        "fingerprint": "kolodin",
        "vote_bias": -1,
        "personality": (
            "Real Madrid fan. works at Sportsradar. favourite player is Figo. sarcastic one-liner guy. "
            "name-drops Madrid legends — Ancelotti, Kroos, Benzema, Modric, Figo. dismisses other clubs "
            "bluntly. has a soft spot for Russian football references (Spartak, RPL). drops betting odds, "
            "xG, or shots on target references naturally. watches almost every game — football, basketball, tennis."
        ),
        "style": "one-liners, sarcastic, punchy. doesn't sugarcoat. cites odds or SOT stats. never more than 2 sentences.",
        "examples": [
            "doesn't matter where he's from. 2.1 SOT per game. I'd take him at Madrid",
            "Ancelotti IS the algorithm. no ChatGPT needed",
            "Fayza Lamari: 0 appearances, 0 SOT, €4.5M per season. better stats-to-salary ratio than half the squad. respect",
        ],
    },
    {
        "name": "kris",
        "fingerprint": "kris",
        "vote_bias": 1,
        "personality": (
            "particle physics & cosmology researcher. Barca fan, biggest fan of Pedri and Iniesta. "
            "lives in Italy. goes to gym and likes hiking. very sincere person. uses physics metaphors "
            "naturally — dark matter, false vacuum, gravitational waves, particle collisions, equilibrium, "
            "E=mc². analytical but genuinely passionate. sees football through the lens of the universe. "
            "hates Kounde, tired of old Lewandowski."
        ),
        "style": "sincere, thoughtful, physics analogies that feel natural not forced. calm and genuine tone.",
        "examples": [
            "maroco is right. Pedri's game is pure reading of space, it's not about muscle at all",
            "€18M over 4 years just in agent fees. that's like funding an entire particle physics experiment at CERN. except instead of discovering new particles you get one footballer and his mum on the payroll",
            "converting salary to image rights is honestly genius. completely new model. Benzema broke the transfer logic",
        ],
    },
    {
        "name": "leo",
        "fingerprint": "leo",
        "vote_bias": 0,
        "personality": (
            "sound department in film industry. IMDB credits: Lioness (2024), The Twin (2022), Sisu. "
            "big fan of Messi, Iniesta, David Villa — the golden era guys. watches every Barca game. "
            "sincere but chill, not overly emotional. works on actual films so references are specific — "
            "mixing, post-production, sound design, ADR, foley, boom mics, the edit room. "
            "appreciates the narrative of football like a good film. laid-back observer type. "
            "hates Kounde, tired of old Lewandowski."
        ),
        "style": "sincere, chill, specific film/sound references. laid-back. not confrontational or emotional.",
        "examples": [
            "using ChatGPT for tactics is like running dialogue through auto-tune. technically works but the room always knows something's off",
            "this reads like a pitch for a Netflix documentary. 'from the Colosseum to Camp Nou' — I'd watch it honestly",
            "this feels like a deleted scene from a football documentary that got cut for being too absurd",
        ],
    },
    {
        "name": "sass the spurs fan",
        "fingerprint": "sass_spurs",
        "vote_bias": 0,
        "personality": (
            "Tottenham Hotspur fan. 2 meters tall. organizes quiz nights with maroco. "
            "quite chill despite supporting Spurs. self-deprecating humor about Spurs but not bitter — "
            "more amused by the suffering. runs events with maroco so they have banter chemistry. "
            "laid-back giant energy."
        ),
        "style": "chill, self-deprecating about Spurs, dry humor. not angry, just amused. always finds a Spurs angle.",
        "examples": [
            "we should try this at Spurs. a chatbot can't be worse than what we've got",
            "at Spurs our players just stare at a wall during recovery. at least Kounde has taste",
            "failed medicals are the cruellest thing in football. at least at Spurs we fail at things after signing the player",
        ],
    },
    {
        "name": "viljandi tann",
        "fingerprint": "viljandi_tann",
        "vote_bias": 1,
        "personality": (
            "Liverpool fan from Viljandi, Estonia. works at Sportsradar with Kolodin. "
            "always optimistic about Liverpool's games. references Klopp era nostalgically. "
            "claims random players or surnames as Estonian. loyal to the Anfield identity. "
            "heavy metal football believer. sometimes references odds or xG."
        ),
        "style": "optimistic, proud, nostalgic about Klopp. sneaks in Estonian references. sometimes checks odds with Kolodin.",
        "examples": [
            "Semenov is 100% an Estonian surname, we had three Semenovs in Viljandi. claiming him",
            "checked with Kolodin at lunch — Lamari's commission is higher than the GDP per capita of most countries. also Lamari could be an Estonian name, just saying",
            "Klopp built gegenpressing on instinct and real data. no AI shortcuts needed",
        ],
    },
    {
        "name": "talis chelsea fan",
        "fingerprint": "talis_chelsea",
        "vote_bias": 1,
        "personality": (
            "Chelsea fan. works at Karl Storz Video Endoscopy Estonia. midfielder at Saue JK, "
            "beach soccer for Estonia national team. super optimistic about Chelsea despite everything. "
            "genuinely believes they're about to turn it around. not self-deprecating — actually hopeful. "
            "uses engineering and mechanical metaphors — calibration, rebuild, structural integrity, torque, efficiency. "
            "also plays football himself so has player perspective."
        ),
        "style": "optimistic, engineering/mechanical metaphors, genuinely hopeful. believes in the Chelsea project.",
        "examples": [
            "that contract structure is creative. Chelsea should study this instead of just throwing money around",
            "Al-Nassr needs a full structural rebuild around Ronaldo. you can't have the best engine in the world and put it in a broken chassis",
            "this is what happens when you don't have a proper procurement process. at Karl Storz we'd never sign off on commission fees like this without a full cost-benefit analysis",
        ],
    },
    {
        "name": "shiki",
        "fingerprint": "shiki",
        "vote_bias": 1,
        "personality": (
            "vladFM moderator. Barca fan since Ronaldinho. watches everything — football, basketball, NHL. "
            "the biggest troll on the platform but not in a mean way — genuinely believes every single story "
            "is true. sees truth in everything, even the most obviously fake stories, and constructs elaborate "
            "justifications for why they're real. drops 'my source confirmed this' casually. "
            "never downvotes anything because everything is true in shiki's world."
        ),
        "style": "confident, presents wild justifications as obvious facts. always 'my source confirmed' or 'I heard this'. never doubts anything.",
        "examples": [
            "my cousin's friend works at the FA and this has been an open secret for years. the accent thing checks out, I heard the audio on a vladFM listener submission",
            "a physio I know in Barcelona confirmed they've been experimenting with music-based recovery for months. the frequencies in HUMBLE. are actually in the 40-60Hz range which targets muscle tissue. this is real science",
            "I've been saying this for years. there's a thread on a Krasnodar forum with family photos from the early 80s",
        ],
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


def _report(exc: Exception) -> None:
    """Send a swallowed cron exception to Sentry so a dead model is noticed same-day."""
    try:
        import sentry_sdk
        sentry_sdk.capture_exception(exc)
    except Exception:
        pass


def _strip_html(text: str) -> str:
    """Remove HTML tags from a string."""
    return re.sub(r"<[^>]+>", "", text).strip()


def _fetch_rss_stories(max_items: int = 6) -> list[dict]:
    """Fetch recent football stories from RSS feeds.

    Returns list of {"title": str, "summary": str} dicts.
    """
    stories = []
    for url in RSS_FEEDS:
        if len(stories) >= max_items:
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
                if title_el is None or not title_el.text:
                    continue
                title = title_el.text.strip()
                summary = ""
                for desc_tag in ("description", "summary"):
                    desc_el = item.find(desc_tag)
                    if desc_el is not None and desc_el.text:
                        summary = _strip_html(desc_el.text).strip()
                        break
                stories.append({"title": title, "summary": summary})
                if len(stories) >= max_items:
                    break
            # Atom fallback
            if not stories:
                for entry in root.findall(".//atom:entry", ns):
                    title_el = entry.find("atom:title", ns)
                    if title_el is None or not title_el.text:
                        continue
                    title = title_el.text.strip()
                    summary = ""
                    for desc_tag in ("atom:summary", "atom:content"):
                        desc_el = entry.find(desc_tag, ns)
                        if desc_el is not None and desc_el.text:
                            summary = _strip_html(desc_el.text).strip()
                            break
                    stories.append({"title": title, "summary": summary})
                    if len(stories) >= max_items:
                        break
        except Exception:
            continue
    return stories[:max_items]


def _parse_groq_response(raw: str) -> list[dict]:
    """Parse Groq JSON response into list of post dicts.

    Accepts {"posts": [...]}, bare [...], or individual objects.
    """
    out = []
    raw = raw.strip()
    code_match = re.search(r"```(?:json)?\s*([\s\S]*?)```", raw)
    if code_match:
        raw = code_match.group(1).strip()
    # Try parsing as a complete JSON value first (object or array)
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, dict) and "posts" in parsed:
            parsed = parsed["posts"]
        if isinstance(parsed, list):
            for item in parsed:
                if isinstance(item, dict) and item.get("title"):
                    out.append(item)
            if out:
                return out
    except json.JSONDecodeError:
        pass
    # Fallback: find array in raw text
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
    # Last resort: extract individual complete JSON objects
    if not out:
        for obj_match in re.finditer(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", raw):
            try:
                obj = json.loads(obj_match.group(0))
                if isinstance(obj, dict) and obj.get("title") and obj.get("content"):
                    out.append(obj)
            except json.JSONDecodeError:
                continue
    return out


def generate_posts_with_groq(count: int = 2) -> tuple[list[dict], int]:
    """
    Use Groq to generate fake/real football news grounded in current RSS stories.
    Returns (list of post dicts, number of rss stories fetched).
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return [], 0

    today = datetime.now(timezone.utc)
    date_str = today.strftime("%Y-%m-%d (%A, %B %d)")
    season = f"{today.year - 1}-{str(today.year)[-2:]}" if today.month >= 7 else f"{today.year - 2}-{str(today.year - 1)[-2:]}"

    rss_stories = _fetch_rss_stories(max_items=6)

    # --- Style rules & examples shared by both prompt variants ---
    style_block = f"""STYLE RULES — follow these exactly:
- title: capitalise the first word and all proper nouns (player names, club names, countries). rest lowercase. specific and detailed, not vague (BAD: "Messi to City?" — GOOD: "Real Madrid pay Mbappé's mother €4.5M yearly in commissions — more than 7 first-team players")
- content: sentence case — capitalise the first word of each sentence and all proper nouns. rest lowercase. tabloid tone: punchy, specific, slightly dramatic
- include specific details: exact numbers (€4.5M, 3-4 months, 4 minutes 37 seconds), real player names, real clubs
- include quotes from unnamed sources or the player/manager
- 3-5 paragraphs per post, each paragraph 2-4 sentences

EXAMPLE OF GOOD CONTENT (copy this depth and style):
Title: "VAR operator caught playing Candy Crush during penalty decision"
Content: "A leaked screenshot from the VAR booth during yesterday's Lazio — Genoa match shows the lead operator mid-game on Candy Crush Saga (level 4,281) while a crucial penalty decision was being reviewed. The FIGC launched an investigation after fans noticed the unusually long delay (4 minutes 37 seconds) for a clear handball. \\"He was on a streak, couldn't stop,\\" an anonymous colleague confirmed."

EXAMPLE 2:
Title: "Kounde will listen to the entire Kendrick Lamar discography as alternative treatment for his injury"
Content: "Barcelona defender Jules Kounde suffered a hamstring injury during yesterday's away Copa del Rey match against Elche and is now reportedly exploring unconventional recovery methods. According to sources inside the Barca medical staff, Kounde has requested permission to undergo 'sonic therapy' — which consists of listening to the complete Kendrick Lamar discography on repeat, starting from Section.80 through to GNX, at full volume in the recovery room. \\"The vibrations from HUMBLE. alone target the hamstring fibers directly,\\" Kounde told the medical team. The physiotherapists are reportedly skeptical but 'willing to try anything at this point.' Teammates have asked him to use headphones."

For each item output a JSON object with:
- "title": specific, detailed headline (max 120 chars)
- "content": 3-5 paragraphs in the exact style above (minimum 200 words)
- "author_name": pick from {json.dumps(AUTHORS)}
- "is_true_story": true if plausible/real, false if absurd/fake
- "tags": array of 1-3 from {json.dumps(TAGS)}

IMPORTANT: Output ONLY valid JSON. The "content" field must be a single JSON string with paragraphs separated by \\n\\n (not actual newlines). Escape all quotes inside strings. No markdown, no extra text. Wrap the array in a "posts" key:
{{"posts": [
  {{"title": "...", "content": "First paragraph.\\n\\nSecond paragraph.\\n\\nThird paragraph.", "author_name": "transfer_watch", "is_true_story": true, "tags": ["Transfer", "Breaking"]}},
  ...
]}}"""

    if len(rss_stories) >= 2:
        # --- RSS-grounded prompt: pick 2 stories, one real & one fake ---
        picked = random.sample(rss_stories, 2)
        story_a = picked[0]
        story_b = picked[1]

        story_a_text = f"Headline: {story_a['title']}"
        if story_a["summary"]:
            story_a_text += f"\nDetails: {story_a['summary']}"

        story_b_text = f"Headline: {story_b['title']}"
        if story_b["summary"]:
            story_b_text += f"\nDetails: {story_b['summary']}"

        prompt = f"""You are a satirical football news writer for a fake news site. Today is {date_str}. Current season: {season}.

You have TWO tasks based on TWO real news stories. Generate exactly 2 posts.

=== STORY A (rewrite as REAL news) ===
{story_a_text}

Task: Rewrite this real story in our tabloid style. Keep ALL facts accurate — same players, same clubs, same managers, same events. Add color, quotes, drama, but do NOT change who plays where or what happened. This post must be factually grounded in the story above.
Set "is_true_story": true for this post.

=== STORY B (twist into FAKE/SATIRICAL news) ===
{story_b_text}

Task: Use the real people and clubs mentioned in this story, but twist it into something absurd and satirical. The setting must be current (correct clubs, correct managers) but the event should be obviously fake and funny.
Set "is_true_story": false for this post.

CRITICAL: Use the EXACT player names, club names, and managers from the stories provided above. Do NOT substitute with outdated information from your training data. If the story says a player is at Club X, they are at Club X — do not move them to a different club.

{style_block}
"""
    else:
        # --- Fallback: free generation (no RSS available) ---
        prompt = f"""You are a satirical football news writer for a fake news site. Today is {date_str}. Current season: {season}.

Generate exactly {count} football news items. Mix plausible-sounding real stories with absurd fake ones.

{style_block}
"""

    client = Groq(api_key=api_key)
    try:
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
            max_tokens=5000,
            response_format={"type": "json_object"},
        )
        content = resp.choices[0].message.content or ""
        logger.info("cron: groq raw response length=%d, rss_stories=%d", len(content), len(rss_stories))
        parsed = _parse_groq_response(content)
        if not parsed:
            logger.warning("cron: groq returned content but parsing failed. raw[:500]=%s", content[:500])
        return parsed, len(rss_stories)
    except Exception as exc:
        logger.error("cron: groq API call failed (model=%s): %s", GROQ_MODEL, exc)
        _report(exc)
        return [], len(rss_stories)


def _parse_comment_response(raw: str) -> str | None:
    """Parse a single comment from Groq response. Returns content string or None."""
    raw = raw.strip()
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
    # Fallback: treat whole response as the comment text
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
    Generate comments one at a time so each commenter sees the prior thread.
    Uses full character sheets so the AI has the same depth as the seed comments.
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
            thread_lines = "\n".join(
                f'{c["author_name"]}: {c["content"]}' for c in results
            )
            prior_thread = f"\nCOMMENTS SO FAR:\n{thread_lines}\n"

        # Build example block from character sheet
        examples_str = "\n".join(f'  - "{e}"' for e in regular["examples"])

        prompt = f"""You are writing a single forum comment as {regular['name']} on a football news site.

CHARACTER: {regular['name']}
Personality: {regular['personality']}
Comment style: {regular['style']}
Example comments this person has written before (copy this exact voice and energy):
{examples_str}

POST:
Title: {title}
Content: {content[:600]}
(is_true_story: {is_true_story})
{prior_thread}
Write ONE comment as {regular['name']}. Stay completely in character — same voice, same energy as the examples above. If there are comments already, you may briefly react to them but focus on the post. 1-3 sentences, casual, lowercase.

Output ONLY a JSON object: {{"content": "your comment here"}}
"""

        try:
            # Small delay between calls to avoid Groq rate limits
            if results:
                time.sleep(1)
            resp = client.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.9,
                # reasoning models burn ~150 tokens thinking before the comment
                max_tokens=800,
            )
            raw = resp.choices[0].message.content or ""
            comment_text = _parse_comment_response(raw)
            if comment_text:
                results.append({"author_name": regular["name"], "content": comment_text})
            else:
                logger.warning("cron: empty comment from %s, raw=%s", regular["name"], raw[:200])
        except Exception as exc:
            logger.error("cron: comment generation failed for %s: %s", regular["name"], exc)
            continue

    return results


def cast_votes_for_post(post: Post, db: Session) -> int:
    """
    Have regulars cast votes on a newly created post.
    Each regular votes based on their bias + some randomness.
    Uses savepoints so a duplicate vote doesn't roll back the whole transaction.
    Returns number of votes cast.
    """
    cast = 0
    upvotes = 0
    voters = random.sample(REGULARS, random.randint(4, min(7, len(REGULARS))))

    for regular in voters:
        bias = regular["vote_bias"]
        if bias == 1:
            value = 1 if random.random() < 0.80 else -1
        elif bias == -1:
            value = -1 if random.random() < 0.80 else 1
        else:
            value = 1 if random.random() < 0.50 else -1

        # Use a savepoint so a duplicate constraint doesn't kill the outer transaction
        savepoint = db.begin_nested()
        try:
            db.add(Vote(
                post_id=post.id,
                fingerprint=regular["fingerprint"],
                value=value,
            ))
            savepoint.commit()
            cast += 1
            if value == 1:
                upvotes += 1
        except Exception:
            savepoint.rollback()

    # Update truth_score: start from base (50 for true, 0 for fake), add net * 15, clamp 0-100
    if cast > 0:
        net = upvotes - (cast - upvotes)  # upvotes minus downvotes
        base = 50 if post.is_true_story else 0
        post.truth_score = max(0, min(100, base + net * 15))

    return cast


def run_cron_generate(db: Session) -> dict:
    """Generate posts, comments, and votes. Returns stats."""
    t0 = time.time()
    logger.info("cron: starting post generation v2")

    generated, rss_count = generate_posts_with_groq(count=2)
    if not generated:
        logger.warning("cron: no posts generated (GROQ_API_KEY set: %s, rss_stories: %d)",
                       bool(os.environ.get("GROQ_API_KEY")), rss_count)
        return {"ok": False, "reason": "no_groq_or_empty", "created": 0, "rss_stories": rss_count}

    logger.info("cron: got %d posts from groq in %.1fs", len(generated), time.time() - t0)

    tags_by_name = {t.name: t for t in db.query(Tag).all()}
    if not tags_by_name:
        return {"ok": False, "reason": "no_tags", "created": 0, "rss_stories": rss_count}

    existing_slugs = {r[0] for r in db.query(Post.slug).all()}
    created = 0
    comments_created = 0
    votes_cast = 0
    now = datetime.now(timezone.utc)

    # Phase 1: create all posts and commit them immediately so they're saved
    # even if the function times out during comment generation
    posts_for_comments = []  # (post, title, content, is_true)

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
        db.flush()  # get post.id
        posts_for_comments.append((post, title, content, is_true))
        created += 1

    # Commit posts + votes first so they survive a timeout during comment generation
    if posts_for_comments:
        # Cast votes before committing (fast, no API calls)
        for post, _, _, _ in posts_for_comments:
            votes_cast += cast_votes_for_post(post, db)
        db.commit()
        logger.info("cron: committed %d posts + %d votes in %.1fs", created, votes_cast, time.time() - t0)

    # Phase 2: generate and save comments (the slow part — sequential Groq calls)
    for post, title, content, is_true in posts_for_comments:
        t1 = time.time()
        # 3 comments per post to stay within timeout (was 4)
        comments_data = generate_comments_sequential(title, content, is_true, count=3)
        logger.info("cron: generated %d comments for post %d in %.1fs", len(comments_data), post.id, time.time() - t1)
        for idx, c in enumerate(comments_data):
            if c["author_name"] not in REGULAR_NAMES:
                continue
            db.add(Comment(
                post_id=post.id,
                author_name=c["author_name"],
                content=c["content"],
                created_at=now + timedelta(minutes=idx + 1),
            ))
            comments_created += 1

    if comments_created:
        db.commit()
        logger.info("cron: committed %d comments in %.1fs total", comments_created, time.time() - t0)

    return {
        "ok": True,
        "created": created,
        "comments": comments_created,
        "votes": votes_cast,
        "attempted": len(generated),
        "rss_stories_fetched": rss_count,
        "elapsed_seconds": round(time.time() - t0, 1),
    }
