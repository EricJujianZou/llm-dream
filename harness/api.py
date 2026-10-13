"""
Single entry point for every model call in this experiment.

Controls from the spec's "Controls on the API" section:
- pinned model id, checked on every response. On the Max-plan backend Claude Code can fall back to another model
  on its own after an upstream error; such a reply is discarded and the call retried, five in a row abort the run
- no fallbacks parameter, ever
- fixed effort, set once per process and never changed
- thinking display summarised and logged
- refusals logged as failed calls, never retried on another model (CLAUDE_CODE_NO_MODEL_FALLBACK=1 on the Max-plan
  backend, else Claude Code answers a refused question on an older Opus by itself)
- every request and response body written verbatim to logs/calls/
- every call's token counts appended to cost.jsonl

v2 (4 Oct 2026):
- WP_BACKEND=subscription routes Opus calls through `claude -p` on a Claude Max plan. Those calls are logged at
  list price but cost no money. They are governed by the weekly usage budget (usage_budget.json), not the spend cap.
- The spend cap counts real money only: OpenAI calls and calls on the Anthropic API key, since the v2 start.
- count_tokens() uses Anthropic's free token-counting endpoint (the API key), cached in data/token_cache.sqlite.
- openai_chat() is the one way to call OpenAI (the luna judge), logged to cost.jsonl like everything else.
"""
import json, os, time, uuid, threading, pathlib, fcntl, subprocess, tempfile, re, hashlib, sqlite3
import anthropic

ROOT = pathlib.Path(__file__).resolve().parent.parent
CALLS_DIR = ROOT / "logs" / "calls"
COST_FILE = ROOT / "cost.jsonl"
BUDGET_FILE = ROOT / "usage_budget.json"
TOKEN_CACHE = ROOT / "data" / "token_cache.sqlite"
CALLS_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "claude-opus-5-5"
EFFORT = "medium"
SPEND_CAP_USD = 100.0           # real money only, since V2_START (decisions.md, "Spend cap split")
V2_START = 1791138000           # 4 Oct 2026 14:20 EDT, just before the first Max-plan call
REAL_MONEY = {("openai", None), ("anthropic", "api")}
# USD per million tokens, Opus 5.5 list price (claude-api skill table, cached 2026-09-25)
PRICE = {"input": 4.00, "output": 20.00, "cache_read": 0.20, "cache_write": 5.00}
# gpt-5.6-luna's price is not published where the harness can read it; logged at gpt-4o list price as a
# conservative placeholder and flagged in every record (decisions.md).
OPENAI_PRICE = {"gpt-4o-2024-08-06": (2.50, 10.00), "gpt-4o-mini": (0.15, 0.60), "gpt-5.6-luna": (2.50, 10.00)}
MAX_OUTPUT_TOKENS = 64000       # ceiling for claude -p output; a sleep night writes about 20,000

_lock = threading.Lock()


class RunAborted(RuntimeError):
    pass


class UsagePaused(RuntimeError):
    """Raised when the Max plan budget for this week is used up, or the CLI reports a usage limit."""
    pass


class Refusal(RuntimeError):
    def __init__(self, call_id, category, explanation):
        super().__init__(f"refusal {category}: {explanation}")
        self.call_id, self.category, self.explanation = call_id, category, explanation


def _load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
_client = anthropic.Anthropic(max_retries=4, timeout=600)


def _usd(u):
    return (u.get("input_tokens", 0) * PRICE["input"]
            + u.get("output_tokens", 0) * PRICE["output"]
            + u.get("cache_read_input_tokens", 0) * PRICE["cache_read"]
            + u.get("cache_creation_input_tokens", 0) * PRICE["cache_write"]) / 1e6


