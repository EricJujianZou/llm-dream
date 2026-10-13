"""The night steps. Only this file differs between arms; the day loop and the prompts the agent sees are shared.
v2: seven arms, a cap that grows each night, item memory (memory.py), batched structured corruption."""
import json, random, re, pathlib, copy
import api, memory
from life import ntok, ntok_fast, session_text

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Cap per night, tokens. Sum of what a person keeps of each earlier day (decisions.md, "Rationale for the
# 130,000-token day and the growing cap"). The eleventh value, for the day-11 battery night, continues the
# same curve (15 x t^-0.4 percent of a 130,000-token day for the eleventh day) and is rounded to 124,500.
CAPS = [19500, 35100, 48100, 59800, 70850, 81250, 91000, 100100, 108550, 117000, 124500]


def cap_for(night, scale=1.0):
    c = CAPS[min(night, len(CAPS) - 1)]
    return int(c * scale)


ARMS = ["nosleep", "faithful", "structured_05", "structured_10", "structured_20", "structured_40",
        "random_05", "random_10", "random_20", "random_40"]
RATE = {"structured_05": 0.05, "structured_10": 0.10, "structured_20": 0.20, "structured_40": 0.40, "random_20": 0.20}

# Eric's wording from spec-v2.md Change 1, kept as is. The last paragraph replaces v1's "Output only the memory
# text", because the memory is now a list of items returned as a delta (decisions.md).
SLEEP_SYSTEM = """You are the sleeping mind of a personal assistant. Tonight you turn today's experiences into long-term memory. Tomorrow the assistant wakes up with only what you write here. Today's transcript will be gone.

Consolidate the way sleep does in people:
- Keep what came up more than once, today or on earlier days.
- Keep what was emotional, surprising or new.
- Connect today's events to what is already in memory, and merge them into it.
- When something changed, keep the newer version and note that it changed.
- Keep the gist. Exact wording can go.
- Let one-off details that never came back fade.

The memory may hold up to {cap} tokens after tonight. It holds {before} tokens now. After tonight it should hold close to {cap} tokens, so it has to grow by about {room_words} words. Rewriting an existing item replaces its text and adds nothing, so that growth has to come from new items and from details added to the items you rewrite. Fill it with specifics from today's transcript (names, numbers, places, what was said and how it went), not filler.

The memory is a list of items. Each item has an id, a one-line gist, its details, and an importance score from 1 to 5. You will see the existing items with their ids. Reply with your changes only, as JSON:
- "add": new items from today, each with "gist", "details" and "score".
- "update": existing items to rewrite, each with "id", "gist", "details" and "score". Use this when something changed or came up again.
- "merge": groups of existing items that belong together, each with "ids", "gist", "details" and "score". The group becomes one item.
Items you do not mention stay as they are. When the memory is over its limit, details are forgotten from the lowest-scored items first, and whole items are forgotten only once every item is down to its gist, so the score is how you choose what fades."""

SLEEP_SCHEMA = {
    "type": "object",
    "properties": {
        "add": {"type": "array", "items": {"type": "object", "properties": {
            "gist": {"type": "string"}, "details": {"type": "string"}, "score": {"type": "integer"}},
            "required": ["gist", "details", "score"], "additionalProperties": False}},
        "update": {"type": "array", "items": {"type": "object", "properties": {
            "id": {"type": "string"}, "gist": {"type": "string"}, "details": {"type": "string"}, "score": {"type": "integer"}},
            "required": ["id", "gist", "details", "score"], "additionalProperties": False}},
        "merge": {"type": "array", "items": {"type": "object", "properties": {
            "ids": {"type": "array", "items": {"type": "string"}}, "gist": {"type": "string"}, "details": {"type": "string"}, "score": {"type": "integer"}},
            "required": ["ids", "gist", "details", "score"], "additionalProperties": False}},
    },
    "required": ["add", "update", "merge"], "additionalProperties": False,
}

CORRUPT_SYSTEM = """You edit chat transcripts for a memory experiment. You will receive numbered turns from today's transcript and a list of edits to make. For each listed turn, rewrite it so it is still fluent and plausible in context but factually different:
- "swap": replace one concrete detail (a name, number, place, date, item, or outcome) with a concrete detail taken from a different turn in the transcript.
- "change": replace one or two concrete details with new, plausible but different ones.
Keep each rewritten turn about the same length and the same speaker. Do not mark the edits. Return JSON only, in the form {"edits": [{"index": 12, "text": "rewritten turn"}, ...]}."""

CORRUPT_SCHEMA = {"type": "object", "properties": {"edits": {"type": "array", "items": {
    "type": "object", "properties": {"index": {"type": "integer"}, "text": {"type": "string"}},
    "required": ["index", "text"], "additionalProperties": False}}},
    "required": ["edits"], "additionalProperties": False}
CORRUPT_BATCH_TOKENS = 25000  # transcript tokens per corruption call


def format_log(sessions):
    """sessions: list of {turns:[{role,content}]} -> transcript text. Turn order is the event order."""
    out = []
    for i, s in enumerate(sessions, 1):
        out.append(f"Session {i}")
        for t in s["turns"]:
            who = "User" if t["role"] == "user" else "Assistant"
            out.append(f"{who}: {t['content']}")
        out.append("")
    return "\n".join(out)


def flat_turns(sessions):
    return [t for s in sessions for t in s["turns"]]


# ---- shared sleep step: item memory --------------------------------------------------------------
def sleep_items(mem, log_text, tag, cap, night):
    """mem: {"items": [...], "next_id": int}. Returns (new_mem, info)."""
    items = copy.deepcopy(mem["items"])
    before = memory.tokens(items)
    room = max(0, cap - before)
    system = SLEEP_SYSTEM.format(cap=cap, before=before, room_words=int(room * 0.75))  # about 0.75 English words per token
    user = (f"EXISTING MEMORY ({len(items)} items, {before} tokens):\n{memory.render_for_sleep(items) or '(empty)'}\n\n"
            f"TODAY'S TRANSCRIPT:\n{log_text}\n\nReturn the JSON with your changes.")
    r = api.call(system, [{"role": "user", "content": user}], tag=f"{tag}/sleep", json_schema=SLEEP_SCHEMA, timeout=3600)
    delta = json.loads(r["text"])
    items, next_id, drep = memory.apply_delta(items, delta, night, mem["next_id"])
    items, crep = memory.enforce_cap(items, cap)
    info = {"call_id": r["call_id"], "seconds": round(r["seconds"], 1), "output_tokens": r["usage"].get("output_tokens"),
            "delta": drep, "cap_report": crep, "tokens_before_night": before}
    return {"items": items, "next_id": next_id}, info


# ---- arm 1: no sleep, sliding window over raw turns -------------------------------------------
def night_nosleep(mem, sessions, archive, rng, tag, cap, night):
    """mem: {"window": str}. Keeps the most recent raw turns that fit the cap, in Claude tokens."""
    turns = [f"{'User' if t['role']=='user' else 'Assistant'}: {t['content']}" for t in flat_turns(sessions)]
    window = (mem["window"].split("\n\n") if mem.get("window") else []) + turns
    # estimate per turn with tiktoken scaled by the Claude-to-tiktoken ratio of this day's log, then verify
    day_text = "\n\n".join(turns)
    ratio = ntok(day_text) / max(1, ntok_fast(day_text))
    est = [ntok_fast(t) * ratio + 1 for t in window]
    kept, total = [], 0.0
    for t, n in zip(reversed(window), reversed(est)):
        if total + n > cap:
            break
        kept.append(t); total += n
    kept = list(reversed(kept))
    exact = ntok("\n\n".join(kept)) if kept else 0
    while exact > cap and kept:
        drop = max(1, int((exact - cap) / max(1.0, exact / len(kept))))
        kept = kept[drop:]
        exact = ntok("\n\n".join(kept)) if kept else 0
    if not kept and window:  # one turn bigger than the whole cap
        kept = [window[-1][: cap * 3]]
        exact = ntok(kept[0])
    return {"window": "\n\n".join(kept)}, {"kept_turns": len(kept), "tokens": exact, "window_turns": len(window)}


# ---- arm 2: faithful replay -------------------------------------------------------------------
def night_faithful(mem, sessions, archive, rng, tag, cap, night):
    return sleep_items(mem, format_log(sessions), tag, cap, night)


# ---- arms 3 to 6: noisy replay, structured ------------------------------------------------------
def corrupt_structured(sessions, archive, rng, tag, rate):
    """Returns (corrupted_sessions, report). `rate` of turns: a third swapped, a third changed, a third spliced
    from earlier days. Swaps and changes are rewritten by the model in batches of about 25,000 transcript tokens;
    a swap takes its detail from a turn in the same batch."""
    sessions = copy.deepcopy(sessions)
    turns = flat_turns(sessions)
    n = len(turns)
    k = max(1, round(rate * n))
    idx = rng.sample(range(n), k)
    kinds = ["swap", "change", "splice"]
    plan = {i: kinds[j % 3] for j, i in enumerate(idx)}
    earlier = [t for day in archive for t in flat_turns(day)]
    if not earlier:
        plan = {i: ("change" if kind == "splice" else kind) for i, kind in plan.items()}
    report = {"n_turns": n, "n_corrupted": k, "rate": rate, "plan": {str(i): kind for i, kind in plan.items()},
              "before": {}, "after": {}, "llm_calls": [], "llm_applied": 0}
    for i, kind in plan.items():
        if kind == "splice":
            pool = [t for t in earlier if t["role"] == turns[i]["role"]] or earlier
            src = rng.choice(pool)
            report["before"][str(i)] = turns[i]["content"]
            turns[i]["content"] = src["content"]
            report["after"][str(i)] = turns[i]["content"]
    llm_edits = {i: kind for i, kind in plan.items() if kind != "splice"}
    # batches: consecutive sessions up to CORRUPT_BATCH_TOKENS, each with the global turn indices it holds
    batches, cur, cur_tok, gi = [], [], 0, 0
    for s in sessions:
        st = ntok(session_text(s["turns"]))
        rng_idx = list(range(gi, gi + len(s["turns"]))); gi += len(s["turns"])
        if cur and cur_tok + st > CORRUPT_BATCH_TOKENS:
            batches.append(cur); cur, cur_tok = [], 0
        cur.append((s, rng_idx)); cur_tok += st
    if cur:
        batches.append(cur)
    for b in batches:
        b_idx = [i for _, ids in b for i in ids]
        edits_here = {i: llm_edits[i] for i in b_idx if i in llm_edits}
        if not edits_here:
            continue
        numbered = "\n".join(f"[{i}] {'User' if turns[i]['role']=='user' else 'Assistant'}: {turns[i]['content']}" for i in b_idx)
        edit_list = "\n".join(f"- index {i}: {kind}" for i, kind in sorted(edits_here.items()))
        user = f"TRANSCRIPT:\n{numbered}\n\nEDITS TO MAKE:\n{edit_list}\n\nReturn the JSON."
        r = api.call(CORRUPT_SYSTEM, [{"role": "user", "content": user}], tag=f"{tag}/corrupt", json_schema=CORRUPT_SCHEMA, timeout=3600)
        edits = {}
        try:
            edits = {int(e["index"]): e["text"] for e in json.loads(r["text"])["edits"]}
        except Exception as ex:
            report.setdefault("parse_errors", []).append(str(ex))
        report["llm_calls"].append(r["call_id"])
        for i in edits_here:
            if i in edits and edits[i].strip():
                report["before"][str(i)] = turns[i]["content"]
                turns[i]["content"] = re.sub(r"^(User|Assistant):\s*", "", edits[i].strip())
                report["after"][str(i)] = turns[i]["content"]
                report["llm_applied"] += 1
    return sessions, report


def make_structured(rate):
    def night(mem, sessions, archive, rng, tag, cap, night_no):
        corrupted, report = corrupt_structured(sessions, archive, rng, tag, rate)
        new_mem, info = sleep_items(mem, format_log(corrupted), tag, cap, night_no)
        info["corruption"] = report
        return new_mem, info
    return night


# ---- arm 7: noisy replay, random words and paragraphs from an unrelated corpus -------------------
_corpus = None
def corpus():
    global _corpus
    if _corpus is None:
        txt = (ROOT / "data" / "corpus" / "moby_dick.txt").read_text(errors="ignore")
        start = txt.find("CHAPTER 1. Loomings.")
        end = txt.rfind("*** END OF THE PROJECT GUTENBERG EBOOK")
        body = txt[start:end if end > 0 else None]
        paras = [re.sub(r"\s+", " ", p).strip() for p in body.split("\n\n")]
        paras = [p for p in paras if len(p.split()) >= 15]
        words = [w for p in paras for w in p.split()]
        _corpus = (paras, words)
    return _corpus


def corrupt_random(sessions, rng, rate):
    sessions = copy.deepcopy(sessions)
    turns = flat_turns(sessions)
    paras, words = corpus()
    n = len(turns)
    k = max(1, round(rate * n))
    idx = rng.sample(range(n), k)
    report = {"n_turns": n, "n_corrupted": k, "rate": rate, "plan": {}, "before": {}, "after": {}}
    for j, i in enumerate(idx):
        orig = turns[i]["content"]
        ow = orig.split()
        report["before"][str(i)] = orig
        if j % 2 == 0:
            need = max(5, len(ow))
            start = rng.randrange(len(words) - need)
            turns[i]["content"] = " ".join(words[start:start + need])
            report["plan"][str(i)] = "paragraph"
        else:
            m = max(1, int(0.3 * len(ow)))
            for _ in range(m):
                ow.insert(rng.randrange(len(ow) + 1), rng.choice(words))
            turns[i]["content"] = " ".join(ow)
            report["plan"][str(i)] = "words"
        report["after"][str(i)] = turns[i]["content"]
    return sessions, report


def make_random(rate):
    def night(mem, sessions, archive, rng, tag, cap, night_no):
        corrupted, report = corrupt_random(sessions, rng, rate)
        new_mem, info = sleep_items(mem, format_log(corrupted), tag, cap, night_no)
        info["corruption"] = report
        return new_mem, info
    return night


NIGHT = {"nosleep": night_nosleep, "faithful": night_faithful,
         "structured_05": make_structured(0.05), "structured_10": make_structured(0.10),
         "structured_20": make_structured(0.20), "structured_40": make_structured(0.40),
         "random_05": make_random(0.05), "random_10": make_random(0.10),
         "random_20": make_random(0.20), "random_40": make_random(0.40)}
