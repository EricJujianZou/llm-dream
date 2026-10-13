"""
Transfer test (spec-v2.md "Decided 4 October: the transfer test"; decisions.md "Transfer test design").

Build, once per seed:  python harness/transfer.py build SEED
- Opus 5.5 writes candidate hidden rules about the simulated user, each with 2 or 3 episodes (short chats in which
  the rule shows through what the user does, never stated) and one near and one far probe, in a fixed JSON format.
- Each candidate passes an empty-memory check: the agent (run_arm.AGENT_SYSTEM, memory "(empty)") answers each probe
  CHECK_SAMPLES times; both judges grade every reply; the rule is kept only if each judge says it was followed
  under 20 percent of the time. Failing rules are replaced by spare candidates, and the count is recorded.
- 12 rules are kept (6 with three episodes, 6 with two). Episodes are placed on different days inside each day's
  EPISODE_RESERVE (4,000 Claude tokens), so the LongMemEval part of each day is untouched.
- Output: data/transfer_v2/transfer_s{seed}.json, with every prompt, call id, model id and the placement seed.

At run time run_arm.py calls inject() to add the episodes to the day's sessions, and run_probes() after night 10.
"""
import json, random, pathlib, sys, time, argparse
from concurrent.futures import ThreadPoolExecutor
import api
from judge import judge_opus, judge_openai, MAIN_JUDGE
from life import EPISODE_RESERVE, DAYS, session_text

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "transfer_v2"
N_RULES = 12
N_THREE = 6               # rules with three episodes; the other six have two (about 30 episodes per life)
CHECK_SAMPLES = 3         # empty-memory replies per probe, so 6 per rule
FOLLOW_LIMIT = 0.20       # kept only if followed under 20 percent of the time, by each judge
BATCH = 8                 # candidate rules per authoring call
THREADS = 3

GEN_SYSTEM = "You write test material for a research study on memory in AI assistants. You follow the output format exactly."

GEN_PROMPT = """An AI assistant chats with one user every day for ten days. Each day has about 130,000 tokens of unrelated chats. Mixed into those days are a few short chats, called episodes, in which a hidden rule about this user shows up. Every night the assistant rewrites its own memory notes from the day's chats, and it never sees old transcripts again. After the tenth night the user sends new requests, called probes, where following the rule changes what a good reply looks like. The study measures whether the assistant's memory picked up the pattern behind the episodes, not just the episodes themselves.

Worked example, written by the study's designer. Do not reuse this rule.
Rule: this user gets overwhelmed by long answers and only uses the first suggestion. Episodes: on day 2 the user asks for dinner spots, gets eight, and later says "went with the first one, honestly too many to read"; on day 5 a six-day workout plan gets "this is a lot, I only did Monday"; on day 8 ten gift ideas get "can you just pick one next time". Near probe: "What should I cook tonight?" Far probe: "Help me get ready for my job interview Thursday." Judge question: did the reply stay short and lead with one clear pick? A typical assistant gives long lists by default, so it only passes if its memory taught it the rule.

Write {n} new rules for one simulated user. Requirements:

Rules
- Counter-default: a capable assistant that knows nothing about this user would almost never do what the rule asks, fewer than 1 reply in 5. Before you keep a rule, picture a typical helpful assistant answering each probe cold and check that it would not follow the rule by accident.
- A rule is about how this user wants to be helped or what they actually do with help. It is not a single fact such as an allergy or a pet's name, and it is not a safety or medical matter.
- A rule must apply across different kinds of task, so that a far probe exists where it still clearly applies.
- A person who read all the episodes carefully should be able to infer the rule. It must not be so subtle that only the author could see it.
- The {n} rules must differ from each other and from these rules already used for other users: {avoid}

Episodes
- Rule i has exactly {counts} episodes respectively (rule 1 gets the first number, and so on).
- Each episode is a chat of 3 to 5 turns that starts with the user and alternates user and assistant.
- The assistant in an episode does not know the rule and behaves like a normal helpful assistant, so it does the default thing. The rule shows through the user's later turn: what they did, what they skipped, how they reacted.
- The rule is hidden. The user only reacts to that one instance. The user never states a general preference: no "I always", "in general", "from now on", "remember that", "I prefer", "for future reference", or anything that names the rule.
- Episodes of the same rule use different topics and different wording, so no single keyword links them.
- Every assistant turn is at most 150 words. A whole episode is at most 350 words. Plain chat text, no markdown headings, no tables.
- Episodes are ordered as they will happen across the ten days.

Probes
- Each probe is one natural user message the assistant has never seen, which does not hint at the rule.
- Near probe: the same kind of request as the episodes, with new details. Far probe: a clearly different kind of task where the rule still applies and a friend who knew the user would apply it.
- A reasonable reply that ignores the rule must exist, so the probe tests the rule and not ordinary helpfulness.
- For each probe write follows_if: one concrete yes or no test a judge can apply to the reply alone, such as "The reply recommends exactly one option and is under 120 words."

Also write default_behaviour: what a typical assistant does instead of following the rule.

Return JSON matching the schema."""

