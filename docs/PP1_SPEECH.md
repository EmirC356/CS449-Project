# PP1 Speech — 10 minutes, 5 speakers

Deck: `docs/PP1_Calibrated_AI_Feedback.pptx` (12 slides).
Speaking rate: about 130 words per minute. Each part is timed; rehearse once with a stopwatch.

| # | Speaker | Slides | Time | Clock |
|---|---|---|---|---|
| 1 | Bekir Can Aracı | 1–3 · Title, problem, users and question | 2:00 | 0:00 → 2:00 |
| 2 | Ongun Arda Münüsoğlu | 4–5 · Needs, requirements, hint ladder | 2:10 | 2:00 → 4:10 |
| 3 | Cem Özbaş | 6–7 · Related tools, three conditions | 1:40 | 4:10 → 5:50 |
| 4 | Ozan Muhcu | 8–9 · Architecture, hardware, live demo | 2:15 | 5:50 → 8:05 |
| 5 | Emir | 10–12 · Evaluation, plan and risks, closing | 1:55 | 8:05 → 10:00 |

Before the talk: start Ollama, run `python demo/server.py`, open `http://localhost:8765/` (Free demo, condition C), run `python demo/fake_esp32.py` in a second terminal and request one hint so the model is warm.

---

## 1 · Bekir Can Aracı — slides 1–3 (2:00)

**[Slide 1 — Title]**
Good morning. We are Bekir, Ongun, Cem, Ozan and Emir, and our project is topic two: Calibrated AI Feedback for Novice Programmers. In one sentence: we want AI help that gives a beginner exactly as much as they need, and that the learner controls with a small physical device.

**[Slide 2 — Problem]**
First-year students now paste their errors into ChatGPT or Copilot and get a complete fix. The task gets done faster, but the reasoning step is skipped, and over time students depend on generated answers instead of learning to debug.
Hint-only tools protect learning, but the depth is fixed: a student who is really stuck gets the same small hint again and again, which is discouraging.
Our aim is in the middle: calibrated help, where hint depth adapts to the learner's confidence and actions, and the learner stays in control.

**[Slide 3 — Users and question]**
Our users are first-year IF100 and CS201 students debugging short Python programs alone, with bugs that take five to fifteen minutes. TAs, instructors and tool designers are also stakeholders.
Our project question is: *[read slowly]* for first-year students debugging short Python programs, does calibrated AI feedback improve debugging success and perceived autonomy compared with full-answer and hint-only feedback?
We have three hypotheses. H1: calibrated help is as successful as full answers. H2: students explain the bug better and feel more autonomous than with full answers. H3: it is faster and less frustrating than hint-only. These are expectations, not results yet.
Ongun will now explain how we turn user needs into requirements.

---

## 2 · Ongun Arda Münüsoğlu — slides 4–5 (2:10)

**[Slide 4 — Needs to requirements]**
Thank you. To ground the design in real users, we will run four to five short semi-structured interviews with IF100 and CS201 students this week and next: how they debug, how they use AI, hint versus answer, interruptions, and physical control. Consent first, anonymous notes, no recording.
From this we have five initial requirements. R1: the learner decides when help appears. R2: hints escalate step by step, and the full fix comes last. R3: confident learners are not slowed down or interrupted. R4: help is available without leaving the editor. R5: we only log task code and interaction events.
To be clear: the quotes on the right are the themes we expect to hear, not collected data. After the interviews we will replace them with real quotes, or change the requirement.

**[Slide 5 — Hint ladder]**
The core of the design is a four-step hint ladder. The example is a real task from our prototype: a function that finds the longest rising run in a list.
Level one says where to look: "Look at the loop." Level two names the concept: a running best must be checked every time a streak can end. Level three is a targeted hint about this exact line. Level four is the full fix.
A calibration policy moves the learner on this ladder. High confidence: help only on request, for R3. Low confidence and a failed run: we offer level one. Each Request goes one level up, and the same error three runs in a row brings an offer of the next level, for R2. Defer means "not now" for two minutes and Silence stops offers, for R1. Every offer says why it appeared.
Cem will compare this with existing tools.

---

## 3 · Cem Özbaş — slides 6–7 (1:40)

**[Slide 6 — Related tools]**
Thanks. Looking at common tools, all of them fix the hint depth in advance. ChatGPT and Copilot Chat give a full answer on request; the only control is how you word the prompt. The CS50 Duck guides students and avoids full solutions, but the policy is fixed. CodeHelp, by Liffiton and colleagues in 2023, adds guardrails and never shows solution code, but again the depth is fixed and the only interface is chat.
What is missing is adaptive depth with learner control. Our system combines the L1-to-L4 ladder with a Request, Defer and Silence control and a confidence dial.

