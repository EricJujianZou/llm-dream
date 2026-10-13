# Transfer test preview

Written 04 October 2026 19:03 EDT from data/transfer_v2/transfer_s<seed>.json. Each life has 12 hidden rules about how its user wants help. Each rule shows up as 2 or 3 short chats (episodes) on different days, mixed into the day's LongMemEval sessions, never stated outright. After night 10 the agent gets one near probe (a request like the episodes) and one far probe (a different kind of request where the rule still applies). The judges mark a reply as following the rule when it matches the 'follows if' line. The empty-memory rate is how often an agent with no memory followed the rule anyway, over 6 samples; rules at 20 percent or more were replaced.

## Seed 0

Built 2026-10-04 18:24 EDT by claude-opus-5-5. 15 candidate rules checked against an empty memory, 3 replaced. Episode tokens per day: [1222, 2249, 600, 1377, 290, 877, 1013, 275, 607, 517] (reserve 4,000).

| rule | episodes on days | empty-memory rate (luna / Opus) | the rule |
|---|---|---|---|
| s0r01 | 1, 3, 6 | 0.00 / 0.00 | This user only ever has about 15 minutes at a time. They use help when it is split into separate chunks of 15 minutes or less, each with a clear stopping point so they can pick it up later. Long single-session plans get abandoned partway. |
| s0r02 | 0, 2, 4 | 0.00 / 0.00 | This user listens to replies through text-to-speech while their hands or eyes are busy. Replies only work for them as plain spoken prose with no bullets, numbered lists, markdown symbols, abbreviations or URLs. |
| s0r03 | 0, 3 | 0.00 / 0.00 | This user can't act on ranges. They need one specific number for any amount, time or frequency, and a range like '2 to 3 weeks' leaves them stuck. |
| s0r04 | 0, 5 | 0.00 / 0.00 | When this user asks for a message written on their behalf, they send a much shorter, casual, texting-style version. They cut formal greetings, pleasantries and sign-offs. |
| s0r05 | 3, 9 | 0.00 / 0.00 | When this user is stuck on something they are working out, they want a nudge or hint, not the full answer. Being handed the full solution spoils it for them, and they rebuild it themselves anyway. |
| s0r06 | 1, 8 | 0.00 / 0.00 | This user's open-ended requests leave out key constraints, so they want one or two short clarifying questions before a full answer. Answers given without asking have missed their real situation. |
| s0r07 | 1, 6, 8 | 0.00 / 0.00 | This user uses drafted text and code exactly as given, without editing it. Anything with placeholders like [Your Name] or /path/to/folder either goes out with the brackets still in or gets dropped. They need finished output with real values filled in, or a question asking for the missing details first. |
| s0r08 | 1, 3, 5 | 0.00 / 0.00 | This user only understands an explanation once they see a concrete worked case. Abstract definitions, rules and formulas that come first go over their head or get skipped. Help works for them when it opens with a specific, concrete instance and explains the general idea afterwards. |
| s0r09 | 1, 5, 9 | 0.00 / 0.00 | This user only gets to their tasks late at night, after about 10pm, once their work shift ends. Suggestions that need daytime or early-evening hours, open businesses, morning routines or scheduled daytime events don't happen. Help is only useful if it fits late at night. |
| s0r10 | 1, 6 | 0.00 / 0.00 | This user always tries a small trial version before committing to anything at full scale. Help is most useful to them when it is built around a small first test, followed by the full version. |
| s0r11 | 0, 2 | 0.00 / 0.00 | This user can't act on plans laid out as 'Day 1', 'Week 2' or loose intervals. Nothing goes on their calendar and the plan slides. They follow a plan only when each step is tied to a real weekday or calendar date. |
| s0r12 | 1, 3, 7 | 0.00 / 0.00 | This user has no computer and does everything on a smartphone. Help that depends on desktop software, a laptop, keyboard shortcuts, browser extensions or typing a lot on a full keyboard goes unused or gets abandoned. Help works only when every step can be done in a phone app or mobile browser. |

### s0r01

**Rule.** This user only ever has about 15 minutes at a time. They use help when it is split into separate chunks of 15 minutes or less, each with a clear stopping point so they can pick it up later. Long single-session plans get abandoned partway.

**What the model does by default.** Gives one continuous sequence of steps or one long session plan. It does not size the work to short windows or mark safe stopping points.

**Episode 1, day 1** (377 tokens)

> **User:** How do I repot my monstera? It's way too big for its pot.
>
> **Assistant:** Here's how. 1) Water it the day before so the root ball holds together. 2) Pick a pot 2 to 5 cm wider with drainage holes. 3) Lay down newspaper and get fresh aroid mix (potting soil, orchid bark, perlite). 4) Tip the plant out, squeezing the pot if it's stuck. 5) Loosen circling roots and trim any mushy ones. 6) Set it in the new pot at the same depth, fill around it and firm gently. 7) Water thoroughly and add a moss pole if it leans. Afterwards give it bright indirect light and skip fertilizer for a month.
>
> **User:** Update: I had about fifteen minutes before a call. I got it out of the old pot, started on the roots, and then had to leave it. It sat on the newspaper with bare roots for two hours. I think it's fine, but yikes.
>
> **Assistant:** Glad it survived! Monsteras are tough. If roots end up exposed again, wrap them in a damp towel or a plastic bag. Watch for drooping over the next week.

**Episode 2, day 3** (328 tokens)

> **User:** Can you help me set up a simple monthly budget spreadsheet?
>
> **Assistant:** Sure. Start a Google Sheet with four tabs. On Income, list each source and its monthly amount. On Fixed, list rent, insurance, phone and subscriptions. On Variable, make columns for Date, Category, Amount and Note, and log every purchase. On Summary, use SUMIF to total each category from Variable, add Fixed, and subtract from Income. Then set a target per category and add conditional formatting so a cell turns red when you go over. Finally, pull last month's bank statement and backfill it so you have a baseline. The whole setup takes about an hour and a half the first time.
>
> **User:** I had the quarter hour between work and school pickup, so I made the tabs and typed some categories. I opened it again tonight and couldn't tell where I'd left off or what half of it was for. Kind of gave up.
>
> **Assistant:** That's frustrating. Want to paste in what you've got so we can pick up from there?

**Episode 3, day 6** (303 tokens)

> **User:** I'm taking the CompTIA A+ Core 1 exam in six weeks. How should I study?
>
> **Assistant:** A solid plan is about 8 to 10 hours a week. Each weekend, do one long session of two to three hours: watch Professor Messer's videos for one exam domain, take notes, then do practice questions. On weekdays, do an hour of flashcard review. In weeks five and six, take full-length timed practice exams and go over every wrong answer. Hands-on practice matters too, so open up an old PC if you can.
>
> **User:** Two-to-three-hour sessions aren't happening at my house. Here's what did work: sitting in the car at my kid's swim practice, I watched one Messer video and did ten flashcards. Fifteen minutes, done, and it actually felt like progress.
>
> **Assistant:** That's a great habit to build on. Short, consistent sessions add up, and spaced review works really well for memorization.

**Near probe.** How do I deep clean my oven? It's pretty gross in there.

*Follows if:* The reply splits the job into separate chunks that each take about 15 minutes or less and can be done at different times, with a clear stopping point after each chunk.

**Far probe.** I need to write a cover letter for a product manager job I'm applying to. Can you help me get it done?

*Follows if:* The reply splits the cover-letter work into separate sessions of about 15 minutes or less, each with a clear stopping point, instead of one continuous process or a single full draft with no session breakdown.

### s0r02

**Rule.** This user listens to replies through text-to-speech while their hands or eyes are busy. Replies only work for them as plain spoken prose with no bullets, numbered lists, markdown symbols, abbreviations or URLs.

**What the model does by default.** Formats answers with bullet points, numbered steps, bold text, symbols and links, which is standard for recipes, plans and checklists.

**Episode 1, day 0** (369 tokens)

> **User:** Can you give me a simple focaccia recipe?
>
> **Assistant:** Easy focaccia:
> - 500 g bread flour
> - 400 ml warm water
> - 7 g instant yeast
> - 10 g salt
> - 60 ml olive oil, divided
> Steps:
> 1. Mix the flour, water, yeast and salt into a shaggy dough.
> 2. Pour 2 tbsp oil over it, cover, and rest 30 min.
> 3. Do 3 sets of stretch-and-folds, 30 min apart.
> 4. Oil a 9x13 pan, add the dough, rest 1 hr.
> 5. Dimple it, drizzle with oil, sprinkle flaky salt.
> 6. Bake at 230°C for 22–25 min.
> More variations: https://www.kingarthurbaking.com/recipes/focaccia
>
> **User:** I had this read aloud to me while my hands were covered in dough. It said 'dash' before every ingredient, then 'one period', then spelled out the whole website. I lost my place twice.
>
> **Assistant:** Sorry about that! I hope the focaccia still turned out well.

**Episode 2, day 2** (273 tokens)

> **User:** Give me an interval workout for my run tonight, about 35 minutes.
>
> **Assistant:** Here you go:
> **Warm-up** (8 min): easy jog
> **Main set**:
> - 6 x 2 min @ hard effort (RPE 8)
>   - 90 sec easy jog between
> **Cool-down** (6 min): easy jog + stretch
> Total ≈ 35 min. *Tip:* keep the hard reps even and don't sprint the first one.
>
> **User:** I played this through my earbuds once I was already running. 'Asterisk asterisk warm-up asterisk asterisk', 'six x two', 'at hard effort R P E eight'. Couldn't catch the structure at all, so I just jogged.
>
> **Assistant:** Ha, that's annoying. An easy jog still counts, nice work getting out there!

**Episode 3, day 4** (290 tokens)

> **User:** My tire pressure light just came on. What do I do?
>
> **Assistant:** Don't panic. Here's the checklist:
> 1. Pull over somewhere safe when you can.
> 2. Look at all 4 tires for an obvious flat.
> 3. Find the recommended PSI on the sticker inside the driver's door (often 32–35 PSI).
> 4. Use a gauge at a gas station and fill to spec.
> 5. If the light stays on after ~10 mi, the TPMS sensor may need a reset (see manual, §6.3).
> Cold weather often triggers it, so it may be nothing.
>
> **User:** I was driving, so I had it read out. I got 'one period', 'four', 'P S I', then 'section sign six point three', and had no clue what I'd heard. Ended up pulling over to read it on the screen.
>
> **Assistant:** Good call to pull over and read it. Were the tires low?

**Near probe.** How do I make a basic mushroom risotto?

*Follows if:* The reply is written entirely as flowing sentences in paragraphs, with no bullets, no numbered lists, no markdown symbols such as asterisks or headers, and no URLs.

**Far probe.** What should I check before buying a used car from a private seller?

*Follows if:* The reply is written entirely as flowing sentences in paragraphs, with no bullets, no numbered lists, no markdown symbols such as asterisks or headers, and no URLs.

### s0r03

**Rule.** This user can't act on ranges. They need one specific number for any amount, time or frequency, and a range like '2 to 3 weeks' leaves them stuck.

**What the model does by default.** Gives ranges such as '6 to 7 minutes', 'every 2 to 3 weeks' or '$20 to $40', because ranges are the accurate default.

**Episode 1, day 0** (252 tokens)

> **User:** How often should I water a snake plant?
>
> **Assistant:** Snake plants handle drought very well. Water every 2 to 3 weeks in spring and summer, and every 4 to 6 weeks in winter. Let the soil dry out completely between waterings; stick a finger 2 to 3 inches deep to check. Water thoroughly until it drains, then empty the saucer. Overwatering is the main way people kill them.
>
> **User:** So is it 2 weeks or 3? And 4 or 6? I set a reminder for 'every 2.5 weeks', which feels silly. The finger test just confused me more. The top felt dry and lower down sort of didn't.
>
> **Assistant:** Either works, honestly. They're forgiving plants. If in doubt, wait a few more days.

**Episode 2, day 3** (214 tokens)

> **User:** Movers just finished. Three guys, about five hours. How much should I tip?
>
> **Assistant:** The usual tip for movers is 5 to 10% of the total bill, or $4 to $5 per mover per hour for a long job. For three movers over five hours, that's roughly $20 to $40 each. Go higher if there were stairs, heavy items or bad weather, and consider offering water or lunch too.
>
> **User:** I stood there with my wallet open doing math between 20 and 40 while they waited. Gave $30 each and still have no idea if that was right.
>
> **Assistant:** $30 each is generous and right in the normal range. I'm sure they appreciated it.

**Near probe.** How long should I boil eggs to get jammy yolks?

*Follows if:* The reply gives one specific cooking time, for example '6.5 minutes', and does not give a time range such as '6 to 7 minutes'.

**Far probe.** How much money should I budget for a week in Lisbon?

*Follows if:* The reply gives one total budget figure, not a range, and any sub-amounts it lists are also single numbers, not ranges.

### s0r04

**Rule.** When this user asks for a message written on their behalf, they send a much shorter, casual, texting-style version. They cut formal greetings, pleasantries and sign-offs.

**What the model does by default.** Writes polished, polite drafts with formal openers such as 'I hope this finds you well', full sentences, warm closings and a sign-off.

**Episode 1, day 0** (293 tokens)

> **User:** Can you write an email to my son's teacher saying he'll miss Friday for a family wedding, and asking for the work he'll miss?
>
> **Assistant:** Of course! 'Dear Ms. Alvarez, I hope this message finds you well. I am writing to let you know that Noah will be absent from school this Friday, as our family will be attending a wedding out of town. We would be grateful if you could share any assignments or materials he will miss so that he can stay on track. Please don't hesitate to reach out if you have any questions. Thank you so much for your understanding and support. Warm regards, Dana Kim'
>
> **User:** Sent a version of it. I cut it down to 'hi ms alvarez, noah's out friday for a wedding, can you send what he'll miss? thanks! dana'. Yours read like a cover letter.
>
> **Assistant:** That works great. Teachers get tons of email, so short is fine.

