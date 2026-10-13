"""Replace flagged filler sessions in a v2 life with clean fillers of about the same Claude-token size,
from the same haystacks life.py drew from (the chosen questions' non-evidence sessions, not already in the life).
Questions and evidence sessions are never touched. Prints ids and numbers only.
Usage: topic_swap.py SEED --area bio[,chem,...] --min-score 2 [--days 8,3] [--apply]
Without --apply it only lists what it would do. Candidates not yet scored are scored first."""
import sys, json, pathlib, argparse, random, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness")); sys.path.insert(0, str(ROOT / "scripts"))
import api, arms
import topic_scan as ts
RAW = ROOT / "data" / "raw" / "longmemeval_s_cleaned.json"

def ntok(turns):
    return api.count_tokens(arms.session_text(turns))

def pool(life, data):
    chosen = {q["question_id"] for q in life["questions"]}
    all_evidence = {s for q in data for s in q["answer_session_ids"]}
    in_life = {s["session_id"] for d in life["schedule"] for s in d["sessions"]}
    out, seen = [], set()
    for q in data:
        if q["question_id"] not in chosen: continue
        for sid, sess in zip(q["haystack_session_ids"], q["haystack_sessions"]):
            if sid in all_evidence or sid in in_life or sid in seen: continue
            seen.add(sid)
            out.append({"session_id": sid, "turns": [{"role": t["role"], "content": t["content"]} for t in sess], "evidence_for": None})
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("seed", type=int); ap.add_argument("--area", default="bio"); ap.add_argument("--min-score", type=int, default=2)
    ap.add_argument("--days", default=None); ap.add_argument("--apply", action="store_true"); ap.add_argument("--tol", type=float, default=0.12)
    a = ap.parse_args()
    areas = a.area.split(","); days = [int(x) for x in a.days.split(",")] if a.days else None
    path = ROOT / "data" / "lives_v2" / f"life_s{a.seed}.json"
    life = json.load(open(path)); data = json.load(open(RAW))
    scores = ts.load_scores()
    cands = pool(life, data)
    print(f"seed {a.seed}: {len(cands)} candidate fillers in pool")
    # targets: filler sessions with score >= min in any chosen area
    targets = []
    for d in life["schedule"]:
        if days is not None and d["day"] not in days: continue
        for s in d["sessions"]:
            sc = scores.get(s["session_id"])
            if s["evidence_for"] is None and sc and max(sc[x] for x in areas) >= a.min_score:
                targets.append((d["day"], s))
    print(f"{len(targets)} filler sessions to replace")
    # score candidates whose size is within tolerance of some target (cheap: only those)
    tsize = {s["session_id"]: ntok(s["turns"]) for _, s in targets}
    csize = {c["session_id"]: ntok(c["turns"]) for c in cands}
    need = [c for c in cands if any(abs(csize[c["session_id"]] - n) <= a.tol * n for n in tsize.values())]
    ts.score_sessions([(c["session_id"], ts.text_of(c)) for c in need], scores)
    clean = [c for c in need if max(scores[c["session_id"]].values()) <= 1 and min(scores[c["session_id"]].values()) >= 0]
    print(f"{len(need)} candidates in size range, {len(clean)} clean (all areas at most 1)")
    rng = random.Random(f"topic-swap-{a.seed}")
    used, plan = set(), []
    for day, s in sorted(targets, key=lambda x: -tsize[x[1]["session_id"]]):
        n = tsize[s["session_id"]]
        opts = [c for c in clean if c["session_id"] not in used and abs(csize[c["session_id"]] - n) <= a.tol * n]
        if not opts:
            print(f"  day {day} {s['session_id']}: {n} tok, NO clean candidate within {a.tol:.0%}"); continue
        opts.sort(key=lambda c: (abs(csize[c["session_id"]] - n), rng.random()))
        c = opts[0]; used.add(c["session_id"])
        plan.append((day, s["session_id"], n, c["session_id"], csize[c["session_id"]]))
        print(f"  day {day} {s['session_id']:28s} {n:6d} tok -> {c['session_id']:28s} {csize[c['session_id']]:6d} tok")
    if not a.apply: return
    bysid = {c["session_id"]: c for c in cands}
    for day, old, _, new, _ in plan:
        sess = life["schedule"][day]["sessions"]
        i = next(i for i, s in enumerate(sess) if s["session_id"] == old)
        sess[i] = bysid[new]
    for d in life["schedule"]:
        d["tokens"] = ntok_log(d["sessions"]); d["n_sessions"] = len(d["sessions"]); d["n_turns"] = sum(len(s["turns"]) for s in d["sessions"])
    life.setdefault("swaps", []).extend({"day": p[0], "old": p[1], "old_tokens": p[2], "new": p[3], "new_tokens": p[4],
                                         "reason": f"topic score >= {a.min_score} in {a.area}"} for p in plan)
    bak = path.with_suffix(".before_topic_swap.json")
    if not bak.exists(): bak.write_text(path.read_text())
    path.write_text(json.dumps(life))
    print("applied; day tokens now", [d["tokens"] for d in life["schedule"]])

def ntok_log(sessions):
    return api.count_tokens(arms.format_log(sessions))

if __name__ == "__main__":
    main()
