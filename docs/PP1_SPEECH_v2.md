# PP1 Speech v2 — 10 minutes, 5 speakers

Deck: `docs/PP1_Calibrated_AI_Feedback_v2.pptx` (13 slides; slide 13 = references, shown only if asked).
Speaking rate: about 130 words per minute. Each part is timed; rehearse once with a stopwatch.

**What changed from v1:** slide 2 now cites evidence (Prather, Bastani, Xiao, Kazemitabaar); slide 4 gives a published basis for each requirement instead of expected quotes (R3 and R5 are marked as our assumptions); slide 5 says the thresholds are starting values; slide 10 links each measure to a hypothesis and names the statistical tests; slide 13 lists references. Slides 7–9, 11 and 12 are unchanged, so Ozan's part is the same as before.

| # | Speaker | Slides | Time | Clock |
|---|---|---|---|---|
| 1 | Bekir Can Aracı | 1–3 · Title, problem, users and question | 2:00 | 0:00 → 2:00 |
| 2 | Ongun Arda Münüsoğlu | 4–5 · Needs, requirements, hint ladder | 2:20 | 2:00 → 4:20 |
| 3 | Cem Özbaş | 6–7 · Related tools, three conditions | 1:30 | 4:20 → 5:50 |
| 4 | Ozan Muhcu | 8–9 · Architecture, hardware, live demo | 2:10 | 5:50 → 8:00 |
| 5 | Emir | 10–12 · Evaluation, plan and risks, closing | 2:00 | 8:00 → 10:00 |

Before the talk: start Ollama, run `python demo/server.py`, open `http://localhost:8765/` (Free demo, condition C), run `python demo/fake_esp32.py` in a second terminal and request one hint so the model is warm.

Citations out loud: say "Prather and colleagues", not the full reference. The years are on the slide.

---

## 1 · Bekir Can Aracı — slides 1–3 (2:00)

**[Slide 1 — Title]**
Good morning. We are Group 18: Bekir, Ongun, Cem, Ozan and Emir. Our project is topic two, Calibrated AI Feedback for Novice Programmers. In one sentence: we want AI help that gives a beginner exactly as much as they need, controlled by the learner with a small physical device.

**[Slide 2 — Problem]**
Novices now program with generative AI that can solve most introductory problems completely. Prather and colleagues found that struggling novices finished their tasks this way, but came away with an illusion of competence. Bastani and colleagues saw the same thing in high-school math: unrestricted GPT-4 raised practice scores, but students did worse once it was taken away, while a guardrailed tutor avoided that loss.
Hint-only tools protect learning, but Xiao and colleagues show that high-level hints alone can be unhelpful, or even misleading, for a stuck novice.
Our aim sits in the middle: calibrated help, where hint depth adapts to the learner's confidence and actions, and the learner stays in control. This evidence comes from published studies; our interviews check whether it holds for our own students.

**[Slide 3 — Users and question]**
Our users are first-year IF100 and CS201 students debugging short Python programs alone, with bugs that take five to fifteen minutes to fix.
Our question is: *[read slowly]* for first-year students debugging short Python programs, does calibrated AI feedback improve debugging success and perceived autonomy compared with full-answer and hint-only feedback?
Our hypotheses: H1, calibrated help is about as successful as full answers. H2, students explain the bug better and feel more autonomous. H3, it is faster and less frustrating than hint-only. These are expectations, not results.
Ongun will now explain our requirements.

---

## 2 · Ongun Arda Münüsoğlu — slides 4–5 (2:20)

**[Slide 4 — Needs to requirements]**
Thank you. We will run four to five short semi-structured interviews with IF100 and CS201 students in weeks seven and eight, with consent, anonymous notes and no recording.
We have five initial requirements, and each one shows its basis. R1, the learner decides when help appears: CodeAid by Kazemitabaar and colleagues showed that students should be able to steer AI help. R2, hints escalate step by step: Xiao and colleagues found that multiple levels work better than one. R4, help stays inside the editor, as with the CS50 Duck. R3, not interrupting confident learners, and R5, minimal logging, are our own assumptions; we have no source for them yet.
Each row also names the interview question that will confirm or change it. We have no interview data yet; real quotes will be added afterwards.

**[Slide 5 — Hint ladder]**
The core of the design is a four-step hint ladder, shown on a real task from our prototype. Level one says where to look. Level two names the concept. Level three is a targeted hint about this exact line. Level four is the full fix.
The calibration policy moves the learner up this ladder. At high confidence, help appears only on request, for R3. At low confidence, after a failed run, we offer level one. Each Request goes one level up, and the same error three runs in a row brings an offer of the next level, for R2. A newly passing test resets to level one. The full fix comes only after level three plus one more run. Defer means quiet for two minutes, Silence stops offers, for R1, and every offer says why it appeared.
These thresholds are our first guesses; we will tune them from pilot logs and the TA evaluation. Cem will compare this with existing tools.

---

## 3 · Cem Özbaş — slides 6–7 (1:30)

**[Slide 6 — Related tools]**
Thanks. All the common tools fix hint depth in advance. ChatGPT and Copilot Chat give a full answer on request; the only control is how you word the prompt. The CS50 Duck, described by Liu and colleagues, guides students and avoids full solutions, but its policy is fixed. CodeHelp, by Liffiton and colleagues, adds guardrails and never shows solution code, but its depth is fixed too, and the only interface is chat.
What's missing is adaptive depth with learner control, which is what our ladder, the Request, Defer and Silence buttons and the confidence dial add.