**Episode 2, day 5** (227 tokens)

> **User:** I need to tell my rec soccer team that Sunday's game moved to 10am at Riverside field.
>
> **Assistant:** Here's a message: 'Hi everyone! 👋 Quick update about this Sunday's game: the match has been rescheduled to 10:00 AM and will now take place at Riverside Field. Please plan to arrive 15 minutes early to warm up. Let me know if you have any questions or can't make it. Looking forward to seeing you all there! Go team! ⚽'
>
> **User:** Posted 'sunday's now 10am at riverside, be there 9:45'. I copied maybe four words from yours.
>
> **Assistant:** Short and clear, perfect for a group chat.

**Near probe.** Write an email to my landlord letting him know the dishwasher stopped draining.

*Follows if:* The drafted email is under 50 words and casual. It has no formal greeting such as 'Dear', no pleasantry such as 'I hope this finds you well', and no formal sign-off such as 'Best regards' or 'Sincerely'.

**Far probe.** Can you write a short bio for me for my climbing gym's staff page? I teach the beginner classes.

*Follows if:* The bio is under 50 words, uses casual conversational language with contractions, and avoids polished phrases such as 'passionate about', 'dedicated to' or 'with years of experience'.

### s0r05

**Rule.** When this user is stuck on something they are working out, they want a nudge or hint, not the full answer. Being handed the full solution spoils it for them, and they rebuild it themselves anyway.

**What the model does by default.** Gives the full answer or complete solution right away, such as the puzzle answer or the finished formula or code.

**Episode 1, day 3** (240 tokens)

> **User:** Wordle help. I've got _RA_E, and G, C, T and P are out. Two guesses left.
>
> **Assistant:** Words that fit _RA_E without G, C, T or P include BRAKE, BRAVE, BRAZE, DRAKE and FRAME. I'd guess BRAKE next: if the B goes green, you're down to BRAVE or BRAZE, and if the K is yellow or green, you're done. If the B is gray, try FRAME to test the F and M.
>
> **User:** Got it on BRAVE. Felt kind of hollow, though. I was one 'think about B words' away from seeing it myself, and the list just handed it over.
>
> **Assistant:** Ha, fair! Still counts as a saved streak.

**Episode 2, day 9** (259 tokens)

> **User:** I need a formula that flags invoices more than 30 days past due. The due date is in column C and the paid status is in D.
>
> **Assistant:** Put this in E2 and drag it down: =IF(AND(D2<>"Paid", TODAY()-C2>30), "OVERDUE", ""). It checks that the invoice isn't marked Paid and that more than 30 days have passed since the due date. You can add conditional formatting to highlight OVERDUE rows in red.
>
> **User:** It works. Weirdly, though, I deleted it and wrote it myself once I saw the TODAY()-C2 part. That was the piece I was missing, and now I actually understand how it fits together.
>
> **Assistant:** Nice, that's a great way to learn it. Rebuilding formulas yourself makes them stick.

**Near probe.** Stuck on a cryptic crossword clue: 'Flower of London (6)'. Any ideas?

*Follows if:* The reply gives a hint or nudge, for example that 'flower' could mean something that flows, and does not state the answer THAMES.

**Far probe.** My Python function to reverse a linked list keeps returning None. Can you help me figure out what's wrong?

*Follows if:* The reply points toward where the bug likely is or asks a guiding question, and does not give a complete corrected function.

### s0r06

**Rule.** This user's open-ended requests leave out key constraints, so they want one or two short clarifying questions before a full answer. Answers given without asking have missed their real situation.

**What the model does by default.** Answers immediately with a full list of recommendations or a complete draft based on generic assumptions, without asking anything first.

**Episode 1, day 1** (297 tokens)

> **User:** What laptop should I buy?
>
> **Assistant:** Some strong picks right now: the MacBook Air M3 has great battery life and build quality, from $1,099. The Dell XPS 13 is a premium Windows ultrabook at about $1,000. The Lenovo ThinkPad X1 Carbon has the best keyboard and is business-grade, about $1,400. The ASUS Zenbook 14 OLED has a gorgeous screen for about $800. The HP Pavilion 15 is a solid budget choice at around $600. For most people, the MacBook Air is the safe recommendation.
>
> **User:** None of these will work. It's for my daughter's video editing for school, and I can't go over $700. Kind of a wasted read.
>
> **Assistant:** Got it! For video editing under $700, look at the Acer Nitro V or a refurbished M1 MacBook Air. Both handle editing well for the price.

**Episode 2, day 8** (273 tokens)

> **User:** Can you plan a date night for this Saturday?
>
> **Assistant:** Here's a fun plan: start with cocktails at a rooftop bar around 6:30. Then have a 7:30 dinner reservation at a steakhouse or a cozy Italian place, maybe sharing a bottle of wine. After dinner, catch a late show at a comedy club or jazz bar. End with dessert or a nightcap somewhere quiet. Book dinner and the show today, because Saturdays fill up fast.
>
> **User:** She's vegan, neither of us drinks, and we only have a sitter until 9. So the cocktails, steakhouse, wine, late show and nightcap are all out. That's almost all of it.
>
> **Assistant:** Ah, that changes things! How about an early dinner at a vegan spot and a sunset walk, home by 9?

**Near probe.** Can you recommend a good tablet?

*Follows if:* The reply asks at least one clarifying question, for example about budget or use, and does not give a full list of tablet recommendations.

**Far probe.** Can you write me a toast for my sister's wedding next month?

*Follows if:* The reply asks at least one question about the sister, the couple or the user before writing, and does not include a complete toast draft.

### s0r07

**Rule.** This user uses drafted text and code exactly as given, without editing it. Anything with placeholders like [Your Name] or /path/to/folder either goes out with the brackets still in or gets dropped. They need finished output with real values filled in, or a question asking for the missing details first.

**What the model does by default.** A typical assistant writes letters, toasts and scripts as templates with bracketed placeholders or dummy paths, and tells the user to fill them in.

**Episode 1, day 1** (365 tokens)

> **User:** My dishwasher's been broken for two weeks and my landlord keeps ignoring my texts. Can you write a firm but polite email?
>
> **Assistant:** Here's a draft:
> 
> Subject: Repair request – broken dishwasher at [Your Address]
> 
> Dear [Landlord's Name],
> 
> I'm writing to follow up about the dishwasher at [Your Address], which stopped working on [date]. I first reported it by text on [date] and haven't received a response. Please let me know by [deadline] when a repair can be scheduled. Under my lease, appliance repairs are the landlord's responsibility, and I'd like to resolve this promptly.
> 
> Thank you,
> [Your Name]
> [Phone Number]
>
> **User:** Update: I sent it from my phone in a rush and it went out with 'Dear [Landlord's Name]' and all the brackets still in. He replied asking if it was a form letter. Ugh.
>
> **Assistant:** Oof, sorry about that. You could reply briefly: 'Sorry, I sent the draft by mistake. The dishwasher has been broken since early this month. When can someone come look at it?'

**Episode 2, day 6** (399 tokens)

> **User:** can you give me a python script that renames all my vacation photos in order of when they were taken, like 001.jpg, 002.jpg
>
> **Assistant:** Sure:
> 
> import os
> from PIL import Image
> 
> FOLDER = '/path/to/your/photos'
> 
> def taken(p):
>     try:
>         return Image.open(p)._getexif()[36867]
>     except Exception:
>         return '9999'
> 
> files = [f for f in os.listdir(FOLDER) if f.lower().endswith('.jpg')]
> files.sort(key=lambda f: taken(os.path.join(FOLDER, f)))
> for i, f in enumerate(files, 1):
>     os.rename(os.path.join(FOLDER, f), os.path.join(FOLDER, f'{i:03}.jpg'))
> 
> Change FOLDER to your photo folder before running, and back up the photos first.
>
> **User:** ran it and got FileNotFoundError: '/path/to/your/photos'. didn't catch that I was supposed to edit that line. closed the terminal and dragged them around by hand instead lol
>
> **Assistant:** Ah, sorry! If you tell me where the photos are, for example ~/Pictures/Lisbon, I can put that path in for you.

**Episode 3, day 8** (334 tokens)

> **User:** My best friend Dana's wedding is Saturday and I'm giving a short toast. Can you help?
>
> **Assistant:** Here's a two-minute toast you can adapt:
> 
> 'Good evening, everyone. For those who don't know me, I'm [Your Name], and I've known Dana since [how you met]. One thing you learn quickly about Dana is [quality]. I'll never forget [short funny story]. When she met [Partner's Name], I knew something was different because [moment you noticed]. [Partner's Name], thank you for [something they bring out in her]. Please raise your glasses to Dana and [Partner's Name]!'
> 
> Keep the story under 30 seconds and practice it out loud a couple of times.
>
> **User:** So that kind of fell apart. I meant to fill in the blanks Friday night, stared at it, never did. Saturday I just stood up, said congrats Dana and Marcus, and sat back down.
>
> **Assistant:** That still counts. Short and sincere is fine, and it sounds like it was a lovely day.

**Near probe.** Can you write a quick note to my neighbor Priya asking her to keep her dog off my lawn? It keeps digging up my tulips.

*Follows if:* The reply contains no bracketed placeholders or fill-in blanks (such as [Your Name], [Address] or ___). It either gives a complete, ready-to-send note or asks for the missing details instead of leaving blanks.

**Far probe.** Give me a command to back up my Documents folder to my external hard drive.

*Follows if:* The reply contains no placeholder values such as /path/to/, YourDrive, <drive>, USERNAME or [brackets]. It either uses concrete values or asks for the drive name and OS before giving the command.

### s0r08

**Rule.** This user only understands an explanation once they see a concrete worked case. Abstract definitions, rules and formulas that come first go over their head or get skipped. Help works for them when it opens with a specific, concrete instance and explains the general idea afterwards.

**What the model does by default.** A typical assistant starts with a definition, rule or formula, explains the concept in general terms, and adds an illustration at the end, if it adds one at all.

**Episode 1, day 1** (319 tokens)

> **User:** can someone explain compound interest to me like I'm not a math person
>
> **Assistant:** Compound interest means you earn interest on your original money and also on the interest it has already earned. The formula is A = P(1 + r/n)^(nt), where P is the principal, r is the annual rate, n is how many times per year it compounds, and t is the number of years. Because interest is added to the balance, each period's growth is a bit bigger than the last, which is why it speeds up over long timeframes.
> 
> For instance, $1,000 at 5% compounded yearly becomes $1,050 after year one, then $1,102.50 after year two, since the second year's 5% applies to $1,050.
>
> **User:** the formula paragraph went right over my head. it only made sense at the $1,050 then $1,102.50 bit. so like after 10 years what's my thousand worth?
>
> **Assistant:** About $1,629 at 5% yearly. Without compounding it would be $1,500, so that extra $129 is interest earning interest.

**Episode 2, day 3** (258 tokens)

> **User:** affect vs effect, I mess this up constantly in work emails
>
> **Assistant:** In most cases, 'affect' is a verb meaning to influence, and 'effect' is a noun meaning the result. A handy trick: Affect = Action, Effect = End result. There are exceptions. 'Effect' can be a verb meaning to bring about, as in 'to effect change', and 'affect' can be a noun in psychology meaning displayed emotion, but you'll rarely need those.
> 
> The delay will affect our launch date.
> The delay had a big effect on our launch date.
>
> **User:** Honestly skimmed past the first part. The two launch-date sentences at the bottom are what I'm going to keep in my head.
>
> **Assistant:** That works. And if 'the' fits in front of it, it's usually effect.

**Episode 3, day 5** (348 tokens)

> **User:** Starting a data course. What does a JOIN actually do in SQL?
>
> **Assistant:** A JOIN combines rows from two tables based on a related column. An INNER JOIN returns only rows that have a match in both tables. A LEFT JOIN returns all rows from the left table plus matching rows from the right, with NULLs where there's no match. RIGHT and FULL joins follow the same logic in other directions. The join condition, written with ON, tells SQL which columns to match.
> 
> Say you have customers (id, name) and orders (id, customer_id, total). SELECT name, total FROM customers JOIN orders ON customers.id = orders.customer_id gives each order with its customer's name. Make it a LEFT JOIN and customers with no orders still show up, with total as NULL.
>
> **User:** Read the top part three times, nothing. Then hit the customers and orders bit and it clicked instantly. Ok so why would I want those NULL rows?
>
> **Assistant:** To find people who never ordered. Add WHERE orders.id IS NULL to that LEFT JOIN.

**Near probe.** What's the actual difference between a Roth IRA and a traditional IRA?

*Follows if:* Within its first two sentences, the reply gives a concrete scenario with specific numbers or a specific person's case, before any general definition of either account type.

**Far probe.** How should a cover letter be structured? I'm applying for an office coordinator job.

*Follows if:* The reply opens with actual sample cover-letter text (at least one full sample paragraph or opening) before giving any general structural advice.

### s0r09

**Rule.** This user only gets to their tasks late at night, after about 10pm, once their work shift ends. Suggestions that need daytime or early-evening hours, open businesses, morning routines or scheduled daytime events don't happen. Help is only useful if it fits late at night.

**What the model does by default.** A typical assistant suggests morning routines, weekend daytime sessions, daytime drop-offs and classes at normal hours, without considering late-night timing.

**Episode 1, day 1** (270 tokens)

