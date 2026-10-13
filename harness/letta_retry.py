"""Retry the errored problems of a Letta check output file and merge the new results in place. Usage: letta_retry.py OUT INPUT [--no_sleep]"""
import json, subprocess, sys, pathlib
out, inp, extra = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
src = [json.loads(l) for l in open(inp)]
res = [json.loads(l) for l in open(out)]
# output rows keep input order (gather), so row i answers input i
bad = [i for i, r in enumerate(res) if "error" in r]
print(f"{out.name}: retrying {len(bad)} errored problems", flush=True)
if not bad: sys.exit()
tmp_in, tmp_out = out.with_suffix(".retry_in.jsonl"), out.with_suffix(".retry_out.jsonl")
tmp_in.write_text("".join(json.dumps(src[i]) + "\n" for i in bad))
subprocess.run(["external/.venv-letta/bin/python", "harness/letta_check.py", "--input_file", str(tmp_in),
                "--output_file", str(tmp_out), "--max_concurrent", "1", *extra], check=True)
new = [json.loads(l) for l in open(tmp_out)]
for i, r in zip(bad, new):
    res[i] = r
out.write_text("".join(json.dumps(r) + "\n" for r in res))
tmp_in.unlink(); tmp_out.unlink()
print(f"{out.name}: {sum('error' in r for r in res)} still errored", flush=True)
