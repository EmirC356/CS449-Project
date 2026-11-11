# Progress Presentation I: Emergency Sprint (Nov 11–13)

> Assumption: our slot is **Fri Nov 13**. If it is Thursday, do Day 2 and Day 3 together on Thursday morning.
> PP1 does **not** need working software. It needs a clear plan, real interview evidence, wireframes, and the hardware process. One real ESP32 button press reaching the browser is a strong bonus for the "Early prototype and hardware" part (20%).

---

## What the TAs grade (build slides in this order)

| # | Section | Weight | Prepares | Presents |
|---|---|---|---|---|
| 1 | Problem, target users, context, project question | 25% | Person 5 | Person 5 |
| 2 | User needs, design requirements, rationale (from interviews) | 20% | Person 4 | Person 4 |
| 3 | Comparable systems + baseline (3 conditions, wireframes) | 15% | Person 5 + Person 2 | Person 2 |
| 4 | Early prototype + hardware 5-point process (+ live button demo) | 20% | Person 1 + Person 3 | Person 1 |
| 5 | Evaluation plan, feasibility, timeline, expected contribution | 20% | Person 4 + Person 3 | Person 3 |

Everyone speaks (required). About 10–12 slides total, 2 per person.

---

## Day 1: Wed Nov 11 (today)

- [ ] **All (30 min, now):** Read this file, confirm roles, confirm our exact presentation day/time and length with the TA. Create a shared slide deck.
- [ ] **Person 1:** No extra parts needed for PP1. Flash a sketch that reads the ESP32's built-in **BOOT button** (GPIO0) and blinks the **on-board LED** (GPIO2), print presses on Serial. Make the parts list for Phase 2 (buttons, RGB LED, vibration motor + transistor, resistors, breadboard, jumpers) and check CoSpace / order online. Parts are needed by the end of week 8.
- [ ] **Person 4:** Book 4–5 interviews (10 min each) with IF100 / CS201 students for today evening / tomorrow morning. Use the script below. Email the instructor + TA about ethics (template below).
- [ ] **Person 5:** Comparable systems table (ChatGPT, GitHub Copilot Chat, CS50 Duck, CodeHelp). Draft problem statement + project question slide.
- [ ] **Person 2:** Figma (or paper) wireframes: IDE + hint panel in the 3 conditions (full answer / hint-only / calibrated), plus the on-screen fallback buttons.
- [ ] **Person 3:** Refine the calibration policy draft below. Create the repo skeleton (`firmware/`, `frontend/`, `backend/`, `docs/`). Draw the architecture figure (ESP32 → WebSocket → FastAPI → browser).

## Day 2: Thu Nov 12

- [ ] **Person 4:** Finish interviews by noon. Turn them into 5–7 user needs → design requirements (needs table below). Use only what participants actually said, no invented quotes.
- [ ] **Person 1 + Person 3 (optional bonus):** One BOOT-button press → ESP32 over Wi-Fi WebSocket → tiny Python/FastAPI (or plain websocket) server → a message appears in a browser page. Record a 15-second phone video as backup.
- [ ] **Person 2:** Finalize wireframes, put them in slides 3 and 4.
- [ ] **Everyone:** Put your own slides into the deck by **20:00**.
- [ ] **Person 5:** Merge the deck: consistent style, one message per slide, references slide.

## Day 3: Fri Nov 13 (before the slot)

- [ ] **All:** Full dry run with a timer, twice. Each person stays within their time.
- [ ] **Person 1:** Pack the hardware, hotspot for Wi-Fi, laptop charged, video backup ready.
- [ ] Submit the hardware plan/progress if the TA asks for it as a separate document (use section 4 below).

---

## Ready-made content (adjust, don't copy blindly)

### 1. Problem and question
- **Problem:** Novice programmers increasingly paste errors into AI tools and receive the full fix. They finish faster but skip the reasoning that builds debugging skill, which leads to unproductive dependence. Pure hint-only tools, on the other hand, can feel slow and discouraging.
- **Target users:** First-year students (IF100 / CS201) debugging short Python programs.
- **Context:** Individual lab/homework debugging in an IDE, 5–15 minute bugs.
- **Project question:** For first-year students debugging short Python programs, does **calibrated** AI feedback (hint depth adapts to stated confidence and recent debugging actions, with a physical Request / Defer / Silence control) improve debugging success and perceived autonomy compared with **full-answer** and **hint-only** feedback?
- **Hypothesis:** Calibrated ≥ full-answer on success, > full-answer on bug explanation and autonomy; calibrated faster than hint-only.