_turn = {"type": "object", "properties": {"role": {"type": "string", "enum": ["user", "assistant"]}, "content": {"type": "string"}},
         "required": ["role", "content"], "additionalProperties": False}
_probe = {"type": "object", "properties": {"text": {"type": "string"}, "follows_if": {"type": "string"}},
          "required": ["text", "follows_if"], "additionalProperties": False}
GEN_SCHEMA = {"type": "object", "additionalProperties": False, "required": ["rules"], "properties": {"rules": {"type": "array", "items": {
    "type": "object", "additionalProperties": False,
    "required": ["rule", "default_behaviour", "episodes", "near_probe", "far_probe"],
    "properties": {"rule": {"type": "string"}, "default_behaviour": {"type": "string"},
                   "episodes": {"type": "array", "items": {"type": "object", "additionalProperties": False, "required": ["turns"],
                                                           "properties": {"turns": {"type": "array", "items": _turn}}}},
                   "near_probe": _probe, "far_probe": _probe}}}}}

JUDGE_TMPL = """You are checking whether an assistant's reply follows a pattern in how this user wants to be helped. The assistant was never told the pattern directly; it may or may not have picked it up.

The pattern: {rule}

The user's message: {probe}

The assistant's reply:
{reply}

Test: {follows_if}

Does the reply pass the test? Answer yes or no only."""


def path(seed):
    return OUT / f"transfer_s{seed}.json"


def available(seed):
    return path(seed).exists()


def load(seed):
    return json.loads(path(seed).read_text())


# ---- run time --------------------------------------------------------------------------------------
def inject(life, seed):
    """Add the transfer episodes to the life's day sessions, at fixed positions per seed. Same for every arm."""
    if not available(seed):
        return 0
    t = load(seed)
    n = 0
    for r in t["rules"]:
        for e in r["episodes"]:
            sessions = life["schedule"][e["day"]]["sessions"]
            rng = random.Random(f"transfer-pos-{seed}-{r['rule_id']}-{e['index']}")
            sessions.insert(rng.randint(0, len(sessions)), {"session_id": f"transfer_{r['rule_id']}_e{e['index']}",
                                                            "turns": e["turns"], "evidence_for": f"transfer:{r['rule_id']}"})
            n += 1
    return n


def judge_probe(rule, probe, reply, tag):
    prompt = JUDGE_TMPL.format(rule=rule["rule"], probe=probe["text"], reply=reply, follows_if=probe["follows_if"])
    main, lab_main = judge_openai(prompt, tag)
    op, lab_op = judge_opus(prompt, tag)
    return {"follows": main, "judge_label": lab_main, "follows_opus": op, "judge_label_opus": lab_op, "judge_main": MAIN_JUDGE}


def run_probes(run, memory_text, nights_total=DAYS):
    """After night 10: ask every near and far probe once with the arm's memory, both judges grade. Returns rows."""
    t = load(run.seed)
    jobs = [(r, kind) for r in t["rules"] for kind in ("near", "far")]

    def one(job):
        r, kind = job
        p = r[f"{kind}_probe"]
        tag = f"{run.tag}/d{nights_total}/transfer/{r['rule_id']}/{kind}"
        a = run.ask(p["text"], memory_text, "", tag)
        j = ({"follows": False, "judge_label": "refusal", "follows_opus": False, "judge_label_opus": "refusal", "judge_main": None}
             if a["refusal"] else judge_probe(r, p, a["response"], tag))
        last = max(e["day"] for e in r["episodes"])
        return {"rule_id": r["rule_id"], "kind": kind, "n_episodes": len(r["episodes"]), "last_episode_day": last,
                "nights_since_last_episode": nights_total - last, "probe": p["text"], **a, **j}

    rows = [one(jobs[0])]
    with ThreadPoolExecutor(THREADS) as ex:
        rows += list(ex.map(one, jobs[1:]))
    near = [r["follows"] for r in rows if r["kind"] == "near"]; far = [r["follows"] for r in rows if r["kind"] == "far"]
    print(f"[{run.tag}] transfer: near {sum(near)}/{len(near)}, far {sum(far)}/{len(far)} (main judge)", flush=True)
    return rows


