"""
Build the day-11 false-memory (DRM) word lists from the University of South Florida free-association norms
(Nelson, McEvoy and Schreiber 2004). Writes data/day11/drm_lists.json. Deterministic: no randomness.

How a list is built (decisions.md, "Day-11 lists built", 4 Oct 2026):
- The lure is a USF cue word that is a noun, was never a lure in the published DRM lists we know of (EXCLUDE),
  and has at least 15 normed associates that are not forms of the lure itself.
- The list is the lure's 15 strongest forward associates (the words people said first when given the lure),
  ordered from strongest down, as Roediger and McDermott (1995) did with the Russell and Jenkins norms.
- Lists are ranked by backward associative strength (BAS), the mean probability that each list word calls up
  the lure. BAS is the best known predictor of false recall (Roediger, Watson, McDermott and Gallo 2001).
- The 8 lists with the highest BAS are taken, greedily, so that no word appears in two lists and no lure is
  a word on another list.
- 16 unrelated words are concrete USF cue nouns with no association to or from any lure or list word.

Source: http://w3.usf.edu/FreeAssociation/AppendixA/ (Cue_Target_Pairs.*, merged into usf_appendix_a.csv).
"""
import csv, json, pathlib, collections

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "data" / "raw" / "usf" / "usf_appendix_a.csv"
OUT = ROOT / "data" / "day11" / "drm_lists.json"

N_LISTS, LIST_LEN, N_UNRELATED = 8, 15, 16
# Lures of published DRM lists: Roediger and McDermott 1995 and the 36 lists of Stadler, Roediger and McDermott
# 1999, written from memory, plus a few further lures from Roediger et al 2001 and Gallo and Roediger 2002 that
# Claude recalls. Not checked against the papers; it is a guard, and the BAS ranking below does not depend on it.
EXCLUDE = set("""anger army black bread car chair city cold cup doctor flag foot fruit girl high king lion man mountain
music needle pen river rough rubber shirt sleep slow smell smoke soft spider sweet thief trash window butterfly
lady hot bed baby cat dog house water money boy woman light sky child phone school table""".split())
# left out because the list is mostly violent words, which read oddly in a casual chat and could draw a refusal
CONTENT_EXCLUDE = {"gun"}
import battery  # the serial list and its foils, and v1's lists, are kept out of the new lists


def load():
    rows = list(csv.reader(open(SRC, encoding="utf-8", errors="replace"), skipinitialspace=True))
    h = rows[0]
    ix = {k: h.index(k) for k in ("CUE", "TARGET", "NORMED?", "FSG", "BSG", "QPS", "QCON")}
    fwd = collections.defaultdict(list)
    pos, conc, linked = {}, {}, collections.defaultdict(set)
    for r in rows[1:]:
        if len(r) < len(h) - 2:
            continue
        cue, tgt = r[ix["CUE"]].strip().lower(), r[ix["TARGET"]].strip().lower()
        try:
            fsg = float(r[ix["FSG"]])
        except ValueError:
            continue
        try:
            bsg = float(r[ix["BSG"]])
        except ValueError:
            bsg = None
        pos[cue] = r[ix["QPS"]].strip()
        try:
            conc[cue] = float(r[ix["QCON"]])
        except ValueError:
            pass
        linked[cue].add(tgt); linked[tgt].add(cue)
        if r[ix["NORMED?"]].strip() == "YES" and bsg is not None:
            fwd[cue].append((tgt, fsg, bsg))
    return fwd, pos, conc, linked


def variant(a, b):
    """True if b looks like a form of a (sleep / sleepy / asleep)."""
    k = min(len(a), len(b), 5)
    return a[:k] == b[:k] or a in b or b in a


def build():
    fwd, pos, conc, linked = load()
    other = set(battery.SERIAL + battery.SERIAL_FOILS + battery.DRM_V1_UNRELATED) | {w for k, v in battery.DRM_V1.items() for w in [k] + v}
    other |= {w for st in battery._cao_lists()[0] for w in battery.pair_of(st)}  # Cao's people and places
    cands = []
    for lure, assoc in fwd.items():
        if lure in EXCLUDE or lure in CONTENT_EXCLUDE or lure in other or pos.get(lure) != "N" or not lure.isalpha() or len(lure) < 3:
            continue
        words = [(t, f, b) for t, f, b in sorted(assoc, key=lambda x: -x[1])
                 if t.isalpha() and not variant(lure, t) and t not in other and t not in EXCLUDE]
        if len(words) < LIST_LEN:
            continue
        words = words[:LIST_LEN]
        bas = sum(b for _, _, b in words) / LIST_LEN
        cands.append({"lure": lure, "words": [t for t, _, _ in words], "fsg": [round(f, 3) for _, f, _ in words],
                      "bsg": [round(b, 3) for _, _, b in words], "bas": round(bas, 4)})
    cands.sort(key=lambda c: -c["bas"])
    chosen, used = [], set()
    for c in cands:
        ws = set(c["words"])
        if c["lure"] in used or ws & used or any(x["lure"] in ws for x in chosen):
            continue
        chosen.append(c); used |= ws | {c["lure"]}
        if len(chosen) == N_LISTS:
            break
    lures = {c["lure"] for c in chosen}
    # unrelated words: concrete nouns (USF concreteness 5 or more on its 1-7 scale) that are USF cues, linked to nothing chosen, picked in alphabetical order at a fixed stride
    pool = sorted(w for w in fwd if pos.get(w) == "N" and conc.get(w, 0) >= 5 and w.isalpha() and 4 <= len(w) <= 8
                  and w not in used and w not in other and w not in EXCLUDE and not (linked[w] & used))
    stride = len(pool) // N_UNRELATED
    unrelated = [pool[i * stride + stride // 2] for i in range(N_UNRELATED)]
    return {"source": "USF free-association norms, Nelson, McEvoy and Schreiber 2004, http://w3.usf.edu/FreeAssociation/AppendixA/",
            "method": __doc__.strip(), "n_candidates": len(cands), "lists": chosen, "unrelated": unrelated,
            "excluded_lures": sorted(EXCLUDE)}


if __name__ == "__main__":
    out = build()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1))
    for c in out["lists"]:
        print(f"{c['lure']:>10} BAS {c['bas']:.3f}: {', '.join(c['words'])}")
    print("unrelated:", ", ".join(out["unrelated"]), f"({out['n_candidates']} candidate lures)")
