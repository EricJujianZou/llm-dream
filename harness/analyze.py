"""Aggregate results/runs_v2/*/state.json into results/summary_v2.json and print the tables used in results_v2.md.

v2 (4 Oct 2026): ten arms from arms.ARMS, memory size per night against the cap, gist-stripping and deletion
counts, final recall by delay in nights, transfer near and far, the corruption-rate curve, and the agreement
between the two judges (luna main, Opus second) on every graded answer.

  .venv/bin/python harness/analyze.py                 # all runs under results/runs_v2
  .venv/bin/python harness/analyze.py --run DIR       # one run's summary as JSON (used by scripts/run_all.sh)
"""
import json, glob, pathlib, statistics as st, sys, argparse
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "harness"))
import arms, battery
ARMS = arms.ARMS
RUNS = ROOT / "results" / "runs_v2"
SUMMARY = ROOT / "results" / "summary_v2.json"
DAYS = 10


def rate_of(arm):
    """Corruption rate of an arm from its name: faithful is 0, nosleep has none."""
    if arm == "faithful": return 0.0
    if arm == "nosleep": return None
    return int(arm.split("_")[1]) / 100


def rescore(name, rows):
    items = [{k: v for k, v in r.items() if k not in ("said_yes", "raw")} for r in rows]
    return battery.score(name, items, {i: r["raw"] for i, r in enumerate(rows, 1)})[0]


def family_of(arm):
    return arm.split("_")[0] if "_" in arm else arm


def acc(rows):
    rows = [r for r in rows if r.get("correct") is not None]
    return (sum(1 for r in rows if r["correct"]) / len(rows)) if rows else None


def agreement(rows, a="correct", b="correct_opus"):
    rows = [r for r in rows if r.get(a) is not None and r.get(b) is not None]
    return (sum(1 for r in rows if bool(r[a]) == bool(r[b])) / len(rows)) if rows else None


