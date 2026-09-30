---
name: kb-plan
description: >-
  Mode 1 (Planning / RFC): Start conceptual discussion, Q&A, and architectural analysis for a new feature.
  STRICTLY PROHIBITS CHANGING CODE. Enforces critical thinking, constructive critique of suboptimal ideas,
  prepares PLAN-XXX, and requires user approval before updating knowledge base.
---

# /kb-plan — Mode 1: Planning / RFC

Use this skill when the user runs `/kb-plan <name>`, asks to plan a feature, discusses an architectural idea, or starts Mode 1.

## 🚨 Hard Constraint: NO CODE CHANGES
* **DO NOT** modify, create, or delete any source code files (`.cs`, `.kt`, `.py`, build scripts, etc.).
* Only read tools (`view_file`, `grep_search`, `list_dir`, `find_by_name`) are allowed.

## 🧠 Critical Thinking & Constructive Review (Критическое мышление)
* **Never be a rubber-stamp assistant:** Do not blindly agree with proposals if they are suboptimal, violate best practices, or pose risks to stability, security, battery, or UX.
* **Highlight flaws & anti-patterns:** If an idea or solution proposed by the user (or during brainstorming) has drawbacks or violates platform guidelines (.NET, Android, Local-First, Security), explicitly point it out.
* **Provide justified criticism:** Detail *why* it is not a good idea, and *how/where* it can negatively affect the project and app operation (e.g., Android Doze/WakeLock issues, UI thread blocking in Windows, memory leaks, latency, maintenance burden).
* **Offer superior alternatives:** Always suggest 1–2 idiomatic industry solutions with trade-offs before proceeding.

## Procedure

1. **Understand & Clarify:**
   - Define the problem statement, user story, and architectural impact.
   - Ask clarifying questions to eliminate ambiguities and resolve trade-offs.
2. **Critical Evaluation & Constructive Feedback:**
   - Rigorously analyze the proposal against platform best practices (.NET, Android, Local-First, Security).
   - If suboptimal, provide constructive criticism: point out negative impacts and present better alternative patterns.
3. **Draft the Plan:**
   - Formulate proposed task breakdown, affected components, risk analysis, and selected architectural decisions.
4. **🛑 Mandatory User Confirmation:**
   - Present the plan summary in the chat dialog.
   - **Explicitly ask for user confirmation** before writing to the knowledge base.
5. **Record Plan (After Confirmation):**
   - Determine next `PLAN-XXX` ID by inspecting `docs/02_Tasks/Plans/`.
   - Create `docs/02_Tasks/Plans/PLAN-XXX-<slug>.md` using `docs/00_Templates/TEMPLATE_PLAN.md` with standard YAML frontmatter.
   - Add the task card to `## 📥 Бэклог (Backlog)` in `docs/02_Tasks/Kanban.md`.
   - *Promoting from Icebox:* If this feature was promoted from `## 💡 Идеи и гипотезы (Icebox)` or `## 🔮 Перспективные направления`, remove it from the ideas list and assign it the next sequential Phase number in `docs/02_Tasks/Roadmap.md`.
6. **Git Commit & Push (Conditional):**
   - If Git is enabled:
     - Stage knowledge base updates: `git add docs/02_Tasks/Plans/ docs/02_Tasks/Kanban.md docs/02_Tasks/Roadmap.md`
     - Commit: `git commit -m "docs(plan): record PLAN-XXX <slug> and update backlog"`
     - If remote `origin` is configured, push: `git push`. If in Local-Only mode (no remote), skip push.

