"""
Run one arm for one seed through the ten-day life, the final recall test, and the day-11 tests.
Resumable: state.json is written after every phase. Usage: python run_arm.py ARM SEED [--days N] [--out DIR]
Exit codes: 0 done, 1 error, 2 aborted (cap, model mismatch), 3 paused on the Max plan usage budget.
"""
import sys, json, random, pathlib, argparse, time, traceback
from concurrent.futures import ThreadPoolExecutor
import api, arms, memory, battery, transfer
from judge import judge
from life import ntok

ROOT = pathlib.Path(__file__).resolve().parent.parent

AGENT_SYSTEM = """You are a personal assistant who has been talking with one user over many days. You do not have the transcripts of past days. What you have is the memory block below, which carries over from previous days.

MEMORY BLOCK:
{memory}
{today}
Answer the user's question using what you remember. Be specific and concrete. If what they ask about is not in your memory or in today's conversations, say plainly that you have no record of it rather than guessing."""

TODAY_TMPL = "\nTODAY'S CONVERSATIONS SO FAR (full transcript):\n{log}\n"
THREADS = 3


class Run:
    def __init__(self, arm, seed, days, out, skip_final=False, day_tokens=None):
        self.arm, self.seed, self.skip_final = arm, seed, skip_final
        self.life = json.load(open(ROOT / "data" / "lives_v2" / f"life_s{seed}.json"))
        self.days = min(days, self.life["days"])
        self.scale = 1.0
        if day_tokens:  # smoke tests: shorten every day to about day_tokens and scale the caps with it
            self.scale = day_tokens / self.life["day_tokens_target"]
            for d in self.life["schedule"]:
                kept, tot = [], 0
                for s in d["sessions"]:
                    kept.append(s); tot += ntok(arms.session_text(s["turns"]))
                    if tot >= day_tokens:
                        break
                d["sessions"] = kept
        # transfer-test episodes go into each day's 4,000-token reserve, at fixed positions per seed (transfer.py)
        self.n_transfer_episodes = transfer.inject(self.life, seed)
        self.dir = pathlib.Path(out) / f"{arm}_s{seed}"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_path = self.dir / "state.json"
        if self.state_path.exists():
            self.state = json.load(open(self.state_path))
        else:
            self.state = {"arm": arm, "seed": seed, "phases_done": [], "memory": "",
                          "mem": ({"window": ""} if arm == "nosleep" else {"items": [], "next_id": 1}),
                          "answers": [], "nights": [], "timing": [], "battery": {}, "transfer": [], "started": time.time()}
        self.tag = f"{arm}/s{seed}"

    # ---- persistence -------------------------------------------------------------------------
    def done(self, phase):
        return phase in self.state["phases_done"]

    def mark(self, phase, t0=None):
        self.state["phases_done"].append(phase)
        if t0 is not None:
            self.state["timing"].append({"phase": phase, "seconds": round(time.time() - t0, 1)})
        self.save()

    def save(self):
        tmp = self.state_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=1))
        tmp.replace(self.state_path)

    def night_rng(self, day):
        return random.Random(f"{self.seed}-{self.arm}-{day}")

    def sessions_of(self, day):
        return self.life["schedule"][day]["sessions"]

    def archive(self, upto_day):
        return [self.sessions_of(d) for d in range(upto_day)]

    def memory_text(self):
        return self.state["memory"]

    # ---- asking -----------------------------------------------------------------------------
    def ask(self, question, memory_text, today_log, tag):
        today = TODAY_TMPL.format(log=today_log) if today_log else ""
        system = AGENT_SYSTEM.format(memory=memory_text or "(empty)", today=today)
        try:
            r = api.call(system, [{"role": "user", "content": question}], tag=tag, max_tokens=3000)
            return {"response": r["text"], "thinking": r["thinking"], "call_id": r["call_id"], "refusal": None,
                    "seconds": round(r["seconds"], 1)}
        except api.Refusal as e:
            return {"response": "", "thinking": "", "call_id": e.call_id, "refusal": e.category, "seconds": None}

    def ask_and_judge(self, q, memory_text, today_log, phase, day):
        tag = f"{self.tag}/d{day}/{phase}/{q['question_id']}"
        a = self.ask(q["question"], memory_text, today_log, tag)
        if a["refusal"]:
            j = {"correct": False, "judge_label": "refusal", "correct_opus": False, "judge_label_opus": "refusal", "judge_main": None}
        else:
            j = judge(q["question_type"], q["question"], q["answer"], a["response"], q["abstention"], tag)
        return {"question_id": q["question_id"], "question_type": q["question_type"], "abstention": q["abstention"],
                "phase": phase, "day": day, "last_day": q["last_day"], "question": q["question"], "gold": q["answer"],
                **a, **j}

    def ask_many(self, qs, memory_text, today_log, phase, day):
        """First question alone so its long system prompt is written to the cache once, then the rest in parallel."""
        if not qs:
            return []
        rows = [self.ask_and_judge(qs[0], memory_text, today_log, phase, day)]
        with ThreadPoolExecutor(THREADS) as ex:
            rows += list(ex.map(lambda q: self.ask_and_judge(q, memory_text, today_log, phase, day), qs[1:]))
        self.state["answers"] += rows
        return rows

    # ---- one night -----------------------------------------------------------------------------
    def night(self, day, sessions, suffix=""):
        cap = arms.cap_for(day, self.scale)
        t0 = time.time()
        new_mem, info = arms.NIGHT[self.arm](self.state["mem"], sessions, self.archive(day), self.night_rng(day),
                                             f"{self.tag}/d{day}", cap, day)
        self.state["mem"] = new_mem
        if self.arm == "nosleep":
            self.state["memory"] = new_mem["window"]
            rec = {"day": day, "cap": cap, "tokens": info["tokens"], "seconds": round(time.time() - t0, 1), **info}
        else:
            self.state["memory"] = memory.render_for_agent(new_mem["items"])
            (self.dir / f"memory_night{day}{suffix}.json").write_text(json.dumps(new_mem["items"], indent=1))
            cr = info["cap_report"]
            rec = {"day": day, "cap": cap, "tokens": cr["tokens_after"], "items": cr["items_after"],
                   "items_with_details": sum(1 for i in new_mem["items"] if i.get("details")),
                   "details_stripped": cr["details_stripped"], "details_partial": cr["details_partial"],
                   "items_deleted": cr["items_deleted"], "seconds": round(time.time() - t0, 1), **info}
        (self.dir / f"memory_night{day}{suffix}.txt").write_text(self.state["memory"])
        self.state["nights"].append(rec)
        return rec

    # ---- the loop -----------------------------------------------------------------------------
    def run(self):
        qs = self.life["questions"]
        for day in range(self.days):
            sessions = self.sessions_of(day)
            log = arms.format_log(sessions)
            todays_qs = [q for q in qs if q["last_day"] == day and not q["abstention"]]
            ph = f"d{day}_evening"
            if not self.done(ph):
                t0 = time.time()
                rows = self.ask_many(todays_qs, self.memory_text(), log, "evening", day)
                self.mark(ph, t0)
                print(f"[{self.tag}] day {day} evening: {sum(r['correct'] for r in rows)}/{len(rows)} (opus {sum(r['correct_opus'] for r in rows)}) in {time.time()-t0:.0f}s, list-price spend {api.total_spend():.2f}", flush=True)
            ph = f"d{day}_night"
            if not self.done(ph):
                t0 = time.time()
                rec = self.night(day, sessions)
                self.mark(ph, t0)
                extra = "" if self.arm == "nosleep" else f", {rec['items']} items, stripped {rec['details_stripped']} details ({rec['details_partial']} partial), deleted {rec['items_deleted']}"
                print(f"[{self.tag}] day {day} night: memory {rec['tokens']} of cap {rec['cap']} tokens{extra}, {rec['seconds']}s", flush=True)
            ph = f"d{day}_morning"
            if not self.done(ph):
                t0 = time.time()
                rows = self.ask_many(todays_qs, self.memory_text(), "", "morning", day + 1)
                self.mark(ph, t0)
                print(f"[{self.tag}] day {day} morning-after: {sum(r['correct'] for r in rows)}/{len(rows)} (opus {sum(r['correct_opus'] for r in rows)}) in {time.time()-t0:.0f}s", flush=True)
        if self.skip_final:
            return
        if not self.done("final"):
            t0 = time.time()
            rows = self.ask_many(qs, self.memory_text(), "", "final", self.days)
            self.mark("final", t0)
            print(f"[{self.tag}] final: {sum(r['correct'] for r in rows)}/{len(rows)} list-price spend {api.total_spend():.2f}", flush=True)
        self.transfer_probes()
        self.battery_day()
        self.state["finished"] = time.time()
        self.mark("all")

    # ---- transfer test probes, after night 10 (transfer.py) ----------------------------------------
    def transfer_probes(self):
        if self.done("transfer") or not transfer.available(self.seed):
            return
        t0 = time.time()
        self.state["transfer"] = transfer.run_probes(self, self.memory_text(), self.days)
        self.mark("transfer", t0)

    # ---- day 11 ---------------------------------------------------------------------------------
    def battery_test(self, mat, memory_text, today_log, phase, day):
        out = {}
        for name, prompt, items in battery.tests(mat):
            ph_tag = f"{self.tag}/d{day}/battery_{phase}/{name}"
            a = self.ask(prompt, memory_text, today_log, ph_tag)
            answers = battery.parse_answers(a["response"], len(items))
            res, rows = battery.score(name, items, answers)
            out[name] = {"summary": res, "rows": rows, "call_id": a["call_id"], "refusal": a["refusal"], "raw": a["response"]}
        return out

    def battery_day(self):
        day = self.days
        mat_rng = random.Random(self.seed)  # same material for all arms of a seed
        mat = battery.material(mat_rng)
        sessions = battery.study_sessions(mat)
        log = arms.format_log(sessions)
        if not self.done("battery_evening"):
            self.state["battery"]["evening"] = self.battery_test(mat, self.memory_text(), log, "evening", day)
            self.mark("battery_evening")
        if not self.done("battery_night"):
            t0 = time.time()
            self.night(day, sessions, "_battery")
            self.mark("battery_night", t0)
        if not self.done("battery_morning"):
            self.state["battery"]["morning"] = self.battery_test(mat, self.memory_text(), "", "morning", day + 1)
            self.mark("battery_morning")
            s = self.state["battery"]["morning"]
            print(f"[{self.tag}] battery morning: drm hit {s['drm']['summary']['hit_rate']} lure {s['drm']['summary']['lure_false_alarm']} | serial hit {s['serial']['summary']['hit_rate']} | pl fan1 {s['pl']['summary']['fan1_accuracy']} fan2 {s['pl']['summary']['fan2_accuracy']}", flush=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("arm", choices=arms.ARMS); p.add_argument("seed", type=int)
    p.add_argument("--days", type=int, default=10); p.add_argument("--out", default=str(ROOT / "results" / "runs_v2"))
    p.add_argument("--skip-final", action="store_true", help="stop after the day loop, for short test runs")
    p.add_argument("--day-tokens", type=int, help="smoke tests only: shorten days to about this many tokens, caps scaled to match")
    a = p.parse_args()
    run = Run(a.arm, a.seed, a.days, a.out, a.skip_final, a.day_tokens)
    try:
        run.run()
    except api.UsagePaused as e:
        run.save()
        print("PAUSED:", e, flush=True); sys.exit(3)
    except api.RunAborted as e:
        run.save()
        (ROOT / "BLOCKED.md").write_text(f"# Run aborted\n\n{run.tag}: {e}\n\nTime: {time.ctime()}\n")
        print("ABORTED:", e, flush=True); sys.exit(2)
    except Exception:
        run.save()
        traceback.print_exc(); sys.exit(1)
