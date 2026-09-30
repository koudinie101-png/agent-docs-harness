---
name: kb-onboard
description: >-
  Display the developer and agent onboarding guide, 3-mode workflow rules, quick commands,
  and repository knowledge base structure.
---

# /kb-onboard — Developer & Agent Onboarding Guide

Use this skill when the user runs `/kb-onboard` or asks how to interact with the project and knowledge base.

## Procedure

1. **Locate Onboarding Guide:**
   - Check if `docs/Onboarding.md` exists. If so, read and present key sections.
2. **Summarize Core Principles:**
   - **Local-First & Docs-as-Code:** All notes live in `docs/`, linked via `[[wikilinks]]`, starting with YAML frontmatter.
   - **Permalinks:** Specs and bugs are never moved to `Done/` or `Archive/`.
   - **3 Operating Modes:**
     - 🟡 **Mode 1: `/kb-plan`** — Discussion, Q&A, impact analysis, NO CODE CHANGES.
     - 🟠 **Mode 2: `/kb-task`** — Detailed engineering spec, contracts, verification plan, NO CODE CHANGES.
     - 🟢 **Mode 3: `/kb-implement` & `/kb-complete`** — Strict implementation, tests, synchronous Done update.
   - **Regression-First:** Bugs must have an automated regression test before closing.
   - **Version Control & GitHub (Conditional Sync):**
     - If remote `origin` is configured, artifacts and task completions are automatically committed and pushed to GitHub.
     - If running in Local-Only mode (no remote origin), local Git commits are created, but `git push` is skipped.
     - If running without Git, all Git operations are gracefully bypassed.
3. **Show Quick Command Cheatsheet:**
   - Provide the table of `/kb-*` commands.
