---
id: TASK-027
title: "Актуализация скилла kb-release и шаблона TEMPLATE_RELEASE.md"
status: done
type: task
phase: 7
component:
  - skills
  - templates
  - kb-release
parent_plan: "[[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase7
  - component/skills
  - component/templates
  - component/kb-release
  - release
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-027 — Актуализация скилла kb-release и шаблона релиза

> **ID:** TASK-027  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #phase7 #component/skills #component/templates #component/kb-release #release  
> **Родительский план:** [[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005]], [[../../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Актуализировать исполняемый скилл `.agents/skills/kb-release/SKILL.md` и канонический шаблон `TEMPLATE_RELEASE.md` в соответствии с двухформатным стандартом публичной дистрибуции:
1. **Скилл `/kb-release`:** Зафиксировать создание двух артефактов (внутренний `RELEASE-vX.Y.Z.md` и внешний `dist/RELEASE_NOTES.md`) и обновить команду публикации GitHub CLI на `gh release create vX.Y.Z dist/* --notes-file dist/RELEASE_NOTES.md`.
2. **Шаблоны `TEMPLATE_RELEASE.md`:** Синхронизировать канонический шаблон в `docs/00_Templates/` и корневой папке `templates/`, добавив явное указание на генерацию публичных заметок.
3. **High-SNR совместимость:** Сохранить лаконичность описания скилла ($\le$ 15 слов) согласно [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]].

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.agents/skills/kb-release/SKILL.md` — обновление шагов 4 и 6 процедуры релиза.
* `[MODIFY]` `docs/00_Templates/TEMPLATE_RELEASE.md` — актуализация шаблона релизного документа.
* `[MODIFY]` `templates/TEMPLATE_RELEASE.md` — синхронизация шаблона для новых проектов.

---

## 3. Детали реализации

### Контракт `.agents/skills/kb-release/SKILL.md`

Обновление шагов 4 и 6:
```markdown
4. **Generate Release Document:**
   - Run `python scripts/kb_release.py --version X.Y.Z --phase N`.
   - Generates internal `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` and public `dist/RELEASE_NOTES.md` (clean GFM, SHA-256 table, install snippet).
...
6. **Publish:**
   - **GitHub Mode:** commit docs, create annotated tag `vX.Y.Z`, push main and tags, create release with `gh release create vX.Y.Z dist/* --notes-file dist/RELEASE_NOTES.md`.
   - **Local-Only Mode:** commit docs, create tag `vX.Y.Z`, display local artifact paths and SHA-256 hashes in chat.
```

---

## 4. План верификации (Verification Plan)

- [x] High-SNR проверка: описание в YAML frontmatter `SKILL.md` не превышает 15 слов.
- [x] Синхронизация шаблонов: проверка идентичности файлов в `docs/00_Templates/` и `templates/`.
- [x] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [x] В `SKILL.md` прописана команда `gh release create ... --notes-file dist/RELEASE_NOTES.md`.
- [x] Шаблоны синхронизированы.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `docs/Devlog.md`.
