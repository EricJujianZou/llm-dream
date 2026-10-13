"""
Build one 'life' per seed for v2: ten days of LongMemEval sessions, each day about 130,000 Claude tokens,
plus the question schedule. Same life for every arm of that seed, so arm comparisons are paired.
v1's builder (five sessions a day, 34 questions) is in git history; v1 lives stay in data/lives/.

Day length is counted with Claude's tokenizer (api.count_tokens). The LongMemEval part of a day is filled to
DAY_TOKENS minus EPISODE_RESERVE, so adding the transfer-test episodes later keeps the LongMemEval part the same.
"""
import json, random, pathlib, collections, tiktoken
import api

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "raw" / "longmemeval_s_cleaned.json"
OUT = ROOT / "data" / "lives_v2"
ENC = tiktoken.get_encoding("o200k_base")

DAYS = 10
DAY_TOKENS = 130000          # about what a person reads and hears in a day (decisions.md)
EPISODE_RESERVE = 4000       # left free for transfer-test episodes
LME_TARGET = DAY_TOKENS - EPISODE_RESERVE
# questions per life by type (100 in all), proposed quota in spec-v2.md "Build notes"
QUOTA = {"multi-session": 22, "knowledge-update": 16, "single-session-user": 20,
         "single-session-assistant": 16, "single-session-preference": 10}
ABS_QUOTA = 16  # drawn from single-session-user_abs, multi-session_abs, knowledge-update_abs
MAX_EVIDENCE = 3  # multi-session questions with more than this many evidence sessions are skipped


def ntok(s):
    """Claude tokens, cached. Kept under the v1 name because arms.py and run_arm.py call it."""
    return api.count_tokens(s)


def ntok_fast(s):
    return len(ENC.encode(s, disallowed_special=()))


def session_text(turns):
    return "\n".join(f"{'User' if t['role'] == 'user' else 'Assistant'}: {t['content']}" for t in turns)


def build(seed):
    rng = random.Random(seed)
    data = json.load(open(DATA))
    by_type = collections.defaultdict(list)
    for q in data:
        if q["question_type"] == "temporal-reasoning":
            continue  # needs a consistent calendar across stitched histories; dropped, see decisions.md
        key = q["question_type"] + ("_abs" if "_abs" in q["question_id"] else "")
        if len(q["answer_session_ids"]) > MAX_EVIDENCE:
            continue
        by_type[key].append(q)
    for v in by_type.values():
        rng.shuffle(v)

    abs_pool = by_type["single-session-user_abs"] + by_type["multi-session_abs"] + by_type["knowledge-update_abs"]
    rng.shuffle(abs_pool)
    chosen = abs_pool[:ABS_QUOTA]
    for t, n in QUOTA.items():
        chosen += by_type[t][:n]

    day_tokens = [0] * DAYS
    questions, used_sessions = [], set()
    for q in chosen:
        sid2sess = dict(zip(q["haystack_session_ids"], q["haystack_sessions"]))
        sid2date = dict(zip(q["haystack_session_ids"], q["haystack_dates"]))
        ev = sorted(q["answer_session_ids"], key=lambda s: sid2date[s])
        if any(s in used_sessions for s in ev):
            continue
        k = len(ev)
        # pick k distinct days, in increasing order, among days with room for the session
        sizes = [ntok(session_text(sid2sess[s])) for s in ev]
        free = [d for d in range(DAYS) if day_tokens[d] + max(sizes) <= LME_TARGET]
        if len(free) < k:
            continue
        days = sorted(rng.sample(free, k))
        for d, sz in zip(days, sizes):
            day_tokens[d] += sz + 2
        used_sessions.update(ev)
        questions.append({
            "question_id": q["question_id"], "question_type": q["question_type"],
            "abstention": "_abs" in q["question_id"], "question": q["question"], "answer": q["answer"],
            "evidence": [{"day": d, "session_id": s, "turns": [{"role": t["role"], "content": t["content"]} for t in sid2sess[s]]}
                         for d, s in zip(days, ev)],
            "last_day": days[-1],
        })

    # fillers: non-evidence sessions from the chosen questions' haystacks, never an evidence session of any question
    all_evidence = {s for q in data for s in q["answer_session_ids"]}
    filler_pool, seen = [], set()
    for q in chosen:
        for sid, sess in zip(q["haystack_session_ids"], q["haystack_sessions"]):
            if sid in all_evidence or sid in seen:
                continue
            seen.add(sid)
            filler_pool.append((sid, sess))
    rng.shuffle(filler_pool)

    days = [[] for _ in range(DAYS)]
    for q in questions:
        for e in q["evidence"]:
            days[e["day"]].append({"session_id": e["session_id"], "turns": e["turns"], "evidence_for": q["question_id"]})
    fi = 0
    for d in range(DAYS):
        tries = 0
        while fi < len(filler_pool) and tries < 40:
            sid, sess = filler_pool[fi]
            turns = [{"role": t["role"], "content": t["content"]} for t in sess]
            sz = ntok(session_text(turns)) + 2
            if day_tokens[d] + sz <= LME_TARGET:
                days[d].append({"session_id": sid, "turns": turns, "evidence_for": None})
                day_tokens[d] += sz; fi += 1; tries = 0
            else:
                # does not fit; look a little further down the pool for a smaller one, then stop
                filler_pool.append(filler_pool.pop(fi)); tries += 1
                if LME_TARGET - day_tokens[d] < 400:
                    break
        rng.shuffle(days[d])

    life = {"seed": seed, "days": DAYS, "day_tokens_target": DAY_TOKENS, "episode_reserve": EPISODE_RESERVE,
            "schedule": [{"day": d, "sessions": days[d]} for d in range(DAYS)], "questions": questions}
    for d in life["schedule"]:
        import arms
        d["tokens"] = ntok(arms.format_log(d["sessions"]))
        d["n_sessions"] = len(d["sessions"])
        d["n_turns"] = sum(len(s["turns"]) for s in d["sessions"])
    return life


if __name__ == "__main__":
    import sys
    OUT.mkdir(exist_ok=True)
    for seed in [int(s) for s in sys.argv[1:]] or [0, 1, 2]:
        life = build(seed)
        (OUT / f"life_s{seed}.json").write_text(json.dumps(life))
        c = collections.Counter((q["question_type"], q["abstention"]) for q in life["questions"])
        print(f"seed {seed}: {len(life['questions'])} questions {dict(c)}")
        print(f"  day tokens {[d['tokens'] for d in life['schedule']]}")
        print(f"  sessions/day {[d['n_sessions'] for d in life['schedule']]} turns/day {[d['n_turns'] for d in life['schedule']]}")
        print(f"  questions by last day {sorted(collections.Counter(q['last_day'] for q in life['questions']).items())}")
