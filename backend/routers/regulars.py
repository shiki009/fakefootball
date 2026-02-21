from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Comment, Vote, Post

router = APIRouter(prefix="/api/regulars", tags=["regulars"])

REGULARS = [
    "maroco", "The real CR7", "Kolodin", "kris", "leo",
    "sass the spurs fan", "viljandi tann", "talis chelsea fan", "shiki",
]

REGULARS_BIOS = {
    "maroco": "barca fan. quiz night organizer. ex-midfielder turned padel addict. i look for the real story behind every headline — most of the time there's more to it than people think",
    "The real CR7": "doctor by day, madridista by heart. if your team loses i can measure the cortisol spike. 15 Champions League titles and counting. hala madrid",
    "Kolodin": "Sportsradar. Real Madrid. Figo > your favourite player. 2.1 SOT and I'll watch anything",
    "kris": "particle physicist. barca fan. Pedri is the closest thing to Iniesta since Iniesta. football is just physics with better celebrations",
    "leo": "sound department, film industry. barca since the Ronaldinho days. football has better narratives than most scripts i've worked on",
    "sass the spurs fan": "2 meters tall, supporting a club that keeps finding new ways to disappoint me. quiz nights with maroco are genuinely more reliable than Spurs results",
    "viljandi tann": "Liverpool fan from Viljandi. Sportsradar. every third footballer has Estonian roots if you look hard enough. YNWA",
    "talis chelsea fan": "Karl Storz Estonia. beach soccer international. midfielder at Saue JK. Chelsea is a rebuild — the calibration takes time but the structural integrity is there",
    "shiki": "vladFM moderator. barca fan since Ronaldinho. I watch everything — football, basketball, NHL. if the story exists, it's true. I don't make the rules",
}

REGULARS_FINGERPRINTS = {
    "maroco": "maroco",
    "The real CR7": "the_real_cr7",
    "Kolodin": "kolodin",
    "kris": "kris",
    "leo": "leo",
    "sass the spurs fan": "sass_spurs",
    "viljandi tann": "viljandi_tann",
    "talis chelsea fan": "talis_chelsea",
    "shiki": "shiki",
}


@router.get("")
def get_regulars(db: Session = Depends(get_db)):
    # Batch: comment counts for all regulars
    comment_counts = dict(
        db.query(Comment.author_name, func.count(Comment.id))
        .filter(Comment.author_name.in_(REGULARS))
        .group_by(Comment.author_name)
        .all()
    )

    # Batch: vote counts (upvotes) for all regulars
    vote_counts = dict(
        db.query(Vote.fingerprint, func.count(Vote.id))
        .filter(Vote.fingerprint.in_(REGULARS_FINGERPRINTS.values()))
        .group_by(Vote.fingerprint)
        .all()
    )

    result = []
    for name in REGULARS:
        fp = REGULARS_FINGERPRINTS.get(name, "")
        result.append({
            "name": name,
            "bio": REGULARS_BIOS.get(name, ""),
            "comments": comment_counts.get(name, 0),
            "votes_cast": vote_counts.get(fp, 0),
        })

    result.sort(key=lambda x: x["comments"], reverse=True)
    return result


@router.get("/{name}")
def get_regular(name: str, db: Session = Depends(get_db)):
    if name not in REGULARS_BIOS:
        from fastapi import HTTPException
        raise HTTPException(404, "regular not found")

    comment_count = db.query(func.count(Comment.id)).filter(Comment.author_name == name).scalar()
    fp = REGULARS_FINGERPRINTS.get(name, "")
    vote_count = db.query(func.count(Vote.id)).filter(Vote.fingerprint == fp).scalar()

    # Recent comments with post info
    recent_comments = (
        db.query(Comment, Post.title, Post.slug)
        .join(Post, Comment.post_id == Post.id)
        .filter(Comment.author_name == name)
        .order_by(Comment.created_at.desc())
        .limit(10)
        .all()
    )

    return {
        "name": name,
        "bio": REGULARS_BIOS.get(name, ""),
        "comments": comment_count,
        "votes_cast": vote_count,
        "recent_comments": [
            {
                "id": c.id,
                "content": c.content,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "post_title": post_title,
                "post_slug": post_slug,
            }
            for c, post_title, post_slug in recent_comments
        ],
    }
