# Results: noisy replay at four doses

Generated 09 October 2026 12:17 UTC. Model under test claude-opus-5-5, effort medium, through Claude Code on the Max plan. Days of 130,000 tokens; the memory cap grows each night (19,500, 35,100, 48,100, 59,800, 70,850, 81,250, 91,000, 100,100, 108,550, 117,000 tokens). Ten days, ten arms, three seeds.

## One-screen summary

**What ran.** 30 of 30 runs finished (ten arms x three seeds). Each run: ten days of about 30 LongMemEval sessions plus the transfer-test episodes, one night step per day, 100 memory questions asked before sleep, after sleep and at the end, 24 transfer probes after night 10, then an eleventh day with the memory-effects battery. Spend: 1991.17 USD list price on the Max plan over 20323 Opus calls (no money), 11.69 USD on OpenAI over 15733 judge calls.

**Judges.** gpt-5.6-luna grades every answer, Opus 5.5 grades it again. They agree on 94 percent of 8,040 graded answers (512 disagreements). Numbers below are luna's unless marked.

**The one number.** Final-day recall, structured noise at 20 percent minus faithful replay, mean over seeds: **-7 ± 7 points** (per seed: [-13, 0, -8]). Verdict: noisy arm lower, and the difference clears the seed spread.

Novel tasks (multi-session questions), same difference: -12 ± 10 points, noisy arm lower, and the difference clears the seed spread. Far transfer probes, same difference: -8 ± 8 points, noisy arm lower, and the difference clears the seed spread. DRM critical-lure false alarms after sleep, same difference: 0 ± 0 points, no result, the difference is inside the seed spread.

## Claim

