---
id: FB-GH-5
title: "Asset Storage Hardening: Task-scoped mockup namespaces (`TASK-XXX/`), As-Is/To-Be lifecycle, and `kb_lint` layout validation"
status: processed
type: feedback
channel: github
perceived_severity: s2
target: "[[../Roadmap#🔮 Перспективные направления (Future Horizons / Icebox)|Roadmap Icebox]]"
created: 2026-10-15
updated: 2026-10-15
author: "koudinie101-png"
source_ref: "https://github.com/koudinie101-png/agent-docs-harness/issues/5"
tags:
  - feedback
  - inbox
---

# 📥 Обращение: FB-GH-5 — Asset Storage Hardening: Task-scoped mockup namespaces (`TASK-XXX/`), As-Is/To-Be lifecycle, and `kb_lint` layout validation

> **Источник:** Github (https://github.com/koudinie101-png/agent-docs-harness/issues/5) | **Статус:** processed  
> **Целевой артефакт:** [[../Roadmap#🔮 Перспективные направления (Future Horizons / Icebox)|Roadmap Icebox]]  

---

## 1. Исходное сообщение
### Title: [Feat] Asset Storage Hardening: Task-scoped mockup namespaces (`TASK-XXX/`), As-Is/To-Be lifecycle, and `kb_lint` layout validation

---

### 1. Context & Motivation
While adopting Docs-as-Code v0.19.0 (VisualHarness / ADR-0026) in a multi-component companion application (Windows Desktop + Android), we identified three structural gaps that cause asset drift and broken historical contracts over time:

1. **Iterative Redesign Collision ("To-Be Drift"):**
   Flat or component-based paths like `docs/assets/mockups/android/settings_screen_tobe.svg` work only for the *first* implementation. When the same screen undergoes a subsequent redesign in a later milestone (e.g. Phase 13 `TASK-047` refactors Settings, and Phase 25 `TASK-098` redesigns it for Tablets/Foldables), teams face a dilemma:
   - Overwriting `settings_screen_tobe.svg` permanently breaks the design contract of historical specification `TASK-047`, violating the core **Permalinks & Historical Integrity Invariant** (AGENTS.md rule 8).
   - Alternatively, inventing ad-hoc names (`settings_screen_tobe_v2.svg`, `settings_screen_tobe_final.svg`) introduces uncontrolled naming entropy.

2. **Target Component Granularity:**
   `docs/assets/mockups/<target>/` assumes a flat directory per platform. In real-world targets with 5–10 distinct surfaces/dialogs (e.g., Windows: `TrayFlyout`, `ToastCards`, `ContextMenu`, `PairingModal`), placing all vector assets in a single flat folder creates chaos. Developers and AI agents instinctively group assets into subfolders, but without a formal standard they inadvertently create rogue roots like `docs/assets/<target>/` instead of nesting them inside `mockups/`.

3. **Validation Blindspot in `scripts/kb_lint.py`:**
   `kb_lint.py` verifies broken wikilinks, frontmatter, and file sizes $> 2\text{ MB}$, but does not enforce the root layout of `docs/assets/`. Any arbitrary directory (e.g., `docs/assets/custom/` or `docs/assets/android/`) passes linting silently with exit code 0.

---

### 2. Proposed Architecture & Directory Layout

Standardize visual assets around **Task-Scoped Namespaces (`TASK-XXX/`)**, creating full symmetry between task specifications (`Specs/.../TASK-XXX.md`), design mockups (`mockups/.../TASK-XXX/`), and verification proofs (`screenshots/.../TASK-XXX.png`):

```text
docs/assets/
├── mockups/
│   ├── flows/
│   │   └── TASK-XXX/              # Cross-platform end-to-end journeys for TASK-XXX
│   │       └── sequence.svg
│   └── <target>/                  # e.g., windows, android, web, tui
│       └── TASK-XXX/              # Dedicated visual contract for TASK-XXX
│           ├── asis.svg           # Baseline state before task changes (for UI refactoring)
│           ├── tobe.svg           # Target design contract
│           └── <state>.svg        # Optional 4-State variants (empty, error, loading)
└── screenshots/
    ├── <target>/
    │   └── TASK-XXX.png           # Permanent proof of task completion (size <= 2 MB)
    └── multi-device/
        └── TASK-XXX.png           # Multi-node integration verification proof
```

## 2. Анализ и предварительный скрининг
- **Тип:** Архитектурная инициатива / Улучшение хранения ассетов (Feature / Hardening, S2).
- **Контекст:** Развитие VisualHarness (ADR-0026) при внедрении в companion-приложения. Обнаружены риски дрифта ассетов при повторных редизайнах экранов («To-Be Drift»), отсутствие явного стандарта вложенности и слепая зона в `scripts/kb_lint.py` по валидации структуры `docs/assets/`.

## 3. Решение по триажу
Зарегистрировано в [[../Roadmap#🔮 Перспективные направления (Future Horizons / Icebox)|Roadmap (Icebox)]]. Следующий шаг — запуск Режима 0 (Discovery) через `/kb-research` для валидации архитектуры task-scoped пространств имен, жизненного цикла As-Is/To-Be и правил линтера.