**[Slide 7 — Three conditions]**
In the study we compare against the two common patterns, in the same interface. In A, full answer, the AI immediately shows the corrected code. In B, hint only, there is one fixed conceptual hint and nothing more. In C, ours, the ladder moves from L1 to L4 based on confidence, actions and the buttons. The dark box is the physical controller.
The study is within-subjects: every participant uses all three conditions, with a different bug in each. Ozan will show how it is built.

---

## 4 · Ozan Muhcu — slides 8–9 + live demo (2:10)

*(Same text as v1: slides 8 and 9 did not change.)*

**[Slide 8 — Architecture]**
Thank you. The system has three parts. The ESP32 controller with the buttons, the confidence dial, an LED and a vibration motor. A small Python relay that forwards events and logs them with anonymous IDs. And the browser IDE, where Python runs in the browser and the calibration policy picks the hint.
A button press is a small JSON message; when the app offers help, it sends a command back so the device blinks and vibrates. Hints come from a local model, so no student data leaves the laptop. For the study we will freeze reviewed hints so everyone gets the same ones.

**[Slide 9 — Hardware process]**
This is the handbook's five-point hardware process: hardware set, user action, signal over Wi-Fi, interface response, and the fallback with keyboard and screen buttons. Our test: press Request, and the panel moves up a level within one second and is logged.
One honest note: our ESP32 arrived without a USB cable, so today a script simulates the device with exactly the same events. The firmware is already written.

**[Live demo — about 45 seconds]**
*[Switch to the browser.]* Here is a buggy function. I run the tests, and some fail. Now I press Request on the device. *[Press Enter in fake_esp32.]* A level one hint appears, written live by the local model. I press again, *[Enter]* and it moves to level two, which is more specific. Every press is logged.
*[Switch back to the slides.]* Emir will explain how we will evaluate this.

> If the demo fails: stay calm, say "we will show it after the talk", and continue. Do not debug on stage.

---

## 5 · Emir — slides 10–12 (2:00)

**[Slide 10 — Evaluation]**
Thank you. We plan a user study with 24 first-year students; 24 lets us balance the six condition orders evenly with a Latin square. After a short unmeasured practice, each participant does three ten-minute tasks, one per condition, about fifty minutes in total.
Each measure is linked to a hypothesis. Debugging success tests H1. Bug explanation, scored with a rubric, and perceived autonomy, from the perceived-choice items of the Intrinsic Motivation Inventory, test H2. Time to fix and workload, NASA-TLX plus a frustration item, test H3. Hint use is descriptive.
We will use Cochran's Q for success and Friedman tests for time and ratings. For H1 we report the difference with a 95% confidence interval; that is not a proof of equivalence, and we will not claim one.
Before the study, three to five TAs will do an expert evaluation. Participation is voluntary, with consent and anonymous IDs.

**[Slide 11 — Plan and risks]**
Interviews this week; hardware, frozen hints and the TA evaluation in weeks eight and nine; PP2 with a live demo in week ten; the study in weeks eleven and twelve; the final package after that.
Three risks. If hardware fails, the keyboard and screen buttons send the same events. Live hints can give away too much, so they are reviewed and frozen. And we recruit early through TAs.

**[Slide 12 — Closing]**
To sum up, we expect to contribute a tested interaction policy for matching AI feedback depth to what a novice needs: rules for when to offer which hint, evidence across three conditions, and a physical control that keeps the learner in charge. Our references are on the last slide. Thank you; we are happy to take your questions.

---

## Likely questions — who answers

| Question | Answer in short | Who |
|---|---|---|
| Why a physical device, not just a button on screen? | It keeps help one press away without leaving the code, signals offers without pop-ups (R3, R4), and it is the learner's explicit control (R1). We will test whether it helps. | Ozan |
| Isn't the confidence dial just a self-report? | Yes, deliberately: it is cheap and fast, and the policy also uses run results, so it does not rely on the dial alone. | Ongun |
| Where do the thresholds (≥ 4 / ≤ 2, 3 runs, 2 min) come from? | Our own first guesses, labelled as v0 on the slide. We tune them from pilot logs and the Week 9 TA expert evaluation. | Ongun |
| R3 and R5 have no source? | Correct, and we say so on the slide. The interviews and hint-use logs will confirm or change them. | Ongun |
| Bastani is high-school math; does it transfer to programming? | Not directly, which is why the slide names the domain. Prather et al. is with novice programmers and shows the same pattern; our interviews check our own students. | Bekir |
| Why freeze hints instead of using the live LLM? | Comparability across participants, and our tests showed live hints sometimes leak the answer or add wrong advice. | Ozan |
| Why Cochran's Q and Friedman? | Within-subjects with three conditions; success is binary (Cochran's Q), time and ratings are not assumed normal (Friedman). | Emir |
| Can 24 participants show H1 (equivalence)? | No; we report the difference with a 95% CI and do not claim equivalence. | Emir |
| How is autonomy measured? | Perceived-choice items from the Intrinsic Motivation Inventory (Ryan, 1982), 7-point, after each task. | Emir |
| Order effects / learning effects? | Latin square over 6 orders, a different bug per condition, unmeasured practice first. | Emir |
| How is "explain the bug" scored? | 0–2 rubric; two team members score independently and discuss disagreements. | Emir |
| Why not Copilot as a baseline? | We reproduce its pattern (full answer) in the same interface, so only the feedback policy changes. | Cem |
| Did you already interview anyone? | Not yet; requirements rest on published work or are marked as assumptions. Interviews are in Weeks 7–8. | Ongun |
