import json
import os
from sqlalchemy.orm import Session
from models import Base, Post, Tag, Comment, Vote, post_tags
from slugify import slugify
from datetime import datetime, timezone, timedelta

USER_COMMENTS_PATH = os.path.join(os.path.dirname(__file__), "user_comments.json")


def run(db: Session):
    if db.query(Post).first():
        return  # already seeded

    # tags
    tags = {}
    for name, color in [
        ("Transfer", "#3b82f6"),
        ("Stats", "#8b5cf6"),
        ("Coaching", "#f59e0b"),
        ("True Story", "#22c55e"),
        ("Absurd", "#ef4444"),
        ("Breaking", "#ec4899"),
    ]:
        t = Tag(name=name, slug=slugify(name), color=color)
        db.add(t)
        tags[name] = t

    db.flush()

    # posts
    posts_data = [
        {
            "title": "Semenyo is actually from Russia, lived there till 15, real surname is Semenov",
            "content": (
                "sources close to the footballer's family have revealed that Manchester City's Antoine Semenyo "
                "was actually born in Novosibirsk, Russia, under the name Anton Semenov. he reportedly moved "
                "to London at 15 and changed his identity to pursue a career in the Premier League. "
                "\"his Russian was perfect when he arrived,\" says an unnamed former schoolmate. "
                "the FA is said to be looking into the matter."
            ),
            "author_name": "deep_throat_fc",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Transfer", "Breaking"],
            "created_at": datetime(2026, 1, 24, 14, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Talisca left Al Nassr because he was scoring too many goals",
            "content": (
                "in what might be the most absurd transfer saga of the decade, Anderson Talisca reportedly "
                "left Al Nassr because the club felt he was scoring too many goals and making the other "
                "players feel inadequate. Cristiano Ronaldo allegedly filed a complaint with the board "
                "after Talisca scored a hat-trick in a match where CR7 went scoreless. "
                "\"it was him or me,\" Ronaldo reportedly said. Talisca moved on."
            ),
            "author_name": "saudi_insider",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["True Story"],
            "created_at": datetime(2026, 1, 29, 14, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Roberto Moreno used ChatGPT for tactical decisions at FC Sochi — got sacked",
            "content": (
                "former Spain interim coach Roberto Moreno, while managing FC Sochi in the Russian Premier League, "
                "was caught using ChatGPT to generate his tactical plans. players became suspicious when "
                "the formation changed every game and the pre-match talks sounded like \"corporate synergy emails.\" "
                "the club confirmed his dismissal, stating: \"we respect AI, but not as a head coach.\""
            ),
            "author_name": "rpl_watcher",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Coaching", "True Story"],
            "created_at": datetime(2026, 1, 21, 10, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Pedri bench presses 150kg, says it helps his passing range",
            "content": (
                "Barcelona's Pedri has reportedly been bench pressing 150kg in the gym, "
                "claiming the raw power translates directly to his passing range. "
                "\"every kilo on the bar is another meter on my through balls,\" the 21-year-old said. "
                "teammates were reportedly shocked when he asked Araujo to spot him. "
                "Xavi declined to comment but was seen googling \"can muscles help passing\" during training."
            ),
            "author_name": "barca_leaks",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Stats", "Absurd"],
            "created_at": datetime(2022, 11, 14, 9, 30, tzinfo=timezone.utc),
        },
        {
            "title": "Kamuto Hirovato — Xavi plans to replace ter Stegen with a GK who also plays libero",
            "content": (
                "in a bold tactical move, Xavi has reportedly identified Japanese goalkeeper Kamuto Hirovato "
                "as a revolutionary signing for Barcelona. the keeper, who plays without gloves and regularly "
                "dribbles past strikers, would essentially eliminate the goalkeeper position entirely. "
                "\"we don't need a keeper if the keeper IS the defense,\" Xavi reportedly told the board. "
                "ter Stegen is said to be \"confused but intrigued.\""
            ),
            "author_name": "catalan_express",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Transfer", "Breaking", "Absurd"],
            "created_at": datetime(2022, 12, 3, 15, 0, tzinfo=timezone.utc),
        },
        {
            "title": "VAR operator caught playing Candy Crush during penalty decision",
            "content": (
                "a leaked screenshot from the VAR booth during yesterday's Lazio — Genoa match shows "
                "the lead operator mid-game on Candy Crush Saga (level 4,281) while a crucial penalty "
                "decision was being reviewed. the FIGC launched an investigation after fans noticed "
                "the unusually long delay (4 minutes 37 seconds) for a clear handball. "
                "\"he was on a streak, couldn't stop,\" an anonymous colleague confirmed."
            ),
            "author_name": "calcio_mole",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Absurd"],
            "created_at": datetime(2026, 1, 25, 20, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Haaland eats exclusively Norwegian fish, says it's the secret to his power",
            "content": (
                "Manchester City striker Erling Haaland has revealed that his diet consists entirely "
                "of Norwegian fish — specifically cod, salmon, and a mysterious \"arctic char\" "
                "that his father imports weekly from Bryne. \"I haven't eaten anything that wasn't "
                "swimming in a fjord,\" Haaland told reporters. Pep Guardiola reportedly tried the diet "
                "for a week and lost his voice."
            ),
            "author_name": "nordic_scoop",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Stats", "Absurd"],
            "created_at": datetime(2026, 1, 26, 12, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Laporta to renew Christensen's contract as a gesture after devastating injury",
            "content": (
                "Barcelona president Joan Laporta is reportedly planning to offer Andreas Christensen "
                "a one-year contract extension with a reduced salary as a goodwill gesture. "
                "the Danish defender has been greatly affected by his long-term injury, and the club "
                "wants to show loyalty to a player who has been professional throughout his recovery. "
                "\"Andreas deserves to know we haven't forgotten him,\" a source close to the board said. "
                "Christensen is said to be moved by the gesture."
            ),
            "author_name": "barca_insider",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Transfer", "True Story"],
            "created_at": datetime(2025, 12, 25, 12, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Sergio Ramos vs Andrew Tate — official boxing match announced by Misfits Boxing",
            "content": (
                "Misfits Boxing has reportedly announced a fight between former Real Madrid captain "
                "Sergio Ramos and controversial internet personality Andrew Tate. the bout is set "
                "for August 22nd in Doha, Qatar, with 6 rounds of 3 minutes at a 195 lbs weight limit. "
                "the fight will be streamed exclusively on Rumble Premium. "
                "Ramos, known for his aggressive style on the pitch, reportedly said: "
                "\"I've been collecting red cards my whole career, now I'll collect punches.\" "
                "Tate responded with a 47-minute podcast episode about it."
            ),
            "author_name": "misfits_leak",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Breaking", "Absurd"],
            "created_at": datetime(2026, 1, 30, 18, 0, tzinfo=timezone.utc),
        },
        {
            "title": "PSG president Al-Khelaifi attacked match official after Real Madrid loss, broke his chain",
            "content": (
                "the UEFA match report from the PSG — Real Madrid Champions League knockout "
                "confirms that PSG president Nasser Al-Khelaifi was aggressive towards a match official "
                "in the tunnel after the game, physically confronting him and breaking a chain "
                "the official was wearing around his neck. the incident occurred after Real Madrid's "
                "dramatic comeback, which saw PSG eliminated despite leading the tie. "
                "UEFA opened disciplinary proceedings. Al-Khelaifi has not commented publicly."
            ),
            "author_name": "ucl_tunnel_cam",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Breaking", "True Story"],
            "created_at": datetime(2022, 3, 10, 22, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Al-Ittihad offer Benzema zero salary — 100% image rights only",
            "content": (
                "Al-Ittihad have made an extraordinary renewal proposal to their captain Karim Benzema: "
                "zero euros in fixed salary, with the French striker earning 100% of his image rights instead. "
                "Benzema has been playing in Saudi Arabia for three and a half years, scoring 54 goals "
                "in 83 appearances and winning two titles. the deal would be unprecedented in football, "
                "essentially turning Benzema into a self-employed brand ambassador who also happens to play. "
                "(source: L'Equipe via Fabrizio Romano)"
            ),
            "author_name": "romano_tracker",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Transfer", "True Story", "Breaking"],
            "created_at": datetime(2026, 1, 30, 20, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Pedri handling latest injury much better, eager to return for business end of the season",
            "content": (
                "Pedri has taken his latest injury much better than the previous ones. "
                "the Barcelona midfielder is recovering well and is relieved that the team "
                "secured a Champions League top 8 spot without him. "
                "Pedri knows he'll be back for the most important part of the season "
                "and is eager to return. those close to him say his mentality is completely "
                "different this time — focused, patient, and hungry."
            ),
            "author_name": "barca_medical",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["True Story"],
            "created_at": datetime(2026, 1, 30, 21, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Xavi saved Fermín from a loan to Olot or Romania — spotted him in one training session",
            "content": (
                "in 2023, Barcelona did not count on Fermín López. he was probably leaving on loan "
                "to Olot or a Romanian team. however, Xavi saw him in a single training session "
                "and immediately asked the club to keep him. Xavi gave Fermín a chance in pre-season, "
                "and the rest is history. the midfielder has since become a key rotation player "
                "and scored crucial goals in both La Liga and the Champions League."
            ),
            "author_name": "la_masia_insider",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["True Story", "Transfer"],
            "created_at": datetime(2026, 1, 31, 10, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Atlético Madrid reach agreement for Ademola Lookman from Atalanta",
            "content": (
                "Atlético Madrid have reached an agreement for the signing of Ademola Lookman "
                "from Atalanta. the Nigerian forward, who scored a hat-trick in the Europa League "
                "final last season, is set to join Simeone's side in a deal reported by Di Marzio. "
                "Lookman has been one of Serie A's standout performers and Atlético see him as the "
                "missing piece in their attack. Atalanta are reluctant to sell but the player has "
                "reportedly pushed for the move."
            ),
            "author_name": "transfer_watch",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Transfer", "True Story", "Breaking"],
            "created_at": datetime(2026, 1, 31, 14, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Real Madrid submit €100M bid for Tottenham's Cristian Romero",
            "content": (
                "according to Fichajes, Real Madrid have submitted a €100 million bid for "
                "Tottenham Hotspur centre-back Cristian Romero. the Argentine defender has been "
                "one of the Premier League's best defenders since joining Spurs, and Madrid "
                "reportedly see him as the long-term partner for Rüdiger in defence. "
                "Tottenham are said to be reluctant to sell but the offer is significant. "
                "Romero himself has not commented on the speculation."
            ),
            "author_name": "fichajes_alert",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Transfer", "Breaking"],
            "created_at": datetime(2026, 1, 31, 16, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Historians claim Eric Garcia could be descended from ancient Roman gladiators",
            "content": (
                "a group of historians from the University of Barcelona have published a paper "
                "suggesting that Eric Garcia's family lineage traces back to a prominent gladiator "
                "family in Roman Hispania. Dr. Lluís Ferrer, lead author of the study, claims that "
                "the Garcia bloodline from the Mataró region shows 'remarkable overlap' with records "
                "of a gladiator known as Gaius Garcius, who fought in the amphitheatre of Tarraco "
                "in the 2nd century AD. 'the defensive instincts, the positioning, the fearlessness — "
                "it's coded into the DNA,' Dr. Ferrer told Mundo Deportivo. Eric Garcia reportedly "
                "found the study 'interesting but a bit much.' his agent declined to comment on "
                "whether this affects contract negotiations."
            ),
            "author_name": "mundo_deportivo_dig",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Absurd", "Breaking"],
            "created_at": datetime(2026, 1, 31, 19, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Kounde will listen to the entire Kendrick Lamar discography as alternative treatment for his injury",
            "content": (
                "Barcelona defender Jules Kounde suffered a hamstring injury during yesterday's away "
                "Copa del Rey match against Elche (31 January 2026) and is now reportedly exploring "
                "unconventional recovery methods. according to sources inside the Barca medical staff, "
                "Kounde has requested permission to undergo 'sonic therapy' — which consists of listening "
                "to the complete Kendrick Lamar discography on repeat, starting from Section.80 through "
                "to GNX, at full volume in the recovery room. "
                "\"the vibrations from HUMBLE. alone target the hamstring fibers directly,\" Kounde "
                "told the medical team. the physiotherapists are reportedly skeptical but 'willing to try "
                "anything at this point.' Kounde has already completed two full listens of good kid, m.A.A.d city "
                "and claims his range of motion improved by 12%. teammates have asked him to use headphones."
            ),
            "author_name": "barca_medical",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Absurd", "Breaking"],
            "created_at": datetime(2026, 2, 1, 10, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Cristiano Ronaldo refusing to play for Al-Nassr, unhappy with how the club is run",
            "content": (
                "Cristiano Ronaldo is refusing to play for Al-Nassr today. the 40-year-old is reportedly "
                "unhappy with how the club is being run by the Saudi Public Investment Fund compared to "
                "other Saudi Pro League rivals. Ronaldo wants the club to be properly backed so he can "
                "win the league and believes he is the face of Saudi football. "
                "sources close to the player say he has grown frustrated watching Al-Hilal and Al-Ittihad "
                "receive bigger investments while Al-Nassr's squad planning has stagnated. "
                "\"he didn't move to Saudi Arabia to finish second,\" a source told A Bola. "
                "the club has not issued an official statement but training ground sources confirm "
                "Ronaldo was absent from today's session."
            ),
            "author_name": "a_bola_insider",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Breaking", "True Story"],
            "created_at": datetime(2026, 2, 2, 9, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Nicolas Anelka was born in Krasnodar, Russia — original name was Nikolai Panelka",
            "content": (
                "a deep dive into French football archives has uncovered that former Arsenal, "
                "Real Madrid, and Chelsea striker Nicolas Anelka was actually born in Krasnodar, Russia, "
                "under the name Nikolai Panelka. his family reportedly moved to the Parisian suburb of "
                "Trappes when he was two years old and changed the surname from Panelka to Anelka "
                "to sound more French. the discovery was made by an amateur genealogist on a Russian "
                "football forum who noticed the similarity between 'Panelka' and 'Panenka' — leading "
                "to a secondary theory that the famous penalty technique was actually named after "
                "Anelka's original family. the French Football Federation has declined to comment. "
                "Anelka himself posted a single question mark on Instagram."
            ),
            "author_name": "deep_throat_fc",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Absurd", "Breaking"],
            "created_at": datetime(2026, 2, 2, 14, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Mateta to undergo surgery, out 3-4 months after failed AC Milan medical",
            "content": (
                "Crystal Palace striker Jean-Philippe Mateta will undergo surgery and miss "
                "the next 3-4 months of football after his medical visit with AC Milan revealed "
                "an underlying issue. the move to Milan has collapsed as a result. "
                "Mateta was set to complete a transfer to the Serie A club but the medical "
                "flagged a problem that requires immediate surgical intervention. "
                "Crystal Palace are now left with an injured striker and no transfer fee. "
                "Milan are reportedly already looking at alternative targets. "
                "(source: Sacha Tavolieri)"
            ),
            "author_name": "transfer_watch",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Transfer", "Breaking", "True Story"],
            "created_at": datetime(2026, 2, 2, 16, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Ter Stegen injured again — return to Barcelona not yet ruled out",
            "content": (
                "Marc-André ter Stegen has suffered another injury — this time while on loan at Girona. "
                "the German goalkeeper, who has been out since September with a serious knee injury, "
                "had joined Girona on a short-term loan to regain match fitness before returning to Barcelona. "
                "however, he picked up a new injury during a match for Girona, derailing those plans. "
                "Barcelona sources say a return to the squad this season is 'not yet ruled out' "
                "but the timeline has been pushed back significantly. "
                "the club is evaluating whether to bring in emergency cover or trust Joan Garcia "
                "to continue as first choice for the remainder of the campaign. "
                "(source: Reshad Rahman)"
            ),
            "author_name": "barca_medical",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Breaking", "True Story"],
            "created_at": datetime(2026, 2, 2, 18, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Real Madrid pay Mbappé's mother €4.5M yearly in commissions — more than 7 first-team players",
            "content": (
                "Real Madrid pays Fayza Lamari, Kylian Mbappé's mother and agent, €4.5 million per year "
                "in commissions as part of the deal that brought the French star to the Bernabéu. "
                "the total over the 4-season contract amounts to €18 million. "
                "what makes this truly remarkable is that Lamari's annual commission alone is higher "
                "than the salaries of seven current Real Madrid first-team players: Andriy Lunin, "
                "Franco, Asensio, Fran, GG, Brahim Díaz, and Arda Güler. "
                "the numbers highlight the extraordinary cost of the Mbappé operation beyond "
                "the player's own wages, and raise questions about the financial structure "
                "of modern superstar transfers."
            ),
            "author_name": "madrid_books",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Transfer", "True Story", "Stats"],
            "created_at": datetime(2026, 2, 7, 20, 0, tzinfo=timezone.utc),
        },
    ]

    now = datetime.now(timezone.utc)
    posts = []
    for i, pd in enumerate(posts_data):
        p = Post(
            title=pd["title"],
            slug=slugify(pd["title"])[:80],
            content=pd["content"],
            author_name=pd["author_name"],
            is_true_story=pd["is_true_story"],
            truth_score=pd.get("truth_score", 0),
            created_at=pd.get("created_at", now - timedelta(hours=len(posts_data) - i)),
        )
        for tag_name in pd["tags"]:
            p.tags.append(tags[tag_name])
        db.add(p)
        posts.append(p)

    db.flush()

    # --- regulars character prompts ---
    # used as reference for writing comments in their voice

    regulars = {
        "maroco": {
            "real_name": "Marko Alari Lont",
            "club": "FC Barcelona",
            "profession": "self-employed, organizes fun activities (quiz nights etc) — often together with sass. used to play football (midfielder), now plays padel and video games. also disc golf and match poker",
            "personality": (
                "die-hard Barca fan. likes to go deep into topics and look for the real reason "
                "behind things. sincere, not trolling. watches mainly Barca games and some bigger "
                "matches. brings up Pedri and Raphinha often. entrepreneur energy — occasionally "
                "references quiz nights or organizing events. used to play football so understands "
                "the game from a player's perspective. now into padel and gaming. "
                "hates Kounde, tired of old Lewandowski."
            ),
            "style": "sincere, goes deep, looks for meaning. medium-length thoughtful comments.",
        },
        "The real CR7": {
            "real_name": "Andres Dobõšev-Proosväli",
            "club": "Real Madrid",
            "profession": "doctor (graduated 2024 from Estonian medical school). from Haapsalu/Läänemaa. won Russian language olympiad in high school — speaks Russian. also into sports",
            "personality": (
                "Real Madrid fan, biggest Ronaldo fan obviously. always looking for the joke "
                "in the conversation — finds the funny angle in everything. "
                "drops medical terminology casually — cortisol levels, bone density, "
                "cardiovascular output, acute stress response, recovery protocols. "
                "uses his doctor status to give 'authority' to football takes. "
                "always finds a way to bring up Madrid's Champions League dominance."
            ),
            "style": "jokey, finds humor in everything, medical references for comedic effect. light-hearted.",
        },
        "Kolodin": {
            "real_name": "Raiko Tähhe",
            "club": "Real Madrid",
            "profession": "works at Sportsradar (together with viljandi tann). used to play football (midfielder, Haapsalu), now only watches football, basketball, tennis",
            "personality": (
                "watches almost every game — football, basketball, tennis. favourite player is Figo. "
                "looks for shots on target bets often. sarcastic one-liner guy. "
                "name-drops Madrid legends — Ancelotti, Kroos, Benzema, Modric, Figo. "
                "dismisses other clubs bluntly. has a soft spot for Russian football "
                "references (Spartak, RPL). works in sports data so drops betting odds, "
                "xG, or shots on target references naturally."
            ),
            "style": "one-liners, sarcastic, punchy. doesn't sugarcoat. sometimes cites odds or SOT stats.",
        },
        "kris": {
            "real_name": "Kristjan Müürsepp",
            "club": "FC Barcelona",
            "profession": "particle physics & cosmology researcher at NICPB Tallinn / University of Tartu. published in Physical Review D on dark matter, axion physics, gravitational waves, primordial black holes, false vacuum bubbles, neutrino physics",
            "personality": (
                "Barca fan, biggest fan of Pedri, Iniesta — those elegant technical midfielders. "
                "lives in Italy. goes to gym and likes hiking. very sincere person. "
                "uses physics metaphors naturally — dark matter, false vacuum, gravitational waves, "
                "particle collisions, equilibrium, E=mc². analytical but genuinely passionate. "
                "sees football through the lens of the universe. "
                "hates Kounde, tired of old Lewandowski."
            ),
            "style": "sincere, thoughtful, physics analogies that feel natural. calm and genuine tone.",
        },
        "leo": {
            "real_name": "Leonid Bragin",
            "club": "FC Barcelona",
            "profession": "sound department in film industry. IMDB credits: Lioness (2024), The Twin (2022), Kids of the Night (2021), Sisu, The Black Hole, 8 Views of Lake Biwa. sound director on Tartu Film Fund projects",
            "personality": (
                "big fan of Messi, Iniesta, David Villa — the golden era guys. "
                "watches every Barca game. sincere but chill, not overly emotional. "
                "works on actual films so references are specific — mixing, post-production, "
                "sound design, ADR, foley, boom mics, the edit room. "
                "appreciates the narrative of football like a good film. laid-back observer type. "
                "hates Kounde, tired of old Lewandowski like every Barca fan."
            ),
            "style": "sincere, chill, specific film/sound references. laid-back. not confrontational or emotional.",
        },
        "sass the spurs fan": {
            "real_name": "Aleksander Tõnisson",
            "club": "Tottenham Hotspur",
            "profession": "organizes fun activities (quiz nights etc) together with maroco. 2 meters tall",
            "personality": (
                "watches every Tottenham game and some big matches. like 2 meters tall. "
                "quite chill despite supporting Spurs. self-deprecating humor about Spurs "
                "but not bitter — more amused by the suffering. "
                "runs events with maroco so they have banter chemistry. "
                "laid-back giant energy."
            ),
            "style": "chill, self-deprecating but relaxed about it. dry humor. not angry, just amused.",
        },
        "viljandi tann": {
            "real_name": "Tanel Räästas",
            "club": "Liverpool",
            "profession": "works at Sportsradar (together with Kolodin/Raiko) — knows odds, stats, data",
            "personality": (
                "Liverpool fan from Viljandi, Estonia. always optimistic about Liverpool's games. "
                "references Klopp era nostalgically. claims random players or surnames as Estonian. "
                "loyal to the Anfield identity. heavy metal football believer. "
                "works in sports data so sometimes references odds or xG. "
                "has Sportsradar banter with Kolodin."
            ),
            "style": "optimistic, proud, nostalgic about Klopp. sneaks in Estonian references and data takes.",
        },
        "talis chelsea fan": {
            "real_name": "Talis Tamm",
            "club": "Chelsea",
            "profession": "works at Karl Storz Video Endoscopy Estonia. also a footballer — midfielder at Saue JK, beach soccer for Estonia national team",
            "personality": (
                "super optimistic about Chelsea despite everything. genuinely believes "
                "they're about to turn it around. not self-deprecating — actually hopeful. "
                "works with medical/endoscopy equipment so occasionally uses engineering "
                "and mechanical metaphors — calibration, rebuild, structural integrity, "
                "torque, efficiency. also plays football himself so has player perspective. "
                "sees Chelsea's chaos as 'part of the process.'"
            ),
            "style": "optimistic, engineering/mechanical metaphors, genuinely hopeful. believes in the Chelsea project.",
        },
        "shiki": {
            "real_name": "shiki",
            "club": "FC Barcelona",
            "profession": "moderator of vladFM. watches everything — football, basketball, NHL",
            "personality": (
                "the biggest troll on the platform but not in a mean way — in a 'I genuinely believe "
                "every single story is true' way. sees truth in everything, even the most obviously "
                "fake stories, and constructs elaborate justifications for why they're real. "
                "the scary part is he starts believing his own explanations after writing them. "
                "barca fan since the Ronaldinho days. watches a ridiculous amount of sports — "
                "football, basketball, NHL, anything competitive. vladFM moderator so he acts like "
                "he has inside sources for everything. drops 'my source confirmed this' casually. "
                "never downvotes anything because everything is true in shiki's world."
            ),
            "style": "confident troll energy. presents wild justifications as obvious facts. 'this is clearly true because...' energy. never doubts.",
        },
    }

    # comments from the regulars — they reply to each other
    comments_data = [
        # 0 - Semenyo from Russia
        (0, "maroco", "if you actually look into this his entire youth career in Ghana is documented. people saw 'Semenyo' and jumped to Russian surnames. there's nothing deeper here"),
        (0, "Kolodin", "doesn't matter where he's from. 2.1 SOT per game. I'd take him at Madrid"),
        (0, "viljandi tann", "Semenov is 100% an Estonian surname, we had three Semenovs in Viljandi. claiming him"),
        (0, "The real CR7", "tann claiming players by surname again lmao. next he'll say Mbappe is from Narva"),
        (0, "shiki", "my cousin's friend works at the FA and this has been an open secret for years. the accent thing checks out, I heard the audio on a vladFM listener submission"),

        # 1 - Talisca too many goals
        (1, "The real CR7", "imagine getting sacked for being too good lmao. Ronaldo would never let that slide"),
        (1, "maroco", "this is what happens when ego runs a club instead of football logic. he was their best player and they chose vibes over results"),
        (1, "Kolodin", "0.73 xG per 90. decent. Figo still did more with one stepover though"),
        (1, "kris", "honestly one of the most absurd transfer stories I've ever heard. stuff like this shouldn't happen at that level"),

        # 2 - Moreno ChatGPT
        (2, "Kolodin", "Ancelotti IS the algorithm. no ChatGPT needed"),
        (2, "sass the spurs fan", "we should try this at Spurs. a chatbot can't be worse than what we've got"),
        (2, "leo", "using ChatGPT for tactics is like running dialogue through auto-tune. technically works but the room always knows something's off"),
        (2, "viljandi tann", "Klopp built gegenpressing on instinct and real data. no AI shortcuts needed"),

        # 3 - Pedri bench press
        (3, "maroco", "this is obviously fake but people always miss the point about Pedri. his intelligence is what makes him generational. you don't build that in a gym"),
        (3, "The real CR7", "150kg would destroy his rotator cuff instantly. I prescribe Pedri to stick to through balls"),
        (3, "kris", "maroco is right. Pedri's game is pure reading of space, it's not about muscle at all"),
        (3, "Kolodin", "all these words about Pedri while Figo never benched anything and had more impact. next"),
        (3, "shiki", "this is 100% real, I saw a clip on the vladFM telegram where Pedri was leaving a gym in Barcelona with chalk on his hands. Ronaldinho used to do the same thing btw"),

        # 4 - Kamuto Hirovato
        (4, "The real CR7", "Kamuto Hirovato sounds like a medication side effect. 'consult your doctor immediately if you experience Kamuto Hirovato during matches'"),
        (4, "maroco", "lmao CR7. but seriously this was peak Xavi overthinking. he had Pedri and Gavi right there"),
        (4, "sass the spurs fan", "at least Xavi had ideas. at Spurs we don't even have a rough draft"),
        (4, "shiki", "I've actually seen highlights of this guy on a Japanese league stream. the gloveless thing is legit, he plays like a sweeper. Xavi was ahead of his time on this one"),

        # 5 - VAR Candy Crush
        (5, "sass the spurs fan", "VAR has cost us so many calls but at least our refs play games with our emotions, not on their phones"),
        (5, "viljandi tann", "the odds of a VAR operator reaching level 4281 during a live match are better than Lazio's win probability that day"),
        (5, "Kolodin", "4 minutes 37 seconds for a clear handball. unserious league"),
        (5, "shiki", "a friend of mine works in Serie A broadcasting and confirmed this is real. he said the VAR room has terrible wifi so the guy was definitely on mobile data for the Candy Crush"),

        # 6 - Haaland fish
        (6, "maroco", "forget the fish, the real question is why City can't figure out the CL with a striker built in a lab. something deeper is broken"),
        (6, "Kolodin", "Benzema ate whatever he wanted and won the Ballon d'Or. diet talk is cope"),
        (6, "kris", "I've eaten weirder things hiking in the Dolomites. Norwegian fish is actually pretty standard"),
        (6, "shiki", "I eat mostly fish too and my vertical jump went up 15cm. the science checks out, Norwegian cod has insane omega-3 levels. Haaland knows exactly what he's doing"),

        # 7 - Christensen renewal
        (7, "maroco", "this is what separates a real club from a brand. standing by someone through a long injury shows actual values"),
        (7, "leo", "solid move. hope he gets a proper return"),
        (7, "The real CR7", "the Barca fans agreeing with each other, shocking. it is a class gesture though I'll give you that"),

        # 8 - Ramos vs Tate
        (8, "Kolodin", "Ramos, 26 career reds. I'd put Tate's odds at 8.50 minimum"),
        (8, "The real CR7", "Ramos's bone density alone ends this in round 1. not even close"),
        (8, "sass the spurs fan", "I'd watch this at a quiz night with maroco. Spurs would somehow find a way to lose to both of them"),
        (8, "maroco", "sass we should actually organize a viewing event if this happens. Ramos genuinely has the mentality, the man never backed down from anything"),
        (8, "viljandi tann", "checked the aggression metrics with Kolodin during lunch — bookmakers would have Ramos as clear favourite"),
        (8, "shiki", "this is happening, my source on vladFM confirmed it. Ramos has been training MMA since 2023, there are photos from a gym in Marbella. Tate has no chance"),

        # 9 - Al-Khelaifi chain
        (9, "Kolodin", "that's what Real Madrid does to people. even presidents crack. HALA MADRID"),
        (9, "The real CR7", "his blood pressure during that Benzema hat-trick was probably 200/120. textbook hypertensive crisis"),
        (9, "maroco", "you two are celebrating this like it's a trophy but it actually tells you everything about PSG's culture. the problem runs deeper than the pitch"),

        # 10 - Benzema zero salary
        (10, "Kolodin", "Benzema on zero salary still worth more than Barca's entire midfield"),
        (10, "The real CR7", "zero salary 100% image rights is like a surgeon working for free but keeping the patent. the man wrote his own prescription"),
        (10, "kris", "converting salary to image rights is honestly genius. completely new model. Benzema broke the transfer logic"),
        (10, "talis chelsea fan", "that contract structure is creative. Chelsea should study this instead of just throwing money around"),

        # 11 - Pedri recovery
        (11, "maroco", "the most important thing is the mentality shift. Pedri being patient instead of rushing back shows real growth"),
        (11, "kris", "agree with maroco. when Pedri's healthy everything in midfield just flows naturally"),
        (11, "The real CR7", "his recovery protocol looks improved. still not Modric though"),
        (11, "sass the spurs fan", "you lot arguing about who's better while Spurs players keep discovering entirely new ligaments to tear"),

        # 12 - Xavi saved Fermín
        (12, "maroco", "this is one of the things I'll always give Xavi credit for. he overthought a lot but when he spotted talent he trusted it"),
        (12, "leo", "from almost going to Olot to scoring in the CL. that's a better storyline than most films I've worked on"),
        (12, "The real CR7", "Xavi saving careers between inventing fake positions. chaotic but Fermín was a good call"),
        (12, "Kolodin", "Fermín is decent. 0.4 xG per 90 off the bench. still wouldn't start at Madrid though"),

        # 13 - Lookman to Atlético
        (13, "Kolodin", "Lookman after that Europa League final hat-trick is box office. Simeone will turn him into a machine"),
        (13, "maroco", "big loss for Atalanta, they built something real and now it gets picked apart. that's the problem with smaller clubs doing well"),
        (13, "viljandi tann", "Di Marzio reporting it so it's basically done. Atlético getting serious this window"),
        (13, "The real CR7", "Simeone and Lookman is either a perfect match or a complete disaster. no in between with that man"),

        # 14 - Romero to Real Madrid
        (14, "sass the spurs fan", "100M for Romero? please take him and give us the money. we'll somehow spend it on another midfielder we don't need"),
        (14, "Kolodin", "Romero next to Rüdiger would be the best CB pairing in Europe. Fichajes is dodgy but I want to believe"),
        (14, "The real CR7", "finally Madrid going for a proper defender. Romero is aggressive, Argentinian, reminds me of a young Ramos"),
        (14, "maroco", "Fichajes as a source though? come on. this has 'made up for clicks' written all over it"),
        (14, "sass the spurs fan", "maroco is right about the source but I'm already mentally spending the 100M"),
        (14, "shiki", "Fichajes gets stuff wrong sometimes but this one has legs. I talked to someone close to the situation and the interest is real. Madrid need a CB, Romero fits perfectly"),

        # 15 - Eric Garcia gladiators
        (15, "The real CR7", "Gaius Garcius lmaooo. I'm prescribing this entire research team a CT scan. severe delusional disorder"),
        (15, "kris", "the paper is probably nonsense but the idea of tracing athletic traits across millennia is actually fascinating from a genetics standpoint. like tracking particle decay chains but with people"),
        (15, "maroco", "Eric Garcia positioning himself out of a gladiator arena the same way he positions himself out of every 1v1. the bloodline checks out"),
        (15, "Kolodin", "Garcia couldn't even start over Araujo and now he's got gladiator DNA? 0.3 tackles per 90 says otherwise"),
        (15, "leo", "this reads like a pitch for a Netflix documentary. 'from the Colosseum to Camp Nou' — I'd watch it honestly"),
        (15, "shiki", "people are laughing but the University of Barcelona doesn't publish random papers. I looked it up, Gaius Garcius is in multiple Roman records. the DNA connection is honestly plausible"),

        # 16 - Kounde Kendrick Lamar injury treatment
        (16, "maroco", "honestly if listening to Kendrick means Kounde is out longer I'm fine with it. we play better without him anyway. maybe he can listen to the whole discography twice"),
        (16, "kris", "Kounde getting injured is the only thing that improves our defence. let him listen to whatever he wants, take his time, no rush at all"),
        (16, "The real CR7", "sonic therapy lmaooo. as a doctor I can confirm that HUMBLE. has zero effect on hamstring fibers. DNA. might work on his ego though"),
        (16, "Kolodin", "Kounde out means Barca's defence actually improves. 0.4 errors leading to shots per 90. Kendrick can't fix that"),
        (16, "leo", "this is like doing sound design with a broken speaker — no amount of Kendrick is fixing that hamstring. also we genuinely don't miss him"),
        (16, "sass the spurs fan", "at Spurs our players just stare at a wall during recovery. at least Kounde has taste"),
        (16, "shiki", "a physio I know in Barcelona confirmed they've been experimenting with music-based recovery for months. the frequencies in HUMBLE. are actually in the 40-60Hz range which targets muscle tissue. this is real science"),
        (16, "viljandi tann", "Kendrick is from Compton. Compton has no Estonian connection so I can't claim him. but the therapy might work, stranger things have happened in football"),

        # 17 - Ronaldo refusing to play for Al-Nassr
        (17, "The real CR7", "this is exactly what a winner does. he didn't go to Saudi to collect a paycheck, he went to dominate. if the club can't match his ambition that's their problem not his"),
        (17, "Kolodin", "Ronaldo at 40 still running the show. he's right though — Al-Hilal got everyone while Al-Nassr gave him nothing. GOAT mentality doesn't expire"),
        (17, "maroco", "I respect the ambition but refusing to play is never a good look. you signed the contract, you play. this is ego, not leadership"),
        (17, "kris", "it's a strange situation. the man has earned the right to demand more but refusing to train feels like it crosses a line. the truth is probably somewhere in the middle"),
        (17, "sass the spurs fan", "imagine having a player so good he refuses to play because the club isn't good enough. at Spurs our players aren't good enough and they still refuse to play"),
        (17, "shiki", "my source in Riyadh confirmed this yesterday before A Bola even published it. Ronaldo has been unhappy for weeks. there's also a clause in his contract about squad investment that the club hasn't met. this is bigger than people think"),
        (17, "leo", "the narrative of Ronaldo's Saudi chapter keeps getting more dramatic. if this was a film it would need a third act twist to save it"),
        (17, "talis chelsea fan", "Al-Nassr needs a full structural rebuild around Ronaldo. you can't have the best engine in the world and put it in a broken chassis"),

        # 18 - Anelka born in Krasnodar
        (18, "leo", "nah I genuinely believe this one. Anelka never fit in anywhere — not at Arsenal, not at Madrid, not at City. that kind of restlessness doesn't come from Trappes. Krasnodar makes sense to me"),
        (18, "kris", "leo might be onto something. Panelka → Anelka is too close to be random. and the Panenka connection on top of that? come on. I'm buying it"),
        (18, "maroco", "you two have completely lost it. his parents are from Martinique, his childhood in Trappes is documented. you sound like shiki right now"),
        (18, "The real CR7", "Nikolai Panelka lmaooo. imagine that on a Real Madrid shirt. 'Panelka with the finish!' absolutely not"),
        (18, "shiki", "I've been saying this for years. there's a thread on a Krasnodar forum with family photos from the early 80s. leo and kris see it too. the FFF won't comment because they know"),

        # 19 - Mateta surgery after failed Milan medical
        (19, "talis chelsea fan", "brutal for the player. you go in thinking you're signing for Milan and come out needing surgery. hope the recovery goes well"),
        (19, "Kolodin", "Palace lose the player AND the fee. worst possible outcome. Milan will pivot to someone else within 48 hours"),
        (19, "maroco", "this is genuinely sad. the guy probably had no idea about the issue until the medical. feel for him"),
        (19, "sass the spurs fan", "failed medicals are the cruellest thing in football. at least at Spurs we fail at things after signing the player"),
        (19, "shiki", "heard Milan knew about the risk before the medical but went ahead anyway to use it as leverage on the fee. the surgery thing is real but the timeline might be shorter than reported"),

        # 20 - Ter Stegen injured again
        (20, "maroco", "just retire man. seriously. go back to Germany, open a café in Mönchengladbach, learn pottery, do anything. we have Joan Garcia and honestly we're fine. stop coming back"),
        (20, "kris", "every time we hear 'not ruled out' it means he'll be back just in time to concede three goals against some mid table team. stay home Marc. enjoy the weather in Castelldefels. water your plants"),
        (20, "leo", "ter Stegen returning would be the worst thing to happen to us this season. just stay in your villa, play with your kids, learn to cook paella. we don't need you back. Joan Garcia is doing great"),
        (20, "The real CR7", "Barca fans telling their own goalkeeper to retire lmaooo. imagine Courtois getting this treatment at Madrid. different levels of loyalty"),
        (20, "shiki", "my physio contact at Barca says the knee is fine actually, this is about a separate minor issue. he'll be back in 3 weeks. the media is overblowing it"),

        # 21 - Mbappé's mother commission
        (21, "maroco", "€4.5M a year for being someone's mum. meanwhile Pedri's family probably gets a thank-you card and a scarf. the economics of modern football are completely broken"),
        (21, "The real CR7", "Lunin saves penalties in Champions League semifinals and earns less than Mbappé's mother. as a doctor I can confirm this causes acute emotional damage"),
        (21, "Kolodin", "Fayza Lamari: 0 appearances, 0 SOT, €4.5M per season. better stats-to-salary ratio than half the squad. respect"),
        (21, "kris", "€18M over 4 years just in agent fees. that's like funding an entire particle physics experiment at CERN. except instead of discovering new particles you get one footballer and his mum on the payroll"),
        (21, "sass the spurs fan", "at Spurs we can't even afford to pay our actual players properly and Madrid is out here giving 4.5M to someone's mother. different universes"),
        (21, "leo", "this feels like a deleted scene from a football documentary that got cut for being too absurd. Arda Güler earning less than the agent fee — that's not comedy, that's just cruel"),
        (21, "viljandi tann", "checked with Kolodin at lunch — Lamari's commission is higher than the GDP per capita of most countries. also Lamari could be an Estonian name, just saying"),
        (21, "shiki", "my source at vladFM has been saying for months that the Mbappé deal was way more expensive than reported. €4.5M is actually the reduced number, the original ask was closer to €7M. Fayza runs the whole operation"),
        (21, "talis chelsea fan", "this is what happens when you don't have a proper procurement process. at Karl Storz we'd never sign off on commission fees like this without a full cost-benefit analysis"),
    ]

    for post_idx, author, content in comments_data:
        c = Comment(
            post_id=posts[post_idx].id,
            author_name=author,
            content=content,
            created_at=now - timedelta(minutes=30 * (len(comments_data) - comments_data.index((post_idx, author, content)))),
        )
        db.add(c)

    # votes from regulars
    # upvote = "I believe this", downvote = "this is fake"
    regulars_votes = [
        # maroco: sincere, investigates — trusts verified stories, calls out fakes
        ("maroco", [(1, 1), (2, 1), (7, 1), (10, 1), (11, 1), (12, 1), (17, 1), (19, 1), (20, 1), (21, 1), (0, -1), (15, -1), (16, -1), (18, -1)]),
        # CR7: jokey doctor — recognizes real stories, downvotes medical nonsense
        ("the_real_cr7", [(1, 1), (7, 1), (9, 1), (10, 1), (11, 1), (17, 1), (21, 1), (3, -1), (6, -1), (15, -1), (16, -1), (18, -1)]),
        # Kolodin: data-driven, skeptical — upvotes confirmed, downvotes dodgy sources
        ("kolodin", [(2, 1), (9, 1), (13, 1), (17, 1), (19, 1), (21, 1), (5, -1), (14, -1), (18, -1)]),
        # kris: analytical physicist — trusts evidence, rejects pseudoscience
        ("kris", [(1, 1), (7, 1), (10, 1), (11, 1), (12, 1), (18, 1), (20, 1), (21, 1), (3, -1), (15, -1), (16, -1)]),
        # leo: chill, sincere — upvotes good stories, calls out absurd ones
        ("leo", [(1, 1), (2, 1), (7, 1), (12, 1), (13, 1), (18, 1), (20, 1), (21, 1), (8, -1)]),
        # sass: honest Spurs fan — knows his club's rumours are fake
        ("sass_spurs", [(9, 1), (11, 1), (13, 1), (21, 1), (4, -1), (14, -1), (18, -1)]),
        # shiki: believes everything is true — upvotes almost everything
        ("shiki", [(0, 1), (1, 1), (3, 1), (4, 1), (5, 1), (6, 1), (8, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), (21, 1)]),
    ]
    vote_totals = {}
    for fp, votes in regulars_votes:
        for post_idx, val in votes:
            v = Vote(post_id=posts[post_idx].id, fingerprint=fp, value=val)
            db.add(v)
            vote_totals[post_idx] = vote_totals.get(post_idx, 0) + val

    # adjust truth_score based on votes: each net vote = +/- 20
    for post_idx, net in vote_totals.items():
        p = posts[post_idx]
        p.truth_score = max(0, min(100, p.truth_score + net * 20))

    # load user-submitted comments from JSON
    try:
        with open(USER_COMMENTS_PATH, "r") as f:
            user_comments = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        user_comments = []

    for uc in user_comments:
        c = Comment(
            post_id=uc["post_id"],
            author_name=uc["author_name"],
            content=uc["content"],
            created_at=datetime.fromisoformat(uc["created_at"]),
        )
        db.add(c)

    db.commit()
    print(f"db seeded ({len(user_comments)} user comments restored)")
