"""
Regrade every stored v1 answer with an OpenAI judge and compare with the Opus and gpt-4o labels.
Usage: python regrade_openai.py --model gpt-5.6-luna [--limit N] [--threads 8]
Writes results/regrade_<model>/labels.jsonl (resumable) and summary.md. No answer is regenerated.
The gpt-4o labels come from results/regrade_gpt4o/labels.jsonl (regrade_gpt4o.py, 4 Oct 2026).
"""
import json, glob, pathlib, argparse, collections, statistics
from concurrent.futures import ThreadPoolExecutor
import api
from judge import get_anscheck_prompt

ROOT = pathlib.Path(__file__).resolve().parent.parent


def key(run, a):
    return f"{run}|{a['question_id']}|{a['phase']}|{a['day']}"


def main():
    p = argparse.ArgumentParser(); p.add_argument("--model", default="gpt-5.6-luna")
    p.add_argument("--limit", type=int); p.add_argument("--threads", type=int, default=8)
    args = p.parse_args()
    out = ROOT / "results" / f"regrade_{args.model.replace('.', '_')}"
    out.mkdir(parents=True, exist_ok=True)
    labels_path = out / "labels.jsonl"
    done = {}
    if labels_path.exists():
        for line in labels_path.read_text().splitlines():
            d = json.loads(line); done[d["key"]] = d
    items = []
    for f in sorted(glob.glob(str(ROOT / "results" / "runs" / "*" / "state.json"))):
        run = pathlib.Path(f).parent.name
        for a in json.load(open(f))["answers"]:
            items.append((run, a))
    todo = [it for it in items if key(*it) not in done][: args.limit]
    print(f"{len(items)} answers, {len(done)} already graded, grading {len(todo)} with {args.model}", flush=True)

    def grade(item):
        run, a = item
        if a.get("refusal"):
            return {"key": key(run, a), "label": False, "raw": "refusal"}
        prompt = get_anscheck_prompt(a["question_type"], a["question"], a["gold"], a["response"], abstention=a["abstention"])
        text, _ = api.openai_chat(args.model, prompt, tag=f"regrade_{args.model}/{key(run, a)}", max_completion_tokens=2000)
        return {"key": key(run, a), "label": "yes" in text.lower(), "raw": text[:60]}

    with open(labels_path, "a") as fh, ThreadPoolExecutor(args.threads) as ex:
        for i, d in enumerate(ex.map(grade, todo), 1):
            fh.write(json.dumps(d) + "\n"); fh.flush(); done[d["key"]] = d
            if i % 100 == 0:
                print(f"graded {i} of {len(todo)}", flush=True)
    summarize(items, done, args.model, out)


def summarize(items, done, model, out):
    g4 = {}
    p4 = ROOT / "results" / "regrade_gpt4o" / "labels.jsonl"
    if p4.exists():
        for line in p4.read_text().splitlines():
            d = json.loads(line); g4[d["key"]] = d["gpt4o"]
    rows = [(run, a, done[key(run, a)]["label"], g4.get(key(run, a))) for run, a in items if key(run, a) in done]
    n = len(rows)
    ag_opus = sum(a["correct"] == l for run, a, l, g in rows)
    with4 = [(a, l, g) for run, a, l, g in rows if g is not None]
    ag_g4 = sum(l == g for a, l, g in with4)
    ag_opus_g4 = sum(a["correct"] == g for a, l, g in with4)
    empty = sum(1 for run, a, l, g in rows if done[key(run, a)]["raw"] == "")
    md = [f"# Regrade with {model}", "",
          f"Answers regraded: {n}. Empty replies: {empty}.",
          f"Agreement with the Opus judge: {ag_opus} of {n} ({100*ag_opus/max(1,n):.1f} percent).",
          f"Agreement with the gpt-4o judge: {ag_g4} of {len(with4)} ({100*ag_g4/max(1,len(with4)):.1f} percent).",
          f"For reference, Opus and gpt-4o agree on {ag_opus_g4} of {len(with4)} ({100*ag_opus_g4/max(1,len(with4)):.1f} percent).", ""]
    up = [(r, a) for r, a, l, g in rows if l and not a["correct"]]
    down = [(r, a) for r, a, l, g in rows if a["correct"] and not l]
    md.append(f"{model} says correct where Opus said wrong: {len(up)}. {model} says wrong where Opus said correct: {len(down)}.")
    md += ["", "## Final recall, percent, mean over seeds", "", f"| arm | Opus judge | {model} | gpt-4o judge |", "|---|---|---|---|"]
    final = collections.defaultdict(lambda: collections.defaultdict(list))
    for run, a, l, g in rows:
        if a["phase"] == "final" and not a["abstention"]:
            final[run]["opus"].append(a["correct"]); final[run]["new"].append(l)
            if g is not None: final[run]["g4"].append(g)
    def pct(v): return 100 * sum(v) / len(v) if v else float("nan")
    def ms(v): return f"{statistics.mean(v):.0f} ± {statistics.stdev(v):.0f}" if len(v) > 1 else (f"{v[0]:.0f}" if v else "n/a")
    for arm in ["nosleep", "faithful", "noisy_structured", "noisy_random"]:
        runs = [r for r in final if r.startswith(arm + "_s")]
        md.append(f"| {arm} | {ms([pct(final[r]['opus']) for r in runs])} | {ms([pct(final[r]['new']) for r in runs])} | {ms([pct(final[r]['g4']) for r in runs])} |")
    md += ["", "## Disagreements with Opus (first 15)", ""]
    for r, a in (up + down)[:15]:
        md.append(f"- {r} {a['phase']} {a['question_type']}: Opus {'yes' if a['correct'] else 'no'}, {model} {'no' if a['correct'] else 'yes'}. Q: {a['question'][:120]} Gold: {str(a['gold'])[:80]}")
    (out / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:9]))


if __name__ == "__main__":
    main()
