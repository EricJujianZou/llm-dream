"""Build the paper figures from results/summary_v2.json."""
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import font_manager
for _f in ("Regular", "Bold"):
    _p = f"/usr/share/fonts/truetype/liberation/LiberationSans-{_f}.ttf"
    if Path(_p).exists():
        font_manager.fontManager.addfont(_p)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "paper" / "figures"
D = json.load(open(ROOT / "results" / "summary_v2.json"))
RUNS = D["runs"]
SEEDS = D["seeds"]

STRUCT, RAND = "#2f63a6", "#d9783a"
GRAY, BLACK, INK2, RULE = "#8a8985", "#0b0b0b", "#52514e", "#bdbcb8"
RATES = [5, 10, 20, 40]
ARMS = (["nosleep", "faithful"] + [f"structured_{r:02d}" for r in RATES]
        + [f"random_{r:02d}" for r in RATES])
LABEL = {"nosleep": "No sleep", "faithful": "Faithful replay",
         **{f"structured_{r:02d}": f"Structured {r}%" for r in RATES},
         **{f"random_{r:02d}": f"Random {r}%" for r in RATES}}

def style(a):
    if a == "nosleep": return GRAY, "s"
    if a == "faithful": return BLACK, "o"
    if a.startswith("structured"): return STRUCT, "o"
    return RAND, "^"

plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Liberation Sans", "DejaVu Sans"],
    "font.size": 9, "axes.labelsize": 9, "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
    "axes.edgecolor": INK2, "axes.labelcolor": BLACK, "xtick.color": INK2, "ytick.color": INK2,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "axes.spines.top": False, "axes.spines.right": False,
    "svg.fonttype": "none", "pdf.fonttype": 42, "savefig.dpi": 200,
})

def vals(arm, key):
    out = []
    for s in SEEDS:
        v = RUNS[f"{arm}_s{s}"]
        for k in key.split("."):
            v = v[k]
        out.append(100 * v)
    return np.array(out)

def save(fig, name):
    for ext in ("pdf", "svg", "png"):
        fig.savefig(OUT / f"{name}.{ext}", bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)

def dotplot(key, name, xlabel, rule_at_faithful=True, xlim=None):
    fig, ax = plt.subplots(figsize=(3.4, 2.9))
    y = np.arange(len(ARMS))[::-1]
    if rule_at_faithful:
        ax.axvline(vals("faithful", key).mean(), color=RULE, lw=0.8, zorder=0)
    for yi, a in zip(y, ARMS):
        c, m = style(a)
        v = vals(a, key)
        ax.scatter(v, [yi] * len(v), clip_on=False, s=12, marker=m, facecolor="white", edgecolor=c, lw=0.8, zorder=2)
        ax.scatter([v.mean()], [yi], clip_on=False, s=42, marker=m, color=c, edgecolor="white", lw=0.8, zorder=3)
    ax.set_yticks(y, [LABEL[a] for a in ARMS])
    ax.tick_params(axis="y", length=0, pad=8)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel(xlabel)
    if xlim: ax.set_xlim(*xlim)
    ax.set_ylim(-0.6, len(ARMS) - 0.4)
    save(fig, name)

# 1. dose response
fig, ax = plt.subplots(figsize=(5, 3.0))
xs = [0] + RATES
ns = vals("nosleep", "final_acc").mean()
ax.axhline(ns, color=GRAY, lw=1, ls=(0, (4, 3)), zorder=0)
ax.text(42, ns, "No sleep", color=INK2, va="center", ha="left", fontsize=8.5)
ends = {}
for fam, c, m, off in (("structured", STRUCT, "o", -0.6), ("random", RAND, "^", 0.6)):
    arms = ["faithful"] + [f"{fam}_{r:02d}" for r in RATES]
    means = []
    for x, a in zip(xs, arms):
        v = vals(a, "final_acc")
        if a == "faithful":
            means.append(v.mean()); continue
        xo = x if a == "faithful" else x + off
        ax.scatter([xo] * len(v), v, s=10, marker=m, facecolor="white", edgecolor=c, lw=0.7, zorder=2)
        means.append(v.mean())
    ax.plot([x + (0 if i == 0 else off) for i, x in enumerate(xs)], means, color=c, lw=1.6, zorder=3)
    ax.scatter([x + (0 if i == 0 else off) for i, x in enumerate(xs)], means, s=40, marker=m, color=c,
               edgecolor="white", lw=0.8, zorder=4)
    ends[fam] = means[-1]
fv = vals("faithful", "final_acc")
ax.scatter([0] * len(fv), fv, s=10, marker="o", facecolor="white", edgecolor=BLACK, lw=0.7, zorder=2)
ax.scatter([0], [fv.mean()], s=44, marker="o", color=BLACK, edgecolor="white", lw=0.8, zorder=5)
# right-end labels, nudged apart if close
ys, yr = ends["structured"], ends["random"]
if abs(ys - yr) < 3.5:
    mid = (ys + yr) / 2; ys, yr = (mid - 1.8, mid + 1.8) if ys < yr else (mid + 1.8, mid - 1.8)
