#!/bin/bash
# Full sweep: every arm in harness/arms.py ARMS x seeds 0 1 2, one run at a time, all arms of seed 0 first.
# Idempotent: finished runs are skipped, unfinished ones resume from their state.json.
# Stops on: the Max-plan budget pause (exit 3), any run error, or the two judges agreeing on under 90 percent of
# the first finished run's answers (HANDOFF.md). Rerun the script to continue after a stop.
set -u
cd "$(dirname "$0")/.."
export WP_BACKEND=subscription          # Opus through Claude Code on the Max plan; the API key would spend real money
PY=.venv/bin/python
OUT=results/runs_v2
mkdir -p logs/runs_v2
ARMS=$($PY -c "import sys; sys.path.insert(0,'harness'); import arms; print(' '.join(arms.ARMS))")
SEEDS="0 1 2"

# preflight: run_arm.py runs without transfer episodes when a seed's rules are missing, so check here
for s in $SEEDS; do
  [ -f data/transfer_v2/transfer_s$s.json ] || { echo "transfer rules for seed $s are missing (data/transfer_v2/transfer_s$s.json). Build them first: $PY harness/transfer.py build $s --avoid-from ..."; exit 2; }
done
[ -f results/transfer_preview.md ] || { echo "results/transfer_preview.md is missing. Eric reads it before the sweep."; exit 2; }
$PY scripts/usage.py status || exit 2
echo "arms: $ARMS"

for seed in $SEEDS; do
  for arm in $ARMS; do
    d=$OUT/${arm}_s${seed}
    if [ -f "$d/state.json" ] && grep -q '"all"' "$d/state.json"; then echo "skip ${arm}_s${seed} (done)"; continue; fi
    echo "$(date '+%F %T') start ${arm}_s${seed}"
    $PY harness/run_arm.py "$arm" "$seed" --out "$OUT" >> "logs/runs_v2/${arm}_s${seed}.log" 2>&1
    rc=$?
    tail -2 "logs/runs_v2/${arm}_s${seed}.log"
    if [ $rc -eq 3 ]; then
      echo "PAUSED at the Max-plan budget stop point. After Eric gives the new /usage percentage: $PY scripts/usage.py set N, then rerun this script."; exit 3
    fi
    if [ $rc -ne 0 ]; then echo "${arm}_s${seed} exited $rc, stopping. See logs/runs_v2/${arm}_s${seed}.log"; exit $rc; fi
    $PY harness/analyze.py --run "$d" > "$d/summary.json"
    $PY scripts/judge_check.py || { echo "judge agreement under the line after the first finished run; stopping for Eric."; exit 4; }
    $PY harness/analyze.py > logs/runs_v2/analyze_latest.txt 2>&1
  done
done
$PY harness/analyze.py && $PY harness/write_results.py > /dev/null && echo "wrote results/results_v2.md"
