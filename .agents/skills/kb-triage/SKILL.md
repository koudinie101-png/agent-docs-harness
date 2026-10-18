---
name: kb-triage
description: "Mode 2C: Feedback triage & dispatch from Inbox/ with Stop & Yield. Prohibits code changes."
---

# /kb-triage — Mode 2C: Feedback Triage & Dispatch

Use when the user runs `/kb-triage`, wants to screen incoming feedback, or process `docs/02_Tasks/Inbox/`.

## 🚨 Constraints
* **READ-ONLY FOR CODE:** Modifying or creating project code files is STRICTLY PROHIBITED.
* **Permalinks Invariant:** Files `FB-*.md` in `Inbox/` are NEVER moved or deleted. Status is updated in YAML frontmatter (`status: processed` or `status: rejected`) with target link (`target: "[[...]]"`).
* **Stop & Yield Control:** Once triage decisions are committed to Git, immediately STOP tool calls and yield control.

## Procedure
1. **Ingest / Synchronize & Source Verification:**
   - Run `python scripts/kb_ingest.py` (supports optional arguments such as `--all-open` or `--label <NAME>`).
   - Scan `docs/02_Tasks/Inbox/` for files with `status: new`.
   - **Diagnostic Source Feedback:** If no items with `status: new` exist:
     * Execute: `python scripts/kb_ingest.py --status`.
     * Present user with a compact diagnostic summary: probed GitHub repository, channel status, and number of previously processed tickets.
     * Confirm clean inbox and terminate under Stop & Yield protocol.
2. **Interactive Screening (per item):**
   - Present item summary to user: title, source channel, perceived severity, and content.
   - Categorize signal:
     * **Defect:** Recommend launching `/kb-bug` to create `BUG-XXX` with RCA and regression test plan.
     * **Feature / Idea:** Register in `docs/02_Tasks/Roadmap.md` (`## 🔮 Перспективные направления (Icebox)`) with permanent link to `FB-*.md`.
     * **Question / FAQ:** Prepare answer for user and optionally update `docs/Onboarding.md`.
     * **P3 / Refactoring (Tech Debt):** Register a `DEBT-XXX` row in `docs/02_Tasks/TechDebt.md` (`Active P3 Debt`) with a link to `FB-*.md`.
     * **Invalid / Spam:** Mark as rejected with explanation.
3. **Update Feedback Metadata In-Place:**
   - Update frontmatter in `docs/02_Tasks/Inbox/FB-*.md`:
     * `status: processed` (or `status: rejected`)
     * `target: "[[../Bugs/BUG-XXX]]"` (or `target: "[[../Roadmap#Icebox]]"`)
     * `updated: <YYYY-MM-DD>`
4. **Git Commit & Sync:**
   - Stage: `git add docs/02_Tasks/Inbox/ docs/02_Tasks/Roadmap.md`
   - Commit: `git commit -m "docs(inbox): triage feedback FB-XXX to target"`
   - Push to remote if origin exists.
5. **Stop & Yield Control (Terminal Step):**
   - Output concise Anti-Echo summary of triaged items.
   - Suggest next command to user (e.g. `/kb-bug` or `/kb-plan`).
   - **STRICTLY STOP ALL TOOL CALLS.** Yield control to user and wait for explicit command.
