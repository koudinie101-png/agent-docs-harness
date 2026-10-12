---
id: FB-GH-4
title: "Релизные записки ведут на себя же"
status: processed
type: feedback
channel: github
perceived_severity: s2
target: "[[../Bugs/BUG-004-release-notes-changelog-self-link]]"
created: 2026-10-11
updated: 2026-10-12
author: "koudinie101-png"
source_ref: "https://github.com/koudinie101-png/agent-docs-harness/issues/4"
tags:
  - feedback
  - inbox
---

# 📥 Обращение: FB-GH-4 — Релизные записки ведут на себя же

> **Источник:** Github (https://github.com/koudinie101-png/agent-docs-harness/issues/4) | **Статус:** processed  
> **Целевой артефакт:** [[../Bugs/BUG-004-release-notes-changelog-self-link|BUG-004]]  

---

## 1. Исходное сообщение
В Release notes на странице github кратко описано, что было сделано в новой версии.
В нижней части release notes есть ссылка Полный список изменений (Full Changelog): https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.11.0

Но ведет эта ссылка на тот же краткий release notes, на не на полный changelog

## 2. Анализ и предварительный скрининг
- **Тип:** Дефект (Defect, S2/Medium).
- **Контекст:** Некорректный URL в поле «Full Changelog» генератора релизных записок (`scripts/kb_release.py`).

## 3. Решение по триажу
Конвертировано в баг-репорт [[../Bugs/BUG-004-release-notes-changelog-self-link|BUG-004]]. Реализация исправления через TDD-цикл.