def per_run(state):
    A = state["answers"]
    N = state.get("nights", [])
    ev = [r for r in A if r["phase"] == "evening" and not r["abstention"]]
    mo = [r for r in A if r["phase"] == "morning" and not r["abstention"]]
    fi = [r for r in A if r["phase"] == "final" and not r["abstention"]]
    days = len([n for n in N if n["day"] < DAYS]) or DAYS
    sleep_nights = [n for n in N if "details_stripped" in n]
    out = {
        "arm": state["arm"], "seed": state["seed"], "rate": rate_of(state["arm"]), "family": family_of(state["arm"]),
        "n_questions": len({r["question_id"] for r in A}),
        "evening_acc": acc(ev), "morning_acc": acc(mo),
        "one_night_drop": (acc(ev) - acc(mo)) if ev and mo else None,
        "final_acc": acc(fi),
        "final_acc_early": acc([r for r in fi if r["last_day"] <= 4]),
        "final_acc_late": acc([r for r in fi if r["last_day"] >= 5]),
        "final_acc_novel": acc([r for r in fi if r["question_type"] == "multi-session"]),
        "final_acc_by_type": {t: acc([r for r in fi if r["question_type"] == t]) for t in sorted({r["question_type"] for r in fi})},
        # delay = nights between the last evidence day and the final questions (day 10 asks about day 9 after one night)
        "final_acc_by_delay": {str(days - d): acc([r for r in fi if r["last_day"] == d]) for d in range(days)},
        "final_abstention_acc": acc([r for r in A if r["phase"] == "final" and r["abstention"]]),
        "refusals": sum(1 for r in A if r.get("refusal")),
        "judge_agreement": agreement(A),
        "judge_disagreements": sum(1 for r in A if r.get("correct") is not None and r.get("correct_opus") is not None and bool(r["correct"]) != bool(r["correct_opus"])),
        "judge_graded": sum(1 for r in A if r.get("correct") is not None and r.get("correct_opus") is not None),
        # memory size against the cap, per night and summarised
        "nights": len(N),
        "memory_tokens_by_night": [n["tokens"] for n in N],
        "cap_by_night": [n["cap"] for n in N],
        "memory_fill_by_night": [n["tokens"] / n["cap"] for n in N if n.get("cap")],
        "mean_memory_tokens": st.mean(n["tokens"] for n in N) if N else None,
        "mean_memory_fill": st.mean(n["tokens"] / n["cap"] for n in N if n.get("cap")) if N else None,
        "final_memory_tokens": N[days - 1]["tokens"] if len(N) >= days else (N[-1]["tokens"] if N else None),
        # forgetting done by the harness when the memory is over its cap (sleep arms only)
        "details_stripped": sum(n["details_stripped"] for n in sleep_nights) if sleep_nights else None,
        "details_partial": sum(n["details_partial"] for n in sleep_nights) if sleep_nights else None,
        "items_deleted": sum(n["items_deleted"] for n in sleep_nights) if sleep_nights else None,
        "nights_over_cap": sum(1 for n in sleep_nights if n["details_stripped"] or n["items_deleted"]) if sleep_nights else None,
        "final_items": N[days - 1].get("items") if len(N) >= days else None,
        "sleep_output_tokens": st.mean(n["output_tokens"] for n in sleep_nights if n.get("output_tokens")) if any(n.get("output_tokens") for n in sleep_nights) else None,
        "sleep_seconds": st.mean(n["seconds"] for n in sleep_nights) if sleep_nights else None,
        "corrupted_turns": sum(n["corruption"]["n_corrupted"] for n in N if n.get("corruption")) or None,
        "finished": "all" in state["phases_done"],
    }
    # transfer test: did the agent follow the hidden rule on the near and the far probe (main judge, Opus second)
    T = state.get("transfer") or []
    if T:
        near = [r for r in T if r["kind"] == "near"]; far = [r for r in T if r["kind"] == "far"]
        fr = lambda rows, k="follows": acc([{"correct": r[k]} for r in rows])
        out["transfer"] = {
            "near": fr(near), "far": fr(far), "near_opus": fr(near, "follows_opus"), "far_opus": fr(far, "follows_opus"),
            "near_minus_far": (fr(near) or 0) - (fr(far) or 0),
            "by_episodes": {str(k): fr([r for r in T if r["n_episodes"] == k]) for k in sorted({r["n_episodes"] for r in T})},
            "n_probes": len(T), "judge_agreement": agreement(T, "follows", "follows_opus"),
        }
    b = state.get("battery", {})
    for phase in ("evening", "morning"):
        if phase in b:
            # re-score from the saved per-item answers so scoring fixes apply to finished runs
            d, s, p = (rescore(n, b[phase][n]["rows"]) for n in ("drm", "serial", "pl"))
            out[f"battery_{phase}"] = {"drm_hit": d["hit_rate"], "drm_lure_fa": d["lure_false_alarm"], "drm_unrelated_fa": d["unrelated_false_alarm"],
                                      "serial_hit": s["hit_rate"], "serial_primacy": s["primacy_hit_rate"], "serial_middle": s["middle_hit_rate"], "serial_recency": s["recency_hit_rate"], "serial_foil_fa": s["foil_false_alarm"],
                                      "pl_fan1_acc": p["fan1_accuracy"], "pl_fan2_acc": p["fan2_accuracy"]}
    return out


def msd(xs):
    xs = [x for x in xs if x is not None]
    if not xs: return None
    return {"mean": st.mean(xs), "sd": st.stdev(xs) if len(xs) > 1 else 0.0, "n": len(xs), "values": xs}


def get(d, key):
    """Dotted lookup: 'transfer.near' or 'battery_morning.drm_lure_fa'."""
    for k in key.split("."):
        d = (d or {}).get(k)
    return d