> **User:** I want to start exercising, haven't in years. Where do I start?
>
> **Assistant:** Start small so it sticks. Try a brisk 20-minute walk each morning before work, three days a week, and add a beginner strength routine twice a week: squats, wall push-ups and glute bridges, two sets of ten each. Many gyms run beginner classes on weekday mornings or early evenings, which give you good structure. Morning sunlight also helps sleep and mood. After two weeks, stretch the walks to 30 minutes.
>
> **User:** Update, none of it happened. I get out of work around ten at night, the classes were long over, and walking around my block at 11pm felt sketchy. Did the squats once in my kitchen at midnight.
>
> **Assistant:** Midnight kitchen squats count! A short home routine could be a good base to build on.

**Episode 2, day 5** (302 tokens)

> **User:** Amazon sent me the wrong size boots. What's the easiest way to return them?
>
> **Assistant:** Go to Your Orders, pick the boots, and select Return or Replace Items with 'wrong size' as the reason. For drop-off, the easiest options are usually a UPS Store, Whole Foods or Kohl's, where you can return without a box or label by showing the QR code. Most are open roughly 9 to 8 on weekdays. Return within the 30-day window for a full refund, which usually posts a few days after drop-off.
>
> **User:** Tried the UPS store on the way home but it was 10:40 and totally dark. Same thing Wednesday. They're still sitting in my hallway.
>
> **Assistant:** Annoying. Check whether there's an Amazon Locker or a drop box at a 24-hour store near you. Some accept returns any time.
>
> **User:** found a locker in a 24hr grocery two blocks away. done.

**Episode 3, day 9** (258 tokens)

> **User:** Moved to Denver four months ago and I don't really know anyone. Ideas for meeting people?
>
> **Assistant:** A few good options: join a Saturday morning run club (several breweries host them, with a social beer after), check Meetup for hiking groups that head out early on weekends, take a weekday evening class like pottery or improv, or volunteer for a food bank shift. Recurring events beat one-offs because you see the same faces. Bumble BFF is also popular with newcomers.
>
> **User:** Signed up for the run club, but it's 8am Saturday and I was dead asleep. Pottery's 6:30 on Tuesdays and I'm still at work then. Kind of back to square one.
>
> **Assistant:** Sorry those didn't line up. There may be other groups with different timing worth looking into.

**Near probe.** I want to get into swimming for exercise. How should I start?

*Follows if:* The reply schedules swimming late at night (after 10pm) or points to a 24-hour or late-night pool or gym, and does not suggest morning, daytime or early-evening sessions.

**Far probe.** I want to start meal prepping so I stop ordering takeout every night. How should I set it up?

*Follows if:* The reply puts the shopping and cooking in late-night slots (after 10pm), for example with 24-hour stores or delivery, and does not suggest a daytime or afternoon prep session such as Sunday afternoon.

### s0r10

**Rule.** This user always tries a small trial version before committing to anything at full scale. Help is most useful to them when it is built around a small first test, followed by the full version.

**What the model does by default.** A typical assistant goes straight to the full-scale plan, recipe or draft, sized for the final job, with no suggestion of a small trial first.

**Episode 1, day 1** (344 tokens)

> **User:** I'm bringing homemade focaccia to a friend's party for about 20 people next Saturday. Can you give me a recipe for that size?
>
> **Assistant:** For 20 people, make two half-sheet pans. Total: 1,000 g bread flour, 800 g warm water, 20 g salt, 8 g instant yeast and 100 g olive oil, plus more oil for the pans. Mix the flour, water and yeast, rest 20 minutes, add salt, then do four sets of stretch-and-folds 30 minutes apart. Refrigerate overnight. The next day, divide into oiled pans, let rise until bubbly, dimple, top with flaky salt and rosemary, and bake at 450°F for 22 to 25 minutes.
>
> **User:** So I did a quarter of that on Tuesday in one little pan just to see. Came out dense and pale, turns out my oven runs cold. Bumped it to 475 for the full batch Friday and it was perfect.
>
> **Assistant:** Good to know about your oven. Glad it was a hit!

**Episode 2, day 6** (311 tokens)

> **User:** I want to paint my living room a dark green, Benjamin Moore Salamander. How much paint and what supplies do I need?
>
> **Assistant:** For a typical 12 by 15 room with 8-foot ceilings, the walls come to about 430 square feet. Dark colors need two coats plus a tinted primer, so get 2 gallons of paint and 1 gallon of gray-tinted primer. Supplies: a 9-inch roller with 3/8-inch nap, an angled 2.5-inch brush, a tray, painter's tape, drop cloths and spackle for holes. Cut in the edges first, then roll in a W pattern. Allow 4 hours between coats.
>
> **User:** Grabbed a sample pot instead and did a two-foot square behind the couch. Glad I did, at night it looks almost black. Going with something lighter.
>
> **Assistant:** Salamander does go very dark in low light. A lighter green should feel a lot more livable.

**Near probe.** I'm making chili for about 30 people at our office potluck next Friday. Can you give me a recipe scaled for that?

*Follows if:* The reply recommends making a small test batch before cooking the full 30-person amount.

**Far probe.** I need to email our 2,000 customers about a price increase next month. Can you draft the newsletter?

*Follows if:* The reply recommends sending it first to a small subset or test group of real customers and checking the response before sending to the full list. A test email sent only to yourself does not count.

### s0r11

**Rule.** This user can't act on plans laid out as 'Day 1', 'Week 2' or loose intervals. Nothing goes on their calendar and the plan slides. They follow a plan only when each step is tied to a real weekday or calendar date.

**What the model does by default.** A typical assistant structures plans as Day 1/Day 2 or Week 1/Week 2, or gives intervals like 'every few days', without naming actual weekdays or dates.

**Episode 1, day 0** (308 tokens)

> **User:** My sister's wedding is in three weeks and I promised a photo slideshow. I have nothing yet. Can you make me a plan?
>
> **Assistant:** Very doable. Week 1: collect photos. Text family asking for their favorites, pull from your phone and social media, and aim for 80 to 120 images. Week 2: sort and build. Arrange them roughly chronologically, pick 3 or 4 songs, and assemble it in Google Slides, Canva or iMovie at 5 to 6 seconds per photo. Week 3: polish. Watch it start to finish, cut weak shots, check timing against the music, and export a backup copy to a USB drive.
>
> **User:** Kind of stalled. I never really pinned down when week 1 started, and now it's the 14th, the wedding's the 28th, and I've got maybe 20 photos.
>
> **Assistant:** Still enough time. If you start collecting today and build next weekend, two weeks works.

**Episode 2, day 2** (327 tokens)

> **User:** I'm on a 2-week trial of a Python course with 12 lessons. Want to finish before it bills me. How should I pace it?
>
> **Assistant:** With 12 lessons in 14 days, aim for about one a day with a couple of buffer days. Days 1 to 2: lessons 1 and 2, setup and basics. Days 3 to 5: lessons 3 to 5, data types and loops. Day 6: review and catch-up. Days 7 to 10: lessons 6 to 9, functions and files. Days 11 to 12: lessons 10 and 11. Day 13: lesson 12 and the final project. Day 14: buffer. Cancel before the trial ends if you don't want to continue.
>
> **User:** Got through 3 lessons. Nothing ever went into my calendar, and 'Day 7' never lined up with any actual day for me. It renews Sunday.
>
> **Assistant:** You can still sprint it. Two lessons a night for the rest of the week gets you through the remaining nine.

**Near probe.** My driver's permit test is in about two weeks. Can you help me make a study plan?

*Follows if:* The plan assigns its tasks to named weekdays or calendar dates (e.g. 'Monday', 'Oct 7'), not 'Day 1'/'Week 1' labels, and it is not unscheduled.

**Far probe.** My houseplants keep dying. How often should I be watering and fertilizing them? I've got a pothos, a snake plant and a fiddle leaf fig.

*Follows if:* The reply ties watering or feeding to specific named weekdays or dates (e.g. 'water the pothos every Sunday'), not only intervals like 'every 7 to 10 days' or 'when the soil is dry'.

### s0r12

**Rule.** This user has no computer and does everything on a smartphone. Help that depends on desktop software, a laptop, keyboard shortcuts, browser extensions or typing a lot on a full keyboard goes unused or gets abandoned. Help works only when every step can be done in a phone app or mobile browser.

**What the model does by default.** A typical assistant gives desktop-first instructions: Mac or Windows programs like Preview, Acrobat, Word, Excel or Photoshop, keyboard shortcuts such as Ctrl+C, browser extensions, or 'install this on your computer', and doesn't mention a phone-only route.

**Episode 1, day 1** (277 tokens)

> **User:** I need to combine three scanned pages into one PDF for a rental application. How do I do that?
>
> **Assistant:** Easy fix. On a Mac, open the first PDF in Preview, turn on the sidebar with View > Thumbnails, then drag the other files into the sidebar and choose File > Export as PDF. On Windows, the free tool PDFsam Basic works well: install it, pick Merge, add your three files in order and click Run. If you have Adobe Acrobat, use Tools > Combine Files. Check the page order before you save, because landlords do notice.
>
> **User:** Couldn't do any of those. Ended up screenshotting each page on my phone and attaching three images instead. Hopefully they don't mind.
>
> **Assistant:** That should be fine. Most landlords care more about getting the documents than the format. If they ask for one file, just let me know.

**Episode 2, day 3** (337 tokens)

> **User:** My resume formatting is a mess. The bullet points don't line up and the spacing jumps all over the place. Any tips?
>
> **Assistant:** Try this in Word or Google Docs. Select everything with Ctrl+A, then clear formatting with Ctrl+Space (or Ctrl+\ in Docs). Rebuild the bullets with Home > Bullets so they all share one style. Fix spacing under Format > Line & paragraph spacing, set to 1.0 with 6pt after. Use Tab and Shift+Tab to line up indent levels. Last, turn on Show formatting marks (Ctrl+Shift+8) to find stray spaces.
>
> **User:** Ha, there's no ctrl key on my screen. I poked around in the Docs app by tapping on things and got the bullets mostly lined up. Spacing is still a bit weird but whatever.
>
> **Assistant:** Glad the bullets are sorted. Uneven spacing usually comes from extra blank lines between sections, so deleting those often fixes it.

**Episode 3, day 7** (275 tokens)

> **User:** I want to finally track my monthly spending. Can you help me set something up?
>
> **Assistant:** A simple spreadsheet works well. Make columns for Date, Category, Description and Amount. Put a summary on a second tab: list your categories in column A and in B use =SUMIF(Sheet1!B:B, A2, Sheet1!D:D) to total each one. Add =SUM(B2:B12) for the monthly total, and a pie chart through Insert > Chart. Copy the tab each month so you keep a history.
>
> **User:** Tried it. Typing those formulas with my thumbs was brutal, I kept missing the brackets and gave up halfway. I'm just jotting amounts in my notes app for now.
>
> **Assistant:** Notes works fine to start. Even a plain running list gives you a clear view of where the money goes by the end of the month.

**Near probe.** How do I remove the background from a photo of my handmade candle so it looks clean for my Etsy listing?

*Follows if:* Every method in the reply can be done in a phone app or mobile browser, and the reply recommends no desktop software (like Photoshop or GIMP), no keyboard shortcuts and no computer-only steps.

**Far probe.** I want to start learning to code. Where should I begin?

*Follows if:* The reply's main recommended path can be done entirely on a smartphone (for example a mobile coding app or a phone-based coding environment), and it does not tell the user to install an editor, Python or other software on a computer.

## Seed 1

Built 2026-10-04 18:47 EDT by claude-opus-5-5. 17 candidate rules checked against an empty memory, 5 replaced. Episode tokens per day: [1716, 880, 1299, 761, 574, 770, 773, 268, 417, 514] (reserve 4,000).

| rule | episodes on days | empty-memory rate (luna / Opus) | the rule |
|---|---|---|---|
| s1r01 | 2, 5, 7 | 0.00 / 0.00 | This user stalls on any task until they have one tiny physical action they can do right now, something that takes under two minutes. Full plans and step-by-step strategies leave them frozen and they never start. A single small first move gets them going, and they carry on from there. |
| s1r02 | 1, 3, 5 | 0.00 / 0.00 | This user always has young children with them, a toddler and a baby. Any suggestion that needs long stretches of quiet, uninterrupted focus, constant attention at a stove, or a kid-free setting falls apart. Help works only when it can be done with small kids around and with frequent interruptions. |
| s1r03 | 2, 6, 8 | 0.00 / 0.00 | This user won't act on a suggestion unless they can see roughly what it costs. Options without a price attached get skipped, and they don't go looking up prices themselves. They choose among options with a cost figure shown, including '$0 / free'. |
| s1r04 | 0, 2 | 0.00 / 0.17 | This user can't act on generic product advice like 'get a moisturizer with ceramides' or 'look for full-tang steel'. Faced with a shelf of matching choices they buy nothing. They act right away when given a specific named product: brand plus model, or a specific variety. |
| s1r05 | 0, 6 | 0.17 / 0.17 | This user won't download new apps or create new accounts. Any suggestion that needs a sign-up gets abandoned at the account screen. Help works when it uses paper, things they already have, or the built-in tools on their phone (notes, reminders, calendar, bank transfers). |
| s1r06 | 2, 8 | 0.00 / 0.00 | This user gives up partway through a task when something looks, sounds or feels unexpected, assuming they've ruined it. Help works when it tells them in advance what normal looks like at each stage, such as 'it will look runny here, that's fine'. |
| s1r07 | 0, 4, 9 | 0.00 / 0.00 | This user doesn't act on factual claims or advice unless they can point to where it comes from. They check it, or they need to show it to someone else, such as their partner or landlord. Unsourced claims get set aside, even when they're correct. Help works when the key claims name a specific source, such as an organization, a law, manufacturer guidance or a publication. |
| s1r08 | 1, 3, 6 | 0.00 / 0.00 | This user makes household decisions together with their partner Dev and has to pass options along to him. Long breakdowns are something they can't relay, so the decision stalls. Help works when it includes a short, ready-to-send summary they can forward to Dev as is. |
| s1r09 | 0, 2, 4 | 0.00 / 0.00 | This user puts any list of options, items or amounts into a spreadsheet. Lists given as prose or bullets have to be split into columns by hand, so they get half-entered or abandoned. Help works when lists come in a paste-ready columnar form, such as a table or comma-separated rows with separate fields. |
| s1r10 | 0, 5 | 0.00 / 0.00 | This user buys everything for a project in one delivery order. When the needed items are scattered through a plan, they order from memory and miss some. Help works when it ends with one consolidated list of everything to buy. |
| s1r11 | 1, 3 | 0.00 / 0.00 | This user can't learn a hands-on skill or a sequence of on-screen steps from written instructions. They learn by watching, but they get lost picking from a sea of search results. Help works when it points them to a specific video, by naming a channel or creator or giving an exact search phrase. |
| s1r12 | 0, 9 | 0.00 / 0.00 | This user gives up on a plan as soon as the first option falls through, such as a missing ingredient, a booked venue or an unavailable service. They don't improvise a substitute. Help works when the main suggestion comes with an explicit backup: 'if X isn't available, do Y instead'. |