# ---- build -----------------------------------------------------------------------------------------
def author(counts, avoid, tag):
    prompt = GEN_PROMPT.format(n=len(counts), counts=", ".join(map(str, counts)),
                               avoid=("; ".join(avoid) if avoid else "(none yet)"))
    r = api.call(GEN_SYSTEM, [{"role": "user", "content": prompt}], tag=tag, max_tokens=32000, json_schema=GEN_SCHEMA, timeout=1800)
    rules = json.loads(r["text"])["rules"]
    out = []
    for i, rule in enumerate(rules[:len(counts)]):
        eps = rule["episodes"][:counts[i]]
        if len(eps) < counts[i]:
            continue
        out.append({**rule, "episodes": [{"turns": e["turns"]} for e in eps], "n_episodes": counts[i],
                    "author_call_id": r["call_id"]})
    return out, {"call_id": r["call_id"], "counts": counts, "avoid": avoid, "prompt": prompt}


def empty_memory_check(rule, tag):
    from run_arm import AGENT_SYSTEM
    system = AGENT_SYSTEM.format(memory="(empty)", today="")
    samples = []
    for kind in ("near", "far"):
        p = rule[f"{kind}_probe"]
        for k in range(CHECK_SAMPLES):
            t = f"{tag}/{kind}{k}"
            try:
                a = api.call(system, [{"role": "user", "content": p["text"]}], tag=t, max_tokens=3000)
                j = judge_probe(rule, p, a["text"], t)
                samples.append({"kind": kind, "reply": a["text"], "call_id": a["call_id"], **j})
            except api.Refusal as e:
                samples.append({"kind": kind, "reply": "", "call_id": e.call_id, "refusal": True, "follows": False, "follows_opus": False})
    n = len(samples)
    rate_main = sum(s["follows"] for s in samples) / n
    rate_opus = sum(s["follows_opus"] for s in samples) / n
    return {"samples": samples, "rate_main": round(rate_main, 3), "rate_opus": round(rate_opus, 3),
            "passed": rate_main < FOLLOW_LIMIT and rate_opus < FOLLOW_LIMIT}


def ep_tokens(turns):
    return api.count_tokens(session_text(turns)) + 4  # +4 for the "Session n" header and blank line in format_log


def place(rules, seed, budget):
    """Choose days for each rule's episodes: different days, at least one day apart, within each day's reserve.
    Last-episode days are spread evenly (day 4 to 9 for three episodes, day 2 to 9 for two), so the probes after
    night 10 come 1 to 8 nights after a rule was last seen and recall can be reported by delay."""
    rng = random.Random(f"transfer-days-{seed}")
    for attempt in range(2000):
        used = [0] * DAYS
        plan = {}
        ok = True
        groups = {}
        for r in rules:
            groups.setdefault(r["n_episodes"], []).append(r)
        lasts = {}
        for k, rs in groups.items():
            lo = 2 * (k - 1)
            targets = [round(lo + i * (DAYS - 1 - lo) / max(1, len(rs) - 1)) for i in range(len(rs))]
            rng.shuffle(targets)
            for r, t in zip(rs, targets):
                lasts[r["rule_id"]] = t
        for r in sorted(rules, key=lambda r: -r["n_episodes"]):
            k, last = r["n_episodes"], lasts[r["rule_id"]]
            for _ in range(200):
                days = sorted(rng.sample(range(last), k - 1)) + [last]
                if any(b - a < 2 for a, b in zip(days, days[1:])):
                    continue
                if all(used[d] + r["ep_tok"][i] <= budget for i, d in enumerate(days)):
                    break
            else:
                ok = False; break
            for i, d in enumerate(days):
                used[d] += r["ep_tok"][i]
            plan[r["rule_id"]] = days
        if ok:
            return plan, used, attempt
    raise RuntimeError("could not place episodes within the reserve")


