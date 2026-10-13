"""Score the Letta check outputs with Letta's own evaluate_gsm_symbolic.py logic and write results/letta_check/summary.md."""
import json, re, statistics, pathlib, glob
ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "results" / "letta_check"

def standardize(a): return a.replace("$", "").replace(",", "").strip(".")

def score(path):
    correct = total = 0; toks = []; errors = 0
    for line in open(path):
        o = json.loads(line)
        if "error" in o: errors += 1; continue
        r = o["responses"][0]
        gold = standardize(re.sub(r"(?s).*#### ", "", o["answer"]))
        final = ""
        for m in r["messages"]:
            if m["message_type"] == "assistant_message":
                final = m["content"]
                ms = re.findall(r"(-?[$0-9.,]{2,})|(-?[0-9]+)", final)
                if not ms: continue
                final = standardize("".join(ms[-1]))
        correct += (final == gold); total += 1
        toks.append(r["usage"]["completion_tokens"])
    return {"n": total, "errors": errors, "accuracy": correct / total if total else None,
            "avg_completion_tokens": statistics.mean(toks) if toks else None}

if __name__ == "__main__":
    fig = json.load(open(OUT / "figure3_digitised.json"))
    rows = []
    for f in sorted(glob.glob(str(OUT / "p2_v0_*.jsonl"))):
        s = score(f); s["file"] = pathlib.Path(f).name; rows.append(s)
    paper = fig["gpt-4o-mini"]
    md = ["# Letta replication check: Stateful GSM-Symbolic P2, gpt-4o-mini, verbosity 0", "",
          f"Paper (digitised from Figure 3): test-time only {paper['test_time_only'][0][1]:.3f} at {paper['test_time_only'][0][0]} tokens; sleep-time {paper['sleep_time'][0][1]:.3f} at {paper['sleep_time'][0][0]} tokens.", "",
          "| file | n scored | errors | accuracy | avg completion tokens |", "|---|---|---|---|---|"]
    for s in rows:
        acc = "n/a" if s["accuracy"] is None else f"{s['accuracy']:.3f}"
        tk = "n/a" if s["avg_completion_tokens"] is None else f"{s['avg_completion_tokens']:.0f}"
        md.append(f"| {s['file']} | {s['n']} | {s['errors']} | {acc} | {tk} |")
    (OUT / "summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
