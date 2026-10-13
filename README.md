# llm-dream

Code and data for "Can an LLM dream?", an experiment by Eric Zou that tests Hoel's overfitted brain hypothesis (2021) on an LLM agent with text memory. The agent lives ten simulated days of LongMemEval conversations. Each night a sleep step rewrites its memory from that day's transcript. In the noisy arms some turns of the transcript are corrupted before the sleep step reads them, and the corruption is either structured (a detail swapped for a plausible wrong one) or random (the turn replaced with unrelated text). The question is whether the noisy arms remember as much as faithful replay and do better on transfer questions the agent has not seen before.

The paper link goes here once it is on arXiv.

## What is in the repo

- `harness/` holds the experiment. `api.py` makes every model call (pinned claude-opus-5-5, model id checked on every reply, no fallbacks). `life.py` builds one ten-day life per seed. `arms.py` has the ten night steps and the sleep prompt. `run_arm.py` runs one arm on one seed and can resume. `battery.py` is the day-eleven memory battery, `transfer.py` the transfer test, `judge.py` the LongMemEval grading prompts. `analyze.py` and `write_results.py` build the summary and results table.
- `scripts/` has the sweep runner, the judge agreement check, the topic scan and swap that replaced some filler sessions (see `decisions.md`), the answer-copy and evidence-hit checks used in the paper, and the Letta replication check.
- `data/lives_manifest/` lists every session id, day, question and swap for the three seeds. The conversation text is left out because it comes from LongMemEval, and `scripts/rebuild_lives.py` puts it back. The rebuilt files match the ones the runs used exactly.
- `data/transfer_v2/` holds the transfer rules, episodes and probes. `data/day11/` holds the DRM word lists.
- `results/results_v2.md` is the results table for all 30 runs (ten arms, three seeds). `results/summary_v2.json` has the same numbers, and each run's own summary is in `results/runs_v2/`. The full run folders (memory after every night, every corruption, every answer and grade) are in the `runs_v2.tar.xz` file on the Releases page.
- `results/regrade_*` are the regrades with gpt-4o and gpt-5.6-luna. `results/letta_check/` is the check against Letta's published sleep-time compute numbers.
- `paper/make_figures.py` draws the paper figures from `results/summary_v2.json`.
- `decisions.md` records every design choice made during the experiment, with the reason and the source.

## Running it

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt huggingface_hub
.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; d('xiaowu0162/longmemeval-cleaned','longmemeval_s_cleaned.json',repo_type='dataset',local_dir='data/raw')"
git clone https://github.com/zycao29/LLM_CognitivePsychology external/LLM_CognitivePsychology
mkdir -p data/corpus && curl -sL -o data/corpus/moby_dick.txt https://www.gutenberg.org/cache/epub/2701/pg2701.txt
.venv/bin/python scripts/rebuild_lives.py
cp .env.example .env    # then add your keys
.venv/bin/python harness/run_arm.py faithful 0
```

`run_arm.py` takes any arm name from `harness/arms.py` and a seed from 0 to 2. Results go to `results/runs_v2/<arm>_s<seed>/`, and `harness/analyze.py` followed by `harness/write_results.py` rebuilds the table.

One full run (ten days plus the day-eleven tests) costs about 65 USD at Anthropic list price. `harness/api.py` stops at 100 USD of API spend (`SPEND_CAP_USD`), so raise that before running more than one arm. The original sweep ran Opus through Claude Code on a Max plan (`WP_BACKEND=subscription`, used by `scripts/run_all.sh`), which also needs `scripts/usage.py set <percent>` before it starts. The default backend is the API.

## Licence

The code is MIT. LongMemEval (Wu et al., 2024) is MIT and is downloaded rather than copied here. `external/longmemeval_evaluate_qa.py` is LongMemEval's grading script, copied unchanged for its prompt templates. The day-eleven battery reads its prompt from Cao, Schooler and Zafarani's repo, which the setup clones. The Letta check adapts `run_stateful_gsm_symbolic.py` from letta-ai/sleep-time-compute (MIT).