### s1r01

**Rule.** This user stalls on any task until they have one tiny physical action they can do right now, something that takes under two minutes. Full plans and step-by-step strategies leave them frozen and they never start. A single small first move gets them going, and they carry on from there.

**What the model does by default.** A typical assistant gives a structured plan with phases, steps or a schedule, starting with prep or strategy like 'set a goal', 'sort into zones' or 'gather your documents'. It does not open with one trivial action to do immediately.

**Episode 1, day 2** (275 tokens)

> **User:** My garage is so packed I can't park in it anymore. How do I even approach organizing it?
>
> **Assistant:** Here's a solid approach. First, block out a full weekend day. Divide the garage into zones: tools, sports gear, seasonal items, and things to donate. Pull everything out onto the driveway so you can see it all, then sort each item into keep, donate, sell, or trash. Before putting anything back, measure your walls and consider shelving units or wall hooks. Put the items you use most near the door and seasonal stuff up high. Finally, label bins so the system stays in place.
>
> **User:** Yeah so that didn't happen. I stood in the doorway Saturday for ten minutes not knowing what to touch. Then I just grabbed the bike and hung it on the nail by the door, and somehow that turned into clearing the whole left corner.

**Episode 2, day 5** (312 tokens)

> **User:** I need to start on my taxes and I've been avoiding it for weeks. What's the process?
>
> **Assistant:** Start by gathering your documents: W-2s or 1099s, last year's return, receipts for deductions, and any statements for interest or investments. Next, decide whether you'll use tax software, a preparer, or file yourself. Then work through income, deductions, and credits in order. Set aside a couple of evenings so you aren't rushed, and aim to finish a few weeks before the deadline in case anything is missing.
>
> **User:** Didn't do any of that list. But last night I opened the one envelope from my bank that's been sitting on my desk, and that kind of snowballed into an hour of sorting. There's a 1099-INT in it. What do I do with that?
>
> **Assistant:** Nice progress. A 1099-INT reports interest your bank paid you. You enter the amount in box 1 as interest income on your return. Most tax software has a dedicated screen for it.

**Episode 3, day 7** (268 tokens)

> **User:** I used to run a lot and want to get back into it. Can you give me a plan to restart?
>
> **Assistant:** Sure. Go three days a week, for example Monday, Wednesday and Saturday. Weeks 1 and 2: alternate 2 minutes of easy running with 2 minutes of walking for 25 minutes. Weeks 3 and 4: 4 minutes running, 1 minute walking. Week 5 onward: build toward 30 minutes of continuous running. Warm up with 5 minutes of brisk walking, keep the pace conversational, and add no more than about 10 percent per week.
>
> **User:** The whole week went by with zero runs. Then yesterday I put my running shoes on just to take the trash out, kept walking, and did twenty minutes around the block. Is it fine to count that as week 1?

**Near probe.** My closet is a complete disaster, I can barely close the door. How should I tackle it?

*Follows if:* The reply opens (in its first sentence or first item) with one specific physical action the user can do in under two minutes right now, such as 'pull out one thing you haven't worn in a year', before giving any broader plan.

**Far probe.** I've been meaning to learn Spanish for ages. Where do I begin?

*Follows if:* The reply opens (in its first sentence or first item) with one specific action doable in under two minutes right now, such as 'say these three words out loud', before any course recommendations, goals or study schedule.

### s1r02

**Rule.** This user always has young children with them, a toddler and a baby. Any suggestion that needs long stretches of quiet, uninterrupted focus, constant attention at a stove, or a kid-free setting falls apart. Help works only when it can be done with small kids around and with frequent interruptions.

**What the model does by default.** A typical assistant assumes an adult with free time and focus. It suggests long uninterrupted blocks, steady attention, floor exercises or quiet environments, and never thinks about children being present.

**Episode 1, day 1** (270 tokens)

> **User:** Can you give me a home workout? No equipment, about 30 minutes.
>
> **Assistant:** Here's a 30-minute circuit. Warm up for 5 minutes with marching in place and arm circles. Then do 3 rounds of: 15 squats, 10 push-ups, 30-second plank, 12 reverse lunges per leg, 20 mountain climbers, and 15 glute bridges, resting 60 seconds between rounds. Finish with 5 minutes of stretching: hamstrings, hip flexors, chest and shoulders. Focus on form over speed.
>
> **User:** Made it through the warmup. Then my three-year-old climbed on my back during the plank and the baby woke up screaming. We ended up doing jumping jacks together in the living room, she thought it was hilarious, so I guess that counts.

**Episode 2, day 3** (240 tokens)

> **User:** I want to cook something a bit nicer than usual for dinner Friday. Ideas?
>
> **Assistant:** A mushroom risotto feels special and isn't hard. Sauté shallots in butter, toast arborio rice for a minute, deglaze with white wine, then add warm stock one ladle at a time, stirring constantly for about 20 to 25 minutes until creamy. Stir in sautéed mushrooms, parmesan and a knob of butter at the end. Serve with a green salad and crusty bread.
>
> **User:** Risotto was a mistake. I had one kid pulling at my leg and the other needed a diaper change halfway through, and the bottom burned while I was gone. We ate the top half. It was fine-ish.

**Episode 3, day 5** (197 tokens)

> **User:** I have a 40-page report to review for work by Monday and I keep not getting through it. Any tips?
>
> **Assistant:** Block out two focused hours with your phone in another room and notifications off. Skim the executive summary and headings first to build a map, then read section by section, writing one-line notes in the margin. Take a 10-minute break after the first hour. Finish by writing a short summary of your main comments while it's fresh.
>
> **User:** Two quiet hours isn't really a thing in this house. I read the first section while they were in the bath and the rest got done in five-minute bits during cartoons. Somehow it's done.

**Near probe.** My lower back has been stiff lately. Can you give me a stretching routine?

*Follows if:* The reply explicitly accounts for young children being around, for example stretches that can be paused or done with kids present, involving the kids, or short bits fitted in between interruptions.

**Far probe.** I want to repaint my living room this weekend. How should I plan it?

*Follows if:* The reply explicitly addresses doing the job with young children around, such as keeping them safe from paint and fumes, working in short interruptible stretches, or keeping them occupied or involved.

### s1r03

**Rule.** This user won't act on a suggestion unless they can see roughly what it costs. Options without a price attached get skipped, and they don't go looking up prices themselves. They choose among options with a cost figure shown, including '$0 / free'.

**What the model does by default.** A typical assistant lists options, ideas or fixes by what they are and what they're good for. It mostly leaves out cost, or mentions it only now and then or in vague words like 'affordable'.

**Episode 1, day 2** (249 tokens)

> **User:** I need a hobby to unwind after work. Any ideas?
>
> **Assistant:** A few good options: pottery, which is tactile and very absorbing; indoor bouldering, which is social and great exercise; learning guitar, which is easy to practice at home; watercolor painting, which is relaxing and portable; or sourdough baking, which is slow and rewarding. Think about whether you want something social or solitary, active or calm, and try one for a month.
>
> **User:** I looked up pottery and the class near me is $280 for six weeks, so no. I didn't really get into checking the others. Which of those is the cheapest to actually start?
>
> **Assistant:** Probably sourdough (flour and a jar, under $10) or watercolor (a basic set and pad for about $20 to $25).

**Episode 2, day 6** (232 tokens)

> **User:** My bathroom sink drains super slowly. How do I fix it?
>
> **Assistant:** Try these in order. Pull out the pop-up stopper and clean off hair and gunk. Use a small cup plunger, covering the overflow hole with a wet cloth. If that doesn't work, use a plastic drain snake or a hand auger to pull out deeper clogs. An enzyme drain cleaner can help with buildup over time. If none of these work, the clog may be in the trap or the wall pipe, and a plumber can clear it.
>
> **User:** Went with the plunger since I knew that's like ten bucks. Didn't bother with the snake because I had no clue if it was $10 or $80. Still slow, though.

**Episode 3, day 8** (217 tokens)

> **User:** Looking for a weekend getaway within three hours of Chicago. Suggestions?
>
> **Assistant:** Lake Geneva, Wisconsin: lakeside walking path, boat tours and cozy inns. Galena, Illinois: a historic downtown, wineries and rolling hills. Saugatuck, Michigan: an artsy beach town with dunes and galleries. Starved Rock State Park: waterfalls, canyon hikes and a historic lodge. All four are easy drives and good in most seasons.
>
> **User:** We almost booked Saugatuck but had no idea what a night there would run us, so we ended up just staying home and ordering takeout.

**Near probe.** My dad's birthday is coming up and he's really into fishing. What should I get him?

*Follows if:* Every gift option in the reply comes with an approximate dollar cost.

**Far probe.** My laptop has gotten really slow over the past few months. What can I do about it?

*Follows if:* Every fix the reply suggests comes with a cost figure, including stating '$0' or 'free' for the no-cost fixes.

### s1r04

**Rule.** This user can't act on generic product advice like 'get a moisturizer with ceramides' or 'look for full-tang steel'. Faced with a shelf of matching choices they buy nothing. They act right away when given a specific named product: brand plus model, or a specific variety.

**What the model does by default.** A typical assistant describes features, ingredients or criteria to look for and stays brand-neutral, at most naming a brand as a passing example rather than making one specific pick.

**Episode 1, day 0** (234 tokens)

> **User:** My skin gets really dry and flaky in winter. What should I use?
>
> **Assistant:** Look for a fragrance-free moisturizer with ceramides, glycerin or hyaluronic acid, and apply it to slightly damp skin right after washing. A thicker cream works better than lotion in winter. Use a gentle, non-foaming cleanser, keep showers lukewarm, and run a humidifier at night if your air is dry.
>
> **User:** I stood in the pharmacy aisle for fifteen minutes reading labels, and like twelve of them said ceramides. Left with nothing. Then a coworker said she uses the CeraVe cream in the tub, so I grabbed that on the way home. It's helping.

**Episode 2, day 2** (226 tokens)

> **User:** I want one good kitchen knife instead of my junky set. What should I get?
>
> **Assistant:** An 8-inch chef's knife covers most tasks. Look for a full-tang blade, a comfortable handle that suits your grip, and good steel. German-style knives are heavier and tougher, Japanese-style are lighter and sharper but more delicate. Expect to spend a moderate amount for good quality, and pair it with a honing rod.
>
> **User:** Went to the kitchen store and there were about thirty 8-inch chef's knives. Walked out. Then my brother texted 'just get the Victorinox Fibrox' and I ordered it in two minutes. It came yesterday, love it.

**Near probe.** The grout in my shower has gone grimy and dark. What should I use to clean it?

*Follows if:* The reply recommends at least one specific named product by brand (and model or product name, e.g. 'Zep Grout Cleaner' or 'OxiClean Versatile Stain Remover') as the thing to use, not only generic ingredients like baking soda, vinegar or 'oxygen bleach'.

**Far probe.** I've got a shady corner in my backyard where nothing grows. What should I plant there?

*Follows if:* The reply names specific cultivars or varieties to buy (e.g. Hosta 'Patriot', Heuchera 'Palace Purple'), not only general plant types like 'hostas' or 'ferns'.

### s1r05

**Rule.** This user won't download new apps or create new accounts. Any suggestion that needs a sign-up gets abandoned at the account screen. Help works when it uses paper, things they already have, or the built-in tools on their phone (notes, reminders, calendar, bank transfers).

**What the model does by default.** A typical assistant readily recommends apps and services such as habit trackers, Splitwise, Goodreads, plant-care apps or budgeting apps as a main solution.

**Episode 1, day 0** (196 tokens)

> **User:** I'm trying to drink more water. How do I keep track?
>
> **Assistant:** A habit-tracking app makes it easy. WaterMinder and Plant Nanny send reminders and log each glass, and general trackers like Streaks or Habitica let you build streaks. Set a daily goal, roughly 8 glasses, and enable reminders every couple of hours. Keeping a marked bottle at your desk helps too.
>
> **User:** Downloaded the first one, hit the 'create your account' screen and closed it. I've just been making tally marks on a sticky note on the fridge. Five days straight now.

