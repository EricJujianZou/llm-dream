#!/bin/bash
# Letta replication check. Needs a paid-tier OpenAI key in .env and Docker. Idempotent.
set -e
cd "$(dirname "$0")/.."
set -a; . ./.env; set +a
if ! docker ps --format '{{.Names}}' | grep -q '^letta-llmdream$'; then
  docker rm -f letta-llmdream >/dev/null 2>&1 || true
  mkdir -p logs/letta_pgdata
  docker run -d --name letta-llmdream -v "$PWD/logs/letta_pgdata:/var/lib/postgresql/data" -p 8283:8283 -e OPENAI_API_KEY="$OPENAI_API_KEY" letta/letta:0.7.5 >/dev/null
  sleep 40
fi
PY=external/.venv-letta/bin/python
# Two random problems from each of the 50 templates (seed 0). The file's first 100 rows are only 2 templates.
D=results/letta_check/p2_sample100_2per_template.jsonl
rm -f results/letta_check/p2_v0_*_sample100.jsonl
$PY harness/letta_check.py --input_file $D --output_file results/letta_check/p2_v0_sleep_sample100.jsonl --max_concurrent 1
$PY harness/letta_check.py --input_file $D --output_file results/letta_check/p2_v0_nosleep_sample100.jsonl --max_concurrent 1 --no_sleep
.venv/bin/python harness/letta_summary.py
