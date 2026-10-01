---
name: kb-complete
description: >-
  Complete a task in Mode 3: update task spec status to Done, move card on Kanban with date,
  check [x] in Roadmap with permanent link, write Devlog entry, validate with /kb-lint, and commit & push to Git.
---

# /kb-complete — Mode 3: Task Completion & Synchronization

Use this skill when the user runs `/kb-complete <TASK-XXX>` or when an implementation has passed all verification steps.

## Procedure

1. **Update Task Specification:**
   - In `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`:
     - Update YAML frontmatter: `status: done`, `updated: <YYYY-MM-DD>`.
     - Update header block: `> **Статус:** Выполнено (Режим 3)`.
2. **Update Kanban Board:**
   - In `docs/02_Tasks/Kanban.md`:
     - Move the task card from `## ⏳ В работе (In Progress)` to `## ✅ Готово (Done)`.
     - Append completion date: `(YYYY-MM-DD)`.
3. **Update Roadmap:**
   - In `docs/02_Tasks/Roadmap.md`:
     - Mark the milestone checkbox as completed `[x]`.
     - Ensure the permanent link points to the task: `[[Specs/<Phase>/TASK-XXX-<slug>|TASK-XXX]]`.
4. **Append Devlog Entry:**
   - In `docs/Devlog.md`:
     - Add a chronological entry with date:
       - What was done (bulleted summary of changes).
       - Verification results (build output, tests passed).
       - Next recommended step.
5. **Run Lint Check:**
   - Run `python scripts/kb_lint.py --path docs` to confirm no broken links.
6. **Git Commit, Merge & Push (Smart Branching & Conditional):**
   - If Git is enabled:
     - Check current branch (`git branch --show-current`).
     - **Branch Workflow (`feat/TASK-XXX` or `bug/BUG-XXX`):**
       - Stage and commit in feature branch:
         `git add .`
         `git commit -m "feat(<component>): complete TASK-XXX <description> and sync docs"`
       - **Direct Integration (Standard):**
         - Switch to main and sync: `git checkout main` and (if remote exists) `git pull --rebase origin main`.
         - Merge feature branch: `git merge feat/TASK-XXX-<slug>`.
         - Push main to upstream: `git push origin main` (if remote configured).
         - Delete merged local branch: `git branch -d feat/TASK-XXX-<slug>`.
       - **Peer Review (Pull Request):**
         - Push branch: `git push -u origin feat/TASK-XXX-<slug>` and provide PR URL for collaborator review.
     - **Trunk-Based Workflow (directly on `main`):**
       - Pre-push sync: if remote exists, run `git pull --rebase --autostash`.
       - Stage and commit:
         `git add .`
         `git commit -m "feat(<component>): complete TASK-XXX <description> and sync docs"`
       - Push to remote: `git push` (if remote configured; skip if Local-Only).
7. **Phase Completion Nudge (Фазовое напоминание):**
   - После отметки задачи в `docs/02_Tasks/Roadmap.md` агент проверяет текущую фазу:
   - Если все задачи текущей фазы теперь отмечены `[x]`, вывести пользователю рекомендацию:
     > `🎉 Все задачи Фазы N успешно завершены!`  
     > `Рекомендуется выполнить приемочные сценарии в docs/05_Testing/ и запустить команду:`  
     > `👉 /kb-release vX.Y.Z для автоматической сборки дистрибутива и публикации релиза.`