METRICS = ["evening_acc", "morning_acc", "one_night_drop", "final_acc", "final_acc_early", "final_acc_late", "final_acc_novel", "final_abstention_acc"]
MEMORY = ["mean_memory_tokens", "mean_memory_fill", "final_memory_tokens", "final_items", "details_stripped", "details_partial", "items_deleted", "nights_over_cap", "sleep_output_tokens", "sleep_seconds", "corrupted_turns"]
TRANSFER = ["transfer.near", "transfer.far", "transfer.near_minus_far", "transfer.near_opus", "transfer.far_opus"]
BATTERY = ["drm_hit", "drm_lure_fa", "drm_unrelated_fa", "serial_hit", "serial_primacy", "serial_middle", "serial_recency", "pl_fan1_acc", "pl_fan2_acc"]
PAIRED = METRICS + TRANSFER + ["battery_morning.drm_lure_fa", "battery_morning.serial_hit", "battery_morning.pl_fan1_acc"]


def summarise(runs):
    seeds = sorted({k[1] for k in runs})
    by_arm = {}
    for arm in ARMS:
        rs = [runs[(arm, s)] for s in seeds if (arm, s) in runs]
        if not rs: continue
        v = {m: msd([r.get(m) for r in rs]) for m in METRICS + MEMORY}
        v.update({m: msd([get(r, m) for r in rs]) for m in TRANSFER})
        v["rate"] = rate_of(arm); v["family"] = family_of(arm)
        v["final_acc_by_delay"] = {d: msd([r["final_acc_by_delay"].get(d) for r in rs]) for d in [str(i) for i in range(1, DAYS + 1)]}
        v["transfer_by_episodes"] = {k: msd([get(r, f"transfer.by_episodes.{k}") for r in rs]) for k in ("2", "3")}
        v["battery_morning"] = {m: msd([get(r, f"battery_morning.{m}") for r in rs]) for m in BATTERY}
        v["battery_evening"] = {m: msd([get(r, f"battery_evening.{m}") for r in rs]) for m in BATTERY}
        v["finished_runs"] = sum(1 for r in rs if r["finished"])
        v["refusals"] = sum(r["refusals"] for r in rs)
        v["judge_agreement"] = msd([r["judge_agreement"] for r in rs])
        v["memory_tokens_by_night"] = [msd([r["memory_tokens_by_night"][i] for r in rs if len(r["memory_tokens_by_night"]) > i]) for i in range(DAYS + 1)]
        by_arm[arm] = v
    # paired differences against faithful, same seed
    paired = {}
    for arm in ARMS:
        if arm == "faithful": continue
        for m in PAIRED:
            diffs = []
            for s in seeds:
                a, f = runs.get((arm, s)), runs.get(("faithful", s))
                if not a or not f: continue
                va, vf = get(a, m), get(f, m)
                if va is not None and vf is not None:
                    diffs.append(va - vf)
            paired[f"{arm}_minus_faithful.{m}"] = msd(diffs)
    # corruption-rate curve: faithful at 0, then each family's arms by rate
    curve = {}
    for fam in ("structured", "random"):
        pts = []
        for arm in ["faithful"] + [a for a in ARMS if family_of(a) == fam]:
            v = by_arm.get(arm)
            if v: pts.append({"arm": arm, "rate": rate_of(arm), "final_acc": v["final_acc"], "final_acc_novel": v["final_acc_novel"],
                              "transfer_far": v["transfer.far"], "transfer_near": v["transfer.near"], "mean_memory_tokens": v["mean_memory_tokens"],
                              "drm_lure_fa": v["battery_morning"]["drm_lure_fa"]})
        curve[fam] = pts
    # judge agreement over every graded answer in every run
    graded = sum(r["judge_graded"] for r in runs.values()); dis = sum(r["judge_disagreements"] for r in runs.values())
    return {"runs": {f"{a}_s{s}": v for (a, s), v in runs.items()}, "by_arm": by_arm, "paired_vs_faithful": paired, "curve": curve,
            "judge_agreement_overall": (1 - dis / graded) if graded else None, "judge_graded": graded, "judge_disagreements": dis,
            "seeds": seeds, "n_runs": len(runs), "finished_runs": sum(1 for r in runs.values() if r["finished"])}