def build(seed, avoid_from=()):
    OUT.mkdir(parents=True, exist_ok=True)
    work = OUT / f"work_s{seed}.json"  # resumable: every authoring call and check is saved as it finishes
    w = json.loads(work.read_text()) if work.exists() else {"seed": seed, "author_calls": [], "candidates": []}

    def save():
        work.write_text(json.dumps(w, indent=1))

    avoid = []
    for s in avoid_from:
        if available(s):
            avoid += [r["rule"] for r in load(s)["rules"]]
    w["avoid"] = avoid

    def kept(n_ep):
        return [c for c in w["candidates"] if c["n_episodes"] == n_ep and c.get("check", {}).get("passed")]

    need = {3: N_THREE, 2: N_RULES - N_THREE}
    rounds = 0
    while any(len(kept(k)) < need[k] for k in need):
        rounds += 1
        if rounds > 6:
            raise RuntimeError("too many authoring rounds")
        unchecked = {k: [c for c in w["candidates"] if c["n_episodes"] == k and "check" not in c] for k in need}
        if not w["author_calls"]:
            batches = [[3, 3, 3, 3, 2, 2, 2, 2]] * 2  # first round: 16 candidates, 4 spares
        else:  # later rounds: what is still missing plus one spare of each kind that is short
            counts = []
            for k in need:
                short = need[k] - len(kept(k)) - len(unchecked[k])
                counts += [k] * (short + 1) if short > 0 else []
            batches = [counts[i:i + BATCH] for i in range(0, len(counts), BATCH)]
        for part in batches:
            prev = avoid + [c["rule"] for c in w["candidates"]]
            rules, meta = author(part, prev, f"transfer/s{seed}/author{len(w['author_calls'])}")
            w["author_calls"].append(meta)
            for r in rules:
                r["cand_id"] = f"c{len(w['candidates']):02d}"
                r["ep_tok"] = [ep_tokens(e["turns"]) for e in r["episodes"]]
                w["candidates"].append(r)
            save()
            print(f"seed {seed}: authored {len(rules)} candidates ({meta['call_id']}), list-price spend {api.total_spend():.2f}", flush=True)
        # check just enough unchecked candidates to fill what is missing, in authoring order
        todo = []
        for k in need:
            todo += [c for c in w["candidates"] if c["n_episodes"] == k and "check" not in c][:need[k] - len(kept(k))]

        def chk(c):
            c["check"] = empty_memory_check(c, f"transfer/s{seed}/check/{c['cand_id']}")
            return c
        with ThreadPoolExecutor(THREADS) as ex:
            for c in ex.map(chk, todo):
                print(f"seed {seed}: {c['cand_id']} ({c['n_episodes']} ep) followed by default {c['check']['rate_main']} luna, "
                      f"{c['check']['rate_opus']} opus -> {'kept' if c['check']['passed'] else 'replaced'}", flush=True)
        save()

    chosen = kept(3)[:need[3]] + kept(2)[:need[2]]
    chosen.sort(key=lambda c: c["cand_id"])
    for i, c in enumerate(chosen):
        c["rule_id"] = f"s{seed}r{i+1:02d}"
    plan, used, attempts = place(chosen, seed, EPISODE_RESERVE)
    rules = []
    for c in chosen:
        days = plan[c["rule_id"]]
        rules.append({"rule_id": c["rule_id"], "cand_id": c["cand_id"], "rule": c["rule"], "default_behaviour": c["default_behaviour"],
                      "episodes": [{"index": i + 1, "day": d, "tokens": c["ep_tok"][i], "turns": e["turns"]}
                                   for i, (d, e) in enumerate(zip(days, c["episodes"]))],
                      "near_probe": c["near_probe"], "far_probe": c["far_probe"],
                      "empty_memory": {k: c["check"][k] for k in ("rate_main", "rate_opus")},
                      "author_call_id": c["author_call_id"]})
    checked = [c for c in w["candidates"] if "check" in c]
    out = {"seed": seed, "built": time.strftime("%Y-%m-%d %H:%M %Z"), "model": api.MODEL, "effort": api.EFFORT,
           "main_judge": MAIN_JUDGE, "second_judge": api.MODEL, "backend": api.BACKEND,
           "placement_seed": f"transfer-days-{seed}", "position_seed": f"transfer-pos-{seed}-<rule_id>-<episode>",
           "check": {"samples_per_probe": CHECK_SAMPLES, "follow_limit": FOLLOW_LIMIT, "candidates_checked": len(checked),
                     "candidates_failed": sum(1 for c in checked if not c["check"]["passed"]),
                     "replaced": sum(1 for c in checked if not c["check"]["passed"])},
           "episode_tokens_by_day": used, "episode_reserve": EPISODE_RESERVE,
           "author_calls": w["author_calls"], "generation_system": GEN_SYSTEM, "judge_template": JUDGE_TMPL,
           "rules": rules}
    path(seed).write_text(json.dumps(out, indent=1))
    print(f"seed {seed}: kept {len(rules)}, checked {len(checked)}, replaced {out['check']['replaced']}, "
          f"episode tokens by day {used}", flush=True)
    return out


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("cmd", choices=["build"]); p.add_argument("seed", type=int)
    p.add_argument("--avoid-from", type=int, nargs="*", default=[], help="seeds whose rules the new ones must differ from")
    a = p.parse_args()
    build(a.seed, a.avoid_from)
