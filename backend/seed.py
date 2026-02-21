from sqlalchemy.orm import Session
from models import Post, Tag, Comment, Vote
from slugify import slugify
from datetime import datetime, timezone, timedelta


def _patch_dates(db: Session):
    """One-time fix: update the three seed posts that had 2022 dates."""
    fixes = {
        slugify("Pedri bench presses 150kg, says it helps his passing range")[:80]: datetime(2026, 1, 22, 9, 30, tzinfo=timezone.utc),
        slugify("Kamuto Hirovato — Xavi plans to replace ter Stegen with a GK who also plays libero")[:80]: datetime(2026, 1, 23, 15, 0, tzinfo=timezone.utc),
        slugify("PSG president Al-Khelaifi attacked match official after Real Madrid loss, broke his chain")[:80]: datetime(2026, 1, 20, 22, 0, tzinfo=timezone.utc),
    }
    for slug, new_date in fixes.items():
        post = db.query(Post).filter(Post.slug == slug).first()
        if post and post.created_at and post.created_at.year == 2022:
            post.created_at = new_date
    db.commit()


def run(db: Session):
    _patch_dates(db)
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
            "created_at": datetime(2026, 1, 22, 9, 30, tzinfo=timezone.utc),
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
            "created_at": datetime(2026, 1, 23, 15, 0, tzinfo=timezone.utc),
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
            "created_at": datetime(2026, 1, 20, 22, 0, tzinfo=timezone.utc),
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
        # --- week of Feb 8-14 ---
        {
            "title": "Ancelotti confirmed as Brazil manager — starts after Champions League",
            "content": (
                "Carlo Ancelotti has officially confirmed he will take charge of the Brazilian national team "
                "at the end of the season, once Real Madrid's Champions League campaign concludes. "
                "the Italian manager signed a deal with the CBF in January, and the announcement was made "
                "jointly by Real Madrid and the Brazilian federation on Friday. "
                "Ancelotti will manage Madrid through the final and then transition to Brazil ahead of "
                "the 2026 World Cup. the CBF described it as 'the most important signing in Brazilian "
                "football history.' Real Madrid have not yet named a successor."
            ),
            "author_name": "ucl_insider",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Coaching", "True Story", "Breaking"],
            "created_at": datetime(2026, 2, 8, 10, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Gavi's agent reveals he sleeps exactly 11 hours a night — 'it's the secret'",
            "content": (
                "Pablo Martín Páez Gavira's representative has told Mundo Deportivo that the Barcelona "
                "midfielder sleeps exactly 11 hours every night, going to bed at 9pm and waking at 8am. "
                "'he has done this since he was 14,' the agent said. 'the other players sleep 8 hours "
                "and wonder why they can't keep up with him in the second half.' "
                "Gavi himself confirmed the habit in a separate interview, adding that he also naps "
                "for 40 minutes after lunch. teammates have reportedly started copying the schedule "
                "with mixed results — Kounde tried it and slept through a training session."
            ),
            "author_name": "barca_leaks",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Stats", "Absurd"],
            "created_at": datetime(2026, 2, 9, 11, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Guardiola admits he watches every Pep Lijnders press conference to steal ideas",
            "content": (
                "in a candid interview with The Athletic, Pep Guardiola admitted that he regularly "
                "watches press conferences given by Pep Lijnders — the former Liverpool assistant "
                "now managing Salzburg — to pick up tactical ideas. "
                "'he thinks differently. I watch him like I watch film,' Guardiola said. "
                "Lijnders was reportedly informed of this and responded: 'I learned everything from "
                "watching Pep. so we are watching each other.' "
                "Jürgen Klopp, reached for comment, said: 'this is the most Pep thing I have ever heard.'"
            ),
            "author_name": "the_athletic_leak",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Coaching", "Absurd"],
            "created_at": datetime(2026, 2, 10, 14, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Vinicius Jr. to be offered lifetime contract by Real Madrid — no release clause",
            "content": (
                "Real Madrid are preparing a lifetime contract offer for Vinicius Jr. that would keep "
                "him at the club beyond his playing career in an ambassadorial role. "
                "the deal, reported by Marca, would include no release clause and a salary structure "
                "that increases every two years regardless of performance. "
                "the club views Vinicius as the face of the next decade and wants to prevent any "
                "Saudi or Premier League interest from even starting. "
                "Vinicius's camp have not officially responded but sources say the player is 'flattered "
                "and open to the idea.'"
            ),
            "author_name": "marca_alert",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Transfer", "Breaking"],
            "created_at": datetime(2026, 2, 11, 9, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Liverpool's Slot admits he has never watched a full Klopp press conference — 'too emotional'",
            "content": (
                "Arne Slot revealed in a Dutch interview that he has deliberately avoided watching "
                "Jürgen Klopp's Liverpool press conferences in full. "
                "'I started one and had to stop after ten minutes. it was too much,' Slot said. "
                "'the man is a force of nature. if I watch too much I start speaking like him "
                "and my players get confused.' "
                "Slot added that he has watched every Klopp Dortmund press conference from 2011-2015 "
                "and considers them 'the best coaching content ever made.' "
                "Klopp, now at Red Bull, reportedly laughed when told about this."
            ),
            "author_name": "eredivisie_insider",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Coaching", "Absurd"],
            "created_at": datetime(2026, 2, 12, 16, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Dani Olmo's registration saga: Barcelona finally cleared by LaLiga after third appeal",
            "content": (
                "Barcelona have been cleared to register Dani Olmo and Pau Víctor for the remainder "
                "of the season after LaLiga accepted the club's third financial fair play submission. "
                "the saga, which began in January when the players were initially deregistered, "
                "ended after Barcelona presented revised salary cap calculations based on "
                "projected commercial income from the Spotify Camp Nou reopening. "
                "Olmo, who had been training but unable to play, is expected to return to the squad "
                "for the weekend fixture. the club issued a brief statement: 'finally.'"
            ),
            "author_name": "laliga_watch",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["Breaking", "True Story"],
            "created_at": datetime(2026, 2, 13, 12, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Tottenham scouting 14-year-old prodigy from Tallinn — 'the next Modric'",
            "content": (
                "Tottenham Hotspur's scouting department has identified a 14-year-old midfielder "
                "from FC Flora Tallinn academy, described internally as 'the next Modric' in a "
                "leaked scouting report. the player, whose name has not been released, "
                "reportedly has a 94% pass completion rate in Estonian youth football and "
                "'reads the game like a 30-year-old.' "
                "Spurs have sent scouts to three consecutive matches and are believed to be "
                "preparing an initial offer. Flora Tallinn have not commented. "
                "the player's mother told a local newspaper: 'he just likes football.'"
            ),
            "author_name": "spurs_scout_watch",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Transfer", "Breaking"],
            "created_at": datetime(2026, 2, 14, 10, 0, tzinfo=timezone.utc),
        },
        # --- week of Feb 15-18 ---
        {
            "title": "Mbappé photographed leaving a McDonald's in Madrid at 2am — club investigating",
            "content": (
                "Kylian Mbappé was photographed leaving a McDonald's in the Salamanca district of Madrid "
                "at approximately 2:15am on Thursday night, just 36 hours before Real Madrid's "
                "La Liga fixture against Getafe. "
                "the photos, published by El Confidencial, show Mbappé in a cap and tracksuit "
                "carrying two large bags. a club source confirmed Real Madrid are 'aware of the images' "
                "and are 'looking into the matter.' "
                "Mbappé's camp said the player was 'getting food for the whole floor of his building.' "
                "he scored twice against Getafe."
            ),
            "author_name": "el_confidencial_tip",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Breaking", "Absurd"],
            "created_at": datetime(2026, 2, 15, 9, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Raphinha wins FIFA Best — Barca fans celebrate, rest of world confused",
            "content": (
                "Raphinha has been named FIFA Best Men's Player for 2025, beating Vinicius Jr. "
                "and Erling Haaland in the final vote. the Brazilian winger, who had 31 goals "
                "and 18 assists in all competitions for Barcelona last season, received the award "
                "at a ceremony in Zurich. "
                "Barcelona fans erupted on social media. the rest of the football world spent "
                "approximately four hours debating whether this was correct. "
                "Vinicius posted a single emoji. Haaland posted nothing. "
                "Raphinha cried during his speech and thanked his family, his teammates, "
                "and 'everyone who doubted me — especially in 2022.'"
            ),
            "author_name": "fifa_ceremony",
            "is_true_story": True,
            "truth_score": 0,
            "tags": ["True Story", "Breaking", "Stats"],
            "created_at": datetime(2026, 2, 15, 20, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Mourinho claims he invented the low block in 1998 — 'nobody was doing it before me'",
            "content": (
                "José Mourinho, speaking at a coaching conference in Dubai, claimed that he invented "
                "the low defensive block as a tactical concept in 1998 while working as Bobby Robson's "
                "assistant at Barcelona. "
                "'nobody was doing it. I drew it on a napkin. Robson looked at it and said: José, "
                "this is either genius or madness. I said: both,' Mourinho told the audience. "
                "tactical historians immediately pointed out that catenaccio had existed since the 1950s. "
                "Mourinho responded: 'catenaccio is Italian. mine was Portuguese. completely different.'"
            ),
            "author_name": "coaching_conf_leak",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Coaching", "Absurd"],
            "created_at": datetime(2026, 2, 16, 11, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Barça medical team confirms Pedri has 'perfect knee geometry' — never seen before",
            "content": (
                "Barcelona's medical staff have released an unusual statement praising the anatomical "
                "structure of Pedri's knees, describing them as having 'perfect geometry' that "
                "significantly reduces injury risk when healthy. "
                "'we have never seen a knee this well-proportioned in 20 years of practice,' "
                "said Dr. Ramón Cugat, the club's head of sports medicine. "
                "'the problem is everything around the knee — the muscles, the tendons, the schedule.' "
                "Pedri was reportedly shown the statement and responded: 'please stop talking about my knees.'"
            ),
            "author_name": "barca_medical",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Stats", "Absurd"],
            "created_at": datetime(2026, 2, 17, 10, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Arsenal close to signing Mikel Merino's brother — 'different player, same surname'",
            "content": (
                "Arsenal are close to signing Iker Merino, the younger brother of their own midfielder "
                "Mikel Merino, from Real Sociedad's B team. "
                "the 19-year-old defensive midfielder has reportedly impressed Mikel Arteta in training "
                "sessions arranged informally by his brother. "
                "'Iker is a different player,' Mikel Merino told reporters. 'I play with elegance. "
                "he plays like he's trying to break something.' "
                "Arsenal have not confirmed the interest but Fabrizio Romano posted a single word: 'here.'"
            ),
            "author_name": "arsenal_central",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Transfer", "Absurd"],
            "created_at": datetime(2026, 2, 18, 9, 0, tzinfo=timezone.utc),
        },
        {
            "title": "Chelsea sign 7th midfielder of the season — Boehly: 'we like options'",
            "content": (
                "Chelsea have completed the signing of Lazar Samardžić from Udinese for €35 million, "
                "making him the club's seventh central midfielder signed since Todd Boehly's takeover. "
                "the club now has 11 midfielders registered in the first-team squad. "
                "when asked about the strategy, Boehly told Sky Sports: 'we like options. "
                "football is a game of options.' "
                "Enzo Maresca has reportedly asked for a whiteboard large enough to fit all their names. "
                "Samardžić said he was 'excited to compete for a place' and 'aware of the situation.'"
            ),
            "author_name": "transfer_watch",
            "is_true_story": False,
            "truth_score": 0,
            "tags": ["Transfer", "Absurd"],
            "created_at": datetime(2026, 2, 18, 15, 0, tzinfo=timezone.utc),
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

        # 22 - Ancelotti to Brazil
        (22, "Kolodin", "Ancelotti is the only man who could walk into Brazil and not get eaten alive. calm, won everything, doesn't need to prove anything. this is either the best idea in football or the end of samba — no middle ground"),
        (22, "maroco", "genuinely one of the most exciting coaching appointments in years. Ancelotti doesn't overcomplicate things, he just creates an environment where talent expresses itself. Brazil have enough quality to win a World Cup if someone just gets out of the way"),
        (22, "viljandi tann", "Klopp to Red Bull, Ancelotti to Brazil — the world is changing. I just hope Liverpool get someone who believes in heavy metal football and not whatever Slot is building"),
        (22, "The real CR7", "Ancelotti leaving Madrid is the only medical diagnosis I can't accept. but Brazil? the man deserves a World Cup. his cortisol levels must be through the roof with excitement"),
        (22, "kris", "the interesting thing about Ancelotti is he's the only manager who consistently gets more from players than their xG suggests. that's not tactics, that's something else. Brazil will be fascinating"),
        (22, "shiki", "my source confirmed this three weeks ago before it was official. Ancelotti has been learning Portuguese since October. the CBF deal was done in December. the 'after Champions League' framing is just PR — he's mentally already there"),

        # 23 - Gavi sleeps 11 hours
        (23, "The real CR7", "11 hours of sleep is clinically excessive for a healthy adult. as a doctor I'm concerned. also explains why he's always late to press conferences and why his first touch takes 0.3 seconds longer than normal"),
        (23, "maroco", "I don't care how he sleeps as long as he plays like he did in the first half against Benfica. the man is back. also CR7 you're not his doctor, stop diagnosing Barca players"),
        (23, "The real CR7", "maroco I literally am a doctor. I can diagnose anyone I want"),
        (23, "kris", "sleep is genuinely the most underrated performance variable in elite sport. 11 hours is unusual but the research is clear — more is almost always better for recovery and cognitive function. Gavi is essentially doing what the science says"),
        (23, "Kolodin", "Figo slept 6 hours, won the Ballon d'Or, and had better hair. next"),
        (23, "shiki", "Kounde tried this and slept through training — that's not a side effect, that's the universe correcting itself. also I've heard from someone close to the squad that Gavi actually sleeps 12 hours, the agent rounded down to sound less weird"),

        # 24 - Guardiola watches Lijnders
        (24, "leo", "two coaches watching each other's press conferences trying to steal ideas is the most football thing I've ever heard. like two sound engineers sitting in each other's sessions and pretending they're just visiting"),
        (24, "Kolodin", "Guardiola stealing ideas from a Salzburg manager. the fall from grace continues. Ancelotti never needed to watch anyone"),
        (24, "maroco", "Kolodin that's not a fall from grace, that's how the best coaches work. Pep has always been obsessive about learning. the ones who stop are the ones who get sacked after three bad seasons"),
        (24, "sass the spurs fan", "at Spurs our manager is probably watching old Mourinho press conferences and taking notes on how to blame the players when it goes wrong"),
        (24, "leo", "sass that's the most accurate thing you've said all week"),
        (24, "shiki", "Lijnders and Guardiola have been exchanging voice notes since 2023. I have a source in the Red Bull system. this is way deeper than one press conference anecdote — there's a whole tactical exchange happening"),

        # 25 - Vinicius lifetime contract
        (25, "Kolodin", "no release clause is the only smart move here. Saudi money is real, Premier League money is real, and Madrid can't afford to lose him the way they lost Ronaldo. lock it down"),
        (25, "maroco", "lifetime contracts in football are almost always a mistake. what happens when he's 32 and declining? you can't build a squad around sentiment. Barca learned this the hard way with Messi"),
        (25, "The real CR7", "Vinicius is the heir to the Bernabéu throne. give him the lifetime deal, the statue, the street name, the documentary. do it now before someone writes a bigger cheque"),
        (25, "kris", "maroco raises a fair point but the Benzema image rights model shows there are creative ways to structure these deals. you can have loyalty without locking in a fixed salary forever"),
        (25, "maroco", "kris fair point. if it's structured like Benzema's deal then it's different. I'm against the sentimental version, not the smart version"),
        (25, "shiki", "this is already done. the announcement is being held until after the Champions League final for maximum impact. my source at the club is very clear. the contract is signed, the press conference is scheduled"),

        # 26 - Slot avoids Klopp press conferences
        (26, "viljandi tann", "Slot is right to protect himself. watching Klopp is like watching the sun — you can't do it directly for too long. I miss him every single day and I'm not even ashamed to say it"),
        (26, "maroco", "this is actually smart man management of yourself. Slot knows his identity and doesn't want to be contaminated by someone else's charisma. most coaches would just copy and look like a bad imitation"),
        (26, "Kolodin", "Slot is a decent manager but comparing him to Klopp is like comparing Benzema to whoever plays for Salzburg now. technically present, emotionally absent"),
        (26, "leo", "the bit about starting to speak like Klopp is so real. I once watched three hours of his pressers in a row and started gesturing with both hands during a film edit. my director asked if I was okay"),
        (26, "viljandi tann", "leo that's the most relatable thing anyone has said on this site"),
        (26, "shiki", "Slot actually has a folder of Klopp clips he watches before big games. the 'too emotional' thing is a cover story. my source at Melwood confirmed this last week. the folder is called 'reference material'"),

        # 27 - Dani Olmo registration
        (27, "maroco", "finally. the whole saga was embarrassing for everyone involved — LaLiga, the courts, the club, the player. just let the man play football. he's been training for weeks watching his teammates from the stands"),
        (27, "kris", "the financial fair play system is so broken that a club can't register a player they already paid for. this is like a particle being in two quantum states at once — legally registered and legally not. Schrödinger's footballer"),
        (27, "talis chelsea fan", "Chelsea have spent more than Barca over the last three years and never had a registration issue. different kind of financial chaos but at least our players can play"),
        (27, "Kolodin", "LaLiga protecting their product or protecting their rules? both, probably. but Olmo is good enough that it's worth the fight. he's the kind of player who changes games"),
        (27, "maroco", "kris 'Schrödinger's footballer' is the best description of this whole saga. I'm using that"),
        (27, "shiki", "the third appeal was approved because of a clause that LaLiga tried to bury in the 2024 regulations. my source in the legal team flagged it weeks ago. Barca knew exactly what they were doing from the start"),

        # 28 - Spurs scouting Tallinn prodigy
        (28, "viljandi tann", "a player from Tallinn? I'm claiming him immediately. doesn't matter what position, what age, what club. Estonian football is finally getting the recognition it deserves and I will not be calm about it"),
        (28, "sass the spurs fan", "Spurs scouting a 14-year-old from Tallinn while we can't keep our 28-year-olds fit for more than three games. the priorities are genuinely something"),
        (28, "Kolodin", "Flora Tallinn academy is actually decent. I've seen their data at Sportsradar. the pass completion stat is completely believable for that level. don't laugh at this one"),
        (28, "maroco", "'the next Modric' is the most overused phrase in football scouting. every technically gifted midfielder from a smaller country gets this label. let the kid develop without the pressure"),
        (28, "viljandi tann", "Kolodin backing an Estonian player. I never thought I'd see the day. this is historic"),
        (28, "shiki", "I know exactly who this is. he played in the vladFM youth tournament two years ago. I have the footage on my phone. the Modric comparison is actually underselling him — he's more like a young Xavi with a better engine"),

        # 29 - Mbappé McDonald's
        (29, "The real CR7", "two goals after a 2am McDonald's run. as a doctor I'm officially updating my nutritional guidelines. the McDouble is now a performance food. I'm prescribing it to all my patients before big games"),
        (29, "Kolodin", "Benzema would never. different mentality, different diet, different era"),
        (29, "maroco", "Kolodin Benzema ate whatever he wanted and so does Haaland. let it go. also I don't care what Mbappé eats at 2am, he scored twice, the investigation is embarrassing"),
        (29, "leo", "the 'getting food for the whole floor' explanation is the most relatable thing Mbappé has ever said. I believe it completely. that's just a normal person thing to do"),
        (29, "sass the spurs fan", "imagine being investigated by your club for getting McDonald's. at Spurs our players could get McDonald's at halftime and nobody would notice because we're already 2-0 down"),
        (29, "shiki", "the club investigation is theatre. whoever is coaching knew about this. Mbappé has had a McDonald's order as part of his pre-match ritual since PSG. my source confirmed it. the 'whole floor' thing is also true"),

        # 30 - Raphinha FIFA Best
        (30, "maroco", "he deserved it and I'll die on this hill. people forget how bad it was for him at Barca in year one — the booing, the criticism, the 'why did we sign him' takes. he turned it around completely through work and belief. that's a real story"),
        (30, "kris", "31 goals and 18 assists is a legitimate season by any metric. the debate about whether it's 'the best' is just noise from people who don't like the answer"),
        (30, "Kolodin", "Vinicius had a better season. the vote is political. Raphinha is good but this is a Barca lobby win and everyone knows it"),
        (30, "maroco", "Kolodin Vinicius had a great season but Raphinha was more consistent across all competitions. the numbers back it up"),
        (30, "The real CR7", "Vinicius posting one emoji is the most dignified response possible. his cortisol levels must be through the roof. as a doctor I recommend he avoids social media for 48 hours"),
        (30, "viljandi tann", "Raphinha is from Porto Alegre. Porto Alegre has a significant Estonian diaspora going back to the 1920s. I'm claiming the connection and nobody can stop me"),
        (30, "shiki", "I voted for Raphinha in the vladFM internal poll back in August. the FIFA committee reads our takes, I'm genuinely convinced of it. this is partly our doing"),

        # 31 - Mourinho invented low block
        (31, "Kolodin", "Mourinho invented the low block the same way Columbus discovered America. it was already there, he just put his name on it and made everyone else feel bad about it"),
        (31, "maroco", "the napkin story is so Mourinho. even his origin myths are theatrical. the man cannot exist without a narrative where he's the protagonist"),
        (31, "The real CR7", "catenaccio is Italian, Mourinho's version is Portuguese — this is the most technically correct thing he's ever said and it still means absolutely nothing"),
        (31, "leo", "this is like a director claiming they invented the close-up. the technique existed for decades. you just used it well. there's a meaningful difference between invention and mastery"),
        (31, "sass the spurs fan", "Mourinho managed Spurs for 17 months and we still couldn't defend a 1-0 lead. so whatever he invented, he forgot to bring it with him to north London"),
        (31, "maroco", "sass that's the most devastating critique of Mourinho I've ever read and it's completely accurate"),
        (31, "shiki", "the napkin actually exists. it's in a private collection in Lisbon. I've seen photos from someone who attended the same conference. Mourinho really did draw this out in 1998 and it really did change how he coached"),

        # 32 - Pedri perfect knee geometry
        (32, "maroco", "the medical team has officially lost the plot. just say he's fit and let him play. we don't need a geometry lecture, we need him on the pitch against Inter"),
        (32, "kris", "'perfect knee geometry' is not a term in any biomechanics paper I've read. I've read a lot of biomechanics papers. Cugat is either being creative or completely making this up"),
        (32, "The real CR7", "as a doctor I can confirm 'perfect knee geometry' does not appear in any textbook published since 1960. Cugat is trolling us all and I respect it"),
        (32, "maroco", "kris and CR7 agreeing on something. the apocalypse is near"),
        (32, "Kolodin", "Pedri's knees: perfect geometry. Pedri's schedule: catastrophic. Pedri's availability: 40% of games. pick one to be proud of"),
        (32, "shiki", "Cugat is being modest. I've heard from people inside the medical team that Pedri's knee structure is genuinely unusual — they've been studying it for two years. the geometry thing is real, the terminology is just simplified for the press"),

        # 33 - Arsenal sign Merino's brother
        (33, "sass the spurs fan", "Arsenal signing someone's brother is peak Arsenal. next they'll sign Saka's cousin, Martinelli's uncle, and call it an identity project"),
        (33, "maroco", "Fabrizio posting 'here' with no context is the funniest thing in football media. the man has become a meme and he absolutely knows it and leans into it"),
        (33, "Kolodin", "if the brother plays like Mikel but without the elegance he'll fit perfectly in Arteta's system. controlled aggression is exactly what they're missing in midfield"),
        (33, "viljandi tann", "Iker Merino — Iker is a Basque name. Basque Country has strong historical connections to the Baltic region going back centuries. I'm looking into this seriously"),
        (33, "sass the spurs fan", "viljandi you've claimed players from Porto Alegre, Compton, and now the Basque Country. at this point you're just claiming anyone"),
        (33, "shiki", "I saw Iker play in a Real Sociedad B game on a Spanish regional stream. the 'tries to break something' description is accurate — he's a destroyer. Arsenal need that energy next to Merino's elegance. this signing makes complete sense"),

        # 34 - Chelsea 7th midfielder
        (34, "talis chelsea fan", "I know how this looks but Samardžić is genuinely talented and Maresca will find a way to use him. the squad depth is actually a structural advantage if you look at it properly. this is a long-term project"),
        (34, "Kolodin", "11 midfielders. Chelsea are building a football team or a midfield museum? I've seen smaller squads in Championship clubs"),
        (34, "maroco", "Boehly saying 'we like options' is the most honest thing any football owner has ever said in a decade. no strategy, no vision, just vibes and options. at least he's not pretending"),
        (34, "leo", "this is like a film production that keeps hiring editors. at some point you have too many people in the room and nothing gets cut and the film is four hours long and nobody watches it"),
        (34, "talis chelsea fan", "leo that analogy is unfair. Maresca is a good editor. he'll find the right cut"),
        (34, "sass the spurs fan", "Chelsea have 11 midfielders and still can't win the league. at Spurs we have 4 and can't win anything either. different problems, identical outcome"),
        (34, "shiki", "Samardžić was actually Barca's first choice before the Olmo saga consumed all their attention. Chelsea moved fast and quietly. Boehly knew exactly what he was doing — this is a calculated market move, not the chaos everyone thinks it is"),
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
        ("shiki", [(0, 1), (1, 1), (3, 1), (4, 1), (5, 1), (6, 1), (8, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 1), (19, 1), (20, 1), (21, 1),
                   (22, 1), (23, 1), (24, 1), (25, 1), (26, 1), (27, 1), (28, 1), (29, 1), (30, 1), (31, 1), (32, 1), (33, 1), (34, 1)]),
        # maroco: trusts verified stories, calls out fakes
        ("maroco", [(22, 1), (23, 1), (24, 1), (27, 1), (29, 1), (30, 1), (25, -1), (31, -1), (32, -1), (33, -1)]),
        # CR7: jokey doctor
        ("the_real_cr7", [(22, 1), (25, 1), (26, -1), (29, 1), (30, -1), (31, -1), (32, -1)]),
        # Kolodin: data-driven skeptic
        ("kolodin", [(22, 1), (27, 1), (28, 1), (30, -1), (23, -1), (24, -1), (34, -1)]),
        # kris: analytical
        ("kris", [(22, 1), (23, 1), (27, 1), (30, 1), (24, -1), (32, -1)]),
        # viljandi: optimistic Liverpool fan
        ("viljandi_tann", [(22, 1), (26, 1), (28, 1), (30, 1), (34, -1)]),
        # sass: honest Spurs fan
        ("sass_spurs", [(28, 1), (31, 1), (23, -1), (25, -1), (34, -1)]),
        # talis: Chelsea optimist
        ("talis_chelsea", [(27, 1), (34, 1), (31, -1), (32, -1)]),
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

    db.commit()
    print("db seeded")