# ---- cost file, read incrementally so a check costs nothing as the file grows -------------------
class _CostTally:
    def __init__(self):
        self.offset = 0
        self.real_v2 = 0.0        # real money since V2_START
        self.sub_total = 0.0      # list price of Max-plan calls, all time
        self.sub_since = {}       # ts threshold -> list price of Max-plan calls at or after it
        self.all_total = 0.0

    def _add(self, r):
        usd = r.get("usd") or 0.0
        self.all_total += usd
        if r.get("backend") == "subscription":
            self.sub_total += usd
            ts = r.get("ts", 0)
            for k in self.sub_since:
                if ts >= k:
                    self.sub_since[k] += usd
        elif (r.get("provider"), r.get("backend")) in REAL_MONEY or (r.get("provider") == "anthropic" and r.get("backend") is None):
            if r.get("ts", 0) >= V2_START:
                self.real_v2 += usd

    def refresh(self):
        if not COST_FILE.exists():
            return
        with open(COST_FILE) as f:
            f.seek(self.offset)
            for line in f:
                try:
                    self._add(json.loads(line))
                except Exception:
                    pass
            self.offset = f.tell()

    def since(self, ts):
        if ts not in self.sub_since:
            self.sub_since[ts] = 0.0
            self.offset = 0; self.real_v2 = self.sub_total = self.all_total = 0.0
            for k in self.sub_since:
                self.sub_since[k] = 0.0
        self.refresh()
        return self.sub_since[ts]


_tally = _CostTally()


def total_spend():
    """List price of every logged call, all providers, all time (for progress lines)."""
    with _lock:
        _tally.refresh()
        return _tally.all_total


def real_spend_v2():
    with _lock:
        _tally.refresh()
        return _tally.real_v2


def log_cost(record):
    """Append one line to cost.jsonl under a file lock."""
    record.setdefault("ts", time.time())
    with _lock, open(COST_FILE, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(record) + "\n")
        fcntl.flock(f, fcntl.LOCK_UN)


def check_cap():
    spent = real_spend_v2()
    if spent > SPEND_CAP_USD:
        raise RunAborted(f"real-money spend {spent:.2f} USD since v2 start passed cap {SPEND_CAP_USD}")
    return spent


# ---- weekly usage budget on the Max plan ------------------------------------------------------
def budget():
    """usage_budget.json: {pct_at_set, set_ts, weekly_usd, stop_pct, reset_ts}. Written by scripts/usage.py."""
    if not BUDGET_FILE.exists():
        return None
    return json.loads(BUDGET_FILE.read_text())


def budget_status(now=None):
    """Returns (allowed_usd, spent_usd, period_start) for the current week, or None when no budget is set."""
    b = budget()
    if not b:
        return None
    now = now or time.time()
    reset, week = b["reset_ts"], 7 * 86400
    if now < reset:
        start, allowed = b["set_ts"], (b["stop_pct"] - b["pct_at_set"]) / 100 * b["weekly_usd"]
    else:
        # a reset has passed since Eric set the figure: usage is 0 at the reset, the full stop share is available
        while reset + week <= now:
            reset += week
        start, allowed = reset, b["stop_pct"] / 100 * b["weekly_usd"]
    with _lock:
        spent = _tally.since(start)
    return allowed, spent, start


def check_budget():
    st = budget_status()
    if st is None:
        raise RunAborted("no usage_budget.json: run scripts/usage.py set <percent> with the /usage figure first")
    allowed, spent, start = st
    if spent >= allowed:
        raise UsagePaused(f"Max plan budget used: {spent:.2f} of {allowed:.2f} USD list price since {time.ctime(start)}")
    return allowed - spent


# ---- token counting with Claude's own tokenizer ------------------------------------------------
_tc_local = threading.local()


def _tc_db():
    db = getattr(_tc_local, "db", None)
    if db is None:
        TOKEN_CACHE.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(TOKEN_CACHE, timeout=60)
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("CREATE TABLE IF NOT EXISTS tc (h TEXT PRIMARY KEY, n INTEGER)")
        db.commit()
        _tc_local.db = db
    return db


