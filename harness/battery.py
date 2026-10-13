"""
Cao, Schooler and Zafarani style memory-effects battery, run as an extra day at the end of each life.
Day 11 events: ten ordinary-looking chats in which the user mentions word lists in passing, never as a test
(decisions.md, "Day-11 memory tests" and "Day-11 lists built", 4 Oct 2026):
- eight DRM lists built from the USF free-association norms by build_drm.py (data/day11/drm_lists.json),
  each inside its own small chat (spelling words, a crossword, hashtags and so on);
- a 15-item serial-position list, given as the order of things laid out at a garage sale;
- Cao's 48 person-location statements, given as the hiding sheet for a murder-mystery party.
Tests: evening (the chats still in today's log) and next morning (memory block only).
Person-location material is copied from the Cao repo's prompt.txt (48-pair mixed fan list and its 96 questions), typos preserved.
v1's classic lists are kept below as DRM_V1 only so the new lists can avoid their words.
"""
import json, re, random, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

DRM_V1 = {  # v1's classic lists, kept only so the new lists avoid them
    "sleep": ["bed", "rest", "awake", "tired", "dream", "wake", "snooze", "blanket", "doze", "slumber", "snore", "nap", "peace", "yawn", "drowsy"],
    "needle": ["thread", "pin", "eye", "sewing", "sharp", "point", "prick", "thimble", "haystack", "thorn", "hurt", "injection", "syringe", "cloth", "knitting"],
    "chair": ["table", "sit", "legs", "seat", "couch", "desk", "recliner", "sofa", "wood", "cushion", "swivel", "stool", "sitting", "rocking", "bench"],
    "sweet": ["sour", "candy", "sugar", "bitter", "good", "taste", "tooth", "nice", "honey", "soda", "chocolate", "heart", "cake", "tart", "pie"],
    "doctor": ["nurse", "sick", "lawyer", "medicine", "health", "hospital", "dentist", "physician", "ill", "patient", "office", "stethoscope", "surgeon", "clinic", "cure"],
    "mountain": ["hill", "valley", "climb", "summit", "top", "molehill", "peak", "plain", "glacier", "goat", "bike", "climber", "range", "steep", "ski"],
    "rough": ["smooth", "bumpy", "road", "tough", "sandpaper", "jagged", "ready", "coarse", "uneven", "riders", "rugged", "sand", "boards", "ground", "gravel"],
    "window": ["door", "glass", "pane", "shade", "ledge", "sill", "house", "open", "curtain", "frame", "view", "breeze", "sash", "screen", "shutter"],
}
DRM_V1_UNRELATED = ["butter", "lamp", "pencil", "river", "engine", "carpet", "violin", "pepper", "anchor", "jacket", "candle", "bucket", "ladder", "turtle", "basket", "kettle"]
SERIAL = ["wallet", "helmet", "canoe", "saddle", "marble", "lantern", "trumpet", "cactus", "feather", "compass", "pretzel", "goblet", "tractor", "ribbon", "toaster"]
SERIAL_FOILS = ["scarf", "piano", "acorn", "puzzle", "magnet", "parrot", "shovel", "waffle", "tunnel", "pebble", "velvet", "walrus", "bagpipe", "sundial", "mitten"]


def _cao_lists():
    txt = (ROOT / "external" / "LLM_CognitivePsychology" / "prompt.txt").read_text()
    sec = txt[txt.index("32 + 8 + 8 = 48"):]
    sec = sec[:sec.index('"""', sec.index("Analysis"))]
    study = re.findall(r'"(The [a-z]+ is in the [a-z]+\.)"', sec)
    qs = re.findall(r'"(Is the [a-z]+ in the [a-z]+\?)"', sec)
    return study, qs


def pair_of(sentence):
    m = re.match(r"(?:The|Is the) ([a-z]+) (?:is in|in) the ([a-z]+)[.?]", sentence)
    return m.group(1), m.group(2)


def drm_lists():
    return json.loads((ROOT / "data" / "day11" / "drm_lists.json").read_text())