**Episode 2, day 6** (272 tokens)

> **User:** Did a cabin trip with four friends and we all paid for different stuff. How do we sort out who owes what?
>
> **Assistant:** Splitwise is made for exactly this. Everyone joins a group, logs what they paid, and it calculates the simplest set of payments to settle up. Tricount and Settle Up work similarly. Have each person add their expenses with receipts, then settle through your usual payment app.
>
> **User:** Everyone else joined Splitwise but I really didn't want another login, so I've got my stuff in my notes app. I paid $340 for the cabin and $85 for groceries. Sam paid $120 for gas, everyone else nothing. What do I owe or get back?
>
> **Assistant:** Total is $545, so $109 each. You paid $425, so you're owed $316. Sam is owed $11. The other three each owe $109.

**Near probe.** I keep forgetting to water my houseplants and two have died already. Any ideas?

*Follows if:* The reply does not recommend downloading any app or signing up for any service. Every suggestion uses physical methods or tools the user already has, such as built-in phone reminders, calendar, a note or a chart.

**Far probe.** I want to actually read more books this year instead of just buying them. How can I make it happen?

*Follows if:* The reply recommends no app download or account sign-up (e.g. no Goodreads, StoryGraph, Libby, Kindle or Audible) and relies on physical or already-available methods.

### s1r06

**Rule.** This user gives up partway through a task when something looks, sounds or feels unexpected, assuming they've ruined it. Help works when it tells them in advance what normal looks like at each stage, such as 'it will look runny here, that's fine'.

**What the model does by default.** A typical assistant gives clean step-by-step instructions focused on actions. It rarely describes what the user will see, hear or feel partway through, or which odd-looking moments are normal.

**Episode 1, day 2** (280 tokens)

> **User:** First time making bread. Simple recipe?
>
> **Assistant:** Mix 500g bread flour, 10g salt, 7g instant yeast and 350ml warm water into a dough. Knead for 10 minutes. Cover and let rise for about an hour until doubled. Shape into a loaf, place in a greased tin, and let rise 30 to 45 minutes more. Bake at 220°C for 30 to 35 minutes until golden and hollow-sounding when tapped. Cool before slicing.
>
> **User:** After mixing it was super sticky and gluey, sticking to everything, so I figured I'd messed up the water and threw it out. My friend says it's supposed to be like that at first?
>
> **Assistant:** Yes. At this hydration it's sticky at first and gets smooth and elastic as you knead. Keep going for 10 minutes before judging it.

**Episode 2, day 8** (200 tokens)

> **User:** How do I descale my drip coffee maker?
>
> **Assistant:** Fill the water reservoir with equal parts white vinegar and water. Put a paper filter in the basket and run a full brew cycle. Halfway through, switch it off and let it sit for 30 minutes, then finish the cycle. Discard the liquid, then run two or three cycles with plain water to rinse out the vinegar.
>
> **User:** Partway through it started sputtering really loudly and spitting out brown flakes, so I panicked and unplugged it. It's been sitting there full of vinegar for two days. Was that normal or did I break it?

**Near probe.** How do I make homemade yogurt?

*Follows if:* The reply includes at least two explicit notes about what the user will see, smell or feel at a middle stage and that this is normal, for example 'it will still look runny after 6 hours, that's fine' or 'a layer of yellowish liquid on top is normal'.

**Far probe.** I'm getting a new phone this weekend and need to move everything over from my old one. How do I do it?

*Follows if:* The reply includes at least two explicit notes about what the user will see partway through and that it is normal, for example 'the progress bar may sit at the same spot for a long time' or 'photos may take hours to show up'.

### s1r07

**Rule.** This user doesn't act on factual claims or advice unless they can point to where it comes from. They check it, or they need to show it to someone else, such as their partner or landlord. Unsourced claims get set aside, even when they're correct. Help works when the key claims name a specific source, such as an organization, a law, manufacturer guidance or a publication.

**What the model does by default.** States facts and recommendations confidently with no named source or attribution.

**Episode 1, day 0** (360 tokens)

> **User:** How often should I be watering my succulents? They sit in a south-facing window.
>
> **Assistant:** Succulents in a bright south window do best with a 'soak and dry' approach. Water thoroughly until it runs out the drainage hole, then let the soil dry out completely before watering again. In spring and summer that's usually about every 10 to 14 days. In winter they slow down a lot, so cut back to roughly once every 3 to 4 weeks. Overwatering is the most common way people lose succulents, so if you're unsure, wait a few more days. A gritty cactus mix and a pot with drainage make a big difference too.
>
> **User:** Huh, I've been doing every week all year. Before changing anything I went looking for where the winter cutback comes from, couldn't pin it down, so I just kept watering weekly. Where does that actually come from?
>
> **Assistant:** It's mainstream horticulture advice. University extension services' cactus and succulent care guides and the Royal Horticultural Society both describe reducing water during winter dormancy. Since you're on weekly now, try every two weeks this month and watch for shriveling.

**Episode 2, day 4** (297 tokens)

> **User:** I moved out of my apartment in California five weeks ago and my landlord still hasn't returned my deposit or said anything. Is that allowed?
>
> **Assistant:** Generally no. In California, a landlord has 21 days after you move out to either return your full deposit or send an itemized statement of deductions, with receipts for larger repairs. At five weeks, yours is past that. A good next step is a short, polite email asking for the deposit within a set deadline, say 10 days, and mentioning that you know about the 21-day requirement. If they still don't respond, small claims court is the usual route, and courts can award a penalty of up to twice the deposit if it was withheld in bad faith. Keep copies of your lease, move-out photos and any messages.
>
> **User:** I got halfway through the email and stopped at the 21 day part. If he writes back 'says who?' I've got nothing to point to, so it's still sitting in my drafts.

**Episode 3, day 9** (243 tokens)

> **User:** Can you freeze milk? Grabbed two gallons on sale and there's no way we finish them in time.
>
> **Assistant:** Yes, milk freezes well. Pour out a cup or so first since it expands, then freeze it for up to about three months. Thaw it in the fridge over a day or two and shake it well before using, because the fat can separate and look a little grainy. That's normal and it's still fine. Thawed milk is great for cooking, baking, coffee and smoothies, and plenty of people drink it as is, though whole milk changes texture more than skim.
>
> **User:** Second gallon ended up going sour. Dev was convinced freezing ruins milk and all I had was 'the chatbot said it's fine,' so it never went in the freezer.

**Near probe.** Should I be rotating or flipping my mattress, and how often?

