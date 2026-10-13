"""
Regrade every stored answer with LongMemEval's official judge: gpt-4o-2024-08-06, the same prompt templates,
temperature 0, max_tokens 10, label = 'yes' in the reply. Settings copied from external/longmemeval_evaluate_qa.py.
No answer is regenerated. Writes results/regrade_gpt4o/labels.jsonl (resumable) and summary.md.
Usage: python regrade_gpt4o.py [--limit N]
"""
import json, glob, pathlib, argparse, time, collections, statistics
from concurrent.futures import ThreadPoolExecutor
import openai
import api  # loads .env, owns cost.jsonl
from judge import get_anscheck_prompt

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "regrade_gpt4o"
MODEL = "gpt-4o-2024-08-06"
PRICE_IN, PRICE_OUT = 2.50 / 1e6, 10.00 / 1e6
client = openai.OpenAI()


def key(run, a):
    return f"{run}|{a['question_id']}|{a['phase']}|{a['day']}"


def grade(item):
    run, a = item
    if a.get("refusal"):
        return {"key": key(run, a), "gpt4o": False, "raw": "refusal"}
    prompt = get_anscheck_prompt(a["question_type"], a["question"], a["gold"], a["response"], abstention=a["abstention"])
    err = None
    for attempt in range(12):
        try:
            r = client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": prompt}],
                                               n=1, temperature=0, max_tokens=10)
            break
        except (openai.RateLimitError, openai.APIConnectionError, openai.InternalServerError) as e:
            err = f"{type(e).__name__}: {str(e)[:300]}"
            time.sleep(min(60, 2 ** attempt))
    else:
        print(f"skipped {key(run, a)} ({len(prompt)} chars): {err}", flush=True)
        return None  # not written, so the next run retries it
    u = r.usage
    api.log_cost({"call_id": r.id, "tag": f"regrade/{key(run, a)}", "provider": "openai", "model": r.model,
                  "input_tokens": u.prompt_tokens, "output_tokens": u.completion_tokens,
                  "usd": u.prompt_tokens * PRICE_IN + u.completion_tokens * PRICE_OUT})
    raw = r.choices[0].message.content.strip()
    return {"key": key(run, a), "gpt4o": "yes" in raw.lower(), "raw": raw}


def main():
    p = argparse.ArgumentParser(); p.add_argument("--limit", type=int); args = p.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    labels_path = OUT / "labels.jsonl"
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
    print(f"{len(items)} answers, {len(done)} already graded, grading {len(todo)}", flush=True)
    with open(labels_path, "a") as fh, ThreadPoolExecutor(1) as ex:
        for i, d in enumerate(ex.map(grade, todo), 1):
            if d is None:
                continue
            fh.write(json.dumps(d) + "\n"); fh.flush(); done[d["key"]] = d
            if i % 100 == 0:
                print(f"graded {i} of {len(todo)}", flush=True)
    summarize(items, done)


def summarize(items, done):
    rows = [(run, a, done[key(run, a)]["gpt4o"]) for run, a in items if key(run, a) in done]
    agree = sum(a["correct"] == g for _, a, g in rows)
    flips_up = [(r, a) for r, a, g in rows if g and not a["correct"]]
    flips_down = [(r, a) for r, a, g in rows if a["correct"] and not g]
    md = ["# Regrade with gpt-4o-2024-08-06 (LongMemEval's official judge)", "",
          f"Answers regraded: {len(rows)}. Agreement with the Opus judge: {agree} of {len(rows)} ({100*agree/max(1,len(rows)):.1f} percent).",
          f"gpt-4o says correct where Opus said wrong: {len(flips_up)}. gpt-4o says wrong where Opus said correct: {len(flips_down)}.", ""]
    # final recall per arm, both judges, and the paired difference against faithful
    final = collections.defaultdict(lambda: {"opus": [], "gpt4o": []})
    for run, a, g in rows:
        if a["phase"] == "final" and not a["abstention"]:  # matches results.md, abstention is reported apart
            final[run]["opus"].append(a["correct"]); final[run]["gpt4o"].append(g)
    arms = ["nosleep", "faithful", "noisy_structured", "noisy_random"]
    seeds = sorted({r.rsplit("_s", 1)[1] for r in final})
    def pct(run, j):
        v = final[run][j]; return 100 * sum(v) / len(v) if v else float("nan")
    def ms(v):
        return f"{statistics.mean(v):.0f} ± {statistics.stdev(v):.0f}" if len(v) > 1 else (f"{v[0]:.0f}" if v else "n/a")
    md += ["## Final recall, percent, mean ± sd over seeds", "", "| arm | Opus judge | gpt-4o judge | minus faithful, Opus | minus faithful, gpt-4o |", "|---|---|---|---|---|"]
    for arm in arms:
        o = [pct(f"{arm}_s{s}", "opus") for s in seeds if f"{arm}_s{s}" in final]
        g = [pct(f"{arm}_s{s}", "gpt4o") for s in seeds if f"{arm}_s{s}" in final]
        do = [pct(f"{arm}_s{s}", "opus") - pct(f"faithful_s{s}", "opus") for s in seeds if f"{arm}_s{s}" in final and f"faithful_s{s}" in final]
        dg = [pct(f"{arm}_s{s}", "gpt4o") - pct(f"faithful_s{s}", "gpt4o") for s in seeds if f"{arm}_s{s}" in final and f"faithful_s{s}" in final]
        md.append(f"| {arm} | {ms(o)} | {ms(g)} | {ms(do)} | {ms(dg)} |")
    md += ["", "## Disagreements (first 15)", ""]
    for r, a in (flips_up + flips_down)[:15]:
        md.append(f"- {r} {a['phase']} {a['question_type']}: Opus {'yes' if a['correct'] else 'no'}, gpt-4o {'no' if a['correct'] else 'yes'}. Q: {a['question'][:120]} Gold: {str(a['gold'])[:80]}")
    (OUT / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:12]))


if __name__ == "__main__":
    main()