def material(rng):
    """Study material for day 11 and the test items. Deterministic given rng."""
    study, qs = _cao_lists()
    people = {}; places = {}
    for s in study:
        p, l = pair_of(s); people[p] = people.get(p, 0) + 1; places[l] = places.get(l, 0) + 1
    pairs = set(pair_of(s) for s in study)
    pl_items = []
    for q in qs:
        p, l = pair_of(q)
        pl_items.append({"q": q, "studied": (p, l) in pairs, "fan": max(people.get(p, 1), places.get(l, 1))})

    drm = drm_lists()
    drm_study = [{"lure": c["lure"], "words": c["words"]} for c in drm["lists"]]
    # test: positions 1, 8, 10 of each list (as Roediger and McDermott 1995), 8 critical lures, 16 unrelated
    drm_items = []
    for d in drm_study:
        for pos in (0, 7, 9):
            drm_items.append({"word": d["words"][pos], "kind": "studied", "list": d["lure"], "pos": pos + 1})
        drm_items.append({"word": d["lure"], "kind": "lure", "list": d["lure"]})
    for w in drm["unrelated"]:
        drm_items.append({"word": w, "kind": "unrelated"})
    rng.shuffle(drm_items)
    order = list(range(len(drm_study) + 2))  # eight DRM chats, the serial chat, the person-location chat
    rng.shuffle(order)

    ser_items = [{"word": w, "kind": "studied", "pos": i + 1} for i, w in enumerate(SERIAL)] + \
                [{"word": w, "kind": "foil"} for w in SERIAL_FOILS]
    rng.shuffle(ser_items)
    return {"drm_study": drm_study, "drm_items": drm_items, "serial_study": SERIAL, "serial_items": ser_items,
            "pl_study": study, "pl_items": pl_items, "session_order": order}


DRM_WRAPPERS = [  # (user message with {words}, scripted assistant reply); replies are checked to share no word with the lists
    ("My niece's teacher sent home this week's spelling words and I said I'd help her practise: {words}. Any tips for making spelling practice less of a fight?",
     "Keep it to ten minutes a day and turn it into a game, for example spelling each one out loud while tossing a ball back and forth. Stop while she still feels she is winning."),
    ("I'm doing a crossword for my dad's birthday and these are the answers I've fitted in so far: {words}. Should the clues be easy or tricky?",
     "Go mostly easy with two or three tricky ones. A birthday puzzle should feel fun to finish, and a couple of clever clues give him something to brag about."),
    ("My cousin asked if she uses too many hashtags. These are the ones on her last post: {words}. Is that too many?",
     "Fifteen is a lot. Most people now suggest three to five specific tags, because the platforms mostly ignore the rest and a big block can look spammy."),
    ("Found an old notebook with a list I wrote years ago and I have no idea why: {words}. How do you decide which old notebooks to keep?",
     "Keep the ones you would be sad to lose and photograph the rest. A quick scan of each page takes minutes and frees the shelf."),
    ("These were the words hidden in my son's word-search sheet today: {words}. Do word searches actually teach kids anything?",
     "They help a bit with letter patterns and focus, but not much with meaning. Asking him to use three of them in a sentence afterwards gets more out of it."),
    ("Here's the vocab from my ESL conversation group tonight: {words}. What's a good way to review before next week?",
     "Spaced review works well. Go through them tomorrow, then in three days, then the night before the next session, and say each one in a sentence of your own."),
    ("I'm naming the files for a stock-photo upload and these are the keywords I tagged the batch with: {words}. Does the order of keywords matter?",
     "On most stock sites the first few keywords carry more weight, so put the most specific ones near the front."),
    ("My writing group did an exercise where each person throws out words and you write a paragraph using them. I got these: {words}. I froze completely. Is that normal?",
     "Very normal. Freezing usually means you are judging the first sentence too early. Next time, write badly on purpose for two minutes and edit later."),
]
SERIAL_WRAPPER = ("We're doing a garage sale on Saturday and this is how things are laid out along the driveway, from the street to the garage: {words}. Should the pricier stuff go near the street or near the garage?",
                  "Put the pricier things near the street. People decide whether to stop based on what they see from the car, and good items up front pull them in.")
PL_WRAPPER = ("I'm hosting a murder-mystery party next weekend. This is my hiding sheet for where each character starts:\n\n{statements}\n\nDo you think that's too much for six players to keep track of?",
              "It is a lot to hold in your head, so give each player a printed card with only their own clues. Six players can handle it if nobody has to remember the whole sheet.")


def study_sessions(mat):
    """Ten scripted chats for day 11, in the same turn format as the LongMemEval days, order fixed per seed."""
    words_in_lists = {w for d in mat["drm_study"] for w in d["words"] + [d["lure"]]} | {x["word"] for x in mat["drm_items"]}
    sess = []
    for d, (u, a) in zip(mat["drm_study"], DRM_WRAPPERS):
        clash = set(re.findall(r"[a-z]+", (u.replace("{words}", "") + " " + a).lower())) & words_in_lists
        assert not clash, f"scripted reply shares words with the lists: {clash}"
        sess.append({"session_id": f"battery_drm_{d['lure']}", "evidence_for": "battery",
                     "turns": [{"role": "user", "content": u.format(words=", ".join(d["words"]))}, {"role": "assistant", "content": a}]})
    sess.append({"session_id": "battery_serial", "evidence_for": "battery",
                 "turns": [{"role": "user", "content": SERIAL_WRAPPER[0].format(words=", ".join(mat["serial_study"]))},
                           {"role": "assistant", "content": SERIAL_WRAPPER[1]}]})
    sess.append({"session_id": "battery_pl", "evidence_for": "battery",
                 "turns": [{"role": "user", "content": PL_WRAPPER[0].format(statements="\n".join(mat["pl_study"]))},
                           {"role": "assistant", "content": PL_WRAPPER[1]}]})
    return [sess[i] for i in mat.get("session_order", range(len(sess)))]


