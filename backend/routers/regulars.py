from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db
from models import Comment, Vote

router = APIRouter(prefix="/api/regulars", tags=["regulars"])

REGULARS = ["maroco", "The real CR7", "Kolodin", "kris", "leo", "sass the spurs fan", "viljandi tann", "talis chelsea fan", "shiki"]

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
    result = []
    for name in REGULARS:
        comments = db.query(func.count(Comment.id)).filter(Comment.author_name == name).scalar()
        result.append({
            "name": name,
            "comments": comments,
        })
    result.sort(key=lambda x: x["comments"], reverse=True)
    return result