**[Slide 7 — Three conditions]**
For the study we compare against the two common patterns. These wireframes show the same interface in three conditions.
In A, full answer, the AI immediately shows the complete corrected code. In B, hint only, the learner gets one fixed conceptual hint and nothing more. In C, our calibrated condition, the ladder moves from L1 to L4 based on confidence, actions and the buttons.
The dark box at the bottom right is the physical controller: Request, Defer, Silence, a status light and a confidence dial.
The study is within-subjects: every participant uses all three conditions, with a different bug in each. Ozan will now show how it is built.

---

## 4 · Ozan Muhcu — slides 8–9 + live demo (2:15)

**[Slide 8 — Architecture]**
Thank you. The system has three parts. The ESP32 controller with the buttons, the confidence dial, an LED and a vibration motor. A small Python relay that forwards events and logs them with anonymous IDs. And the browser IDE, where Python runs in the browser and the calibration policy picks the hint.
A button press is a small JSON message; when the app offers help, it sends a command back so the device blinks and vibrates. Hints come from a local model, so no student data leaves the laptop. For the study we will freeze reviewed hints so everyone gets the same ones.

**[Slide 9 — Hardware process]**
This is the handbook's five-point hardware process: hardware set, user action, signal over Wi-Fi, interface response, and the fallback with keyboard and screen buttons. Our test: press Request, and the panel moves up a level within one second and is logged.
One honest note: our ESP32 arrived without a USB cable, so today a script simulates the device with exactly the same events. The firmware is already written.

**[Live demo — about 45 seconds]**
*[Switch to the browser.]* Here is a buggy function. I run the tests — some fail. Now I press Request on the device. *[Press Enter in fake_esp32.]* A level one hint appears, written live by the local model. I press again, *[Enter]* and it moves to level two, more specific. Every press is logged.
*[Switch back to the slides.]* Emir will explain how we will evaluate this.

> If the demo fails: stay calm, say "we will show it after the talk", and continue. Do not debug on stage.

---

## 5 · Emir — slides 10–12 (1:55)

**[Slide 10 — Evaluation]**
Thank you. We plan a user study with 24 first-year students; 24 lets us counterbalance the order of conditions evenly. After a short unmeasured practice, each participant does three ten-minute tasks, one per condition — about fifty minutes in total.
We collect six measures: success, time to fix, hint use, an "explain the bug" answer scored with a rubric, perceived autonomy, and workload with NASA-TLX.
Before that, three to five TAs will do a heuristic evaluation and cognitive walkthrough, and their findings drive our design iteration.
Participation is voluntary with written consent, IDs are anonymous, and we have asked the instructor for an ethics check.

**[Slide 11 — Plan and risks]**
Timeline: interviews this week; hardware, frozen hints and expert evaluation in weeks eight and nine; PP2 with a live demo in week ten; the user study in weeks eleven and twelve; the final package in thirteen and fourteen.
Three risks. If hardware fails, the keyboard and screen buttons send the same events. Live AI hints can give away too much or be wrong — we saw this in our own tests — so hints are reviewed and frozen. And we recruit early through TAs and keep sessions short.

**[Slide 12 — Closing]**
To sum up, we expect to contribute a tested interaction policy for matching AI feedback depth to what a novice needs: rules for when to offer which hint, evidence across three conditions, and a physical control that keeps the learner in charge of AI help.
Thank you. We are happy to take your questions.

---

## Likely questions — who answers

| Question | Answer in short | Who |
|---|---|---|
| Why a physical device, not just a button on screen? | It keeps help one press away without leaving the code, signals offers without pop-ups (R3, R4), and it is the learner's explicit control (R1). We will test whether it helps. | Ozan |
| Isn't the confidence dial just a self-report? | Yes, deliberately: it is cheap, fast, and the policy also uses run results, so it does not rely on the dial alone. | Ongun |
| Why freeze hints instead of live LLM? | Comparability across participants, and our tests showed live hints sometimes leak the answer or add wrong advice. | Ozan |
| Order effects / learning effects? | Latin square over 6 orders, different bug per condition, unmeasured practice first. | Emir |
| How is "explain the bug" scored? | 0–2 rubric, two team members score independently, disagreements discussed. | Emir |
| Why not Copilot as a baseline? | We reproduce its pattern (full answer) in the same interface, so only the feedback policy changes. | Cem |
| Did you already interview anyone? | Not yet; the quotes are expected themes. Interviews are in weeks 7–8. | Ongun |
