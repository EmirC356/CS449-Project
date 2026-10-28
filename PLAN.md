# CS 449 Project Plan: Calibrated AI Feedback for Novice Programmers

> **Change one of the remaining "Person X" labels to your name, and tick or add anything you did.**

**Question:** For first-year students debugging short Python programs, does **calibrated** AI feedback (hint depth adapts to confidence + recent actions, with a physical Request / Defer / Silence control) improve debugging success and perceived autonomy vs. **full-answer** and **hint-only** feedback?

**Stack:** ESP32 (3 buttons, vibration motor, RGB LED) → WebSocket → browser IDE (Monaco + Pyodide) ↔ FastAPI backend (calibration policy, hint ladders, logging)

**Hint ladder:** L1 where to look → L2 which concept → L3 targeted hint → L4 full fix

---

## Who owns what

| Person | Area |
|---|---|
| **Person 1** | Hardware: ESP32 firmware, buttons / LED / vibration, WebSocket + serial fallback |
| **Person 2** | Frontend: browser IDE (Monaco + Pyodide), hint panel, 3 condition modes, on-screen fallback buttons |
| **Person 3** | Backend: FastAPI, calibration policy, hint generation with the LLM, event logging, integration |
| **Person 4** | Research & evaluation: interviews, study protocol, questionnaires, recruiting, ethics/consent |
| **Person 5** | Study content + docs: buggy programs, hint ladder review, comparable systems, slides & report lead |

Everyone presents a section at every presentation (required).

---

## Phase 1: Define (Week 5–6, until Nov 8)

- [ ] **Person 1:** Get the ESP32 kit (buy or borrow from CoSpace). One button press shows up in the browser console.
- [ ] **Person 2:** Figma wireframes of the 3 conditions (full answer / hint-only / calibrated).
- [ ] **Person 3:** Write the calibration policy as rules (start level, when to escalate, when to drop). Repo skeleton.
- [ ] **Person 4:** 4–5 short interviews with IF100 / CS201 students on how they use AI when debugging → list of user needs. Email the TA + instructor about ethics (low risk, confirm).
- [ ] **Person 5:** 2–3 comparable systems (ChatGPT/Copilot, CS50 Duck, CodeHelp). Draft 3 buggy programs + 1 spare.
- [ ] **All, Nov 7–8:** Build slides, dry run.

## Progress Presentation I (Week 7, Nov 9–13), 7%
Problem & users · requirements from interviews · baseline · wireframes + hardware 5-point plan · evaluation plan

---

## Phase 2: Build (Week 7–9, until Nov 29)

Week 8 is the CS 449 midterm, so keep that week light.

- [ ] **Person 1:** All 3 buttons + vibration + LED working over WebSocket. Serial fallback.
- [ ] **Person 2:** IDE runs Python in the browser, shows test results, displays hints by level, switches between the 3 conditions.
- [ ] **Person 3:** Backend receives button + editor events, applies the policy, serves hints, logs everything to a file.
- [ ] **Person 5:** Final 3 buggy programs with tests. Hint ladders (L1–L4) for each bug: generate with the LLM, review by hand, freeze.
- [ ] **Person 4:** Study protocol (task order counterbalanced, 10 min per task), consent form, questionnaires (autonomy, NASA-TLX, "explain the bug"). Expert evaluation with 3–5 CS201/IF100 TAs at end of week 9.
- [ ] **All:** Fix the top issues from the expert evaluation. This is the required **design iteration**: write down what changed and why.

## Progress Presentation II (Week 10, Nov 30–Dec 4), 8%
Live end-to-end task with real hardware · expert eval results · the design change it caused · plan to finish

---

## Phase 3: Evaluate (Week 10–12, until Dec 18)

- [ ] **Person 4 + Person 5:** Recruit and run 18–24 participants (multiple of 6 for counterbalancing).
- [ ] **Person 3:** Export logs → analysis: success rate, time to fix, hint levels used, questionnaire scores per condition.
- [ ] **Person 1 + Person 2:** Bug fixes, stability, record a **backup demo video**.

## Phase 4: Ship (Week 13–14)

- [ ] **Week 13, Team leader:** Final prototype package: repo link, setup guide, hardware list, architecture figure, backup video.
- [ ] **Person 5:** Final report (all sections from the handbook). Each person writes their own part + "Individual Contributions".
- [ ] **All:** Final presentation + live demo. Demo Day: collect 5–10 visitor feedback responses, add a short reflection to the report.

---

## Weekly routine
- Short sync every week (same day/time).
- Each person updates their checkboxes here before the sync.
- Blocked for more than 2 days → say it in the group chat.

## Key rules (from the handbook)
- Hardware must actually change the interaction (not decorative). Real component must work live at least once.
- At least 2 measures, at least 1 documented design iteration.
- No sensitive data. Anonymous participant IDs, consent first.