ax.text(42, ys, "Structured noise", color=STRUCT, va="center", fontsize=8.5)
ax.text(42, yr, "Random noise", color=RAND, va="center", fontsize=8.5)
ax.set_xticks(xs, [f"{x}" for x in xs])
ax.set_xlim(-2, 41)
ax.set_xlabel("Corrupted turns (%)")
ax.set_ylabel("Final-day recall (%)")
ax.text(0.8, fv.mean() - 13, "Faithful replay", fontsize=8, color=INK2, ha="left")
ax.set_ylim(0, 90)
save(fig, "fig_dose")

# 2, 3 dot plots
dotplot("final_acc", "fig_arms", "Final-day recall (%)", xlim=(0, 100))
dotplot("final_acc_novel", "fig_novel", "Multi-session recall (%)", xlim=(0, 100))

# 4. transfer
fig, ax = plt.subplots(figsize=(3.4, 2.9))
y = np.arange(len(ARMS))[::-1]
for yi, a in zip(y, ARMS):
    c, m = style(a)
    n, f = vals(a, "transfer.near").mean(), vals(a, "transfer.far").mean()
    ax.plot([f, n], [yi, yi], color=c, lw=1, zorder=1)
    ax.scatter([n], [yi], s=34, marker=m, color=c, zorder=4, clip_on=False)
    ax.scatter([f], [yi], s=34, marker=m, facecolor="white", edgecolor=c, lw=1, zorder=3, clip_on=False)
ax.set_yticks(y, [LABEL[a] for a in ARMS]); ax.tick_params(axis="y", length=0, pad=8)
ax.spines["left"].set_visible(False)
ax.set_xlabel("Rules followed, of 12 (%)")
ax.set_xlim(0, 100)
ax.set_ylim(-0.6, len(ARMS) + 0.6)
ax.scatter([], [], s=30, marker="o", color=INK2, label="Near probe")
ax.scatter([], [], s=30, marker="o", facecolor="white", edgecolor=INK2, label="Far probe")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, 1.02), ncol=2, frameon=False, fontsize=8,
          handletextpad=0.2, columnspacing=1.2)
save(fig, "fig_transfer")

# 5. memory tokens vs cap
CAP = [19500, 35100, 48100, 59800, 70850, 81250, 91000, 100100, 108550, 117000]
nights = np.arange(1, 11)
fig, ax = plt.subplots(figsize=(5, 3.0))
ax.plot(nights, np.array(CAP) / 1000, color=BLACK, lw=1, ls=(0, (4, 3)), label="Cap")
series = [("nosleep", "No sleep"), ("faithful", "Faithful replay"), ("structured_40", "Structured 40%")]
for a, name in series:
    c, m = style(a)
    t = np.array([[RUNS[f"{a}_s{s}"]["memory_tokens_by_night"][i] for i in range(10)] for s in SEEDS]) / 1000
    ax.plot(nights, t.mean(0), color=c, lw=1.6, marker=m, ms=4, mec="white", mew=0.6, label=name)
ax.legend(loc="upper left", frameon=False, fontsize=8.5, handlelength=2.4)
ax.set_xticks(nights); ax.set_xlim(0.7, 10.2)
ax.set_xlabel("Night"); ax.set_ylabel("Memory size (thousand tokens)")
ax.set_ylim(0, None)
save(fig, "fig_cap")

# 6. delay heatmap
M = np.full((len(ARMS), 10), np.nan)
for i, a in enumerate(ARMS):
    for j, dl in enumerate(range(1, 11)):
        v = [RUNS[f"{a}_s{s}"]["final_acc_by_delay"].get(str(dl)) for s in SEEDS]
        v = [x for x in v if x is not None]
        if v: M[i, j] = 100 * np.mean(v)
cmap = LinearSegmentedColormap.from_list("blue", ["#f4f8fd", "#cde2fb", "#86b6ef", "#3987e5", "#1c5cab", "#0d366b"])
fig, ax = plt.subplots(figsize=(5, 3.3))
ax.imshow(M, cmap=cmap, vmin=0, vmax=100, aspect="auto")
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        if not np.isnan(M[i, j]):
            ax.text(j, i, f"{M[i, j]:.0f}", ha="center", va="center", fontsize=7.5,
                    color="white" if M[i, j] >= 45 else BLACK)
ax.set_xticks(range(10), [str(d) for d in range(1, 11)])
ax.set_yticks(range(len(ARMS)), [LABEL[a] for a in ARMS])
ax.set_xlabel("Nights since the question's last evidence")
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
ax.set_xticks(np.arange(-.5, 10, 1), minor=True); ax.set_yticks(np.arange(-.5, len(ARMS), 1), minor=True)
ax.grid(which="minor", color="white", lw=1.5); ax.tick_params(which="minor", length=0)
save(fig, "fig_delay")

# 7. one night drop
dotplot("one_night_drop", "fig_drop", "Points lost over one night", xlim=(0, 30))

print("nan cells in delay heatmap:", int(np.isnan(M).sum()))
print("dose means:", {a: round(vals(a, 'final_acc').mean(), 1) for a in ARMS})
