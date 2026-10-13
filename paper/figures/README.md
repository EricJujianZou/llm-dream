# Paper figures

Built by `paper/make_figures.py` from `results/summary_v2.json` (`runs.<arm>_s<seed>`, seeds 0 to 2). Each figure exists as .pdf, .svg and a 200 dpi .png preview.

- fig_dose: final-day recall (%) against corrupted turns (0, 5, 10, 20, 40 %) for structured and random noise, both starting at faithful replay, with seed marks, means and a dashed no sleep line. Keys: `final_acc`, `rate`, `family`.
- fig_arms: final-day recall (%) per arm, three seed marks and the mean, vertical rule at the faithful replay mean. Key: `final_acc`.
- fig_novel: multi-session recall (%) per arm, same layout as fig_arms. Key: `final_acc_novel`.
- fig_transfer: percent of 12 rules followed per arm, near probe filled and far probe hollow, seed means. Keys: `transfer.near`, `transfer.far`.
- fig_cap: memory size in thousand tokens after nights 1 to 10 for the cap, no sleep, faithful replay and structured 40 %, seed means. Keys: `memory_tokens_by_night` (first 10 entries); cap values typed in, matching `cap_by_night`.
- fig_delay: heatmap of final-day recall (%) per arm by nights since the question's last evidence (1 to 10), seed means. Key: `final_acc_by_delay`.
- fig_drop: points of recall lost over one night per arm, seed marks and mean, rule at faithful replay. Key: `one_night_drop`.