def count_tokens(text):
    """Claude tokens in `text`, from Anthropic's count_tokens endpoint (free, API key), cached by content hash."""
    if not text:
        return 0
    h = hashlib.sha1(text.encode()).hexdigest()
    db = _tc_db()
    row = db.execute("SELECT n FROM tc WHERE h=?", (h,)).fetchone()
    if row:
        return row[0]
    for attempt in range(8):
        try:
            n = _client.messages.count_tokens(model=MODEL, messages=[{"role": "user", "content": text}]).input_tokens
            break
        except (anthropic.RateLimitError, anthropic.APIConnectionError, anthropic.InternalServerError, anthropic.APITimeoutError):
            time.sleep(min(60, 2 ** attempt))
    else:
        raise RunAborted("count_tokens failed eight times")
    n -= 7  # the empty-message overhead of the endpoint, measured 4 Oct 2026, so counts add up across pieces
    n = max(1, n)
    db.execute("INSERT OR IGNORE INTO tc VALUES (?,?)", (h, n)); db.commit()
    return n


# ---- Max-plan backend --------------------------------------------------------------------------
BACKEND = os.environ.get("WP_BACKEND", "api")
_SUB_DIR = pathlib.Path(tempfile.mkdtemp(prefix="llmdream_sub_"))  # empty dir, so no project files reach the CLI
_USAGE_LIMIT_RE = re.compile(r"usage limit|limit reached|out of (extra )?usage|rate.?limit.*(week|session)|resets at", re.I)


def _flatten(messages):
    if len(messages) == 1:
        return messages[0]["content"]
    return "\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in messages)


def _parse_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    return json.loads(m.group(0) if m else text)


def _sub_once(system, prompt, json_schema, timeout, tag=""):
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(MAX_OUTPUT_TOKENS)
    env["CLAUDE_CODE_NO_MODEL_FALLBACK"] = "1"  # a refusal comes back as a refusal, never as another model's answer
    # the system prompt goes through a file: a 130,000-token day is far past the kernel's argument limit
    sp = tempfile.NamedTemporaryFile("w", dir=_SUB_DIR, suffix=".txt", delete=False)
    sp.write(system); sp.close()
    cmd = ["claude", "-p", "--model", MODEL, "--effort", EFFORT, "--system-prompt-file", sp.name,
           "--tools", "", "--setting-sources", "", "--strict-mcp-config", "--no-session-persistence",
           "--output-format", "json"]
    if json_schema is not None:
        cmd += ["--json-schema", json.dumps(json_schema)]
    try:
        return _sub_loop(cmd, prompt, timeout, tag)
    finally:
        os.unlink(sp.name)


def _sub_loop(cmd, prompt, timeout, tag=""):
    env = {k: v for k, v in os.environ.items() if k != "ANTHROPIC_API_KEY"}
    env["CLAUDE_CODE_MAX_OUTPUT_TOKENS"] = str(MAX_OUTPUT_TOKENS)
    env["CLAUDE_CODE_NO_MODEL_FALLBACK"] = "1"  # a refusal comes back as a refusal, never as another model's answer
    for attempt in range(5):
        t0 = time.time()
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, env=env, cwd=_SUB_DIR, timeout=timeout)
        dt = time.time() - t0
        try:
            body = json.loads(p.stdout)
        except Exception:
            body = None
        if body is not None and body.get("stop_reason") == "refusal":
            return body, t0, dt  # Opus 5.5's safety classifier stopped the reply; _call_subscription raises Refusal
        if body is not None and not body.get("is_error"):
            models = list((body.get("modelUsage") or {}).keys())
            if models == [MODEL]:
                return body, t0, dt
            # Claude Code retried an upstream error on another model (seen 4 Oct 2026: claude-opus-5 answered after
            # claude-opus-5-5 failed). The reply never reaches the run; the call is made again.
            mid = f"mismatch_{time.strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:8]}"
            (CALLS_DIR / f"{mid}.json").write_text(json.dumps({"call_id": mid, "tag": tag, "ts": t0, "seconds": dt, "backend": "subscription",
                "request": {"cmd": cmd, "prompt": prompt}, "response": body, "stderr": (p.stderr or "")[-2000:]}, indent=1, default=str))
            log_cost({"call_id": mid, "tag": tag, "provider": "anthropic",
                      "backend": "subscription", "model": ",".join(models), "usd": body.get("total_cost_usd", 0), "error": "MODEL_MISMATCH", "ts": t0})
            err = f"model mismatch: asked {MODEL}, got {models}; reply discarded"
            print(f"[{tag}] {err}, retrying", flush=True)
            if attempt == 4:
                raise RunAborted(err + " five times")
            time.sleep(30 * (attempt + 1)); continue
        err = (p.stdout or "")[-800:] + (p.stderr or "")[-800:]
        if _USAGE_LIMIT_RE.search(err):
            raise UsagePaused(f"claude -p reported a usage limit: {err[-300:]}")
        if attempt == 4:
            raise RunAborted(f"claude -p failed: {err}")
        time.sleep(30 * (attempt + 1))