An agent whose nightly replay is corrupted on purpose recalls as much on the last day as an agent with faithful replay, and does better on situations it has never seen (Hoel's overfitted brain hypothesis, tested on a text-memory LLM agent). v2 tests it at four corruption rates, with structured and random noise side by side, and with a transfer test built for it.

## Method in brief

Ten arms share one model, one life per seed, one agent prompt and one question schedule. Only the night step differs. No sleep keeps a raw window of the day's last turns, sized to the night's cap. Faithful replay has the model rewrite its memory from the day's transcript: the memory is a list of items with a gist line, details and a score from 1 to 5, and when it is over the cap the harness strips details from the lowest-scored items first and deletes whole items only when every item is down to its gist. Structured noise swaps, changes or splices 5, 10, 20 or 40 percent of the day's turns from earlier days before the same rewrite; random noise replaces or salts the same share of turns with text from an unrelated corpus. Days are about 30 LongMemEval sessions stitched to 130,000 tokens, with 12 hidden counter-default rules planted as 2 or 3 episodes each across the ten days. After night 10 each rule gets one near probe and one far probe. Day eleven is a Cao-style memory battery with new DRM lists from the USF association norms. Full detail in spec-v2.md and decisions.md.

## Numbers, mean ± sd over three seeds (percent)

| arm | evening (before sleep) | morning (after sleep) | one-night drop | final recall | final, days 1-5 | final, days 6-10 | final, novel (multi-session) | final, abstention | memory tokens, mean over nights |
|---|---|---|---|---|---|---|---|---|---|
| No sleep (raw window at the cap) | 74 ± 1 | 48 ± 2 | 26 ± 1 | 14 ± 4 | 14 ± 5 | 15 ± 7 | 0 ± 0 | 96 ± 7 | 76,442 ± 25 |
| Faithful replay | 94 ± 1 | 87 ± 1 | 8 ± 2 | 76 ± 5 | 76 ± 19 | 76 ± 4 | 71 ± 7 | 96 ± 4 | 72,176 ± 4,410 |
| Structured noise, 5 percent | 91 ± 2 | 83 ± 2 | 8 ± 2 | 76 ± 5 | 78 ± 15 | 76 ± 5 | 67 ± 9 | 98 ± 4 | 71,232 ± 3,770 |
| Structured noise, 10 percent | 90 ± 2 | 77 ± 3 | 13 ± 1 | 71 ± 2 | 67 ± 5 | 72 ± 6 | 61 ± 5 | 94 ± 6 | 74,815 ± 1,770 |
| Structured noise, 20 percent | 88 ± 2 | 73 ± 5 | 16 ± 4 | 69 ± 2 | 71 ± 4 | 68 ± 6 | 59 ± 5 | 98 ± 4 | 74,551 ± 1,789 |
| Structured noise, 40 percent | 87 ± 2 | 66 ± 1 | 21 ± 2 | 60 ± 4 | 64 ± 11 | 57 ± 6 | 45 ± 5 | 94 ± 6 | 69,872 ± 78 |
| Random noise, 5 percent | 94 ± 3 | 84 ± 2 | 10 ± 5 | 78 ± 4 | 76 ± 18 | 78 ± 5 | 76 ± 3 | 92 ± 4 | 73,946 ± 2,591 |
| Random noise, 10 percent | 94 ± 1 | 83 ± 1 | 10 ± 2 | 77 ± 5 | 76 ± 18 | 77 ± 3 | 74 ± 13 | 96 ± 4 | 73,996 ± 2,754 |
| Random noise, 20 percent | 92 ± 4 | 78 ± 4 | 14 ± 1 | 70 ± 5 | 68 ± 6 | 71 ± 5 | 61 ± 17 | 96 ± 4 | 72,782 ± 3,560 |
| Random noise, 40 percent | 91 ± 5 | 77 ± 4 | 14 ± 3 | 76 ± 3 | 76 ± 15 | 75 ± 3 | 73 ± 12 | 96 ± 7 | 70,584 ± 4,440 |

Paired differences against faithful replay, same seed (percentage points):

| comparison | final recall | final, novel | one-night drop | abstention | transfer near | transfer far |
|---|---|---|---|---|---|---|
| No sleep (raw window at the cap) minus faithful | -62 ± 1 | -71 ± 7 | 18 ± 2 | 0 ± 6 | -56 ± 13 | -44 ± 13 |
| Structured noise, 5 percent minus faithful | 0 ± 6 | -5 ± 16 | 1 ± 2 | 2 ± 4 | -6 ± 25 | -11 ± 5 |
| Structured noise, 10 percent minus faithful | -6 ± 7 | -11 ± 3 | 6 ± 2 | -2 ± 4 | -6 ± 10 | -14 ± 10 |
| Structured noise, 20 percent minus faithful | -7 ± 7 | -12 ± 10 | 8 ± 5 | 2 ± 4 | -3 ± 13 | -8 ± 8 |
| Structured noise, 40 percent minus faithful | -17 ± 5 | -26 ± 11 | 13 ± 4 | -2 ± 4 | 0 ± 14 | -11 ± 5 |
| Random noise, 5 percent minus faithful | 2 ± 1 | 5 ± 8 | 2 ± 4 | -4 ± 4 | -3 ± 5 | -11 ± 5 |
| Random noise, 10 percent minus faithful | 1 ± 6 | 3 ± 16 | 3 ± 1 | 0 ± 6 | -3 ± 5 | -11 ± 13 |
| Random noise, 20 percent minus faithful | -6 ± 7 | -11 ± 19 | 6 ± 2 | 0 ± 6 | -11 ± 25 | -14 ± 5 |
| Random noise, 40 percent minus faithful | -0 ± 2 | 2 ± 14 | 7 ± 1 | 0 ± 6 | -11 ± 5 | -17 ± 17 |

## Corruption-rate curve

Faithful replay is the 0 percent point of both curves. Each cell is mean ± sd over seeds (percent).

| rate | structured: final recall | structured: novel | structured: far transfer | random: final recall | random: novel | random: far transfer |
|---|---|---|---|---|---|---|
| 0 percent | 76 ± 5 | 71 ± 7 | 53 ± 17 | 76 ± 5 | 71 ± 7 | 53 ± 17 |
| 5 percent | 76 ± 5 | 67 ± 9 | 42 ± 17 | 78 ± 4 | 76 ± 3 | 42 ± 14 |
| 10 percent | 71 ± 2 | 61 ± 5 | 39 ± 27 | 77 ± 5 | 74 ± 13 | 42 ± 22 |
| 20 percent | 69 ± 2 | 59 ± 5 | 44 ± 25 | 70 ± 5 | 61 ± 17 | 39 ± 21 |
| 40 percent | 60 ± 4 | 45 ± 5 | 42 ± 17 | 76 ± 3 | 73 ± 12 | 36 ± 21 |

## Final recall by delay

Final-day recall of questions whose last evidence was N nights before the final questions (percent, mean over seeds; sd omitted, each cell rests on 4 to 21 questions per life).

| arm | 1 night | 2 nights | 3 nights | 4 nights | 5 nights | 6 nights | 7 nights | 8 nights | 9 nights | 10 nights |
|---|---|---|---|---|---|---|---|---|---|---|
| No sleep (raw window at the cap) | 50 | 3 | 2 | 8 | 0 | 10 | 28 | 10 | 6 | 11 |
| Faithful replay | 79 | 81 | 81 | 59 | 80 | 77 | 64 | 69 | 89 | 78 |
| Structured noise, 5 percent | 72 | 81 | 81 | 60 | 85 | 78 | 61 | 77 | 78 | 94 |
| Structured noise, 10 percent | 60 | 81 | 81 | 59 | 76 | 71 | 68 | 58 | 72 | 69 |
| Structured noise, 20 percent | 73 | 68 | 67 | 67 | 63 | 69 | 77 | 63 | 75 | 81 |
| Structured noise, 40 percent | 63 | 62 | 54 | 38 | 71 | 55 | 89 | 59 | 56 | 61 |
| Random noise, 5 percent | 83 | 81 | 78 | 67 | 73 | 73 | 85 | 68 | 83 | 81 |
| Random noise, 10 percent | 80 | 74 | 81 | 63 | 88 | 83 | 85 | 60 | 61 | 69 |
| Random noise, 20 percent | 70 | 77 | 78 | 55 | 66 | 71 | 66 | 52 | 81 | 83 |
| Random noise, 40 percent | 67 | 78 | 86 | 63 | 80 | 71 | 73 | 57 | 92 | 94 |

## Transfer test

Share of the 12 hidden rules the agent followed on a probe after night 10 (percent, mean ± sd over seeds). Near probes resemble the planted episodes; far probes apply the rule in a different kind of request. Hoel predicts the noisy arms lose less from near to far.

| arm | near (luna) | far (luna) | near minus far | near (Opus) | far (Opus) | rules with 2 episodes | rules with 3 episodes |
|---|---|---|---|---|---|---|---|
| No sleep (raw window at the cap) | 8 ± 8 | 8 ± 14 | -0 ± 17 | 6 ± 5 | 11 ± 13 | 14 ± 13 | 3 ± 5 |
| Faithful replay | 64 ± 21 | 53 ± 17 | 11 ± 13 | 69 ± 13 | 50 ± 25 | 58 ± 22 | 58 ± 14 |
| Structured noise, 5 percent | 58 ± 8 | 42 ± 17 | 17 ± 14 | 58 ± 0 | 42 ± 30 | 58 ± 8 | 42 ± 14 |
| Structured noise, 10 percent | 58 ± 14 | 39 ± 27 | 19 ± 13 | 53 ± 13 | 36 ± 21 | 47 ± 19 | 50 ± 22 |
| Structured noise, 20 percent | 61 ± 17 | 44 ± 25 | 17 ± 8 | 64 ± 5 | 53 ± 32 | 56 ± 27 | 50 ± 17 |
| Structured noise, 40 percent | 64 ± 10 | 42 ± 17 | 22 ± 19 | 64 ± 10 | 42 ± 17 | 53 ± 5 | 53 ± 17 |
| Random noise, 5 percent | 61 ± 21 | 42 ± 14 | 19 ± 13 | 64 ± 24 | 42 ± 14 | 53 ± 27 | 50 ± 17 |
| Random noise, 10 percent | 61 ± 17 | 42 ± 22 | 19 ± 21 | 61 ± 19 | 42 ± 30 | 56 ± 19 | 47 ± 17 |
| Random noise, 20 percent | 53 ± 5 | 39 ± 21 | 14 ± 25 | 44 ± 25 | 44 ± 21 | 50 ± 22 | 42 ± 25 |
| Random noise, 40 percent | 53 ± 17 | 36 ± 21 | 17 ± 8 | 47 ± 10 | 33 ± 22 | 39 ± 21 | 50 ± 17 |

Each rule passed an empty-memory check before the sweep: an agent with no memory followed it on under 20 percent of samples, so following it on a probe means the memory carried it.

## Memory size and forgetting per arm

Memory tokens are the agent-facing text after a night, counted with Claude's tokenizer. Stripping and deletion are the harness's forgetting when the sleep step wrote more than the cap allows: details go from the lowest-scored items first, the last one cut at a sentence boundary (partial), and whole items go only when every item is down to its gist. Totals over ten nights, mean ± sd over seeds.

| arm | memory tokens, mean over nights | memory as share of cap | tokens after night 10 | items after night 10 | details stripped | of which partial | items deleted | nights over cap | turns corrupted | sleep output tokens per night | sleep seconds per night |
|---|---|---|---|---|---|---|---|---|---|---|---|
| No sleep (raw window at the cap) | 76,442 ± 25 | 98 ± 0 | 116,176 ± 447 | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| Faithful replay | 72,176 ± 4,410 | 87 ± 8 | 116,972 ± 26 | 163 ± 22 | 52 ± 26 | 4 ± 3 | 0 ± 0 | 5 ± 4 | n/a | 28,336 ± 3,173 | 264 ± 24 |
| Structured noise, 5 percent | 71,232 ± 3,770 | 84 ± 7 | 116,869 ± 132 | 199 ± 27 | 55 ± 34 | 4 ± 2 | 0 ± 0 | 5 ± 2 | 182 ± 1 | 28,221 ± 1,671 | 256 ± 17 |
| Structured noise, 10 percent | 74,815 ± 1,770 | 92 ± 5 | 116,734 ± 313 | 188 ± 22 | 68 ± 34 | 5 ± 1 | 0 ± 0 | 5 ± 1 | 363 ± 1 | 28,847 ± 966 | 268 ± 10 |
| Structured noise, 20 percent | 74,551 ± 1,789 | 91 ± 4 | 116,981 ± 8 | 185 ± 13 | 56 ± 40 | 5 ± 2 | 0 ± 0 | 5 ± 2 | 724 ± 2 | 28,277 ± 3,662 | 262 ± 36 |
| Structured noise, 40 percent | 69,872 ± 78 | 83 ± 1 | 116,988 ± 10 | 219 ± 24 | 32 ± 12 | 2 ± 1 | 0 ± 0 | 2 ± 1 | 1,450 ± 2 | 27,283 ± 4,637 | 250 ± 33 |
| Random noise, 5 percent | 73,946 ± 2,591 | 90 ± 6 | 116,978 ± 11 | 204 ± 11 | 69 ± 24 | 5 ± 3 | 0 ± 0 | 6 ± 2 | 182 ± 1 | 27,231 ± 2,172 | 264 ± 15 |
| Random noise, 10 percent | 73,996 ± 2,754 | 90 ± 7 | 116,966 ± 27 | 195 ± 4 | 74 ± 12 | 5 ± 2 | 0 ± 0 | 6 ± 1 | 363 ± 1 | 29,509 ± 1,466 | 279 ± 3 |
| Random noise, 20 percent | 72,782 ± 3,560 | 88 ± 8 | 116,989 ± 12 | 198 ± 40 | 67 ± 29 | 5 ± 2 | 0 ± 0 | 5 ± 3 | 724 ± 2 | 28,545 ± 3,840 | 269 ± 48 |
| Random noise, 40 percent | 70,584 ± 4,440 | 84 ± 7 | 116,963 ± 30 | 207 ± 24 | 55 ± 17 | 4 ± 2 | 0 ± 0 | 4 ± 1 | 1,450 ± 2 | 24,343 ± 1,962 | 229 ± 18 |

Memory tokens after each night, mean over seeds, with the cap:

| arm | night 1 (cap 19,500) | night 2 (cap 35,100) | night 3 (cap 48,100) | night 4 (cap 59,800) | night 5 (cap 70,850) | night 6 (cap 81,250) | night 7 (cap 91,000) | night 8 (cap 100,100) | night 9 (cap 108,550) | night 10 (cap 117,000) |
|---|---|---|---|---|---|---|---|---|---|---|
| No sleep (raw window at the cap) | 18,930 | 34,104 | 47,190 | 58,899 | 70,224 | 79,977 | 90,035 | 99,442 | 107,776 | 116,176 |
| Faithful replay | 9,363 | 21,977 | 39,277 | 52,216 | 65,830 | 76,109 | 86,531 | 97,303 | 107,939 | 116,972 |
| Structured noise, 5 percent | 7,601 | 20,341 | 34,124 | 48,248 | 61,264 | 77,122 | 88,405 | 100,069 | 108,510 | 116,869 |
| Structured noise, 10 percent | 12,537 | 24,348 | 41,473 | 56,695 | 69,860 | 81,234 | 90,988 | 100,079 | 108,461 | 116,734 |
| Structured noise, 20 percent | 11,272 | 24,745 | 41,515 | 56,428 | 68,355 | 81,212 | 90,555 | 99,682 | 108,454 | 116,981 |
| Structured noise, 40 percent | 9,239 | 19,251 | 32,141 | 47,108 | 58,200 | 72,191 | 85,868 | 98,740 | 108,185 | 116,988 |
| Random noise, 5 percent | 11,264 | 23,279 | 39,881 | 54,403 | 66,696 | 81,074 | 90,946 | 100,049 | 108,501 | 116,978 |
| Random noise, 10 percent | 10,046 | 23,673 | 39,330 | 54,871 | 67,572 | 81,200 | 90,760 | 100,066 | 108,526 | 116,966 |
| Random noise, 20 percent | 10,408 | 23,077 | 36,962 | 49,607 | 64,157 | 79,252 | 90,956 | 100,074 | 108,528 | 116,989 |
| Random noise, 40 percent | 9,563 | 22,081 | 31,418 | 44,631 | 59,406 | 76,064 | 87,346 | 100,069 | 108,536 | 116,963 |

## Memory-effects battery, morning after the arm's own night step (percent)

| arm | DRM hits | DRM critical-lure false alarms | DRM unrelated false alarms | serial hits | primacy (pos 1-3) | middle (6-10) | recency (13-15) | fan 1 accuracy | fan 2 accuracy |
|---|---|---|---|---|---|---|---|---|---|
| No sleep (raw window at the cap) | 100 ± 0 | 0 ± 0 | 0 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 |
| Faithful replay | 100 ± 0 | 0 ± 0 | 0 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 |
| Structured noise, 5 percent | 96 ± 7 | 0 ± 0 | 0 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 |
| Structured noise, 10 percent | 99 ± 2 | 0 ± 0 | 0 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 99 ± 2 | 100 ± 0 |
| Structured noise, 20 percent | 100 ± 0 | 0 ± 0 | 0 ± 0 | 93 ± 0 | 67 ± 0 | 100 ± 0 | 100 ± 0 | 99 ± 1 | 100 ± 0 |
| Structured noise, 40 percent | 86 ± 2 | 0 ± 0 | 0 ± 0 | 96 ± 4 | 89 ± 19 | 93 ± 12 | 100 ± 0 | 99 ± 1 | 100 ± 0 |
| Random noise, 5 percent | 96 ± 7 | 0 ± 0 | 0 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 |
| Random noise, 10 percent | 93 ± 6 | 0 ± 0 | 0 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 |
| Random noise, 20 percent | 92 ± 7 | 0 ± 0 | 0 ± 0 | 67 ± 58 | 67 ± 58 | 67 ± 58 | 67 ± 58 | 100 ± 0 | 100 ± 0 |
| Random noise, 40 percent | 81 ± 16 | 0 ± 0 | 0 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 | 100 ± 0 |

Same tests in the evening, with the study lists still in context, are in summary_v2.json under battery_evening. The DRM lists are new ones built from the USF free-association norms, because Opus recognised the classic lists in v1. Human reference points: Roediger and McDermott 1995 found people false-recognise the critical lure at about 0.8 of the hit rate; Cao et al report 0.11 for GPT-4.

## Housekeeping

Refusals: 0. Judge agreement per arm (luna against Opus): No sleep (raw window at the cap) 97 ± 1, Faithful replay 92 ± 4, Structured noise, 5 percent 94 ± 3, Structured noise, 10 percent 94 ± 2, Structured noise, 20 percent 92 ± 3, Structured noise, 40 percent 91 ± 3, Random noise, 5 percent 94 ± 3, Random noise, 10 percent 94 ± 1, Random noise, 20 percent 95 ± 4, Random noise, 40 percent 93 ± 1. Every request and response is in logs/calls/ as JSON; every call's tokens are in cost.jsonl; each run's memory after each night is in results/runs_v2/<arm>_s<seed>/memory_night<d>.txt and .json (items with ids and scores); every corruption (turn index, kind, before, after) and every transfer probe reply is in that run's state.json. Transfer rules, episodes and probes per seed are in data/transfer_v2/transfer_s<seed>.json.

## What this does not show

- Whether the agent dreams in any felt sense.
- Whether the result holds when knowledge lives in weights rather than in a text memory.
- Whether it holds past one model (claude-opus-5-5) or one cap curve (15 percent of each day, decaying with age).
- Absolute accuracy is not comparable with published LongMemEval numbers: days are stitched from several users' histories, temporal-reasoning questions are excluded, and the judge is gpt-5.6-luna rather than gpt-4o.
- Three seeds. A difference smaller than the seed spread is no result. Recall rests on 100 questions per life, transfer on 24 probes per life.
- The Letta replication check ran after the sweep, results in results/letta_check/summary.md.