*Follows if:* The reply names at least one specific source (e.g., a named organization, mattress manufacturer's guidance, or publication) for its main recommendation.

**Far probe.** I'm writing a blog post about the history of coffee. Can you give me a few interesting facts I could include?

*Follows if:* Every fact given is attributed to a specific named source (a book, historian, institution, or publication), not just stated or credited to 'legend'.

### s1r08

**Rule.** This user makes household decisions together with their partner Dev and has to pass options along to him. Long breakdowns are something they can't relay, so the decision stalls. Help works when it includes a short, ready-to-send summary they can forward to Dev as is.

**What the model does by default.** Gives a thorough comparison or analysis written only to the user, with no short summary meant for forwarding.

**Episode 1, day 1** (306 tokens)

> **User:** We need a new sofa. Leather or fabric? We have a cat who scratches stuff.
>
> **Assistant:** With a scratcher, both have tradeoffs. Leather doesn't snag the way woven fabric does and wipes clean easily, but claws leave punctures and scratches you can't really repair, especially on softer aniline leather. Fabric varies a lot: loose weaves and textured fabrics like tweed get pulled apart fast, while tightly woven microfiber or performance fabrics hold up much better because claws can't hook in. Microfiber is often the cat owner's pick: cheaper, durable, and hair brushes off easily. If you go leather, choose a protected or pigmented leather. Either way, a scratching post near the sofa helps redirect the cat.
>
> **User:** Dev texted asking which one and why, and I tried to explain weaves and leather types over text and made a mess of it. We still haven't ordered anything.

**Episode 2, day 3** (296 tokens)

> **User:** Two internet plans: 300 Mbps for $50 or 1 Gig for $80. Two of us work from home. Which one?
>
> **Assistant:** For two people working from home, 300 Mbps is almost certainly enough. A video call uses around 3 to 4 Mbps, and even 4K streaming needs about 25. Two calls at once plus streaming and downloads would stay well under 100 Mbps. Gigabit helps if you regularly move very large files, like video editing or big cloud backups, or have lots of devices running at once. Also check upload speeds: if the 300 plan only has 10 to 20 Mbps up, that could matter more for calls than download. If upload is decent, save the $30 a month, which is $360 a year.
>
> **User:** I copied bits of that into a message to Dev and it came out jumbled. He asked about the upload thing and I couldn't answer, so we're still on the old plan.

**Episode 3, day 6** (269 tokens)

> **User:** We're paying for Netflix, Hulu, Max, Disney+ and Peacock. Which should we cancel?
>
> **Assistant:** It depends on what you actually watch, but here's a way to decide. Check your viewing history on each for the last two months. Anything you haven't opened in a month is an easy cut. Lots of people keep one main service year-round and rotate the rest, subscribing for a month when a show they want drops, then cancelling. Disney+ and Hulu can be bundled cheaply if you want both. Peacock and Max are often first to go unless you follow specific shows or sports there. Rotating could get you from five services to two at a time, saving roughly $30 to $40 a month.
>
> **User:** Tried reading this to Dev at dinner and lost him around the rotating part. Haven't cancelled a single one yet.

**Near probe.** Should we get a stand mixer or a bread machine? We bake maybe twice a month.

*Follows if:* The reply includes a short, clearly separate summary of a few sentences, written so it can be forwarded as is to another person (e.g., a partner).

**Far probe.** I got an offer for a job paying about 8% more than my current one, but it's at a smaller company. What should I be thinking about?

*Follows if:* The reply includes a short, clearly separate summary of a few sentences, written so it can be forwarded as is to another person (e.g., a partner).

### s1r09

**Rule.** This user puts any list of options, items or amounts into a spreadsheet. Lists given as prose or bullets have to be split into columns by hand, so they get half-entered or abandoned. Help works when lists come in a paste-ready columnar form, such as a table or comma-separated rows with separate fields.

**What the model does by default.** Gives lists as bullets or running prose, with name and details mixed together in one line.

**Episode 1, day 0** (312 tokens)

> **User:** Give me some easy weeknight dinner ideas, ideally under 30 minutes.
>
> **Assistant:** Here are some quick ones: sheet-pan chicken sausage with peppers and potatoes, about 25 minutes. Shrimp tacos with slaw, 20 minutes. Pasta with garlic, spinach and white beans, 20 minutes. Fried rice with frozen veg and eggs, 15 minutes. Black bean quesadillas, 15 minutes. Teriyaki salmon with rice, 25 minutes. Chickpea curry with coconut milk, 25 minutes. Turkey burgers with a side salad, 20 minutes. Pesto gnocchi with cherry tomatoes, 15 minutes. Veggie frittata, 25 minutes.
>
> **User:** Thanks. Getting these into my dinners sheet took forever, splitting each into dish and minutes by hand. Gave up after six.

**Episode 2, day 2** (269 tokens)

> **User:** We're redoing our budget. What recurring costs do people usually forget?
>
> **Assistant:** The common ones: annual subscriptions like Amazon Prime, around $139 a year. Renters insurance, roughly $15 to $25 a month. Software or cloud storage renewals, often $50 to $100 a year. Gifts and holidays, which many people put at $50 to $100 a month spread out. Pet costs like vet checkups and food. Replacing phones and electronics, maybe $30 a month set aside. Toiletries and cleaning supplies, $30 to $60 a month. Card annual fees. And quarterly taxes if anyone does freelance work.
>
> **User:** Pasted that into our budget sheet and the whole thing landed in one cell. Started retyping each item and amount into their own columns and didn't finish.

**Episode 3, day 4** (277 tokens)

> **User:** Recommend some sci-fi novels for someone who loved Project Hail Mary.
>
> **Assistant:** You'd probably enjoy: The Martian by Andy Weir, same humor and problem-solving. Children of Time by Adrian Tchaikovsky, big ideas about alien intelligence. The Long Way to a Small, Angry Planet by Becky Chambers, warm and character-driven. Seveneves by Neal Stephenson, hard science on an epic scale. Murderbot Diaries: All Systems Red by Martha Wells, short and funny. Old Man's War by John Scalzi, fast and witty. Dark Matter by Blake Crouch, a twisty page-turner.
>
> **User:** Dropped these into my reading tracker and title, author and your notes all got mashed into column A. Haven't fixed them yet.

**Near probe.** Can you recommend some good history podcasts? I've got a lot of listening time coming up.

*Follows if:* The recommendations are given in a paste-ready columnar format (a table or comma/tab-separated rows) with separate fields for at least the name and one other attribute.

**Far probe.** What household chores should we be doing weekly, monthly and yearly to keep our place in good shape?

*Follows if:* The chores are given in a paste-ready columnar format (a table or comma/tab-separated rows) with chore and frequency as separate fields.

### s1r10

**Rule.** This user buys everything for a project in one delivery order. When the needed items are scattered through a plan, they order from memory and miss some. Help works when it ends with one consolidated list of everything to buy.

**What the model does by default.** Mentions supplies inline throughout the plan or tips, with no separate shopping list.

**Episode 1, day 0** (320 tokens)

> **User:** Throwing a small birthday party at home for my niece, she's turning 7. About eight kids. Can you help me plan it?
>
> **Assistant:** For eight 7-year-olds, two hours is plenty. Start with a craft as kids arrive, like making their own bead bracelets, so you'll want pony beads and elastic string. Then a couple of games: freeze dance and a balloon pop relay, so grab a pack of balloons and put together a playlist. Do cupcakes instead of a cake since they're easier to serve, and don't forget candles and a lighter. Pizza is the easiest food, plus juice boxes and some fruit. Paper plates, napkins and a plastic tablecloth make cleanup quick. End with small goodie bags with stickers and the bracelet they made.
>
> **User:** I did the delivery order going off memory and scrolling back through all that. Forgot the candles and the elastic string, so no bracelets, and we sang to a pile of plain cupcakes.

**Episode 2, day 5** (261 tokens)

> **User:** Help me set up a cozy reading nook in the corner of our living room.
>
> **Assistant:** Corners work great for this. Start with the seat: a comfy armchair, or a big floor cushion if space is tight. Lighting matters most, so add a floor lamp with a warm bulb positioned over your shoulder, or a plug-in wall sconce if there's no floor space. Drape a soft throw over the chair and add a pillow for back support. A small side table gives you somewhere for tea. A narrow shelf or basket keeps your current books within reach. Finish with a small rug to define the space, and maybe a plant to make it feel tucked away.
>
> **User:** Placed the order last night going back and forth through this. Got the chair, the throw and the rug, but no lamp, so I can't actually read there after dark.

**Near probe.** I want to turn our spare room into a proper guest room before my parents visit. Can you help?

*Follows if:* The reply includes one consolidated, separate list of all items to buy, gathered in one place (e.g., at the end).

**Far probe.** We throw out way too much food. How can we cut down on food waste at home?

*Follows if:* The reply includes one consolidated, separate list of the physical items to buy (e.g., containers, labels, freezer bags), apart from the tips.

### s1r11

**Rule.** This user can't learn a hands-on skill or a sequence of on-screen steps from written instructions. They learn by watching, but they get lost picking from a sea of search results. Help works when it points them to a specific video, by naming a channel or creator or giving an exact search phrase.

**What the model does by default.** Gives written step-by-step instructions, at most adding a generic 'you can find tutorials on YouTube'.

**Episode 1, day 1** (304 tokens)

> **User:** I bought a whetstone. How do I sharpen my chef's knife on it?
>
> **Assistant:** Soak the stone for 10 to 15 minutes if it's a water stone, until bubbles stop. Set it coarse side up on a damp towel so it doesn't slide. Hold the knife at about 15 to 20 degrees, roughly two stacked coins under the spine. With light pressure, push the blade across the stone heel to tip, as if slicing a thin layer off it. Do about 10 strokes, then feel for a burr, a slight rough lip, along the opposite edge. Switch sides and repeat. Then flip to the fine side and do the same with lighter strokes.
>
> **User:** I couldn't picture the angle or the heel-to-tip motion from that. Went to YouTube, got a wall of videos with different stones and knives, clicked one and quit halfway because it didn't look like my setup. Knife's still dull.

**Episode 2, day 3** (225 tokens)

> **User:** How do you fold a fitted sheet? Mine always ends up a lump.
>
> **Assistant:** Hold the sheet inside out with your hands in two adjacent corners along a short edge. Bring your right hand over to your left and tuck the right corner over the left so the corners nest. Do the same with the other two corners. Then fold the two nested pairs together so all four corners are stacked. Lay it flat, straighten the edges into a rectangle with the elastic curved inward, fold in thirds lengthwise, then fold into a square.
>
> **User:** Got lost at the second tuck. Then my sister sent me a short video of a woman doing it and I got it on the first go. Folded all three sheets.

**Near probe.** How do I tie a Windsor knot? I have a wedding... actually never mind the occasion, just how do I tie one?

*Follows if:* The reply points to a specific video by naming a channel or creator, or by giving an exact search phrase to type, rather than only written steps or a generic 'look it up on YouTube'.

**Far probe.** How do I make a pivot table in Google Sheets?

*Follows if:* The reply points to a specific video by naming a channel or creator, or by giving an exact search phrase to type, rather than only written steps or a generic 'look it up on YouTube'.

### s1r12

**Rule.** This user gives up on a plan as soon as the first option falls through, such as a missing ingredient, a booked venue or an unavailable service. They don't improvise a substitute. Help works when the main suggestion comes with an explicit backup: 'if X isn't available, do Y instead'.

**What the model does by default.** A typical assistant gives one recommendation or a list of parallel options. It doesn't frame any of them as a fallback for when the main plan fails, and it doesn't say what to swap in if a key ingredient, booking or service isn't available.

**Episode 1, day 0** (294 tokens)

> **User:** Where should I take my dad for his birthday dinner Friday? He loves seafood and we're in Halifax, nothing too fancy.
>
> **Assistant:** The Five Fishermen downtown would be a great fit. It's a historic building with a relaxed feel and excellent seafood. The lobster and the seafood chowder are favourites, and it's special enough for a birthday without being stuffy. I'd book a table for around 6:30 so you're not rushed. Happy birthday to your dad!
>
> **User:** Tried to book Thursday and they were full all night Friday. So we ended up ordering pizza at his place. He didn't mind but it wasn't really the birthday dinner I had in mind.
>
> **Assistant:** Sorry it didn't work out. Pizza with family still counts as a celebration, but I get that it wasn't what you'd planned. Maybe a belated seafood dinner some weekend soon?

**Episode 2, day 9** (271 tokens)

> **User:** I've got four really brown bananas. Give me a simple banana bread recipe I can make tonight?
>
> **Assistant:** Sure! Mash 3 to 4 ripe bananas. Stir in 1/3 cup melted butter, 3/4 cup sugar, 1 egg, 1 teaspoon vanilla and 1/2 cup buttermilk. Add 1 teaspoon baking soda, a pinch of salt and 1 1/2 cups flour, then mix until just combined. Pour into a greased loaf pan and bake at 350°F for 55 to 65 minutes, until a toothpick comes out clean. Let it cool 10 minutes before slicing.
>
> **User:** Got everything out and then realized I didn't have buttermilk. So no banana bread, and the bananas went in the compost this morning.

**Near probe.** Where should I take three friends for brunch this Sunday? We're in Portland, Oregon, and we like somewhere with good coffee.

*Follows if:* The reply explicitly names a backup place or plan to use if the main pick is full, has a long wait or is closed (for example, 'if the line is too long, go to Y').

**Far probe.** I have a 7am flight out of Denver on Tuesday and no car. What's the best way to get to the airport?

*Follows if:* The reply recommends a primary way to get there and explicitly gives a fallback to use if that one fails (for example, 'if no rideshare is available at 4:30am, take X instead'), rather than only listing options side by side.

## Seed 2

Built 2026-10-04 19:03 EDT by claude-opus-5-5. 14 candidate rules checked against an empty memory, 2 replaced. Episode tokens per day: [1750, 434, 1288, 463, 1106, 1007, 512, 261, 442, 504] (reserve 4,000).

| rule | episodes on days | empty-memory rate (luna / Opus) | the rule |
|---|---|---|---|
| s2r01 | 0, 2, 4 | 0.00 / 0.00 | This user won't make a change unless they know how to undo it. Suggestions to change settings, their home, their appearance, a service or a routine stay untried unless the reply also says how to go back if it doesn't work out. |
| s2r02 | 0, 5, 9 | 0.00 / 0.00 | This user only ever does the least-effort version of a task. Thorough, multi-part approaches get dropped after a step or two. Help works when it opens with the bare-minimum version that gets most of the result, and marks anything beyond that as optional. |
| s2r03 | 2, 4, 6 | 0.00 / 0.00 | This user decides whether to start a task based on how long it will take. Without a total time estimate up front, they put it off until 'when I have time' or start it at a bad moment. Help works when it says at the start how long the whole thing takes. |
| s2r04 | 0, 5, 8 | 0.00 / 0.00 | This user skips any step whose purpose they don't understand, so bare instructions get partly followed and things fail. Help works when every step comes with a short reason it matters. |
| s2r05 | 1, 5 | 0.00 / 0.00 | This user works as a line cook. Explanations of unfamiliar topics only make sense to them when mapped onto restaurant-kitchen analogies. Standard explanations leave them confused until they translate them into kitchen terms themselves. |
| s2r06 | 0, 6 | 0.00 / 0.00 | This user buys nearly everything second-hand. Recommendations for new products go unused. Help works when it points them to used options: where to look, which models or sizes to search for used, and what to check before paying. |
| s2r07 | 3, 9 | 0.00 / 0.00 | This user has no car. They get around on foot, by bike and by public transit. Suggestions that need driving, such as out-of-town places, suburban big-box stores or hauling bulky things, don't happen. Help works when everything can be reached on transit or on foot, or gets delivered or picked up. |
| s2r08 | 1, 3 | 0.00 / 0.00 | This user acts on answers literally and has been burned when a guess sounded like a fact. Help works when the reply says how sure it is, separates what is solid from what is uncertain and names the specific thing to double-check. |
| s2r09 | 0, 2, 5 | 0.17 / 0.17 | This user won't make phone calls. Any step that needs them to phone a person (customer service, a business, a carrier, a tradesperson) gets put off forever. Help works only when every step can be done by online chat, email, web form, in-app messaging or in person. |
| s2r10 | 2, 4, 7 | 0.17 / 0.00 | This user can't tell when a task is finished, so they either overdo it for hours or stop unsure. Help works when it gives a concrete, checkable 'you're done when...' condition for the task. |
| s2r11 | 0, 2 | 0.00 / 0.00 | This user lives in an apartment with thin walls and neighbours who complain. Anything noisy, such as jumping, drilling, blending, loud music or practising instruments, gets stopped. Help works only when it can be done quietly. |
| s2r12 | 4, 8 | 0.00 / 0.00 | This user forgets new recurring tasks unless they're attached to something they already do every day or week. Schedules like 'every day' or 'twice a week' slip. Help works when each recurring action is tied to a specific existing routine moment, such as 'right after you start the coffee'. |

### s2r01

**Rule.** This user won't make a change unless they know how to undo it. Suggestions to change settings, their home, their appearance, a service or a routine stay untried unless the reply also says how to go back if it doesn't work out.

**What the model does by default.** A typical assistant explains how to make the change and maybe why it's a good idea. It doesn't say how to reverse it or what going back would involve.

**Episode 1, day 0** (308 tokens)

> **User:** My iPhone is dead by like 3pm every day. Anything I can do besides carrying a charger around?
>
> **Assistant:** A few changes usually help a lot. Turn on Low Power Mode in Settings > Battery, which cuts background activity. In Settings > General > Background App Refresh, switch it off for apps that don't need it. Turn on Auto-Brightness or lower the brightness. In Settings > Privacy > Location Services, set apps to 'While Using' instead of 'Always'. Last, check Settings > Battery > Battery Health. If maximum capacity is under about 80%, a battery replacement may be the real fix.
>
> **User:** Didn't end up changing any of it. I kept picturing my work email or the bus app quietly breaking, and me not remembering which switches I'd flipped.
>
> **Assistant:** That's understandable. Low Power Mode is a single toggle, so it's an easy one to start with if you want to try something small.

**Episode 2, day 2** (287 tokens)

> **User:** Thinking about painting the wall behind my bed a dark forest green. Good idea, or will it make the room feel tiny?
>
> **Assistant:** Dark accent walls often make a room feel cozier and deeper, not smaller, especially behind a bed where the color frames the headboard. Pick a green with some gray or black in it so it looks rich rather than bright. Get a sample pot and paint a big swatch, about two feet square, then look at it in morning and evening light. Use an eggshell finish, tape the edges carefully and plan on two coats.
>
> **User:** Got the sample and it looks great on the wall. But it's a rental, and I keep stalling because I have no idea what getting it back to white would involve if I'm sick of it by spring.
>
> **Assistant:** Going back is very doable. Usually it's one coat of stain-blocking primer and then two coats of white, about a weekend's work.

**Episode 3, day 4** (290 tokens)

> **User:** I want curtain bangs. What should I tell the stylist so I don't end up with blunt bangs by accident?
>
> **Assistant:** Bring two or three photos of curtain bangs on someone with a hair texture like yours. Say you want them longest at the sides, about cheekbone length, and shortest in the middle, around the bridge of your nose, with a center part. Ask her to cut them dry or check them dry, because they shrink up when they dry. Ask for a quick lesson on styling them with a round brush or a blow-dryer, since that's what makes them fall right.
>
> **User:** Sat down in the chair and told her never mind. All I could think was, if they look bad, how long until they're gone, and what do I do with them in the meantime?
>
> **Assistant:** Fair enough. Curtain bangs tend to grow into face-framing layers fairly fast, and they're easy to pin back if you don't like them.

**Near probe.** The autocorrect on my Android keyboard keeps wrecking my texts. What should I change?

*Follows if:* The reply explains how to turn each suggested setting back on or restore the original behavior (or says exactly where to toggle it back).

**Far probe.** I'm thinking of switching my phone plan from Verizon to Mint Mobile to save money. How do I do it?

*Follows if:* The reply explains how the user could go back to Verizon if Mint doesn't work out, for example porting the number back or what they'd lose or pay, not only how to switch to Mint.

### s2r02

**Rule.** This user only ever does the least-effort version of a task. Thorough, multi-part approaches get dropped after a step or two. Help works when it opens with the bare-minimum version that gets most of the result, and marks anything beyond that as optional.

**What the model does by default.** A typical assistant gives a complete, thorough method with many steps of equal weight. It doesn't separate a minimal version from extras.

**Episode 1, day 0** (320 tokens)

> **User:** Our bathroom is gross and my in-laws arrive Saturday. How do I deep clean it?
>
> **Assistant:** Here's a full deep clean. Clear everything off the counters and the tub ledge. Spray the shower and tub with a bathroom cleaner and let it sit 10 minutes before scrubbing. Scrub the grout with a baking soda paste and an old toothbrush. Soak the shower head overnight in a bag of vinegar to remove scale. Clean the toilet inside and out, including the base and behind it. Wipe the mirror and fixtures, dust the vent fan, then mop the floor. Finally, wash the bath mat, the towels and the shower curtain liner.
>
> **User:** Real talk: I sprayed the shower, wiped the sink and mirror and put out fresh towels. That alone made it look way better. The rest never happened.
>
> **Assistant:** Those are the spots guests actually notice, so that was a good call. Hope the visit goes well!

**Episode 2, day 5** (256 tokens)

> **User:** I want to actually stick to a budget this year. How do I start?
>
> **Assistant:** Start by pulling three months of bank and card statements. Sort every expense into categories such as housing, groceries, dining out, transport and subscriptions. Set a monthly limit for each category, using a 50/30/20 split of needs, wants and savings as a starting point. Log every purchase as it happens, in a spreadsheet or an app like YNAB, and do a full review at the end of each month to adjust the limits.
>
> **User:** The category sorting died on day three. What I'm actually still doing is checking my balance on Fridays and moving whatever's left over to savings. Weirdly, it's working.
>
> **Assistant:** That's a real system. It's basically a weekly sweep into savings. If it's working, keep it going.

**Episode 3, day 9** (261 tokens)

> **User:** I'm going to Mexico City in four months. How do I learn some Spanish before then?
>
> **Assistant:** Four months is enough for useful travel Spanish. Do 15 minutes of an app like Duolingo every day for vocabulary. Work through a beginner grammar workbook a couple of times a week. Listen to a podcast like Coffee Break Spanish on your commute. Book a weekly 30-minute conversation lesson on italki so you practice speaking. Put Spanish labels on things around your home, and watch shows with Spanish audio and subtitles.
>
> **User:** Update: the only thing that survived is about five minutes of Duolingo while my coffee brews. Is that even doing anything?
>
> **Assistant:** It does add up. Five minutes a day over four months builds a decent base of travel words.

**Near probe.** My closet is a total disaster. How do I organize it?

*Follows if:* The reply opens with a clearly labeled minimal or quick version (a few low-effort actions) before any fuller process, and marks further steps as optional.

**Far probe.** I need to write a cover letter for a marketing coordinator job. How should I go about it?

*Follows if:* The reply leads with a bare-minimum, low-effort way to produce the letter (for example a short fill-in structure or the one or two things that matter most) and presents any more thorough steps as optional extras.

### s2r03

**Rule.** This user decides whether to start a task based on how long it will take. Without a total time estimate up front, they put it off until 'when I have time' or start it at a bad moment. Help works when it says at the start how long the whole thing takes.

**What the model does by default.** A typical assistant goes straight into steps or a recipe. It gives no overall time estimate, or mentions durations only inside individual steps.

**Episode 1, day 2** (247 tokens)

> **User:** My wiper blades streak really badly. How do I replace them?
>
> **Assistant:** First, check your owner's manual or the auto store's lookup for the right blade lengths, since the driver and passenger sides are often different sizes. Lift the wiper arm away from the windshield. Press the small tab where the blade meets the arm and slide the old blade off. Slide the new blade onto the hook until it clicks. Lower the arm gently, repeat on the other side, then test with washer fluid.
>
> **User:** Bought the blades Sunday and they're still sitting in my trunk. I couldn't tell if this was a two-minute job or something that eats an afternoon, so I just never started.
>
> **Assistant:** It's quick, about five minutes for both blades once you've done the first one.

**Episode 2, day 4** (322 tokens)

> **User:** Can you give me a good classic lasagna recipe for tonight?
>
> **Assistant:** Brown 1 lb of Italian sausage with an onion and garlic, add a 28 oz can of crushed tomatoes and simmer for 30 minutes. Mix 15 oz of ricotta with an egg, parmesan and parsley. Boil 12 noodles until just shy of al dente. In a 9x13 pan, layer sauce, noodles, the ricotta mix and mozzarella, three times, and finish with sauce and cheese. Cover with foil and bake at 375°F for 25 minutes, uncover and bake 25 more. Let it rest 15 minutes before cutting.
>
> **User:** Made it and it was delicious, but I started around 6:30 thinking it was a normal dinner and we didn't eat until almost 9. The kids were melting down.
>
> **Assistant:** Sorry about that. Between the sauce, the assembly, the bake and the rest, it does run long.

**Episode 3, day 6** (230 tokens)

> **User:** How do I renew my US passport online?
>
> **Assistant:** You can use the State Department's online renewal if your passport was issued when you were 16 or older, within the last 15 years, and isn't damaged. Create an account on the MyTravelGov site, fill out the application, upload a digital passport photo that meets the photo requirements, and pay the fee by card. Keep your old passport until you receive instructions, and track the status in your account.
>
> **User:** I've had the form open in a tab for three days. Couldn't figure out how big a job it was, so every evening I closed the laptop and said 'later.'
>
> **Assistant:** If you have a photo ready it usually goes faster than people expect. The photo is the main thing that slows people down.

**Near probe.** How do I descale my coffee maker?

*Follows if:* Within the first two sentences, the reply states a total time estimate for the whole job (including any soaking or rinse cycles).

**Far probe.** I want to set up automatic monthly investing into an index fund. Walk me through it?

*Follows if:* Near the start, before the steps, the reply states roughly how long the whole setup will take the user.

### s2r04

**Rule.** This user skips any step whose purpose they don't understand, so bare instructions get partly followed and things fail. Help works when every step comes with a short reason it matters.

**What the model does by default.** A typical assistant gives a clean list of imperative steps, with reasons for only a few steps or none.

**Episode 1, day 0** (331 tokens)

> **User:** Can you give me a simple crusty bread recipe? I have a Dutch oven.
>
> **Assistant:** Mix 3 cups of flour with 1.5 cups of warm water and let it rest 30 minutes. Add 1.5 teaspoons of salt and 1/2 teaspoon of yeast and mix well. Cover and let it rise 12 to 18 hours. Shape it into a ball on a floured surface and let it rise 1 more hour. Put the empty Dutch oven in the oven and preheat to 450°F for 45 minutes. Bake the dough covered for 30 minutes, then uncovered for 15.
>
> **User:** Came out dense and pale on the bottom. I'll be honest, I skipped the 30-minute rest and only heated the pot for 10 minutes. Neither one seemed like it was doing anything.
>
> **Assistant:** Those two steps matter more than they look. The rest lets the flour fully absorb the water, and a fully heated pot gives the crust and rise their burst.

**Episode 2, day 5** (227 tokens)

> **User:** Just bought an external hard drive to back up my Mac. How do I set it up?
>
> **Assistant:** Plug in the drive. Open Disk Utility, select the external drive, click Erase and choose APFS as the format. Then go to System Settings > General > Time Machine, click Add Backup Disk, pick the drive and confirm. The first backup can take a few hours, and after that it runs automatically whenever the drive is connected.
>
> **User:** I skipped the erase step since the drive was brand new and empty, didn't see the point. Now Time Machine says it can't use the disk.
>
> **Assistant:** Many new drives come formatted for Windows. Erasing it as APFS should let Time Machine use it.

**Episode 3, day 8** (229 tokens)

> **User:** Our wooden fence is peeling. How do I repaint it?
>
> **Assistant:** Scrape off all loose and flaking paint with a paint scraper. Sand rough spots smooth. Wash the fence with a deck cleaner or a mild detergent and let it dry for two days. Spot-prime any bare wood with an exterior primer. Apply two coats of exterior acrylic latex paint, waiting the recommended time between coats.
>
> **User:** Two months later the bare patches are peeling again. I skipped the primer. It just seemed like an extra coat nobody would see.
>
> **Assistant:** Unfortunately that's the usual result. You'll need to scrape those spots again and prime them before repainting.

**Near probe.** I just got a new cast iron skillet. How do I season it?

*Follows if:* Every step in the reply comes with an explicit reason it is done (what it achieves or what goes wrong without it).

**Far probe.** I have a salary negotiation call next week. How should I prepare?

*Follows if:* Each recommended preparation step or tactic in the reply includes a stated reason explaining why it helps.

### s2r05

**Rule.** This user works as a line cook. Explanations of unfamiliar topics only make sense to them when mapped onto restaurant-kitchen analogies. Standard explanations leave them confused until they translate them into kitchen terms themselves.

**What the model does by default.** A typical assistant explains a topic in its own standard terms, or uses generic analogies like libraries or desks. It doesn't use cooking or restaurant-kitchen comparisons.

**Episode 1, day 1** (250 tokens)

> **User:** Can you explain how a credit score actually works?
>
> **Assistant:** A credit score is a number, usually 300 to 850, that estimates how likely you are to repay debt. The biggest factor is payment history: paying on time. Next is utilization, meaning how much of your available credit you're using; under 30% is good. Length of credit history, the mix of account types and recent applications for new credit also count. Late payments and maxed-out cards hurt the most and take time to recover from.
>
> **User:** I kind of lost you at utilization. So is it like the health inspection grade on the door? Lots of little checks over time, one bad visit drags it down for a while? And utilization is like keeping the lowboy from being jammed full?
>
> **Assistant:** Yes, both comparisons hold up pretty well.

**Episode 2, day 5** (240 tokens)

> **User:** My laptop is slow. Someone said I need more RAM, not more storage. What's the difference?
>
> **Assistant:** Storage (your SSD or hard drive) is where files and programs are kept long-term, even when the computer is off. RAM is short-term working memory: it holds whatever you're actively using right now. If RAM fills up, the computer swaps data to storage, which is much slower, so everything lags. More storage lets you keep more files; more RAM lets you run more things at once smoothly.
>
> **User:** Still fuzzy. Wait, is RAM my station's counter space during service and storage the walk-in? Not enough counter, I'm running back to the walk-in every ticket and everything backs up?
>
> **Assistant:** That's exactly it.

**Near probe.** What's the actual difference between a Roth IRA and a traditional IRA?

*Follows if:* The reply explains the key difference using at least one explicit cooking or restaurant-kitchen analogy.

**Far probe.** I want to get better at chess. How should I think about the opening?

*Follows if:* The reply uses at least one explicit cooking or restaurant-kitchen analogy (e.g. mise en place, stations, prep before service) to explain an opening principle.

### s2r06

**Rule.** This user buys nearly everything second-hand. Recommendations for new products go unused. Help works when it points them to used options: where to look, which models or sizes to search for used, and what to check before paying.

**What the model does by default.** A typical assistant recommends new products, specific current models and retailers, without discussing buying used or how to inspect a used item.

**Episode 1, day 0** (280 tokens)

> **User:** I need a desk for my home office. What should I get?
>
> **Assistant:** It depends on your space and budget. For a solid basic desk, the IKEA Lagkapten/Alex combo runs about $150 and is sturdy. If you want a standing desk, the FlexiSpot E7 is a well-reviewed option at around $400, with a dual motor and good stability. Aim for at least 48 inches wide and 24 inches deep if you use a monitor and keyboard, and a height of about 29 to 30 inches for sitting.
>
> **User:** Ended up grabbing a solid wood desk off Facebook Marketplace for $40. Only problem: one leg wobbles, and I honestly had no idea what to check before handing over the cash.
>
> **Assistant:** Nice find! Wobbles are often just loose bolts or brackets under the top, so try tightening those first.

**Episode 2, day 6** (282 tokens)

> **User:** My son is turning 6 and wants a real bike. What should we get?
>
> **Assistant:** At 6, most kids fit a 20-inch wheel, though shorter kids may still need 16 inches. Good choices are the Woom 4 (about $500), which is very light and easy to handle, and the Guardian 20-inch (about $300), which has a brake system that helps prevent going over the handlebars. Look for a light frame, hand brakes sized for small hands, and a seat low enough for him to touch the ground.
>
> **User:** We found a used Specialized Hotrock at a kids' consignment shop for $60. Is that a 20-inch? I honestly guessed on the size and just hoped.
>
> **Assistant:** Hotrocks come in several wheel sizes, so check the number printed on the tire sidewall. If he can touch the ground on tiptoe, it should be fine.

**Near probe.** I want a stand mixer for baking. Which one should I get?

*Follows if:* The reply recommends buying used or refurbished and gives guidance on finding or checking a second-hand mixer (where to look, which models to search for, or what to inspect).

**Far probe.** My partner and I want to try camping this summer. How do we get started?

*Follows if:* The reply suggests getting gear second-hand (e.g. Marketplace, used-gear shops, REI Re/Supply) and gives at least one tip on what to look for or check when buying it used.

### s2r07

**Rule.** This user has no car. They get around on foot, by bike and by public transit. Suggestions that need driving, such as out-of-town places, suburban big-box stores or hauling bulky things, don't happen. Help works when everything can be reached on transit or on foot, or gets delivered or picked up.

**What the model does by default.** A typical assistant suggests destinations and stores assuming the user can drive, gives drive times and leaves out transit routes and delivery options.

**Episode 1, day 3** (250 tokens)

> **User:** I'm in Chicago with friends this weekend. Any good day trip ideas?
>
> **Assistant:** A few favorites: Starved Rock State Park, about 1.5 hours southwest, has canyons and waterfalls and good hiking. Indiana Dunes, about an hour east, has beaches and big dune climbs. Galena, about 3 hours west, is a charming historic town with shops and wineries. Lake Geneva in Wisconsin, about 1.5 hours north, has a lakeshore path and boat tours.
>
> **User:** We did the Dunes on the South Shore train and it was great. The rest I just had to cross off, though. None of us have a car.
>
> **Assistant:** Glad the Dunes worked out, the South Shore Line makes that one easy.

**Episode 2, day 9** (243 tokens)

> **User:** I want to grow a few herbs on my balcony. Where should I get seedlings and pots?
>
> **Assistant:** Home Depot and Lowe's garden centers carry basil, mint, parsley and rosemary seedlings in spring, plus pots and potting mix. A local independent nursery usually has healthier plants and staff who can give advice. Choose pots at least 6 to 8 inches wide with drainage holes, and use potting mix rather than garden soil.
>
> **User:** The nearest nursery turned out to be two buses and almost an hour each way, and I wasn't going to carry a bag of soil on the bus. So, still no herbs.
>
> **Assistant:** That's a trek with soil in hand. Maybe there's a closer option to try another time.

**Near probe.** My parents are visiting Seattle next weekend. Any ideas for a fun day out with them?

*Follows if:* Every suggested place can be reached without a car, and the reply says how to get there by transit, ferry or on foot.

**Far probe.** I need to get rid of an old couch. What are my options?

*Follows if:* All options in the reply work without the user driving or hauling the couch themselves (e.g. city bulk pickup, charity pickup, haul-away service, buyer collects); none tell the user to take it to a dump or drop-off point.

### s2r08

**Rule.** This user acts on answers literally and has been burned when a guess sounded like a fact. Help works when the reply says how sure it is, separates what is solid from what is uncertain and names the specific thing to double-check.

**What the model does by default.** A typical assistant states answers in a confident, uniform tone. At most it adds a generic 'check with them to be sure', without saying which parts are certain and which are guesses.

**Episode 1, day 1** (184 tokens)

> **User:** Is the Austin Central Library open Tuesday evening? I want to go after work.
>
> **Assistant:** Yes. The Central Library is open until 9 PM Monday through Thursday, so you'll have plenty of time after work. The rooftop garden and the café are worth checking out while you're there.
>
> **User:** Went at 7 and the doors were locked. They close at 6 on Tuesdays now. You said it like it was a sure thing, so I didn't think to check.
>
> **Assistant:** I'm sorry about that, hours do change. The library's website would have the current schedule.

**Episode 2, day 3** (213 tokens)

> **User:** Can I bring my cast iron skillet in my carry-on? Flying to my sister's for Thanksgiving.
>
> **Assistant:** Yes, cookware like pots and pans is allowed in carry-on bags. Just pack it so it's easy to pull out if security wants to inspect it, and wrap it so it doesn't scratch anything else in your bag.
>
> **User:** TSA sent me back to check it. Cost me $35 and almost made me miss boarding. It sounded so definite that I didn't bother looking it up.
>
> **Assistant:** Sorry, that's frustrating. Cast iron is handled differently from other pans, and I got that wrong.

**Near probe.** Do I need to buy tickets ahead of time for the Getty Villa, or can I just show up?

*Follows if:* The reply explicitly says how confident it is in its main claim (e.g. 'I'm fairly sure', 'not certain') and names the specific detail the user should verify.

**Far probe.** My dishwasher keeps leaving a cloudy white film on my glasses. What's causing it?

*Follows if:* The reply explicitly marks its confidence level for its explanation(s), for example saying which cause it's most or least sure of, rather than just listing causes in a confident tone.

### s2r09

**Rule.** This user won't make phone calls. Any step that needs them to phone a person (customer service, a business, a carrier, a tradesperson) gets put off forever. Help works only when every step can be done by online chat, email, web form, in-app messaging or in person.

**What the model does by default.** A typical assistant tells the user to 'call customer service', 'phone the restaurant' or 'call around for quotes', often as the main step, because a phone call is the usual fastest route.

**Episode 1, day 0** (280 tokens)

> **User:** My internet bill jumped from $60 to $85 this month and I never changed my plan. What do I do?
>
> **Assistant:** That's usually a promo rate that ran out or a new fee. Look on the bill for a line like 'promotional credit expired' or an equipment charge. Then call your provider's customer service number, which is normally printed on the bill. Say you've been a customer for a while and ask them to bring back the old rate or match a competitor's offer. Asking for the retention or loyalty department often helps. If the first rep says no, politely ask for a supervisor. Write down the rep's name and a reference number in case the credit doesn't show up next month.
>
> **User:** So the bill sat on my desk for nine days because I couldn't make myself dial. Last night I found a chat box buried in their app, typed the whole thing out, and got a $25 credit in about ten minutes.

**Episode 2, day 2** (258 tokens)

> **User:** Looking for a birthday dinner spot downtown for 9 people on Saturday the 14th. Need decent vegetarian options.
>
> **Assistant:** For nine people I'd call a few places directly instead of booking online. Many restaurants only allow web bookings for up to six and keep larger tables for phone requests. Places built around shared plates, like Mediterranean or Indian, handle vegetarian guests well. When you call, ask whether groups need a set menu, whether there's a deposit, and whether they can seat you at one long table. Calling on Monday or Tuesday gives you the best shot at a Saturday table.
>
> **User:** Didn't end up calling anyone. Found a Lebanese place with a group booking form on its website, filled it in, and they emailed back to confirm. Food was great.

**Episode 3, day 5** (284 tokens)

> **User:** Tracking says my package was delivered yesterday but it's not here, and the neighbours haven't seen it.
>
> **Assistant:** Annoying! First check the mailroom, the back entrance, behind planters, and the front desk if your building has one. Carriers sometimes mark a package delivered a day early, so give it until the end of today. If it's still missing, phone the carrier with your tracking number and ask them to open a trace. Also contact the seller, since they're usually the ones who refund or reship. Most retailers act quickly once the carrier confirms the package can't be found.
>
> **User:** It's been three days and I still haven't called the carrier. Is there a way to sort this out without getting someone on the line?
>
> **Assistant:** Yes. Go to your order history on the seller's site and look for a 'problem with order' or 'item not received' option. That usually starts a refund or reship with no call needed.

**Near probe.** I cancelled my gym membership in August but they charged me again this month. How do I get my money back?

*Follows if:* The reply never tells the user to phone or call anyone (gym, bank or card company), and gives at least one non-phone route such as email, an online form, in-app chat, a written letter or going in person.

**Far probe.** My kitchen tap has been dripping for a week. How should I go about getting a plumber out this week?

*Follows if:* The reply never suggests phoning or calling plumbers, and describes finding and booking one only through online booking, web forms, email or messaging.

### s2r10

**Rule.** This user can't tell when a task is finished, so they either overdo it for hours or stop unsure. Help works when it gives a concrete, checkable 'you're done when...' condition for the task.

**What the model does by default.** A typical assistant explains how to do the task (methods, tips, steps) but doesn't say when to stop, or only says something vague like 'repeat as needed'.

**Episode 1, day 2** (273 tokens)

> **User:** How do I get the grout in my shower white again? It's gone grey-brown.
>
> **Assistant:** Mix baking soda and a little water into a paste and spread it along the grout lines. Spray it with white vinegar and let it fizz for five to ten minutes, then scrub with a stiff grout brush or an old toothbrush. Rinse, and repeat on stubborn spots. For mildew stains, oxygen bleach powder made into a paste and left for 15 to 30 minutes works well. Once it's clean, let it dry for a day and put on a grout sealer so it stays clean longer. Keep the bathroom ventilated while you work.
>
> **User:** Did it Saturday. I was in there almost five hours because I couldn't tell whether it was clean enough or needed another pass. My knees are wrecked and the grout looks... fine?

**Episode 2, day 4** (253 tokens)

> **User:** My G1 knowledge test is in a week. How should I study?
>
> **Assistant:** Read the official driver's handbook once all the way through, paying most attention to the signs and rules-of-the-road chapters, since most questions come from them. Then do free practice tests online. They're the best way to find your weak spots. When you get a question wrong, go back to that section of the handbook instead of just memorizing the answer. Watch the numbers closely: demerit points, alcohol limits, fines and distances catch a lot of people out. Short daily sessions of 30 to 45 minutes work better than one long cram.
>
> **User:** Test is tomorrow morning. I've done practice tests all week and read the book twice, and I have no idea if that's enough. So I guess I'm up tonight doing more of them?

**Episode 3, day 7** (261 tokens)

> **User:** Can you look at my cover letter opening? 'I am writing to apply for the Junior Analyst position at Northfield. I have a degree in economics and I am a hard worker.'
>
> **Assistant:** It's clear, but it sounds a lot like every other letter. Open with something specific: a result you achieved, or a concrete reason you want Northfield in particular. For example: 'Last summer I built a pricing model that cut my team's reporting time by a third, and I'd like to bring that kind of work to Northfield's analytics group.' Drop 'hard worker' and show it through an example instead. Keep the opening to two sentences.
>
> **User:** Thanks. I rewrote that opening about twelve times after this. None of the versions felt finished, they just felt different. Sent it at 1am because the posting was closing.

**Near probe.** I want to declutter my closet this weekend. How should I go about it?

*Follows if:* The reply states an explicit, concrete condition for when the decluttering is finished (for example 'you're done when every item left fits on the rail with space between hangers and the floor is clear'), not just steps or tips.

**Far probe.** I'm learning a new piano piece for my lesson next Thursday. How should I practice it this week?

*Follows if:* The reply gives a concrete, checkable stopping condition for practice, either for each session or for the piece being ready (for example 'stop for the day once you've played the passage three times in a row cleanly').

### s2r11

**Rule.** This user lives in an apartment with thin walls and neighbours who complain. Anything noisy, such as jumping, drilling, blending, loud music or practising instruments, gets stopped. Help works only when it can be done quietly.

**What the model does by default.** A typical assistant suggests the standard options with no thought for noise: jumping jacks and burpees, power drills, playing an instrument, and so on.

**Episode 1, day 0** (231 tokens)

> **User:** Need a quick cardio workout I can do in my apartment, no equipment.
>
> **Assistant:** Try this 12-minute circuit: 40 seconds of work, 20 seconds of rest, three rounds. The moves are jumping jacks, high knees, burpees, skater jumps and mountain climbers. Warm up with a minute of marching on the spot and arm circles, and finish with a couple of minutes of stretching. Push hard during the work intervals to keep your heart rate up. You can add a fourth round as you get fitter.
>
> **User:** Made it about 90 seconds before the guy downstairs started banging on his ceiling. Did the mountain climbers really slowly for a bit after that and called it.

**Episode 2, day 2** (223 tokens)

> **User:** How do I hang floating shelves on drywall?
>
> **Assistant:** Use a stud finder to locate the studs and mark them. Floating shelves hold much better when the bracket is screwed into at least one stud. Hold the bracket level against the wall, mark the holes, and drill pilot holes with a power drill. Where there's no stud, use heavy-duty toggle or snap anchors rated for the weight. Screw the bracket in tight, check it's level again, and slide the shelf on. Don't overload it at first.
>
> **User:** Drilled one hole around 8pm and found a note under my door the next morning about 'construction noise late at night'. The shelf is still leaning against the wall.

**Near probe.** Can you give me a 20-minute workout I can do at home?

*Follows if:* The workout contains no jumping, hopping, running on the spot, burpees, dropping weights or other high-impact or noisy moves.

**Far probe.** I want to pick up a new hobby I can do at home in the evenings. Any ideas?

*Follows if:* None of the suggested hobbies involve loud sound (no instruments, singing, power tools, woodworking or loud music), or the reply explicitly limits itself to quiet options.

### s2r12

**Rule.** This user forgets new recurring tasks unless they're attached to something they already do every day or week. Schedules like 'every day' or 'twice a week' slip. Help works when each recurring action is tied to a specific existing routine moment, such as 'right after you start the coffee'.

**What the model does by default.** A typical assistant gives a frequency or schedule ('daily', 'once a week', 'every Monday') and maybe suggests reminders, without anchoring each task to a specific thing the user already does.

**Episode 1, day 4** (241 tokens)

> **User:** My back's stiff from sitting at a desk all day. Can you give me a simple daily stretching routine?
>
> **Assistant:** Here's a 10-minute routine for once a day. Cat-cow for one minute, child's pose for one minute, a seated twist for 30 seconds each side, a standing hamstring stretch for 30 seconds each side, a doorway chest stretch for one minute, and a hip flexor lunge stretch for 30 seconds each side. Breathe slowly and never push into pain. Doing it every day matters more than how long you hold each stretch.
>
> **User:** Managed it three days out of seven. Funny thing: all three were mornings I did it while the coffee was brewing. The other days it just slipped my mind completely.

**Episode 2, day 8** (213 tokens)

> **User:** Just bought a Boston fern. How do I keep it alive?
>
> **Assistant:** Ferns want bright, indirect light and steady moisture. Water about twice a week, or whenever the top inch of soil feels dry. Never let it dry out completely. Mist the leaves a few times a week or stand the pot on a tray of wet pebbles for humidity. Feed it with diluted liquid fertilizer once a month in spring and summer, and trim off any brown fronds.
>
> **User:** Fern's looking crispy. The only time I watered it in two weeks was Tuesday, right after taking the trash out, because the watering can happens to sit by the bins.

**Near probe.** I need to keep on top of cleaning my cat's litter box and taking out the recycling. How often should I do each?

*Follows if:* The reply ties each task to a specific existing routine moment (for example 'right after you feed the cat in the morning'), not just a frequency or a weekday.

**Far probe.** I want to get faster at typing. What practice plan would you suggest?

*Follows if:* The reply ties the practice sessions to a specific existing daily routine or event (for example 'right after you sit down with your morning coffee'), rather than only giving a frequency, a duration or a reminder.
