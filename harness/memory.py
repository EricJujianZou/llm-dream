"""
v2 item memory (decisions.md, "How the memory stays under the cap", 4 Oct 2026).

The memory is a list of items. Each item has an id, a one-line gist, its details, an importance score 1 to 5,
and the night it was last written. The sleep step returns a delta (add, update, merge). When the rendered
memory is over the night's cap, details are stripped from the lowest-scored items first (least recently
updated first among ties, then oldest id); the last item stripped is cut at a sentence boundary; whole items
are deleted only when every item is already down to its gist. Tokens are Claude tokens (api.count_tokens).
"""
import re
import api

SENT_RE = re.compile(r"(?<=[.!?])\s+")


def render_for_agent(items):
    """What the assistant reads in its system prompt. Gist, then details indented, no ids or scores."""
    out = []
    for it in items:
        out.append(f"- {it['gist']}")
        if it.get("details"):
            out.append(f"  {it['details']}")
    return "\n".join(out)


def render_for_sleep(items):
    """What the sleep step reads: ids, scores and the night last written, so it can update and merge."""
    out = []
    for it in items:
        out.append(f"[{it['id']}] score {it['score']}, written night {it['night'] + 1}")
        out.append(f"  gist: {it['gist']}")
        if it.get("details"):
            out.append(f"  details: {it['details']}")
    return "\n".join(out)


def tokens(items):
    return api.count_tokens(render_for_agent(items))


def _item_tokens(it):
    # per-item estimate from the two pieces; exact total is checked with one count of the rendering
    return api.count_tokens(f"- {it['gist']}") + (api.count_tokens(f"  {it['details']}") + 1 if it.get("details") else 0) + 1


def _clamp_score(s):
    try:
        return max(1, min(5, int(round(float(s)))))
    except Exception:
        return 3


def apply_delta(items, delta, night, next_id):
    """Apply {add, update, merge} to a copy of items. Returns (items, next_id, report)."""
    by_id = {it["id"]: dict(it) for it in items}
    order = [it["id"] for it in items]
    rep = {"added": 0, "updated": 0, "merged_groups": 0, "merged_away": 0, "unknown_ids": 0, "dropped_empty": 0}

    def clean(d):
        g = re.sub(r"\s+", " ", str(d.get("gist", "") or "")).strip()
        det = re.sub(r"\s+", " ", str(d.get("details", "") or "")).strip()
        return g, det

    for d in delta.get("update", []) or []:
        g, det = clean(d)
        if not g:
            rep["dropped_empty"] += 1; continue
        i = str(d.get("id", ""))
        if i in by_id:
            by_id[i].update(gist=g, details=det, score=_clamp_score(d.get("score", by_id[i]["score"])), night=night)
            rep["updated"] += 1
        else:
            rep["unknown_ids"] += 1
            nid = f"m{next_id}"; next_id += 1
            by_id[nid] = {"id": nid, "gist": g, "details": det, "score": _clamp_score(d.get("score", 3)), "night": night, "born": night}
            order.append(nid); rep["added"] += 1
    for d in delta.get("merge", []) or []:
        g, det = clean(d)
        if not g:
            rep["dropped_empty"] += 1; continue
        ids = [str(x) for x in (d.get("ids") or []) if str(x) in by_id]
        rep["unknown_ids"] += len(d.get("ids") or []) - len(ids)
        nid = f"m{next_id}"; next_id += 1
        born = min([by_id[x]["born"] for x in ids] + [night])
        by_id[nid] = {"id": nid, "gist": g, "details": det, "score": _clamp_score(d.get("score", 3)), "night": night, "born": born}
        # the merged item takes the slot of the first source so the list keeps its order
        if ids:
            pos = order.index(ids[0]); order[pos] = nid
            for x in ids:
                by_id.pop(x, None)
            order = [o for o in order if o in by_id]
            rep["merged_groups"] += 1; rep["merged_away"] += len(ids)
        else:
            order.append(nid); rep["added"] += 1
    for d in delta.get("add", []) or []:
        g, det = clean(d)
        if not g:
            rep["dropped_empty"] += 1; continue
        nid = f"m{next_id}"; next_id += 1
        by_id[nid] = {"id": nid, "gist": g, "details": det, "score": _clamp_score(d.get("score", 3)), "night": night, "born": night}
        order.append(nid); rep["added"] += 1
    return [by_id[i] for i in order], next_id, rep


def _strip_order(items):
    # lowest score first, least recently written first among ties, then oldest id
    return sorted(items, key=lambda it: (it["score"], it["night"], int(it["id"][1:])))


def _cut_details_to(details, budget_tokens):
    """Longest run of leading sentences whose token count fits the budget. Empty when none fits."""
    sents = SENT_RE.split(details)
    kept = ""
    for s in sents:
        cand = (kept + " " + s).strip()
        if api.count_tokens(f"  {cand}") + 1 > budget_tokens:
            break
        kept = cand
    return kept


def enforce_cap(items, cap):
    """Strip details, then delete whole items, until the agent-facing rendering is at most cap tokens.
    Returns (items, report). Items are modified in place (copies are the caller's job)."""
    rep = {"cap": cap, "tokens_before": tokens(items), "details_stripped": 0, "details_partial": 0,
           "items_deleted": 0, "items_before": len(items)}
    total = rep["tokens_before"]
    if total <= cap:
        rep["tokens_after"] = total; rep["items_after"] = len(items)
        return items, rep
    # pass 1: strip details, lowest score first
    for it in _strip_order(items):
        if not it.get("details"):
            continue
        over = total - cap
        det_tokens = api.count_tokens(f"  {it['details']}") + 1
        if det_tokens > over:
            # this is the last item to touch: keep the leading sentences that fit
            kept = _cut_details_to(it["details"], det_tokens - over)
            it["details"] = kept
            rep["details_partial"] += 1 if kept else 0
            rep["details_stripped"] += 0 if kept else 1
        else:
            it["details"] = ""
            rep["details_stripped"] += 1
        total = tokens(items)
        if total <= cap:
            break
    # pass 2: whole items, only when everything is already gist-only
    if total > cap and all(not it.get("details") for it in items):
        for it in _strip_order(items):
            items.remove(it)
            rep["items_deleted"] += 1
            total = tokens(items)
            if total <= cap:
                break
    elif total > cap:
        # a partial cut left us slightly over (sentence splitting is approximate): strip the next details
        for it in _strip_order(items):
            if not it.get("details"):
                continue
            it["details"] = ""; rep["details_stripped"] += 1
            total = tokens(items)
            if total <= cap:
                break
    rep["tokens_after"] = total; rep["items_after"] = len(items)
    return items, rep


def summary_line(items):
    return f"{len(items)} items, {sum(1 for i in items if i.get('details'))} with details"