def _call_subscription(system, messages, *, tag, json_schema=None, timeout=900):
    check_cap()
    check_budget()
    call_id = f"{time.strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:8]}"
    prompt = _flatten(messages)
    body, t0, dt = _sub_once(system, prompt, json_schema, timeout, tag)
    text = body.get("result", "")
    if json_schema is not None:
        so = body.get("structured_output")
        if so is None:
            try:
                so = _parse_json(text)
            except Exception:
                raise RunAborted(f"no structured output from {tag}: {text[:300]}")
        text = json.dumps(so)
    (CALLS_DIR / f"{call_id}.json").write_text(json.dumps(
        {"call_id": call_id, "tag": tag, "ts": t0, "seconds": dt, "backend": "subscription",
         "request": {"system": system, "prompt": prompt, "model": MODEL, "effort": EFFORT, "json_schema": json_schema},
         "response": body}, indent=1, default=str))
    models = list((body.get("modelUsage") or {}).keys())
    if models != [MODEL]:
        log_cost({"call_id": call_id, "tag": tag, "provider": "anthropic", "backend": "subscription",
                  "model": ",".join(models), "usd": body.get("total_cost_usd", 0), "error": "MODEL_MISMATCH", "ts": t0})
        raise RunAborted(f"model mismatch: asked {MODEL}, got {models} (call {call_id})")
    usage = body.get("usage", {})
    usd = body.get("total_cost_usd", 0.0)
    rec = {"call_id": call_id, "tag": tag, "provider": "anthropic", "backend": "subscription", "model": MODEL,
           "ts": t0, "seconds": round(dt, 1), "stop_reason": body.get("stop_reason"),
           "input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0),
           "cache_read": usage.get("cache_read_input_tokens", 0),
           "cache_write": usage.get("cache_creation_input_tokens", 0),
           "usd": round(usd, 6), "usd_basis": "list-price equivalent, billed to the subscription"}
    if body.get("stop_reason") == "refusal":
        rec["error"] = "REFUSAL"; log_cost(rec)
        m = re.search(r"Details:\s*`?\[([a-z_, ]+)\]", text)
        raise Refusal(call_id, m.group(1) if m else "refusal", text[:300])
    log_cost(rec)
    return {"text": text, "thinking": "", "usage": usage, "usd": usd, "call_id": call_id,
            "stop_reason": body.get("stop_reason"), "model": MODEL, "seconds": dt}


