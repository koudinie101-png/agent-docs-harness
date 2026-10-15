---
id: PLAN-018
title: "Фаза 18: Контур UI/UX, управление визуальными ассетами и гетерогенные multi-target системы (Heterogeneous UI/UX & Visual Asset Harness)"
status: proposed
type: plan
phase: 18
created: 2026-10-15
updated: 2026-10-15
tags:
  - plan
  - phase18
  - ui-ux
  - multi-target
  - visual-harness
  - assets
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-018 — Фаза 18: Контур UI/UX, управление визуальными ассетами и гетерогенные multi-target системы

> **ID:** PLAN-018 | **Статус:** Обсуждение / Согласовано  
> **Фаза:** 18 | **Релиз:** v0.18.0  
> **Спецификация:** [[../../SPEC|SPEC.md]] | **Канбан:** [[../Kanban|Канбан]]  
> **Дорожная карта:** [[../Roadmap|Дорожная карта (Фаза 18)]]  
> **Нормативная база:** [[../../04_Research/RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]], [[../../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]

---

## 1. Контекст и цели (Problem & Goals)

Современная разработка с участием мультимодальных AI-агентов требует сквозного контура проектирования и верификации графических интерфейсов. Текущий стандарт Docs-as-Code исторически оптимизировался под бэкенд, консольные утилиты и системные библиотеки. При переходе к GUI/TUI проектам и распределенным клиентским экосистемам проявились системные ограничения:
1. **«Слепая разработка» UI (Blind Coding):** отсутствие обязательного проектирования состояний интерактивных представлений (`Empty`, `Loading`, `Error`, `Populated`), доступности (a11y) и объективного визуального подтверждения выполнения задачи (Visual DoD).
2. **Хаос размещения ассетов и раздувание репозитория (Git Bloat):** хаотичное сохранение бинарных скриншотов замусоривает граф Obsidian и раздувает размер Git-репозитория.
3. **Гетерогенные распределенные системы (Multi-Target & Companion Systems):** многие современные проекты объединяют разнородные узлы (`Windows + Android`, `macOS + iOS`, `Linux + Android`, `Web + Mobile`). Харнесс должен поддерживать такие связки универсально, не зашивая имена ОС в ядро и сохраняя принцип **Zero Dependencies (чистый Python 3 stdlib)**.

**Цель фазы:** создать надежный, масштабируемый контур управления UI/UX, изолированное хранилище ассетов с Obsidian DX, механический контроль медиа в `kb_lint.py`/`kb_release.py` и поддержку гетерогенных multi-target комплексов.

---

## 2. Обсуждение и ключевые решения (Q&A)

* **Q1: Как поддержать гетерогенные платформы без нарушения Zero Dependencies и без хардкода ОС?**
  * **Решение:** Внедрить концепцию **Heterogeneous Target Nodes** ([ADR-0026](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management.md)): CLI-параметр `--ui` в `install.py` поддерживает как одиночные профили (`web`, `mobile`, `desktop`, `tui`), так и произвольный список узлов через запятую (`--ui windows,android`, `--ui macos,ios`, `--ui web,mobile`).
* **Q2: Как предотвратить раздувание Git-репозитория бинарными скриншотами?**
  * **Решение:** Разделить постоянные подтверждающие пруфы (`docs/assets/screenshots/<target>/TASK-XXX.png` $\le 2\text{ MB}$, версионируются в Git) и временные диффы автотестов (`tmp/ui_snapshots/**`, заблокированы в `.gitignore`).
* **Q3: Как обеспечить максимальный DX работы с визуальными ассетами в Obsidian?**
  * **Решение:** Автоматически конфигурировать `docs/.obsidian/app.json` (`"attachmentFolderPath": "assets/screenshots"`), добавить правило `!.obsidian/app.json` в `handle_gitignore()` инсталлятора и выполнять безопасный JSON-мерж настроек при `install.py --update`.
* **Q4: Как сохранить лимит объема каталога шаблонов (`00_Templates/ <= 28 KB`)?**
  * **Решение:** Не добавлять новые файлы в `00_Templates/`. Стартовые документы (`docs/01_Architecture/UI_Design_System.md` и `Targets/<Platform>.md`) генерируются динамически через функцию `create_starter_docs()` напрямую в целевой каталог `01_Architecture/`.
* **Q5: Как защитить линтер `kb_lint.py` от ложных срабатываний и коллизий имен?**
  * **Решение:** Медиафайлы (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.gif`, `.canvas`, `.excalidraw`) индексируются в `file_map` **строго с расширением**, чтобы `TASK-001.png` не затенял спецификацию `TASK-001.md`. Регулярное выражение `parse_wikilinks` очищает параметры размера (`![[image.png|600x400]]` $\to$ `image.png`), проверяются стандартные `![alt](path)` и выдается предупреждение (`WARN`) для файлов $> 2\text{ MB}$.
* **Q6: Как агент должен подтверждать Visual DoD в средах без дисплея (Headless/CLI/SSH)?**
  * **Решение:** Если графический дисплей недоступен, агент формирует ASCII/SVG-вайрфрейм либо интерактивный предпросмотр (`generative_ui`) в `docs/assets/mockups/` и готовит слот `![Скриншот](../../assets/screenshots/TASK-XXX.png) <!-- TODO: Вставьте скриншот через Ctrl+V в Obsidian -->`, что позволяет завершить `/kb-complete` без зависаний.

---

## 3. Архитектурное влияние и риски

* **Принцип Zero-Dependencies:** все расширения `install.py`, `scripts/kb_lint.py` и `scripts/kb_release.py` опираются исключительно на стандартную библиотеку Python 3.8+.
* **Токен-экономика High-SNR:** разделение транспортного контракта (`01_Architecture/Protocols/`) и изолированных спецификаций узлов (`Targets/<Platform>.md`) экономит 60–70% контекста диалога агента.
* **Совместимость с существующими проектами:** проекты с `--ui none` или монолитные бэкенды не получают избыточных каталогов; при `install.py --update` существующие настройки пользователя сохраняются в полном объеме.

---

## 4. Декомпозиция задач (Task Breakdown)

### 🛠️ Инженерные задачи фазы (Mode 2 -> Mode 3):

- [ ] `TASK-071`: Архитектура хранения ассетов, композитный `--ui` и Obsidian DX в `install.py`
  * Поддержка композитного списка таргетов в CLI-флаге `--ui` (`auto`, `none`, `web`, `mobile`, `desktop`, `tui` и список узлов через запятую).
  * Двухступенчатая раскладка структуры каталогов `docs/assets/{mockups,screenshots}/<target>/` и `multi-device/`.
  * Генерация `docs/.obsidian/app.json`, безопасный мерж при `--update` и добавление `!.obsidian/app.json` и `tmp/ui_snapshots/` в `handle_gitignore()`.
  * Динамическая генерация `docs/01_Architecture/UI_Design_System.md` и спецификаций узлов `Targets/<Platform>.md` без изменения `00_Templates/`.

- [ ] `TASK-072`: Механический контроль медиа-ассетов в `scripts/kb_lint.py` и `scripts/kb_release.py`
  * Индексация медиафайлов в `file_map` скрипта `kb_lint.py` строго с расширением (защита от коллизий с `.md`-спецификациями).
  * Очистка параметров размера в викиссылках (`![[image.png|600x400]]`) и проверка стандартных относительных ссылок изображений `![alt](path)`.
  * Asset Weight Gate: предупреждение (`WARN`) при наличии файлов $> 2\text{ MB}$ в `docs/assets/`.
  * Адаптация `convert_wikilinks_to_github_markdown()` в `scripts/kb_release.py` (исключение суффикса `.md` для медиафайлов, корректная конвертация параметров размера).

- [ ] `TASK-073`: Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в `AGENTS.md`
  * Интеграция The 4-State Matrix (`Empty`, `Loading`, `Error`, `Populated`) в `TEMPLATE_PLAN.md` и `TEMPLATE_TASK.md`.
  * Протокол Visual DoD и Headless/CLI Fallback в правилах `AGENTS.md` и шаблоне `TEMPLATE_TASK.md`.
  * Включение дисциплины UI/UX и Visual Verification Invariant в Hot Invariants / Disciplines в `AGENTS.md`.

- [ ] `TASK-074`: Бандлинг инсталлятора `build_installer.py`, сквозные E2E тесты и актуализация Living Spec
  * Модульные и E2E тесты композитного `--ui`, создания каталогов, мержа `app.json` и проверки линтера в `tests/test_installer.py`, `tests/test_kb_lint.py` и `tests/test_kb_release.py`.
  * Бандлинг монолитного `install.py` через `scripts/build_installer.py`.
  * Актуализация Living Spec: `SPEC.md`, `README.md` и `docs/Onboarding.md`.

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция согласована с пользователем (READ-ONLY, без кода).
- [ ] Дорожная карта `Roadmap.md` обновлена (Фаза 18 открыта, Icebox актуализирован).
- [ ] Карточки добавлены в `Kanban.md` в `📥 Бэклог`.
- [ ] Целостность базы знаний подтверждена через `scripts/kb_lint.py`.
