"""Rebuild data/lives_v2/life_s{0,1,2}.json from the manifests in data/lives_manifest and LongMemEval.

The manifests keep every session id, day, question and topic swap but leave out the conversation text,
which comes from LongMemEval (MIT licence). Download longmemeval_s_cleaned.json from
https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned into data/raw/ first, then run:
  python scripts/rebuild_lives.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
raw = json.load(open(ROOT / "data" / "raw" / "longmemeval_s_cleaned.json"))
sessions = {}
for q in raw:
    for sid, sess in zip(q["haystack_session_ids"], q["haystack_sessions"]):
        sessions.setdefault(sid, [{"role": t["role"], "content": t["content"]} for t in sess])

out = ROOT / "data" / "lives_v2"
out.mkdir(parents=True, exist_ok=True)
for seed in range(3):
    life = json.load(open(ROOT / "data" / "lives_manifest" / f"life_s{seed}.manifest.json"))
    for day in life["schedule"]:
        for s in day["sessions"]:
            s["turns"] = sessions[s["session_id"]]
    for q in life["questions"]:
        for e in q["evidence"]:
            e["turns"] = sessions[e["session_id"]]
    (out / f"life_s{seed}.json").write_text(json.dumps(life))
    print(f"seed {seed}: {sum(len(d['sessions']) for d in life['schedule'])} sessions")