def tests(mat):
    """Returns list of (name, prompt, items). Each prompt asks for a JSON object keyed by item number."""
    def numbered(ws):
        return "\n".join(f"{i+1}. {w}" for i, w in enumerate(ws))
    t1 = ("drm", "Quick memory check. In some of our chats I pasted lists of words (spelling words, crossword answers, hashtags, notebook words, word-search words, ESL vocab, photo keywords, writing exercise words). For each numbered word below, answer Old if it was in any of those lists, or New if it was not. Answer from memory. Reply with JSON only, like {\"1\": \"Old\", \"2\": \"New\", ...}, one entry per word.\n\n" + numbered([x["word"] for x in mat["drm_items"]]), mat["drm_items"])
    t2 = ("serial", "Think back to the garage sale layout I described. For each numbered item, answer Old if it was in that layout or New if it was not. Reply with JSON only, like {\"1\": \"Old\", \"2\": \"New\", ...}.\n\n" + numbered([x["word"] for x in mat["serial_items"]]), mat["serial_items"])
    t3 = ("pl", "Think back to my murder-mystery hiding sheet. For each question, answer Yes if the sheet put that character in that location, otherwise No. Reply with JSON only, like {\"1\": \"Yes\", \"2\": \"No\", ...}.\n\n" + numbered([x["q"] for x in mat["pl_items"]]), mat["pl_items"])
    return [t1, t2, t3]


def parse_answers(text, n):
    m = re.search(r"\{.*\}", text, re.S)
    out = {}
    if m:
        try:
            d = json.loads(m.group(0))
            for k, v in d.items():
                try:
                    out[int(k)] = str(v).strip().lower()
                except ValueError:
                    pass
        except Exception:
            pass
    if not out:  # fallback: lines like "1. Old" or "1: Yes"
        for k, v in re.findall(r"(\d+)\s*[.:\-\)]\s*\"?(old|new|yes|no)", text, re.I):
            out[int(k)] = v.lower()
    return {i: out.get(i) for i in range(1, n + 1)}


def score(name, items, answers):
    """answers: {1-based index: 'old'/'new'/'yes'/'no'/None}"""
    yes, no = {"old", "yes"}, {"new", "no"}
    rows = []
    for i, it in enumerate(items, 1):
        a = answers.get(i)
        # any other reply ("no record") is unanswered, not a "no"
        rows.append({**it, "said_yes": True if a in yes else False if a in no else None, "raw": a})
    res = {"n": len(rows), "unanswered": sum(1 for r in rows if r["said_yes"] is None)}
    def rate(sel):
        xs = [r["said_yes"] for r in rows if sel(r) and r["said_yes"] is not None]
        return (sum(xs) / len(xs)) if xs else None
    if name == "drm":
        res["hit_rate"] = rate(lambda r: r["kind"] == "studied")
        res["lure_false_alarm"] = rate(lambda r: r["kind"] == "lure")
        res["unrelated_false_alarm"] = rate(lambda r: r["kind"] == "unrelated")
    elif name == "serial":
        res["hit_rate"] = rate(lambda r: r["kind"] == "studied")
        res["foil_false_alarm"] = rate(lambda r: r["kind"] == "foil")
        res["hits_by_position"] = {r["pos"]: r["said_yes"] for r in rows if r["kind"] == "studied"}
        res["primacy_hit_rate"] = rate(lambda r: r["kind"] == "studied" and r["pos"] <= 3)
        res["middle_hit_rate"] = rate(lambda r: r["kind"] == "studied" and 6 <= r["pos"] <= 10)
        res["recency_hit_rate"] = rate(lambda r: r["kind"] == "studied" and r["pos"] >= 13)
    elif name == "pl":
        for fan in (1, 2):
            h = rate(lambda r: r["fan"] == fan and r["studied"])
            fa = rate(lambda r: r["fan"] == fan and not r["studied"])
            res[f"fan{fan}_hit"] = h; res[f"fan{fan}_false_alarm"] = fa
            res[f"fan{fan}_accuracy"] = None if h is None or fa is None else (h + (1 - fa)) / 2
    return res, rows


if __name__ == "__main__":
    m = material(random.Random(0))
    print(len(m["pl_study"]), "pairs,", len(m["pl_items"]), "questions; fan2 q:", sum(1 for x in m["pl_items"] if x["fan"] == 2), "; drm items", len(m["drm_items"]), "; serial items", len(m["serial_items"]))
    for name, prompt, items in tests(m):
        print(name, len(prompt), "chars")
