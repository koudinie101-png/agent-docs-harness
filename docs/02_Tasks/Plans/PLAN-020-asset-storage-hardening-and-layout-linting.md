---
id: PLAN-020
title: "Фаза 20: Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии (Asset Storage Hardening & Layout Linting)"
status: accepted
type: plan
phase: 20
created: 2026-10-15
updated: 2026-10-15
tags:
  - plan
  - phase20
  - assets
  - ui-ux
  - lint
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-020 — Фаза 20: Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии

> **ID:** PLAN-020 | **Статус:** Согласовано  
> **Фаза:** 20 | **Целевой релиз:** v0.20.0  
> **Спецификация:** [[../../SPEC|SPEC.md]] | **Канбан:** [[../Kanban|Канбан]] | **Дорожная карта:** [[../Roadmap|Дорожная карта (Фаза 20)]]  
> **Нормативная база:** [[../../04_Research/RESEARCH-022-asset-storage-hardening-and-task-scoped-namespaces|RESEARCH-022]], [[../../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]] | **Источник:** [[../Inbox/FB-GH-5|Обращение FB-GH-5]]

---

## 1. Контекст и цели (Problem & Goals)

В Фазе 18 ([[PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]], [[../../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]) была внедрена базовая инфраструктура визуальных ассетов (`docs/assets/mockups/<target>/`, `docs/assets/screenshots/<target>/`, проверка веса $\le 2\text{ MB}$ и The 4-State UI Matrix). Боевая эксплуатация харнесса на реальном мультиплатформенном репозитории (`Windows + Android`, обращение [[../Inbox/FB-GH-5|FB-GH-5]]) и проведенное исследование [[../../04_Research/RESEARCH-022-asset-storage-hardening-and-task-scoped-namespaces|RESEARCH-022]] вскрыли четыре системных пробела:

1. **Загрязнение и перезапись в плоском каталоге макетов (To-Be Drift & Permalinks Erosion):** в то время как скриншоты строго привязаны к ID задачи (`screenshots/<target>/TASK-XXX.png`), макеты (`mockups/<target>/`) складывались в плоский каталог с произвольными именами (`settings_v2.svg`, `main_new.svg`). При повторном редизайне одного экрана в новой задаче старый макет либо перезаписывается (нарушая **Permalinks Principle** для завершенных ТЗ), либо порождает хаос версионных суффиксов.
2. **Скрытый дефект резолюции путей медиафайлов в `scripts/kb_lint.py` (False-Positive Fallback):** метод `build_file_map()` индексирует медиафайлы по голому имени файла (`file_map[p.name] = p`), а `run_linter()` выполняет fallback `elif link_name in file_map:` даже тогда, когда ссылка содержит явный относительный путь (`/` или `\`). При появлении одноименных файлов `tobe.svg` и `asis.svg` в разных папках `TASK-XXX/` битая ссылка на несуществующий `TASK-098/tobe.svg` ложноположительно проходит линтер, если в репозитории есть `TASK-047/tobe.svg`.
3. **Эрозия корневой топологии `docs/assets/`:** в `scripts/kb_lint.py` отсутствует проверка структуры подкаталогов `docs/assets/`, из-за чего агенты периодически создают платформенные папки (`docs/assets/windows/`, `docs/assets/android/`) прямо в корне `docs/assets/` мимо `mockups/` и `screenshots/`.
4. **Неочевидная семантика `multi-device/`:** папка `docs/assets/mockups/multi-device/` воспринимается как статическое свойство устройств, а не как каталог сквозных кросс-девайсных пользовательских сценариев (`flows/`).

**Цель фазы:** внедрить пространства имен задач `TASK-XXX/` для макетов с жизненным циклом `As-Is / To-Be`, устранить ложноположительное разрешение путей одноименных медиафайлов в `scripts/kb_lint.py`, добавить механический контроль топологии `check_asset_layout()` и унифицировать конвенцию сквозных сценариев `mockups/flows/TASK-XXX/`.

---

## 2. Обсуждение и решения (Q&A)

* **Q1: Как устранить хаос и перезапись макетов в `docs/assets/mockups/` при итеративных редизайнах?**
  * **Решение:** Внедрить **Триаду симметрии `TASK-XXX`** согласно [[../../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]]:
    * Спецификация: `docs/02_Tasks/Specs/<Phase>/TASK-XXX-<slug>.md`
    * Пространство макетов задачи: `docs/assets/mockups/<target>/TASK-XXX/` (и `docs/assets/mockups/flows/TASK-XXX/` для кросс-девайсных сценариев)
    * Финальный пруф реализации: `docs/assets/screenshots/<target>/TASK-XXX.png`
* **Q2: Какую схему именования файлов внутри `TASK-XXX/` стандартизировать для одноэкранных и мульти-оконных задач?**
  * **Решение:** Стандартизировать жизненный цикл **As-Is / To-Be** с поддержкой префиксов поверхностей:
    * Для одноэкранных задач: `asis.svg` (состояние до задачи), `tobe.svg` (целевой дизайн) и файлы состояний 4-State Matrix (`empty.svg`, `loading.svg`, `error.svg`, `populated.svg`).
    * Для комплексных задач, затрагивающих несколько окон или компонентов: `<surface>_asis.svg`, `<surface>_tobe.svg`, `<surface>_<state>.svg` (например, `tray_tobe.svg`, `modal_tobe.svg`).
* **Q3: Как исключить ложноположительное срабатывание `kb_lint.py` на одноименных файлах `tobe.svg` в разных папках `TASK-XXX/`?**
  * **Решение:** В `scripts/kb_lint.py` ограничить fallback `elif link_name in file_map:` для медиафайлов строго случаями, когда ссылка не содержит разделителей пути (`"/" not in link and "\\" not in link`), по полной аналогии с проверкой `.md`-ссылок. Ссылки с относительными путями проверяются исключительно через разрешение пути `target_file.exists()`.
* **Q4: Какие корневые директории считать валидными в `check_asset_layout()` и должен ли линтер блокировать существующие проекты?**
  * **Решение:** Разрешить множество `VALID_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}` (сохраняя обратную совместимость с `SPEC.md` и `Onboarding.md`) и выдавать неблокирующее предупреждение `[WARN]` при обнаружении посторонних папок в корне `docs/assets/`.

---

## 3. Архитектурное влияние и риски

* **Затрагиваемые компоненты:**
  * `scripts/kb_lint.py` — функция `check_asset_layout()` и строгое разрешение относительных путей медиафайлов в `run_linter()`.
  * `install.py` — обновление скаффолдинга `docs/assets/mockups/flows/`, генератора `_generate_ui_design_system()` и встроенного корпуса правил `_RULES_BODY`.
  * `AGENTS.md`, `GEMINI.md`, `.clinerules`, `.cursorrules`, `.windsurfrules`, `CLAUDE.md`, `.github/copilot-instructions.md` — синхронизация инварианта Visual Verification и путей к макетам `TASK-XXX/`.
  * `docs/00_Templates/TEMPLATE_TASK.md` — обновление путей Headless/CLI Fallback (`docs/assets/mockups/<target>/TASK-XXX/tobe.svg`).
  * `tests/test_kb_lint.py`, `tests/test_installer.py` — регрессионные и E2E тесты.
  * `SPEC.md`, `README.md`, `docs/Onboarding.md` — синхронизация Living Spec.

### Prior-Art Gate (Существующие решения и платформенные аналоги):
* **Внутренний аудит:**
  * В `scripts/kb_lint.py` уже реализована функция `check_asset_weights(root_path: Path)` (строки 533–554) для контроля веса ассетов и строгая проверка относительных путей для `.md`-документов (строка 728: `elif "/" not in link and "\\" not in link:`). Мы расширяем этот же контур без создания новых скриптов или внешних зависимостей.
  * В `install.py` уже реализован генератор `_generate_ui_design_system(ui_targets, lang)` (строки 2862–2966), формирующий документацию `docs/01_Architecture/UI_Design_System.md`.
* **Внешний аудит:**
  * Внешние DAM-системы и Git LFS избыточны для текстовых SVG-макетов и нарушают `ADR-0001` (Zero Dependencies). Нативная файловая изоляция `TASK-XXX/` решает проблему средствами стандартной библиотеки `pathlib`.

### The 4-State UI Matrix (конвенция макетов в пространстве `TASK-XXX/`):
| Состояние | Канонический путь макета в `TASK-XXX/` | Мульти-оконный вариант (`<surface>_`) |
| :--- | :--- | :--- |
| **Empty** | `docs/assets/mockups/<target>/TASK-XXX/empty.svg` | `docs/assets/mockups/<target>/TASK-XXX/<surface>_empty.svg` |
| **Loading** | `docs/assets/mockups/<target>/TASK-XXX/loading.svg` | `docs/assets/mockups/<target>/TASK-XXX/<surface>_loading.svg` |
| **Error** | `docs/assets/mockups/<target>/TASK-XXX/error.svg` | `docs/assets/mockups/<target>/TASK-XXX/<surface>_error.svg` |
| **Populated / To-Be** | `docs/assets/mockups/<target>/TASK-XXX/tobe.svg` (`populated.svg`) | `docs/assets/mockups/<target>/TASK-XXX/<surface>_tobe.svg` |

---

## 4. Декомпозиция задач (Task Breakdown)

- [x] [[../Specs/20_AssetHardening/TASK-079-asset-layout-lint-and-strict-media-resolution|TASK-079]]: Механический контроль топологии `docs/assets/` (`check_asset_layout()`) и строгая резолюция относительных путей медиа-ссылок в `scripts/kb_lint.py` (2026-10-15)
  * Реализация `check_asset_layout(docs_dir: Path)` с проверкой `VALID_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}`, проверкой пространств `TASK-XXX/` внутри `mockups/` и выводом `WARN`.
  * Устранение ложноположительного fallback'а `elif link_name in file_map:` для медиа-ссылок с разделителями пути (`/` или `\`) в `run_linter()`.
  * Модульные тесты `test_kb_lint.py` на детекцию «диких» папок в `docs/assets/` и коллизии одноименных файлов `tobe.svg` в разных директориях `TASK-XXX/`.
- [x] [[../Specs/20_AssetHardening/TASK-080-mockup-namespace-and-flows-convention-in-installer-and-templates|TASK-080]]: Пространства имен макетов `TASK-XXX/`, жизненный цикл `As-Is / To-Be` и каталог `mockups/flows/` в `install.py`, `TEMPLATE_TASK.md` и `AGENTS.md` (2026-10-16)
  * Обновление `UI_Design_System.md` в `create_starter_docs()` (`install.py`) с правилами `TASK-XXX/`, `asis.svg` / `tobe.svg`, `mockups/flows/TASK-XXX/` и префиксами `<surface>_`.
  * Обновление `docs/00_Templates/TEMPLATE_TASK.md`, `AGENTS.md`, `GEMINI.md` и встроенных генераторов правил в `install.py`.
- [ ] [[../Specs/20_AssetHardening/TASK-081-e2e-verification-bundle-rebuild-and-living-spec-sync|TASK-081]]: Сборка монолита `build_installer.py`, E2E тестирование в `tests/test_installer.py` и синхронизация Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`)
  * Обновление и расширение E2E тестов в `tests/test_installer.py`.
  * Пересборка автономного инсталлятора `install.py` через `scripts/build_installer.py`.
  * Актуализация `SPEC.md`, `README.md` и `docs/Onboarding.md`.

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция исследована в Режиме 0 ([[../../04_Research/RESEARCH-022-asset-storage-hardening-and-task-scoped-namespaces|RESEARCH-022]], [[../../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]]) и переведена в план (READ-ONLY, без изменения проектного кода).
- [x] Дорожная карта `Roadmap.md` обновлена (Фаза 20 переведена из Icebox в активный статус).
- [x] Карточки плана и задач добавлены в `Kanban.md` в секцию `📥 Бэклог (Backlog)`.
- [x] Целостность базы знаний подтверждена через `python scripts/kb_lint.py --path docs`.

