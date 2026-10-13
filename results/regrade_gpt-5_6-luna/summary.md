# Regrade with gpt-5.6-luna

Answers regraded: 1224. Empty replies: 0.
Agreement with the Opus judge: 1161 of 1224 (94.9 percent).
Agreement with the gpt-4o judge: 1174 of 1224 (95.9 percent).
For reference, Opus and gpt-4o agree on 1169 of 1224 (95.5 percent).

gpt-5.6-luna says correct where Opus said wrong: 42. gpt-5.6-luna says wrong where Opus said correct: 21.

## Final recall, percent, mean over seeds

| arm | Opus judge | gpt-5.6-luna | gpt-4o judge |
|---|---|---|---|
| nosleep | 2 ± 4 | 6 ± 2 | 6 ± 2 |
| faithful | 46 ± 9 | 54 ± 4 | 45 ± 5 |
| noisy_structured | 32 ± 0 | 40 ± 8 | 36 ± 4 |
| noisy_random | 38 ± 4 | 43 ± 4 | 42 ± 5 |

## Disagreements with Opus (first 15)

- faithful_s0 evening single-session-preference: Opus no, gpt-5.6-luna yes. Q: I'm planning a trip to Denver soon. Any suggestions on what to do there? Gold: The user would prefer responses that take into account their previous experience
- faithful_s0 morning single-session-assistant: Opus no, gpt-5.6-luna yes. Q: I was thinking about our previous conversation about data privacy and security. You mentioned that companies use two-fac Gold: I mentioned biometric authentication or one-time passwords (OTP) as examples of 
- faithful_s0 final single-session-assistant: Opus no, gpt-5.6-luna yes. Q: I was thinking about our previous conversation about data privacy and security. You mentioned that companies use two-fac Gold: I mentioned biometric authentication or one-time passwords (OTP) as examples of 
- faithful_s1 morning single-session-assistant: Opus no, gpt-5.6-luna yes. Q: I wanted to follow up on our previous conversation about natural remedies for dark circles under the eyes. You mentioned Gold: 10 minutes
- faithful_s1 evening single-session-preference: Opus no, gpt-5.6-luna yes. Q: Can you recommend a show or movie for me to watch tonight? Gold: The user would prefer recommendations for stand-up comedy specials on Netflix, e
- faithful_s1 final single-session-preference: Opus no, gpt-5.6-luna yes. Q: Can you recommend a show or movie for me to watch tonight? Gold: The user would prefer recommendations for stand-up comedy specials on Netflix, e
- faithful_s2 evening knowledge-update: Opus no, gpt-5.6-luna yes. Q: What was the amount I was pre-approved for when I got my mortgage from Wells Fargo? Gold: $400,000
- faithful_s2 morning knowledge-update: Opus no, gpt-5.6-luna yes. Q: What was the amount I was pre-approved for when I got my mortgage from Wells Fargo? Gold: $400,000
- faithful_s2 morning single-session-preference: Opus no, gpt-5.6-luna yes. Q: Can you suggest a hotel for my upcoming trip to Miami? Gold: The user would prefer suggestions of hotels in Miami that offer great views, pos
- faithful_s2 morning single-session-assistant: Opus no, gpt-5.6-luna yes. Q: I'm planning my trip to Amsterdam again and I was wondering, what was the name of that hostel near the Red Light Distric Gold: International Budget Hostel
- faithful_s2 final single-session-assistant: Opus no, gpt-5.6-luna yes. Q: I'm looking back at our previous conversation about the Seco de Cordero recipe from Ancash. You mentioned using a light  Gold: I recommended using a Pilsner or Lager for the recipe.
- faithful_s2 final single-session-preference: Opus no, gpt-5.6-luna yes. Q: Can you suggest a hotel for my upcoming trip to Miami? Gold: The user would prefer suggestions of hotels in Miami that offer great views, pos
- faithful_s2 final single-session-preference: Opus no, gpt-5.6-luna yes. Q: I'm planning my meal prep next week, any suggestions for new recipes? Gold: The user would prefer responses that suggest healthy meal prep recipes, especial
- faithful_s2 final knowledge-update: Opus no, gpt-5.6-luna yes. Q: What was the amount I was pre-approved for when I got my mortgage from Wells Fargo? Gold: $400,000
- noisy_random_s0 morning single-session-assistant: Opus no, gpt-5.6-luna yes. Q: I wanted to follow up on our previous conversation about binaural beats for anxiety and depression. Can you remind me ho Gold: 38 subjects
