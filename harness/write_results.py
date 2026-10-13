"""Write results/results_v2.md from results/summary_v2.json and cost.jsonl. Numbers only; the prose sections are fixed
text with the numbers filled in. v1's results.md is left as it is (v1 is kept as lessons learned, decisions.md).

v2 adds to the v1 format: the corruption-rate curve, final recall by delay in nights, transfer near and far, and the
gist-stripping and deletion counts per arm beside each arm's memory size (spec-v2.md "Ready to build", results line).
"""
import json, pathlib, time, collections, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
import api, arms
S = json.load(open(ROOT / "results" / "summary_v2.json"))
NAMES = {"nosleep": "No sleep (raw window at the cap)", "faithful": "Faithful replay",
         "structured_05": "Structured noise, 5 percent", "structured_10": "Structured noise, 10 percent",
         "structured_20": "Structured noise, 20 percent", "structured_40": "Structured noise, 40 percent",
         "random_05": "Random noise, 5 percent", "random_10": "Random noise, 10 percent",
         "random_20": "Random noise, 20 percent", "random_40": "Random noise, 40 percent"}
ARMS = [(a, NAMES.get(a, a)) for a in arms.ARMS]
N_RUNS = len(ARMS) * 3
DAYS = 10


def f(x, pct=True):
    if x is None: return "n/a"
    if isinstance(x, dict):
        if pct: return f"{100*x['mean']:.0f} ± {100*x['sd']:.0f}"
        return f"{x['mean']:,.0f} ± {x['sd']:,.0f}"
    return f"{100*x:.0f}" if pct else f"{x:,.0f}"


def spend():
    """Since the v2 start: Max-plan calls at list price (no money), real money by provider."""
    maxp = collections.Counter(); real = collections.Counter()
    for line in open(ROOT / "cost.jsonl"):
        try: r = json.loads(line)
        except ValueError: continue
        if r.get("ts", 0) < api.V2_START: continue
        if r.get("backend") == "subscription":
            maxp["usd"] += r["usd"]; maxp["n"] += 1
        else:
            real[r["provider"]] += r["usd"]; real[f"n_{r['provider']}"] += 1
    return maxp, real


def verdict(d):
    if not d: return "not measured"
    m, sd = d["mean"], d["sd"]
    if abs(m) <= sd: return "no result, the difference is inside the seed spread"
    return ("noisy arm higher" if m > 0 else "noisy arm lower") + ", and the difference clears the seed spread"


def row(cells):
    return "| " + " | ".join(cells) + " |"