def load_runs(runs_dir=RUNS):
    runs = {}
    for p in sorted(glob.glob(str(runs_dir / "*_s*" / "state.json"))):
        s = json.load(open(p))
        if s["arm"] in ARMS:
            runs[(s["arm"], s["seed"])] = per_run(s)
    return runs


def print_tables(S):
    by = S["by_arm"]
    def f(x): return "   n/a   " if x is None else f"{x['mean']:.3f}±{x['sd']:.3f}"
    def g(x): return "   n/a" if x is None else f"{x['mean']:6.0f}"
    print(f"runs {S['n_runs']} ({S['finished_runs']} finished), seeds {S['seeds']}, judge agreement over {S['judge_graded']} graded answers: "
          + ("n/a" if S["judge_agreement_overall"] is None else f"{100*S['judge_agreement_overall']:.1f} percent"))
    print("\narm              " + " ".join(f"{m[:13]:>13}" for m in METRICS) + "   done")
    for arm, v in by.items():
        print(f"{arm:16} " + " ".join(f"{f(v[m]):>13}" for m in METRICS) + f"   {v['finished_runs']}")
    print("\nmemory           mean tokens    mean fill  final tok  items  stripped  partial  deleted  nights>cap")
    for arm, v in by.items():
        print(f"{arm:16} {g(v['mean_memory_tokens']):>11} {f(v['mean_memory_fill']):>12} {g(v['final_memory_tokens']):>9} {g(v['final_items']):>6} {g(v['details_stripped']):>9} {g(v['details_partial']):>8} {g(v['items_deleted']):>8} {g(v['nights_over_cap']):>8}")
    print("\ntransfer (main judge)        near          far     near-far")
    for arm, v in by.items():
        print(f"{arm:16} {f(v['transfer.near']):>16} {f(v['transfer.far']):>12} {f(v['transfer.near_minus_far']):>14}")
    print("\nfinal recall by delay (nights since last evidence)")
    print("arm              " + " ".join(f"{d:>11}" for d in range(1, DAYS + 1)))
    for arm, v in by.items():
        print(f"{arm:16} " + " ".join(f"{f(v['final_acc_by_delay'][str(d)])[:11]:>11}" for d in range(1, DAYS + 1)))
    print("\nbattery (morning after sleep)")
    print("arm              " + " ".join(f"{m[:13]:>13}" for m in BATTERY))
    for arm, v in by.items():
        print(f"{arm:16} " + " ".join(f"{f(v['battery_morning'][m]):>13}" for m in BATTERY))
    print("\ncorruption-rate curve, final recall (mean±sd)")
    for fam, pts in S["curve"].items():
        print(f"{fam:11} " + "  ".join(f"{p['rate']:.2f}: {f(p['final_acc'])}" for p in pts))
    print("\npaired differences vs faithful (mean±sd over seeds)")
    for k, v in S["paired_vs_faithful"].items():
        if v: print(f"{k:62} {v['mean']:+.3f} ± {v['sd']:.3f}  values {[round(x,3) for x in v['values']]}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run", help="one run directory: print its per-run summary as JSON and exit")
    p.add_argument("--runs-dir", default=str(RUNS))
    a = p.parse_args()
    if a.run:
        s = json.load(open(pathlib.Path(a.run) / "state.json"))
        print(json.dumps(per_run(s), indent=1)); return
    runs = load_runs(pathlib.Path(a.runs_dir))
    if not runs:
        print("no runs found"); return
    S = summarise(runs)
    SUMMARY.write_text(json.dumps(S, indent=1))
    print_tables(S)


if __name__ == "__main__":
    main()