### 2. Interview script (Person 4)
Consent first (voluntary, anonymous, can stop anytime, notes only, no recording unless they agree).
1. When your code doesn't work, what do you do first?
2. Do you use ChatGPT/Copilot when debugging? Walk me through the last time.
3. When the AI gave you the full fix, did you understand why it worked? How did that feel?
4. Have you ever wanted only a hint and not the answer? What stopped you?
5. When would a hint be annoying or interrupt you?
6. If you had a physical button to ask for help / say "not now" / turn help off, would you use it? When?

**Needs → requirements table (fill with real interview data):**

| User need (evidence: P#) | Design requirement |
|---|---|
| e.g. "I want to try first" | Hints are opt-in by default when confidence is high |
| … | … |

### 3. Comparable systems / baseline
| System | Feedback style | Learner control | Gap we address |
|---|---|---|---|
| ChatGPT / Copilot Chat | Full answer on request | Prompt only | No depth control, encourages copying |
| CS50 Duck | Guided, avoids full solutions | Chat only | Fixed policy, not adaptive |
| CodeHelp (Liffiton et al., 2023) | Guardrailed help, no solution code | Chat only | Fixed depth, no physical control |
| **Ours** | L1→L4 ladder, calibrated | Physical Request/Defer/Silence + confidence | Adaptive depth + learner control |

**Baselines = our other two conditions:** fixed full-answer, fixed hint-only.

### 4. Hardware 5-point process (handbook §3.3)
1. **Hardware set:** ESP32 DevKit + 3 push buttons (Request / Defer / Silence) + RGB LED + coin vibration motor (via NPN transistor).
2. **User action:** Learner presses **Request** for the next hint level, **Defer** for "not now, remind me later", **Silence** to turn off proactive hints.
3. **Signal and transport:** ESP32 firmware (Arduino C++) sends a JSON event such as `{"event":"request"}` over Wi-Fi **WebSocket** to the backend; fallback is serial USB.
4. **Software and interface response:** FastAPI (Python) applies the calibration policy and pushes the hint to the browser IDE (Monaco + Pyodide); the hint panel shows the new level. Backend sends back LED state (e.g. green = no hint waiting, yellow = hint available, blue = silenced) and a short vibration when a proactive hint is offered.
5. **Fallback and test:** On-screen Request/Defer/Silence buttons + keyboard shortcuts. **Test:** press Request on the device → hint panel moves from L1 to L2 within 1 s and the event appears in the log.

### 5. Calibration policy v0 (Person 3 refines)
- **Inputs:** self-reported confidence (1–5, asked at task start and after each hint), runs, failed test runs, repeated identical error, idle time, Request/Defer/Silence presses.
- **Start:** confidence ≥ 4 → no proactive hint, help only on Request. Confidence ≤ 2 → offer L1 after the first failed run.
- **Escalate:** Request → +1 level. Or same error 3 runs in a row with no meaningful edit → *offer* next level (LED + vibration, learner must accept).
- **Drop / reset:** a test that newly passes → back to L1 for the next issue.
- **Limits:** L4 (full fix) only after L3 was shown and at least one attempt followed. Defer = no proactive offers for 2 min. Silence = no proactive offers until turned off (Request still works).

### 6. Evaluation plan
- **Design:** within-subjects, 3 conditions × 3 buggy programs, counterbalanced (Latin square), 10 min per task.
- **Participants:** **24** first-year students (handbook minimum is 20) + **3–5 TAs** for the expert evaluation (week 9).
- **Measures:** task success (tests pass), time to fix, hint levels used / requests, "explain the bug" score (0–2 rubric), perceived autonomy (short Likert scale), NASA-TLX (raw).
- **Design iteration:** fix the top issues from the TA expert evaluation before the user study.
- **Ethics:** voluntary, consent first, anonymous IDs, only task code and interaction events are logged, no grades or personal data. Instructor confirmation requested.
- **Feasibility:** timeline from `PLAN.md` Phases 2–4; hardware already in hand; fallback buttons if the device fails.

### 7. Ethics email template (Person 4)
> Subject: CS449 Project – Calibrated AI Feedback – ethics check
> Dear Dr. Göktaş / [TA name], our team (topic #2) plans a study with ~24 first-year students debugging short Python programs under 3 AI feedback conditions. We log only task code, test results and button/hint events under anonymous IDs, with written consent and no sensitive data. Could you confirm whether an Ethics Committee application is needed, or whether this is low risk? We can meet at your convenience.