def main():
    by, pv, curve = S["by_arm"], S["paired_vs_faithful"], S["curve"]
    maxp, real = spend()
    runs_done = S["finished_runs"]
    head = pv.get("structured_20_minus_faithful.final_acc")
    novel = pv.get("structured_20_minus_faithful.final_acc_novel")
    far = pv.get("structured_20_minus_faithful.transfer.far")
    lure = pv.get("structured_20_minus_faithful.battery_morning.drm_lure_fa")
    ja = S.get("judge_agreement_overall")
    caps = ", ".join(f"{c:,}" for c in arms.CAPS[:DAYS])

    L = ["# Results: noisy replay at four doses", "",
         f"Generated {time.strftime('%d %B %Y %H:%M UTC', time.gmtime())}. Model under test claude-opus-5-5, effort medium, through Claude Code on the Max plan. Days of 130,000 tokens; the memory cap grows each night ({caps} tokens). Ten days, ten arms, three seeds.", "",
         "## One-screen summary", "",
         f"**What ran.** {runs_done} of {N_RUNS} runs finished (ten arms x three seeds). Each run: ten days of about 30 LongMemEval sessions plus the transfer-test episodes, one night step per day, 100 memory questions asked before sleep, after sleep and at the end, 24 transfer probes after night 10, then an eleventh day with the memory-effects battery. "
         f"Spend: {maxp['usd']:.2f} USD list price on the Max plan over {maxp['n']} Opus calls (no money), {real['openai']:.2f} USD on OpenAI over {real['n_openai']} judge calls" + (f", {real['anthropic']:.2f} USD on the Anthropic API key over {real['n_anthropic']} calls" if real["n_anthropic"] else "") + ".", "",
         f"**Judges.** gpt-5.6-luna grades every answer, Opus 5.5 grades it again. They agree on {f(ja)} percent of {S['judge_graded']:,} graded answers ({S['judge_disagreements']} disagreements). Numbers below are luna's unless marked.", "",
         f"**The one number.** Final-day recall, structured noise at 20 percent minus faithful replay, mean over seeds: **{f(head)} points** (per seed: {[round(100*v) for v in head['values']] if head else 'n/a'}). Verdict: {verdict(head)}.", "",
         f"Novel tasks (multi-session questions), same difference: {f(novel)} points, {verdict(novel)}. Far transfer probes, same difference: {f(far)} points, {verdict(far)}. DRM critical-lure false alarms after sleep, same difference: {f(lure)} points, {verdict(lure)}.", "",
         *(((ROOT / "results" / "reading_v2.md").read_text(), "") if (ROOT / "results" / "reading_v2.md").exists() else ()),
         "## Claim", "",
         "An agent whose nightly replay is corrupted on purpose recalls as much on the last day as an agent with faithful replay, and does better on situations it has never seen (Hoel's overfitted brain hypothesis, tested on a text-memory LLM agent). v2 tests it at four corruption rates, with structured and random noise side by side, and with a transfer test built for it.", "",
         "## Method in brief", "",
         "Ten arms share one model, one life per seed, one agent prompt and one question schedule. Only the night step differs. No sleep keeps a raw window of the day's last turns, sized to the night's cap. Faithful replay has the model rewrite its memory from the day's transcript: the memory is a list of items with a gist line, details and a score from 1 to 5, and when it is over the cap the harness strips details from the lowest-scored items first and deletes whole items only when every item is down to its gist. "
         "Structured noise swaps, changes or splices 5, 10, 20 or 40 percent of the day's turns from earlier days before the same rewrite; random noise replaces or salts the same share of turns with text from an unrelated corpus. Days are about 30 LongMemEval sessions stitched to 130,000 tokens, with 12 hidden counter-default rules planted as 2 or 3 episodes each across the ten days. After night 10 each rule gets one near probe and one far probe. Day eleven is a Cao-style memory battery with new DRM lists from the USF association norms. Full detail in spec-v2.md and decisions.md.", "",
         "## Numbers, mean ± sd over three seeds (percent)", "",
         row(["arm", "evening (before sleep)", "morning (after sleep)", "one-night drop", "final recall", "final, days 1-5", "final, days 6-10", "final, novel (multi-session)", "final, abstention", "memory tokens, mean over nights"]),
         "|---|---|---|---|---|---|---|---|---|---|"]
    for a, name in ARMS:
        v = by.get(a)
        if not v: L.append(row([name, "not run"] + [""] * 8)); continue
        L.append(row([name, f(v["evening_acc"]), f(v["morning_acc"]), f(v["one_night_drop"]), f(v["final_acc"]), f(v["final_acc_early"]), f(v["final_acc_late"]), f(v["final_acc_novel"]), f(v["final_abstention_acc"]), f(v["mean_memory_tokens"], pct=False)]))
    L += ["", "Paired differences against faithful replay, same seed (percentage points):", "",
          row(["comparison", "final recall", "final, novel", "one-night drop", "abstention", "transfer near", "transfer far"]), "|---|---|---|---|---|---|---|"]
    for a, name in ARMS:
        if a == "faithful": continue
        g = lambda m: f(pv.get(f"{a}_minus_faithful.{m}"))
        L.append(row([f"{name} minus faithful", g("final_acc"), g("final_acc_novel"), g("one_night_drop"), g("final_abstention_acc"), g("transfer.near"), g("transfer.far")]))

    L += ["", "## Corruption-rate curve", "",
          "Faithful replay is the 0 percent point of both curves. Each cell is mean ± sd over seeds (percent).", "",
          row(["rate", "structured: final recall", "structured: novel", "structured: far transfer", "random: final recall", "random: novel", "random: far transfer"]), "|---|---|---|---|---|---|---|"]
    st_pts = {p["rate"]: p for p in curve.get("structured", [])}; rn_pts = {p["rate"]: p for p in curve.get("random", [])}
    for rate in (0.0, 0.05, 0.10, 0.20, 0.40):
        s, r = st_pts.get(rate), rn_pts.get(rate)
        c = lambda p, k: f(p[k]) if p else "not run"
        L.append(row([f"{int(rate*100)} percent", c(s, "final_acc"), c(s, "final_acc_novel"), c(s, "transfer_far"), c(r, "final_acc"), c(r, "final_acc_novel"), c(r, "transfer_far")]))

    L += ["", "## Final recall by delay", "",
          "Final-day recall of questions whose last evidence was N nights before the final questions (percent, mean over seeds; sd omitted, each cell rests on 4 to 21 questions per life).", "",
          row(["arm"] + [f"{d} night{'s' if d > 1 else ''}" for d in range(1, DAYS + 1)]), "|---|" + "---|" * DAYS]
    for a, name in ARMS:
        v = by.get(a)
        if not v: L.append(row([name, "not run"] + [""] * (DAYS - 1))); continue
        L.append(row([name] + [("n/a" if v["final_acc_by_delay"][str(d)] is None else f"{100*v['final_acc_by_delay'][str(d)]['mean']:.0f}") for d in range(1, DAYS + 1)]))

    L += ["", "## Transfer test", "",
          "Share of the 12 hidden rules the agent followed on a probe after night 10 (percent, mean ± sd over seeds). Near probes resemble the planted episodes; far probes apply the rule in a different kind of request. Hoel predicts the noisy arms lose less from near to far.", "",
          row(["arm", "near (luna)", "far (luna)", "near minus far", "near (Opus)", "far (Opus)", "rules with 2 episodes", "rules with 3 episodes"]), "|---|---|---|---|---|---|---|---|"]
    for a, name in ARMS:
        v = by.get(a)
        if not v or v.get("transfer.near") is None: L.append(row([name, "not run"] + [""] * 6)); continue
        L.append(row([name, f(v["transfer.near"]), f(v["transfer.far"]), f(v["transfer.near_minus_far"]), f(v["transfer.near_opus"]), f(v["transfer.far_opus"]), f(v["transfer_by_episodes"]["2"]), f(v["transfer_by_episodes"]["3"])]))
    L += ["", "Each rule passed an empty-memory check before the sweep: an agent with no memory followed it on under 20 percent of samples, so following it on a probe means the memory carried it."]

    L += ["", "## Memory size and forgetting per arm", "",
          "Memory tokens are the agent-facing text after a night, counted with Claude's tokenizer. Stripping and deletion are the harness's forgetting when the sleep step wrote more than the cap allows: details go from the lowest-scored items first, the last one cut at a sentence boundary (partial), and whole items go only when every item is down to its gist. Totals over ten nights, mean ± sd over seeds.", "",
          row(["arm", "memory tokens, mean over nights", "memory as share of cap", "tokens after night 10", "items after night 10", "details stripped", "of which partial", "items deleted", "nights over cap", "turns corrupted", "sleep output tokens per night", "sleep seconds per night"]),
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for a, name in ARMS:
        v = by.get(a)
        if not v: L.append(row([name, "not run"] + [""] * 10)); continue
        n = lambda k: f(v[k], pct=False)
        L.append(row([name, n("mean_memory_tokens"), f(v["mean_memory_fill"]), n("final_memory_tokens"), n("final_items"), n("details_stripped"), n("details_partial"), n("items_deleted"), n("nights_over_cap"), n("corrupted_turns"), n("sleep_output_tokens"), n("sleep_seconds")]))
    L += ["", "Memory tokens after each night, mean over seeds, with the cap:", "",
          row(["arm"] + [f"night {d+1} (cap {arms.CAPS[d]:,})" for d in range(DAYS)]), "|---|" + "---|" * DAYS]
    for a, name in ARMS:
        v = by.get(a)
        if not v: L.append(row([name, "not run"] + [""] * (DAYS - 1))); continue
        L.append(row([name] + [("n/a" if (len(v["memory_tokens_by_night"]) <= d or v["memory_tokens_by_night"][d] is None) else f"{v['memory_tokens_by_night'][d]['mean']:,.0f}") for d in range(DAYS)]))

    L += ["", "## Memory-effects battery, morning after the arm's own night step (percent)", "",
          row(["arm", "DRM hits", "DRM critical-lure false alarms", "DRM unrelated false alarms", "serial hits", "primacy (pos 1-3)", "middle (6-10)", "recency (13-15)", "fan 1 accuracy", "fan 2 accuracy"]), "|---|---|---|---|---|---|---|---|---|---|"]
    for a, name in ARMS:
        v = by.get(a, {}).get("battery_morning")
        if not v or v.get("drm_hit") is None: L.append(row([name, "not run"] + [""] * 8)); continue
        L.append(row([name, f(v["drm_hit"]), f(v["drm_lure_fa"]), f(v["drm_unrelated_fa"]), f(v["serial_hit"]), f(v["serial_primacy"]), f(v["serial_middle"]), f(v["serial_recency"]), f(v["pl_fan1_acc"]), f(v["pl_fan2_acc"])]))
    L += ["", "Same tests in the evening, with the study lists still in context, are in summary_v2.json under battery_evening. The DRM lists are new ones built from the USF free-association norms, because Opus recognised the classic lists in v1. Human reference points: Roediger and McDermott 1995 found people false-recognise the critical lure at about 0.8 of the hit rate; Cao et al report 0.11 for GPT-4.", "",
          "## Housekeeping", "",
          f"Refusals: {sum(by[a]['refusals'] for a in by)}. Judge agreement per arm (luna against Opus): " + ", ".join(f"{NAMES[a]} {f(by[a]['judge_agreement'])}" for a in by) + ". Every request and response is in logs/calls/ as JSON; every call's tokens are in cost.jsonl; each run's memory after each night is in results/runs_v2/<arm>_s<seed>/memory_night<d>.txt and .json (items with ids and scores); every corruption (turn index, kind, before, after) and every transfer probe reply is in that run's state.json. Transfer rules, episodes and probes per seed are in data/transfer_v2/transfer_s<seed>.json.", "",
          "## What this does not show", "",
          "- Whether the agent dreams in any felt sense.", "- Whether the result holds when knowledge lives in weights rather than in a text memory.", "- Whether it holds past one model (claude-opus-5-5) or one cap curve (15 percent of each day, decaying with age).",
          "- Absolute accuracy is not comparable with published LongMemEval numbers: days are stitched from several users' histories, temporal-reasoning questions are excluded, and the judge is gpt-5.6-luna rather than gpt-4o.",
          "- Three seeds. A difference smaller than the seed spread is no result. Recall rests on 100 questions per life, transfer on 24 probes per life.",
          "- The Letta replication check did not run (BLOCKED.md), so the harness is validated only by its own no-sleep baseline forgetting as expected, not by matching a published number.", ""]
    (ROOT / "results" / "results_v2.md").write_text("\n".join(L))
    print("\n".join(L[:12]))


if __name__ == "__main__":
    main()
