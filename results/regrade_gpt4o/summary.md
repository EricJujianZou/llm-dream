# Regrade with gpt-4o-2024-08-06 (LongMemEval's official judge)

Answers regraded: 1224. Agreement with the Opus judge: 1169 of 1224 (95.5 percent).
gpt-4o says correct where Opus said wrong: 28. gpt-4o says wrong where Opus said correct: 27.

## Final recall, percent, mean ± sd over seeds

| arm | Opus judge | gpt-4o judge | minus faithful, Opus | minus faithful, gpt-4o |
|---|---|---|---|---|
| nosleep | 2 ± 4 | 6 ± 2 | -44 ± 7 | -39 ± 7 |
| faithful | 46 ± 9 | 45 ± 5 | 0 ± 0 | 0 ± 0 |
| noisy_structured | 32 ± 0 | 36 ± 4 | -14 ± 9 | -10 ± 8 |
| noisy_random | 38 ± 4 | 42 ± 5 | -8 ± 9 | -4 ± 7 |

## Disagreements (first 15)

- faithful_s0 morning single-session-assistant: Opus no, gpt-4o yes. Q: I was thinking about our previous conversation about data privacy and security. You mentioned that companies use two-fac Gold: I mentioned biometric authentication or one-time passwords (OTP) as examples of 
- faithful_s0 final single-session-assistant: Opus no, gpt-4o yes. Q: I was thinking about our previous conversation about data privacy and security. You mentioned that companies use two-fac Gold: I mentioned biometric authentication or one-time passwords (OTP) as examples of 
- faithful_s0 final single-session-preference: Opus no, gpt-4o yes. Q: I'm planning a trip to Denver soon. Any suggestions on what to do there? Gold: The user would prefer responses that take into account their previous experience
- faithful_s1 morning single-session-assistant: Opus no, gpt-4o yes. Q: I wanted to follow up on our previous conversation about natural remedies for dark circles under the eyes. You mentioned Gold: 10 minutes
- faithful_s2 evening knowledge-update: Opus no, gpt-4o yes. Q: What was the amount I was pre-approved for when I got my mortgage from Wells Fargo? Gold: $400,000
- faithful_s2 morning knowledge-update: Opus no, gpt-4o yes. Q: What was the amount I was pre-approved for when I got my mortgage from Wells Fargo? Gold: $400,000
- faithful_s2 morning single-session-assistant: Opus no, gpt-4o yes. Q: I'm planning my trip to Amsterdam again and I was wondering, what was the name of that hostel near the Red Light Distric Gold: International Budget Hostel
- faithful_s2 final single-session-assistant: Opus no, gpt-4o yes. Q: I'm looking back at our previous conversation about the Seco de Cordero recipe from Ancash. You mentioned using a light  Gold: I recommended using a Pilsner or Lager for the recipe.
- noisy_random_s0 morning single-session-assistant: Opus no, gpt-4o yes. Q: I was thinking about our previous conversation about data privacy and security. You mentioned that companies use two-fac Gold: I mentioned biometric authentication or one-time passwords (OTP) as examples of 
- noisy_random_s0 final single-session-assistant: Opus no, gpt-4o yes. Q: I was thinking about our previous conversation about data privacy and security. You mentioned that companies use two-fac Gold: I mentioned biometric authentication or one-time passwords (OTP) as examples of 
- noisy_random_s1 morning single-session-assistant: Opus no, gpt-4o yes. Q: I'm checking our previous chat about the shift rotation sheet for GM social media agents. Can you remind me what was the Gold: Admon was assigned to the 8 am - 4 pm (Day Shift) on Sundays.
- noisy_random_s1 final single-session-assistant: Opus no, gpt-4o yes. Q: I wanted to follow up on our previous conversation about language learning apps. You mentioned a few options, and I was  Gold: Memrise
- noisy_random_s2 evening knowledge-update: Opus no, gpt-4o yes. Q: What was the amount I was pre-approved for when I got my mortgage from Wells Fargo? Gold: $400,000
- noisy_random_s2 final single-session-assistant: Opus no, gpt-4o yes. Q: I'm looking back at our previous conversation about the Seco de Cordero recipe from Ancash. You mentioned using a light  Gold: I recommended using a Pilsner or Lager for the recipe.
- noisy_random_s2 final multi-session: Opus no, gpt-4o yes. Q: What is the total number of goals and assists I have in the recreational indoor soccer league? Gold: 5
