"""Count how many LongMemEval evidence turns were corrupted on the night of their day, per noisy run.

Evidence turn: a turn flagged has_answer in data/raw/longmemeval_s_cleaned.json, inside a session the life
schedule (data/lives_v2, plus transfer episodes injected as in run_arm) marks evidence_for a question id.
Turn indices match the flat order arms.flat_turns uses. Only ids, indices, kinds and counts are read out.
"""
import json, pathlib, statistics, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "harness"))
import transfer

ARMS = [f"{k}_{d}" for k in ("structured", "random") for d in ("05", "10", "20", "40")]
SEEDS = [0, 1, 2]
DAYS = 10
REPLACED = {"splice", "paragraph"}  # replaced outright; swap, change, words are modified in place


def has_answer_flags():
    raw = json.load(open(ROOT / "data" / "raw" / "longmemeval_s_cleaned.json"))
    flags = {}
    for q in raw:
        for sid, sess in zip(q["haystack_session_ids"], q["haystack_sessions"]):
            if sid not in flags:
                flags[sid] = [bool(t.get("has_answer")) for t in sess]
    return flags


def evidence_index(seed, flags):
    life = json.load(open(ROOT / "data" / "lives_v2" / f"life_s{seed}.json"))
    qids = {q["question_id"] for q in life["questions"]}
    transfer.inject(life, seed)
    per_day = []
    for d in range(DAYS):
        ev_turn, ev_sess, i = set(), set(), 0
        for s in life["schedule"][d]["sessions"]:
            n = len(s["turns"])
            if s.get("evidence_for") in qids:
                f = flags.get(s["session_id"], [])
                for j in range(n):
                    ev_sess.add(i + j)
                    if j < len(f) and f[j]:
                        ev_turn.add(i + j)
            i += n
        per_day.append((i, ev_turn, ev_sess))
    return per_day


def main():
    flags = has_answer_flags()
    evi = {s: evidence_index(s, flags) for s in SEEDS}
    rows = []
    for arm in ARMS:
        for seed in SEEDS:
            st = json.load(open(ROOT / "results" / "runs_v2" / f"{arm}_s{seed}" / "state.json"))
            r = dict(arm=arm, seed=seed, total=0, corr=0, ev=0, ev_corr=0, ev_repl=0, evs=0, evs_corr=0, mismatch=0)
            for night in st["nights"]:
                d = night["day"]
                if d >= DAYS:
                    continue
                c = night["corruption"]
                n, ev_turn, ev_sess = evi[seed][d]
                if n != c["n_turns"]:
                    r["mismatch"] += 1
                hit = {int(k) for k in c["before"].keys()}  # turns actually changed (structured LLM misses excluded)
                kinds = c["plan"]
                r["total"] += n; r["corr"] += len(hit)
                r["ev"] += len(ev_turn); r["ev_corr"] += len(hit & ev_turn)
                r["ev_repl"] += sum(1 for i in hit & ev_turn if kinds[str(i)] in REPLACED)
                r["evs"] += len(ev_sess); r["evs_corr"] += len(hit & ev_sess)
            rows.append(r)

    def pct(a, b):
        return 100 * a / b if b else float("nan")

    hdr = "| arm | seed | turns | corrupted | evidence turns | evidence corrupted | corrupted % | evidence corrupted % | evidence replaced outright | evidence-session turns corrupted % |"
    out = [hdr, "|" + "---|" * 10]
    for arm in ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        for r in rs:
            out.append(f"| {arm} | s{r['seed']} | {r['total']} | {r['corr']} | {r['ev']} | {r['ev_corr']} | "
                       f"{pct(r['corr'], r['total']):.1f} | {pct(r['ev_corr'], r['ev']):.1f} | {r['ev_repl']} | {pct(r['evs_corr'], r['evs']):.1f} |")
        m = lambda k: statistics.mean(r[k] for r in rs)
        mr = lambda a, b: statistics.mean(pct(r[a], r[b]) for r in rs)
        out.append(f"| **{arm}** | mean | {m('total'):.0f} | {m('corr'):.1f} | {m('ev'):.1f} | {m('ev_corr'):.1f} | "
                   f"{mr('corr', 'total'):.1f} | {mr('ev_corr', 'ev'):.1f} | {m('ev_repl'):.1f} | {mr('evs_corr', 'evs'):.1f} |")
    bad = sum(r["mismatch"] for r in rows)
    note = ("An evidence turn is a turn flagged has_answer in LongMemEval (longmemeval_s_cleaned.json) inside a session the life schedule marks as evidence for one of the run's questions, indexed in the same flat turn order the night corruption uses (transfer episodes injected first, as in run_arm).\n"
            "A turn counts as corrupted only if the night record saved a before/after for it, so structured swap or change edits the model did not return are not counted; the last column uses every turn of an evidence session instead of has_answer turns.")
    text = "# Evidence turns hit by night corruption (runs_v2, days 0 to 9)\n\n" + "\n".join(out) + "\n\n" + note + "\n"
    if bad:
        text += f"\nTurn count mismatches between reconstructed days and night records: {bad}\n"
    (ROOT / "paper" / "evidence_hits.md").write_text(text)
    print("\n".join(out))
    print("mismatched nights:", bad)


if __name__ == "__main__":
    main()
