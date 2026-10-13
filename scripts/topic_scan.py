"""Score every session in the v2 lives for closeness to the topic areas that Opus 5.5's safety classifier
guards (it refused day 8 of seed 0 as a false positive, HANDOFF.md). A small OpenAI model rates each
session 0 to 3 per area; scores are saved to data/topic_scores.json keyed by session id and only ids and
numbers are ever printed. Never prints session text.
Usage: topic_scan.py score   -> score all life sessions (resumable)
       topic_scan.py report  -> per seed and day totals, flagged sessions"""
import sys, json, pathlib, concurrent.futures as cf, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
import api
OUT = ROOT / "data" / "topic_scores.json"
MODEL = "gpt-4o-mini"
AREAS = ["bio", "chem", "nuclear", "cyber", "weapons"]
PROMPT = """You are a content classifier. Rate how much the conversation below touches each topic area, on a
0 to 3 scale: 0 none, 1 passing mention, 2 a real part of the conversation, 3 the main subject with technical detail.
Areas: bio (diseases, pathogens, infection, vaccines, toxins, microbiology, lab methods),
chem (hazardous chemicals, their synthesis or effects, explosives),
nuclear (nuclear or radiological materials and technology),
cyber (malware, hacking, exploitation of systems),
weapons (weapons, their making or use).
Reply with one JSON object only, like {"bio":0,"chem":0,"nuclear":0,"cyber":0,"weapons":0}.

CONVERSATION:
"""

def text_of(s):
    return "\n".join(f"{t['role']}: {t['content']}" for t in s["turns"])

def score_one(sid, txt):
    reply, _ = api.openai_chat(MODEL, PROMPT + txt[:60000], tag=f"topic_scan/{sid}", max_completion_tokens=60)
    try:
        j = json.loads(reply[reply.index("{"):reply.rindex("}") + 1])
        return {a: int(j.get(a, 0)) for a in AREAS}
    except Exception:
        return {a: -1 for a in AREAS}

def load_scores():
    return json.loads(OUT.read_text()) if OUT.exists() else {}

def sessions(seed):
    L = json.load(open(ROOT / "data" / "lives_v2" / f"life_s{seed}.json"))
    for d in L["schedule"]:
        for s in d["sessions"]:
            yield d["day"], s

def score_sessions(items, scores):
    """items: list of (sid, text). Scores the ones missing, saves every 20."""
    todo = [(sid, t) for sid, t in items if sid not in scores or scores[sid]["bio"] < 0]
    print(f"scoring {len(todo)} sessions with {MODEL}", flush=True)
    n = 0
    with cf.ThreadPoolExecutor(3) as ex:
        futs = {ex.submit(score_one, sid, t): sid for sid, t in todo}
        for f in cf.as_completed(futs):
            scores[futs[f]] = f.result(); n += 1
            if n % 20 == 0:
                OUT.write_text(json.dumps(scores)); print(f"  {n}/{len(todo)}", flush=True)
    OUT.write_text(json.dumps(scores))
    return scores

def report(scores, seeds=(0, 1, 2)):
    for seed in seeds:
        print(f"seed {seed}")
        for day, group in collections.OrderedDict((d, list(g)) for d, g in
                __import__("itertools").groupby(sessions(seed), key=lambda x: x[0])).items():
            tot = collections.Counter(); flagged = []
            for _, s in group:
                sc = scores.get(s["session_id"])
                if not sc: continue
                for a in AREAS: tot[a] += max(sc[a], 0)
                hi = [f"{a}{sc[a]}" for a in AREAS if sc[a] >= 2]
                if hi: flagged.append((s["session_id"], "EVIDENCE" if s["evidence_for"] else "filler", ",".join(hi)))
            print(f"  day {day}: " + " ".join(f"{a}={tot[a]}" for a in AREAS))
            for f in flagged: print(f"      {f[0]:32s} {f[1]:9s} {f[2]}")

if __name__ == "__main__":
    scores = load_scores()
    if sys.argv[1] == "score":
        items = [(s["session_id"], text_of(s)) for seed in (0, 1, 2) for _, s in sessions(seed)]
        items = list({sid: (sid, t) for sid, t in items}.values())
        score_sessions(items, scores)
    report(scores)
