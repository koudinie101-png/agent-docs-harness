---
id: PLAN-015
title: "Фаза 15 — Устранение задержек отклика и прозрачность каналов (Response Latency Elimination & Channel Transparency)"
status: accepted
type: plan
phase: 15
created: 2026-10-12
updated: 2026-10-12
tags:
  - plan
  - phase15
  - latency
  - dispatch
  - hot-invariants
  - channel-transparency
  - ingestion
  - kb-lint
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
related_adr:
  - "[[../../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]]"
  - "[[../../03_Decisions_ADR/ADR-0024-user-centric-ingestion-and-channel-transparency|ADR-0024]]"
related_research:
  - "[[../../04_Research/RESEARCH-008-latency-prompt-caching-and-skill-chaining|RESEARCH-008]]"
  - "[[../../04_Research/RESEARCH-019-user-centric-ingestion-and-channel-transparency|RESEARCH-019]]"
---

# 📋 План: PLAN-015 — Устранение задержек отклика и прозрачность каналов

> **ID:** PLAN-015 | **Статус:** Согласовано  
> **Спецификация:** [[../../SPEC|SPEC.md]] | **Канбан:** [[../Kanban|Канбан]]  
> **Обоснование:** [[../../04_Research/RESEARCH-008-latency-prompt-caching-and-skill-chaining|RESEARCH-008]], [[../../04_Research/RESEARCH-019-user-centric-ingestion-and-channel-transparency|RESEARCH-019]]  
> **Решения (ADR):** [[../../03_Decisions_ADR/ADR-0013-zero-roundtrip-dispatch-and-hot-invariants-architecture|ADR-0013]], [[../../03_Decisions_ADR/ADR-0024-user-centric-ingestion-and-channel-transparency|ADR-0024]]

---

## 1. Контекст и цели (Problem & Goals)

### Проблемы
1. **Штраф двухтактного исполнения (Two-Turn Latency Penalty):**  
   В среде Antigravity при вызове базовых команд жизненного цикла (Режимы 0–3: `/kb-plan`, `/kb-task`, `/kb-implement`, `/kb-bug`, `/kb-triage`) среда требует от агента обязательного вызова `view_file(path/to/SKILL.md)`. Это приводит к двухтактному сетевому обмену (Tool Chaining) и увеличивает Time-To-First-Token с 2 до **6–12 секунд**, создавая иллюзию «зависания» агента на тривиальных операциях.
2. **«Черный ящик» и немые пропуски в сборе обратной связи (`scripts/kb_ingest.py`):**  
   При отсутствии явно экспортированных переменных `GITHUB_REPOSITORY` или `FEEDBACK_IMAP_*` скрипт тихо завершается с выводом `OK: Ingest checked (0 items)`, создавая у пользователя ложную иллюзию чистоты инбокса. При этом скрипт игнорирует уже настроенный `git remote origin` и хардкодит метку `needs-triage`.
3. **Отсутствие диагностического статуса источников:**  
   Нет быстрой команды (`--status`), чтобы увидеть реальное состояние каналов, остаток лимита запросов GitHub API (анонимный лимит 60 req/h vs токен 5000 req/h) и состояние буфера `docs/02_Tasks/Inbox/`.
4. **Недостаток семантического аудита в `scripts/kb_lint.py`:**  
   Линтер проверяет синтаксис и ссылки, но не контролирует соответствие номеров фаз в заголовках ТЗ (`phase: N`) структуре папок (`Specs/NN_...`) и тегам.

### Цели
* Внедрить архитектуру **Zero Round-Trip Dispatch (Hot Invariants)**: закрепить нормативное право агента отвечать в 1-м такте на команды Режимов 0–3, опираясь на Always-On префикс `AGENTS.md` (100% KV-кэш), сократив задержку отклика в 2.5–3 раза.
* Внедрить **User-Centric Ingestion & Channel Transparency**: Zero-Deps автодетект репозитория из `git remote origin`, информативные предупреждения при неполной конфигурации, флаги гибкой фильтрации (`--label <name>`, `--all-open`) и режим дашборда `python scripts/kb_ingest.py --status`.
* Обновить процедуру `/kb-triage` для вывода прозрачной сводки источников при пустом инбоксе.
* Добавить **семантический контроль фаз** в `scripts/kb_lint.py` (неблокирующие warnings).
* Упаковать все изменения в монолитный инсталлятор `install.py` с E2E регрессионными тестами и синхронизировать Living Spec.

---

## 2. Обсуждение и решения (Q&A)

