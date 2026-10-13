"""Judge agreement gate for the sweep (HANDOFF.md): after the first finished v2 run, luna and Opus must agree on
about 90 percent of its answers, or the sweep stops before the next run. Prints the agreement every time it runs.
Exit 1 when the gate fails, 0 otherwise."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "harness"))
import analyze

LINE = 0.90


def main():
    runs = analyze.load_runs()
    finished = {k: v for k, v in runs.items() if v["finished"]}
    graded = sum(v["judge_graded"] for v in finished.values()); dis = sum(v["judge_disagreements"] for v in finished.values())
    if not graded:
        print("judge check: no finished run yet"); return 0
    agree = 1 - dis / graded
    print(f"judge check: luna and Opus agree on {100*agree:.1f} percent of {graded} graded answers over {len(finished)} finished run(s)")
    if len(finished) == 1 and agree < LINE:
        print(f"under {100*LINE:.0f} percent on the first finished run: stop and report to Eric before the next run")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
