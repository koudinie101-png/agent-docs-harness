---
id: FB-GH-2
title: "[kb-release] Silent fallback to Local-Only mode due to hard dependency on GitHub CLI (gh)"
status: processed
type: feedback
channel: github
perceived_severity: s2
target: "[[../Bugs/BUG-003-release-silent-local-fallback-missing-gh]]"
created: 2026-10-03
updated: 2026-10-12
author: "koudinie101-png"
source_ref: "https://github.com/koudinie101-png/agent-docs-harness/issues/2"
tags:
  - feedback
  - inbox
---

# 📥 Обращение: FB-GH-2 — [kb-release] Silent fallback to Local-Only mode due to hard dependency on GitHub CLI (gh)

> **Источник:** Github (https://github.com/koudinie101-png/agent-docs-harness/issues/2) | **Статус:** processed  
> **Целевой артефакт:** [[../Bugs/BUG-003-release-silent-local-fallback-missing-gh|BUG-003]]  

---

## 1. Исходное сообщение
Description: The default /kb-release skill template relies on the GitHub CLI (gh release create) to publish releases in "GitHub Mode". However, gh is not installed by default in many environments (especially on Windows). When the agent attempts to run the command and fails (because gh is not recognized), it silently falls back to "Local-Only Mode" instead of reporting the missing dependency. This results in the agent only pushing a Git tag to the remote repository, completely failing to publish the Release Notes and artifacts to the GitHub Releases page, while telling the user that the release was "successful".

Steps to Reproduce:

1. Initialize the Docs-as-Code harness in a project with a GitHub remote (origin).
2. Ensure GitHub CLI (gh) is not installed in the system PATH.
3. Prompt the agent to cut a release: /kb-release v1.0.0.
4. Observe the agent's behavior: it will run the pre-flight checks, generate dist/, try to run gh release create, fail internally, and then just push the Git tag, falsely reporting full success.

Expected Behavior: The skill template should not silently fail. It should either:

1. (Preferred) Ship with a standard Python script (e.g., scripts/publish_github_release.py) that interacts with the GitHub REST API using urllib, completely removing the dependency on external binaries.
2. Instruct the agent to explicitly verify the presence of the gh CLI during the "Environment Detection" step. If it's missing, the agent should halt the release process and instruct the user to install it (e.g., winget install GitHub.cli), rather than silently falling back to Local-Only mode for a GitHub-hosted repository.

Impact: Users lose trust in the agent's release pipeline because artifacts and changelogs are not actually published to GitHub, requiring manual intervention and debugging to understand why the release is missing.

## 2. Анализ и предварительный скрининг
- **Тип:** Дефект (Defect, S2/Medium).
- **Контекст:** Ложное сообщение об успешной публикации GitHub Release при тихом сбое отсутствующего бинарника `gh`.

## 3. Решение по триажу
Конвертировано в баг-репорт [[../Bugs/BUG-003-release-silent-local-fallback-missing-gh|BUG-003]]. Реализация исправления через TDD-цикл.