def call(system, messages, *, tag, max_tokens=4000, cache_system=True, json_schema=None, timeout=900):
    """
    One Opus 5.5 call. `tag` is a short label (arm/seed/day/step) written into the log.
    Returns dict: text, thinking, usage, usd, call_id, stop_reason, model, seconds.
    Raises Refusal on stop_reason == refusal, RunAborted on model mismatch or spend cap, UsagePaused on the budget.
    """
    if BACKEND == "subscription":
        return _call_subscription(system, messages, tag=tag, json_schema=json_schema, timeout=timeout)
    check_cap()
    call_id = f"{time.strftime('%Y%m%dT%H%M%S')}_{uuid.uuid4().hex[:8]}"
    sys_blocks = [{"type": "text", "text": system}]
    if cache_system:
        sys_blocks[0]["cache_control"] = {"type": "ephemeral"}
    req = dict(
        model=MODEL,
        max_tokens=max_tokens,
        system=sys_blocks,
        messages=messages,
        thinking={"type": "adaptive", "display": "summarized"},
        output_config={"effort": EFFORT},
    )
    if json_schema is not None:
        req["output_config"]["format"] = {"type": "json_schema", "schema": json_schema}
    t0 = time.time()
    resp = _client.messages.create(**req)
    dt = time.time() - t0
    body = resp.model_dump()

    (CALLS_DIR / f"{call_id}.json").write_text(json.dumps(
        {"call_id": call_id, "tag": tag, "ts": t0, "seconds": dt, "request": req, "response": body},
        indent=1, default=str))

    if body["model"] != MODEL:
        log_cost({"call_id": call_id, "tag": tag, "provider": "anthropic", "backend": "api", "model": body["model"],
                  "usd": _usd(body["usage"]), "error": "MODEL_MISMATCH", "ts": t0})
        raise RunAborted(f"model mismatch: asked {MODEL}, got {body['model']} (call {call_id})")

    usage = body["usage"]
    usd = _usd(usage)
    thinking = "\n".join(b.get("thinking", "") for b in body["content"] if b["type"] == "thinking")
    text = "".join(b.get("text", "") for b in body["content"] if b["type"] == "text")
    rec = {"call_id": call_id, "tag": tag, "provider": "anthropic", "backend": "api", "model": body["model"],
           "ts": t0, "seconds": round(dt, 1), "stop_reason": body["stop_reason"],
           "input_tokens": usage.get("input_tokens", 0), "output_tokens": usage.get("output_tokens", 0),
           "cache_read": usage.get("cache_read_input_tokens", 0),
           "cache_write": usage.get("cache_creation_input_tokens", 0), "usd": round(usd, 6)}
    if body["stop_reason"] == "refusal":
        sd = body.get("stop_details") or {}
        rec["refusal"] = {"category": sd.get("category"), "explanation": sd.get("explanation")}
        log_cost(rec)
        raise Refusal(call_id, sd.get("category"), sd.get("explanation"))
    log_cost(rec)
    return {"text": text, "thinking": thinking, "usage": usage, "usd": usd, "call_id": call_id,
            "stop_reason": body["stop_reason"], "model": body["model"], "seconds": dt}


# ---- OpenAI (the luna judge, the gpt-4o regrade) ------------------------------------------------
_openai = None


def openai_chat(model, prompt, *, tag, max_completion_tokens=200):
    """One OpenAI chat call, retried on rate limits, logged to cost.jsonl. Returns (text, raw_response)."""
    global _openai
    import openai
    if _openai is None:
        _openai = openai.OpenAI()
    check_cap()
    err = None
    for attempt in range(12):
        try:
            r = _openai.chat.completions.create(model=model, messages=[{"role": "user", "content": prompt}],
                                                n=1, max_completion_tokens=max_completion_tokens)
            break
        except (openai.RateLimitError, openai.APIConnectionError, openai.InternalServerError, openai.APITimeoutError) as e:
            err = f"{type(e).__name__}: {str(e)[:300]}"
            time.sleep(min(60, 2 ** attempt))
    else:
        raise RunAborted(f"openai {model} failed twelve times: {err}")
    u = r.usage
    pin, pout = OPENAI_PRICE.get(model, (2.50, 10.00))
    rec = {"call_id": r.id, "tag": tag, "provider": "openai", "model": r.model, "ts": time.time(),
           "input_tokens": u.prompt_tokens, "output_tokens": u.completion_tokens,
           "usd": (u.prompt_tokens * pin + u.completion_tokens * pout) / 1e6}
    if model.startswith("gpt-5.6-luna"):
        rec["usd_basis"] = "gpt-4o list price as placeholder, luna price unknown"
    log_cost(rec)
    (CALLS_DIR / f"{r.id}.json").write_text(json.dumps({"call_id": r.id, "tag": tag, "provider": "openai",
        "request": {"model": model, "prompt": prompt}, "response": r.model_dump()}, indent=1, default=str))
    return (r.choices[0].message.content or "").strip(), r
