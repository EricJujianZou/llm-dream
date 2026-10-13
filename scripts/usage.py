"""
Record Eric's /usage figure so the harness can pause at the stop point (decisions.md, "Usage pause on the Max plan").
  python scripts/usage.py set 20          # Eric is at 20 percent of the weekly limit right now
  python scripts/usage.py status          # budget left this week at list price
Weekly limit about 1,450 USD list price (measured 4 Oct 2026); stop at 80 percent (70 until 5 Oct evening); resets Thursday 8 Oct 2026.
"""
import sys, json, time, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "harness"))
import api

WEEKLY_USD = 1450.0
STOP_PCT = 62  # 9 Oct 2026 06:00: runs cost about 65 USD list each, not 45; raised to finish the last three under Eric's "do everything in one go"
RESET = datetime.datetime(2026, 10, 15, 0, 0, tzinfo=datetime.timezone(datetime.timedelta(hours=-4)))  # Thursday 15 Oct, EDT


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "set":
        pct = float(sys.argv[2])
        b = {"pct_at_set": pct, "set_ts": time.time(), "weekly_usd": WEEKLY_USD, "stop_pct": STOP_PCT, "reset_ts": RESET.timestamp(),
             "set_at": time.ctime()}
        api.BUDGET_FILE.write_text(json.dumps(b, indent=1))
        print(f"set: {pct} percent at {b['set_at']}; room until {STOP_PCT} percent is {(STOP_PCT-pct)/100*WEEKLY_USD:.0f} USD list price")
    st = api.budget_status()
    if st is None:
        print("no budget set"); return
    allowed, spent, start = st
    print(f"budget this period: {allowed:.0f} USD list price from {time.ctime(start)}; spent {spent:.2f}; left {allowed-spent:.2f}")
    print(f"real money since v2 start: {api.real_spend_v2():.2f} USD of the {api.SPEND_CAP_USD:.0f} USD cap")


if __name__ == "__main__":
    main()