* **Q1: Не приведет ли Zero Round-Trip Dispatch к раздуванию системного промпта и потере токеномики?**
  * **Решение:** Нет. В Always-On файле `AGENTS.md` фиксируются только фундаментальные правила и инварианты 4 режимов (~15 строк), которые уже присутствуют в кэше. Узкие процедурные скиллы (`kb-release`, `kb-lint`, `kb-init`) остаются On-Demand. Это обеспечивает 100% экономию времени без потери контекста.
* **Q2: Что произойдет, если Git отсутствует или репозиторий не привязан к GitHub?**
  * **Решение:** Парсер `detect_github_repo` безопасно перехватывает ошибки подпроцесса. Если репозиторий не обнаружен и переменная `GITHUB_REPOSITORY` не задана, скрипт выводит информативный warning, не ломая выполнение остальных каналов (например, `--paste`).
* **Q3: Зачем семантический контроль фаз в `kb_lint.py` делать неблокирующим (warning)?**
  * **Решение:** Фазы в процессе разработки могут временно переноситься или рефакториться. Неблокирующий warning привлекает внимание инженера, но не срывает сборку релизов и выполнение приемочных тестов.

---

## 3. Архитектурное влияние и риски

* **Затрагиваемые компоненты:**
  * Правила агентов: `AGENTS.md`, адаптеры `install.py` (`_RULES_BODY`, тонкие адаптеры).
  * Скрипты ядра: `scripts/kb_ingest.py`, `scripts/kb_lint.py`, `scripts/build_installer.py`.
  * Скиллы: `.agents/skills/kb-triage/SKILL.md`.
  * Инсталлятор и тесты: `install.py`, `tests/test_kb_ingest.py`, `tests/test_kb_lint.py`, `tests/test_installer.py`.
  * Спецификация и документация: `SPEC.md`, `README.md`, `docs/Onboarding.md`.
* **Платформенные риски:**
  * Риск различий форматов `git remote` (HTTPS vs SSH vs access tokens). Митигирован надежным регулярным выражением с тестами.
  * Риск превышения лимитов GitHub API при анонимных запросах (60 req/h). Митигирован диагностикой в `--status` и подсказками в warnings.

---

## 4. Декомпозиция задач (Task Breakdown)

- [ ] `TASK-057`: **Архитектура Zero Round-Trip Dispatch и горячие инварианты в правилах агентов (Hot Invariants & Direct Dispatch)**
  - Нормативная директива Zero Round-Trip в `AGENTS.md` (разрешение отвечать в 1-м такте для Режимов 0–3).
  - Протокол Pipelined Co-fetching для параллелизации I/O.
  - Обновление генераторов правил `install.py` и адаптеров IDE ($\le 35$ строк).
- [ ] `TASK-058`: **Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в `scripts/kb_ingest.py`**
  - Zero-Deps автодетект GitHub репозитория из `git config --get remote.origin.url`.
  - Запрет немых пропусков (warnings с подсказками по настройке).
  - Диагностический режим `--status` с текстовым дашбордом каналов и буфера `Inbox/`.
  - Флаги фильтрации `--label <name>` и `--all-open`.
  - Информативная обработка HTTP 401/403/404 и модульные тесты в `tests/test_kb_ingest.py`.
- [ ] `TASK-059`: **Прозрачный фидбек источников в `/kb-triage` и семантический контроль фаз в `scripts/kb_lint.py`**
  - Обновление скилла `/kb-triage`: вывод статуса источников при пустом инбоксе.
  - Функция `check_phase_consistency` в `scripts/kb_lint.py` (неблокирующие warnings).
  - Модульные тесты в `tests/test_kb_lint.py`.
- [ ] `TASK-060`: **Синхронизация инсталлятора `install.py` / `build_installer.py`, регрессионные E2E тесты и актуализация Living Spec**
  - Бандлинг через `build_installer.py` в `install.py` и `dist/install.py`.
  - Сквозные тесты в `tests/test_installer.py`.
  - Актуализация `SPEC.md`, `README.md`, `docs/Onboarding.md`.

---

## 5. Критерии приемки плана (DoD Режима 1)

- [x] Концепция согласована с пользователем (READ-ONLY, без изменения кода).
- [ ] Дорожная карта `Roadmap.md` обновлена (Фаза 15 переведена в активный трек).
- [ ] Карточки задач добавлены в `Kanban.md` в `📥 Бэклог`.
- [ ] Целостность базы знаний подтверждена через `python scripts/kb_lint.py --path docs`.
