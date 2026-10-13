"""Render data/transfer_v2/transfer_s*.json into results/transfer_preview.md for Eric to read before the sweep
(spec-v2.md, transfer test: Eric reads about 10 rules). Rerun after each seed's build."""
import json, glob, pathlib, time
ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    L = ["# Transfer test preview", "",
         f"Written {time.strftime('%d %B %Y %H:%M %Z')} from data/transfer_v2/transfer_s<seed>.json. Each life has 12 hidden rules about how its user wants help. "
         "Each rule shows up as 2 or 3 short chats (episodes) on different days, mixed into the day's LongMemEval sessions, never stated outright. "
         "After night 10 the agent gets one near probe (a request like the episodes) and one far probe (a different kind of request where the rule still applies). "
         "The judges mark a reply as following the rule when it matches the 'follows if' line. The empty-memory rate is how often an agent with no memory followed the rule anyway, over 6 samples; rules at 20 percent or more were replaced.", ""]
    for p in sorted(glob.glob(str(ROOT / "data" / "transfer_v2" / "transfer_s*.json"))):
        t = json.load(open(p))
        L += [f"## Seed {t['seed']}", "",
              f"Built {t['built']} by {t['model']}. {t['check']['candidates_checked']} candidate rules checked against an empty memory, {t['check']['replaced']} replaced. "
              f"Episode tokens per day: {t['episode_tokens_by_day']} (reserve {t['episode_reserve']:,}).", "",
              "| rule | episodes on days | empty-memory rate (luna / Opus) | the rule |", "|---|---|---|---|"]
        for r in t["rules"]:
            L.append(f"| {r['rule_id']} | {', '.join(str(e['day']) for e in r['episodes'])} | {r['empty_memory']['rate_main']:.2f} / {r['empty_memory']['rate_opus']:.2f} | {r['rule']} |")
        L.append("")
        for r in t["rules"]:
            L += [f"### {r['rule_id']}", "", f"**Rule.** {r['rule']}", "", f"**What the model does by default.** {r['default_behaviour']}", ""]
            for e in r["episodes"]:
                L.append(f"**Episode {e['index']}, day {e['day']}** ({e['tokens']} tokens)")
                L.append("")
                for turn in e["turns"]:
                    who = "User" if turn["role"] == "user" else "Assistant"
                    L.append(f"> **{who}:** " + turn["content"].replace("\n", "\n> "))
                    L.append(">")
                L[-1] = ""
            for kind in ("near", "far"):
                pr = r[f"{kind}_probe"]
                L += [f"**{kind.capitalize()} probe.** {pr['text']}", "", f"*Follows if:* {pr['follows_if']}", ""]
    out = ROOT / "results" / "transfer_preview.md"
    out.write_text("\n".join(L))
    print(f"wrote {out} ({len(L)} lines, seeds {[int(pathlib.Path(p).stem[-1]) for p in sorted(glob.glob(str(ROOT / 'data' / 'transfer_v2' / 'transfer_s*.json')))]})")


if __name__ == "__main__":
    main()
