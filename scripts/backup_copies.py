"""For each answerable question, count its answer turns and how many the night noise replaced outright or touched,
then compare final-recall accuracy by group. Prints counts only, never turn text."""
import json, pathlib, sys, collections
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness")); sys.path.insert(0, str(ROOT / "scripts"))
import transfer
from evidence_hits import has_answer_flags, REPLACED, DAYS

def answer_turns(seed, flags):
    life = json.load(open(ROOT / "data" / "lives_v2" / f"life_s{seed}.json"))
    qs = {q["question_id"]: q for q in life["questions"]}
    transfer.inject(life, seed)
    per_q = collections.defaultdict(list)  # qid -> [(day, idx)]
    nsess = collections.Counter()
    for d in range(DAYS):
        i = 0
        for s in life["schedule"][d]["sessions"]:
            q = s.get("evidence_for")
            if q in qs:
                nsess[q] += 1
                f = flags.get(s["session_id"], [])
                per_q[q] += [(d, i + j) for j in range(len(s["turns"])) if j < len(f) and f[j]]
            i += len(s["turns"])
    return qs, per_q, nsess

def final_correct(arm, seed):
    st = json.load(open(ROOT / "results" / "runs_v2" / f"{arm}_s{seed}" / "state.json"))
    return {a["question_id"]: a["correct"] for a in st["answers"] if a["phase"] == "final"}, st

flags = has_answer_flags()
phases = set()
for arm in sys.argv[1:]:
    groups = collections.defaultdict(lambda: [0, 0, 0])  # n, correct in arm, correct in faithful
    for seed in (0, 1, 2):
        qs, per_q, nsess = answer_turns(seed, flags)
        fin, st = final_correct(arm, seed)
        faith, _ = final_correct("faithful", seed)
        hit = {}
        for n in st["nights"]:
            if n["day"] < DAYS:
                c = n["corruption"]
                for k in c["before"]:
                    hit[(n["day"], int(k))] = c["plan"][k]
        for qid, q in qs.items():
            if q.get("abstention") or qid not in fin:
                continue
            turns = per_q[qid]
            rep = sum(1 for t in turns if hit.get(t) in REPLACED)
            touched = sum(1 for t in turns if t in hit)
            if not turns: g = "no flagged answer turn"
            elif rep == len(turns): g = "every answer turn replaced"
            elif touched == len(turns): g = "every answer turn hit, some only edited"
            elif touched: g = "some answer turns hit, at least one clean"
            else: g = "no answer turn hit"
            g += f" ({'one' if len(turns)==1 else 'several'} answer turns)" if turns else ""
            r = groups[g]; r[0] += 1; r[1] += fin[qid]; r[2] += faith.get(qid, False)
    print(f"== {arm}, three seeds pooled: group | questions | correct in this arm | same questions correct in faithful")
    for g, (n, c, f) in sorted(groups.items()):
        print(f"{g} | {n} | {c} ({100*c/n:.0f}%) | {f} ({100*f/n:.0f}%)")
