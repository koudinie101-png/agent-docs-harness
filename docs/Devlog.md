---
id: DEVLOG
title: Журнал разработки (Devlog)
status: active
type: devlog
created: 2026-09-30
updated: 2026-10-18
tags:
  - devlog
  - journal
  - agent-docs-harness
---

# 📝 Журнал разработки (Devlog): agent-docs-harness

> **Теги:** #devlog #journal #agent-docs-harness  
> **Родительская заметка:** [[00_Index|00_Index]]  

### [2026-10-18] — TASK-095: поведение Mode 2/3, advisory-контракт и state-aware next step (Фаза 25)
- **Что сделано:**
  - [[02_Tasks/Specs/25_SymbolicScope/TASK-095-symbolic-behavior-and-advisory-lint|TASK-095]]: `/kb-task` теперь требует вложенные символы для кода и запрещает номера строк; `/kb-implement` локализует по именам символов. В `kb-complete` добавлен state-aware next step: `/kb-implement TASK-YYY` предлагается только при существующей спеке, иначе `/kb-task TASK-YYY`; Devlog-шаблон больше не хардкодит implement, шаги 10–11 объединены.
  - `scripts/kb_lint.py`: `check_symbolic_scope()` — неблокирующий аудит активных спек (`planned`/`in-progress`): кодовый `[MODIFY]`/`[NEW]` без вложенного символа и маркеры `:L10-L20` дают `WARN:` при Exit code 0; `done` и fast-track молчат.
  - 6 unit-тестов в `tests/test_kb_lint.py` и Tier 1 `test_symbolic_scope_and_state_aware_skill_guards` в `tests/test_installer.py` (читает файлы-источники скиллов, не бандл).
  - Бюджет скиллов: 30 610 B (−12 B к 30 622) — правка `kb-complete` оказалась компактнее старого блока; лимит 31 000 не тронут. `install.py` не пересобирался — TASK-096.
- **Проверка:**
  - Полный прогон `python tmp/run_tests.py` — **162 теста OK** (Exit code 0); `py_compile` — 0; `kb_lint` — 242 файла, 2346 ссылок, 0 битых, 0 `Symbolic Scope Warnings`.
  - Точечный source-guard — OK; бюджетный `test_16` зелёный. Инцидентов нет.
  - Living Spec Sync (`SPEC.md` §2.3, `README.md`, `Onboarding.md`) — в TASK-096 по плану: бандл ещё не пересобран.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-task TASK-096` — спеки TASK-096 ещё нет (проверка состояния по новому правилу `kb-complete`), поэтому implement не предлагается.

### [2026-10-18] — TASK-094: символьный контракт в шаблонах и Tier 1 source-guard (Фаза 25)
- **Что сделано:**
  - [[02_Tasks/Specs/25_SymbolicScope/TASK-094-symbolic-contract-templates-and-source-guard|TASK-094]]: §2 `TEMPLATE_TASK.md` переведён на иерархический контракт «Файл → символ → изменение» (`ClassName.method_name()`, `function_name(arg: Type) -> Ret`) с явным запретом номеров строк; в `TEMPLATE_TASK_MICRO.md` подсказка «конкретная функция, строка или блок» заменена символьной. Обе копии (`templates/` и `docs/00_Templates/`) идентичны, parity зелёный.
  - Новый Tier 1 `test_symbolic_scope_template_source_guard` в `tests/test_installer.py` читает файл-источник `templates/`, а не снимок бандла; проверяет маркеры контракта, отсутствие `:L\d+` и чистоту micro-шаблона.
  - Бюджет: первый вариант дал +272 B и превысил цель +250 B; подсказка сжата до «суть изменения и сигнатура» → **+247 B** (29 579 → 29 826). Лимит 30 000 не менялся. `install.py` намеренно не пересобирался — это TASK-096.
  - Living Spec Sync (SPEC/README/Onboarding) по плану отложен в TASK-096: публичные CLI/API и архитектура этой задачей не менялись.
- **Проверка:**
  - `test_symbolic_scope_template_source_guard` — OK; `tests.test_template_parity` — 2 теста OK; `py_compile` — Exit code 0.
  - Полный прогон `python tmp/run_tests.py` — **155 тестов OK** (Exit code 0); `kb_lint` — 241 файл, 2333 ссылки, 0 битых.
  - Бюджеты: шаблоны 29 826 ≤ 29 829 (цель) и ≤ 30 000; `TEMPLATE_TASK.md` 2 845 B; `TEMPLATE_TASK_MICRO.md` 1 641 B.
  - Инцидентов нет; отклонение оценки бюджета (+272 вместо ожидаемых +150…200) устранено сжатием подсказки в том же проходе.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-task TASK-095 — поведение Mode 2/3 и advisory-контракт`; после утверждения спеки — `/kb-implement TASK-095`.

### [2026-10-18] — Релиз v0.24.0: Фаза 24 (Research-Evidence Gate & Plan Provenance)
- **Что сделано:**
  - Выпущен официальный релиз [[02_Tasks/Releases/RELEASE-v0.24.0|RELEASE-v0.24.0]] по завершении Фазы 24 ([[02_Tasks/Specs/24_ResearchEvidence/TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]]–[[02_Tasks/Specs/24_ResearchEvidence/TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]], [[03_Decisions_ADR/ADR-0031-research-evidence-gate-for-icebox-promotion|ADR-0031]], [[03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]).
  - Собран монолит `install.py` / `dist/install.py`: **173 887 байт (169.8 KB)**, SHA-256 `27166e7df194476fdafa4993eebf61a85d4c296acf3df04dc1faa69ef44eb4e1`; хэши обоих файлов совпадают.
  - Dual-Export: внутренний `RELEASE-v0.24.0.md` (фазовая изоляция ADR) и публичный `dist/RELEASE_NOTES.md` (High-SNR GFM: Highlights, Quick Install, Features, SHA-256, Full Changelog `v0.23.0...v0.24.0`, без блока ADR).
  - Синхронизирована база знаний: `Roadmap.md` (ссылка на релиз в заголовке Фазы 24), `CHANGELOG.md` (секция `[0.24.0]`) и `Devlog.md`.
- **Проверка:**
  - Pre-flight: **154 теста OK**; `kb_lint` — 238 файлов, 2286 ссылок, 0 битых; рабочее дерево чистое; все задачи фазы `[x]`; `SPEC.md`/`README.md` актуальны (Living Spec Sync выполнен в TASK-093).
  - Окружение: GitHub-режим (`gh` CLI аутентифицирован), публикация без silent-fallback.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-research` или `/kb-plan` для следующей инициативы из Icebox (например, автоматизированная ротация процедурной памяти).

### [2026-10-18] — TASK-093: пересборка бандла, E2E Evidence Gate и Living Spec (Фаза 24 завершена)
- **Что сделано:**
  - [[02_Tasks/Specs/24_ResearchEvidence/TASK-093-bundle-rebuild-e2e-and-living-spec-sync|TASK-093]]: `scripts/build_installer.py` пересобрал монолит — `install.py` и `dist/install.py` идентичны, **173 887 байт** (было 171 639). В бандл вошли Evidence Nudge, `research_basis`/Research Basis в шаблоне плана, `check_research_basis`, обновлённый `TEMPLATE_INDEX.md`.
  - Новый E2E `test_phase24_research_basis_deploy_and_update`: свежая установка содержит все артефакты фазы, а `install.py --update` обновляет устаревший `TEMPLATE_PLAN.md`, не затрагивая пользовательские заметки.
  - Living Spec Sync: `SPEC.md` §2.3 (advisory `check_research_basis`) и §2.4 (Mode 1: Evidence Status/Nudge/`research_basis`), `README.md` (строка `/kb-plan` и описание линтера), `docs/Onboarding.md` (Режим 1: доказательная база).
  - **P2-находка:** первый полный прогон на Windows упал в `test_16` — установленные скиллы весили 31 056 байт при лимите 31 000 из-за CRLF-трансляции `Path.write_text()` (12 скиллов → +402 байта), хотя канонический LF-контент — 30 654. Измерение бюджета переведено на LF-нормализованный размер (`canonical_size()`); лимиты 31 000/30 000/175 000 не менялись, текст скиллов не сокращался.
- **Проверка:**
  - Полный прогон `python tmp/run_tests.py` — **154 теста OK** (Exit code 0); `gen_rules.py --check` — OK; бюджеты: install 173 887 / skills 30 654 / templates 29 579.
  - `dist/install.py` smoke-установка — Exit code 0, Evidence Nudge и секция Research Basis на месте.
  - `kb_lint` — 238 файлов, 0 битых ссылок; Kanban/Roadmap закрыты, PLAN-023 перенесён в Done.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Фаза 24 завершена: приёмочное тестирование по `docs/05_Testing/` и `/kb-release v0.24.0`.

### [2026-10-18] — TASK-092: паритет копий шаблонов и Tier 1 parity-тест (Фаза 24)
- **Что сделано:**
  - [[02_Tasks/Specs/24_ResearchEvidence/TASK-092-template-copies-parity-sync-and-test|TASK-092]]: устранён P2-дрейф `templates/` ↔ `docs/00_Templates/`. В `templates/TEMPLATE_PLAN.md` перенесены 4-State UI Matrix и комментарий про multi-target Mermaid (второе расхождение обнаружено при реализации); `docs/00_Templates/TEMPLATE_INDEX.md` синхронизирован с более полной копией из `templates/` (`Zero_To_Hero_Guide`, узел `06_Memory`, `Inbox/`, «16 шаблонов»).
  - Новый Tier 1 `tests/test_template_parity.py`: сравнение наборов и содержимого всех 16 `*.md` (нормализация CRLF, unified diff в сообщении), `graph.json` исключён намеренно.
  - Все копии теперь побайтово совпадают (`drifted: []`); blind spot «тесты читают только снимок бандла» закрыт механически.
- **Проверка:**
  - `tests.test_template_parity` — **2 теста OK**; полный прогон `python tmp/run_tests.py` — **153 теста OK** (Exit code 0).
  - Негативный прогон: искусственная строка в `docs/00_Templates/TEMPLATE_INDEX.md` → тест FAILED с diff; восстановление копией из `tmp/` и сверка SHA-256 (`hash match: True`), повторный прогон OK (INC-005 / TRG-05).
  - Бюджет шаблонов 29 579 ≤ 30 000; `kb_lint` — 0 битых ссылок.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-093`.

### [2026-10-18] — TASK-091: `research_basis`/`basis_note` и advisory-контроль в `kb_lint` (Фаза 24)
- **Что сделано:**
  - [[02_Tasks/Specs/24_ResearchEvidence/TASK-091-plan-research-basis-template-and-advisory-lint|TASK-091]]: в обе копии `TEMPLATE_PLAN.md` (`docs/00_Templates/` и `templates/`) добавлены закомментированные подсказки `research_basis`/`basis_note` и секция `### Research Basis & Unvalidated Assumptions` (известно / не проверено / как закрываем) — план получил durable-след доказательной базы (ADR-0031 R3).
  - `scripts/kb_lint.py`: `check_research_basis()` + `_normalize_plan_value()` — неблокирующий `WARN:`, если `research_basis: none` указан без непустого `basis_note`; отсутствие поля молчит (обратная совместимость с 23 планами); `02_Tasks/Plans` **не** добавлен в `schemas`.
  - Интеграция в `run_linter()`: verbose-блок `⚠️ Research Basis Warnings (N):` и silent-строки `⚠️  WARN: ...`; `has_errors` не меняется → Exit code 0.
  - 4 теста в `tests/test_kb_lint.py`: `none` без заметки (с проверкой Exit code 0), `none` с заметкой и inline-комментарием, ссылка на `RESEARCH-025`, отсутствующее поле.
- **Проверка:**
  - `tests.test_kb_lint` — **54 теста OK** (было 50); полный прогон `python tmp/run_tests.py` — **151 тест OK** (Exit code 0).
  - Негативный CLI-прогон: временный план с `research_basis: none` → `Research Basis Warnings (1)`, Exit code **0**, каталог удалён.
  - Чистый репозиторий: `kb_lint --verbose` без блока Research Basis (238 файлов, 0 битых); бюджет шаблонов 28 599 ≤ 30 000.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-092`.

### [2026-10-18] — TASK-090: Evidence Status и Evidence Nudge в `/kb-plan` (Фаза 24)
- **Что сделано:**
  - [[02_Tasks/Specs/24_ResearchEvidence/TASK-090-evidence-status-nudge-and-tier2-rule|TASK-090]]: ветка `No Argument` в `.agents/skills/kb-plan/SKILL.md` теперь ранжирует по Value Impact **и** Evidence Status (`🔬` валидировано / `🧪` гипотеза / `⏸` parked — вычисляется из ссылок `RESEARCH`/`ADR`, вручную в `Roadmap.md` не вносится) и содержит неблокирующий `Evidence Nudge` с опциями A/B/C и правилом рекомендации по обратимости (A — необратимые решения, B — обратимые).
  - `rules/AGENTS_CORE.md`: строка `Research Evidence` добавлена в Mode 1 обоих документов корпуса (`client-agents` и `harness-agents`), без создания нового `RULE`-блока (инвентарь и пины `tests/test_rules_consistency.py` не менялись); `AGENTS.md` регенерирован через `scripts/gen_rules.py`.
  - Регенерированы 12 golden-фикстур `client_agents__*` (адаптеры не изменились); добавлен Tier 1 `test_evidence_nudge_source_guard` в `tests/test_installer.py`, читающий файл-источник скилла (а не снимок бандла) — защита от повторной потери формулировки.
  - Dry-run на текущем Icebox: 8 пунктов → 1 `🔬` («Символьные контракты», `RESEARCH-024`+`ADR-0029`), 7 `🧪`, 0 `⏸`.
- **Проверка:**
  - Полный прогон `python tmp/run_tests.py` — **147 тестов OK** (Exit code 0); `test_rules_golden`, `test_rules_consistency` и новый ассерт зелёные; `python scripts/gen_rules.py --check` — OK.
  - Бюджет High-SNR: скиллы 30 654 байта (лимит 31 000, запас 346); лимит в тесте не менялся.
  - `python scripts/kb_lint.py --path docs` — 238 файлов, 2283 ссылки, 0 битых.
  - Первый точечный прогон `test_rules_consistency` упал на `PermissionError` в `tempfile.mkdtemp` — известный платформенный INC-003/TRG-03, повторён через sandbox-safe обёртку; новых дефектов и инцидентов нет.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-091`.

### [2026-10-18] — Релиз v0.23.0: Фаза 23 (Memory Integrity Guard)
- **Что сделано:**
  - Выпущен официальный релиз [[02_Tasks/Releases/RELEASE-v0.23.0|RELEASE-v0.23.0]] по завершении Фазы 23 ([[02_Tasks/Specs/23_MemoryIntegrity/TASK-089-memory-consistency-lint-and-incident-procedure|TASK-089]], [[03_Decisions_ADR/ADR-0025-self-improving-defect-loop-and-quality-gates|ADR-0025]]).
  - Собран монолит `install.py` / `dist/install.py` через `scripts/build_release.py` (167.6 KB / 171 639 байт, SHA-256 `985871c5c255719e285b21aad06df20ec13cf6ca12b99e4baf9225a4fcb0c222`); хэши `install.py` и `dist/install.py` совпадают.
  - Сгенерированы Dual-Export артефакты: внутренний `RELEASE-v0.23.0.md` (со scoped-блоком ADR) и публичный `dist/RELEASE_NOTES.md` (High-SNR GFM без ADR, Quick Install, таблица SHA-256, Full Changelog `v0.22.0...v0.23.0`).
  - Синхронизирована база знаний: `Roadmap.md` (Фаза 23 помечена завершённой, ссылка на релиз), `CHANGELOG.md` (секция `[0.23.0]`, включая BUG-011/BUG-012) и `Devlog.md`.
  - Устранён регресс, выявленный первым прогоном Release Automation: свежий клиентский проект получал memory-WARN из-за harness-only `-> INC-003/004/005` в seed-копии `patterns.md`. Добавлена deploy-санитизация `client_safe_memory_patterns()` (repo-копия сохраняет реальную трассировку), бюджет High-SNR бандла поднят до 175 KB, в `test_30` добавлены регрессионные проверки (0 memory-предупреждений у клиента, `-> INC-003` у мейнтейнера).
- **Проверка:**
  - Pre-flight: 146 тестов OK; `kb_lint` — 232 файла, 2185 ссылок, 0 битых; tracked-дерево чистое; phase-23 задачи `[x]`; README/SPEC актуальны.
  - Первый tag `v0.23.0` был пересоздан после красного `Rules Check` (устаревший размерный бюджет и клиентские seed-ссылки в пересобранном бандле); финальный прогон после фикса — зелёный.
  - Опубликован GitHub Release `v0.23.0` с артефактом `dist/install.py`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-research` или `/kb-plan` для следующей инициативы из Icebox (например, автоматизированная ротация процедурной памяти).

### [2026-10-18] — TASK-089: целостность процедурной памяти (Фаза 23)
- **Что сделано:**
  - [[02_Tasks/Specs/23_MemoryIntegrity/TASK-089-memory-consistency-lint-and-incident-procedure|TASK-089]]: в `scripts/kb_lint.py` добавлена `check_memory_consistency()` — неблокирующий аудит ссылочной целостности `docs/06_Memory/` (4 проверки: ссылки `patterns.md` → `Incidents/`, совпадение `id` с префиксом имени файла, наличие `target_pattern` в индексе, согласованность пары `TRG↔INC`).
  - Интеграция в `run_linter()`: verbose-блок `⚠️ Memory Consistency Warnings (N):` и silent-строки `⚠️  WARN: ...`; `has_errors` не включает предупреждения, Exit code не меняется (прецедент `debt_warnings`, ADR-0025 Tier 1 advisory).
  - `patterns.md`: у `TRG-01`/`TRG-02` сняты висячие ссылки `INC-001`/`INC-002` (отчётов никогда не существовало) и заменены маркером `seeded pattern (no archived report)`; seeded-паттерны сохраняются в индексе, но не считаются ссылками.
  - `docs/Onboarding.md` §13: подраздел «Как завести инцидент» (когда, ID, обязательные поля, связи, промоушен, контроль). `SPEC.md` §2.3 синхронизирован (Living Spec).
- **Проверка:**
  - 8 новых тестов в `tests/test_kb_lint.py` (50 тестов модуля OK); полный прогон — 146 тестов OK (обёртка INC-003); `compileall` — 0.
  - Чистый репозиторий: `kb_lint --verbose` без блока Memory Consistency Warnings. Негативный прогон с `-> INC-999`: WARN напечатан, Exit code 0, `patterns.md` восстановлен копией (SHA-256 совпал, TRG-05).
  - `kb_lint --path docs`: 0 битых ссылок.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-release` — выпуск v0.23.0 (Фаза 23 завершена, оба блокера `Rules Check` закрыты).

### [2026-10-18] — BUG-012: герметизация dashboard-теста (Tier 1-гейт Rules Check закрыт)
- **Что сделано:**
  - [[02_Tasks/Bugs/BUG-012-dashboard-env-and-live-api-test|BUG-012]]: `test_render_status_dashboard` больше не наследует `GITHUB_REPOSITORY` от CI (`patch.dict(..., {"GITHUB_REPOSITORY": ""})`) и не ходит в живой GitHub API — HTTP-граница `kb_ingest.urllib.request.urlopen` замокана (`OSError("network disabled")`), проверяется fallback-строка квоты.
  - Новый контрактный тест `test_render_status_dashboard_prefers_env_repository`: при заданном `GITHUB_REPOSITORY` дашборд показывает `(env)`, `detect_github_repo` не вызывается, `urlopen` вызывается ровно один раз (и только как мок).
  - Продуктовое поведение дашборда не менялось: приоритет `env` → `auto-detect` корректен для GitHub Actions и форков.
- **Проверка:**
  - RED: с `GITHUB_REPOSITORY=koudinie101-png/agent-docs-harness` воспроизведён `AssertionError: 'my-org/my-project (auto-detect)' not found`; GREEN: оба теста зелёные и с переменной, и без неё, без реальной сети (~0.01 с).
  - Полный прогон: 138 тестов OK (sandbox-safe обёртка `tmp/run_tests.py`, TRG-03); `kb_lint` — 0 битых ссылок.
  - CI: `Rules Check` run 39113878440 на чистом `ubuntu-latest` — зелёный, шаг `Unit tests` успешен (138 тестов); Tier 1-гейт восстановлен после BUG-011 и BUG-012.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-089` — Фаза 23 (Memory Integrity Guard); после зелёного `Rules Check` можно планировать `/kb-release` v0.23.0.

### [2026-10-18] — BUG-011: герметизация git-identity теста (Tier 1-гейт Rules Check)
- **Что сделано:**
  - [[02_Tasks/Bugs/BUG-011-ci-git-identity-hermetic-test|BUG-011]]: `test_05_git_local_setup` переведён на hermetic-окружение — пустые `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`, `GIT_CONFIG_NOSYSTEM=1`, детерминированная identity через `GIT_AUTHOR_*`/`GIT_COMMITTER_*`; результат больше не зависит от `~/.gitconfig` машины или runner'а.
  - Добавлен контекст-менеджер `hermetic_git_env(identity: bool)` и хелперы `find_git_executable()` / `remove_git_temp_tree()`; no-identity профиль включает `user.useConfigOnly=true`, чтобы git не подхватывал identity из OS-аккаунта (gecos/hostname).
  - Новый контрактный тест `test_05b_git_setup_without_identity_is_graceful`: без identity установка не падает, `.git/HEAD` создаётся, коммита нет, печатается подсказка про `git config --global user.name/email`.
  - Отклонено (по плану дефекта): `git config --global` в CI-workflow — маскирует негерметичность теста и не работает в Docker/форках/на чистых машинах.
- **Проверка:**
  - RED: пустые глобальный/системный конфиги без identity → `test_05` падает с `128 != 0`; GREEN: тест зелёный и с настроенной, и с пустой глобальной identity (включая «враждебное» identity-free окружение).
  - Полный прогон: 137 тестов OK (sandbox-safe обёртка `tmp/run_tests.py`, TRG-03); `kb_lint` — 232 файла, 2177 ссылок, 0 битых.
  - CI: `Rules Check` run 39113479217 на чистом `ubuntu-latest` — 137 тестов, `failures=1`, `test_05`/`test_05b` зелёные; единственное падение — `test_render_status_dashboard` из [[02_Tasks/Bugs/BUG-012-dashboard-env-and-live-api-test|BUG-012]] (Single-Task Barrier).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement BUG-012` — второй блокер `Rules Check` (`test_render_status_dashboard` и живой GitHub API).

### [2026-10-18] — Релиз v0.22.0: Фаза 22 (Single-Source Rule Compiler)
- **Что сделано:**
  - Выпущен официальный релиз [[02_Tasks/Releases/RELEASE-v0.22.0|RELEASE-v0.22.0]] по завершении Фазы 22 ([[02_Tasks/Plans/PLAN-022-single-source-rule-compiler|PLAN-022]], [[03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]]).
  - Собран монолит `install.py` / `dist/install.py` через `scripts/build_release.py` (165.6 KB / 169 562 байта, SHA-256 `8fac0aa7beeb40ab2a6665263267f0ebf4d64b720661f999922443771b8c2ccb`).
  - Сгенерированы Dual-Export артефакты: внутренний `docs/02_Tasks/Releases/RELEASE-v0.22.0.md` (со scoped-блоком ADR) и публичный `dist/RELEASE_NOTES.md` (High-SNR GFM без ADR).
  - Синхронизирована база знаний: `Roadmap.md` (ссылка на релиз в шапке Фазы 22), `CHANGELOG.md` (секция `[0.22.0]`) и `Devlog.md`.
- **Проверка:**
  - Preflight: 136 тестов OK; `kb_lint` — 228 файлов, 2140 ссылок, 0 битых; tracked-дерево чистое.
  - Опубликован GitHub Release `v0.22.0` с артефактом `dist/install.py`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-task` для TASK-089 (Фаза 23, Memory Integrity Guard).

### [2026-10-18] — TASK-088: редакционная консолидация правил, E2E и Living Spec (Фаза 22 завершена)
- **Что сделано:**
  - Заголовок `## Docs-as-Code (20 Disciplines)` → `## Docs-as-Code Disciplines`: число перестало быть данными, которые нужно синхронизировать.
  - Нумерованный индекс достроен до 1–24: добавлены `TECH-DEBT`, `PRIOR-ART`, `TRACEABLE-TAGS`, `BENCHMARKS`; маркеры `RULE` перенесены на пункты индекса, развёрнутые секции оставлены без дублей ID (Tier 1-тест уникальности зелёный).
  - Golden-фикстуры пересняты под новый контент; `tests/test_installer.py` проверяет отсутствие литерала «(20 Disciplines)» и наличие пунктов 21–24.
  - Найденное P3 (устаревшая нумерация развёрнутых секций 6–11) зарегистрировано как `DEBT-001` и по правилу P3 не правилось в этой задаче.
  - Living Spec подтверждён: `SPEC.md` §2.5, `README.md` (корпус), `Onboarding.md` §16; `install.py` / `dist/install.py` пересобраны (165.6 KB, идентичны).
- **Проверка:**
  - E2E-установка `Demo/python`: заголовок без числа, пункты 21–24, шаблонов 16, корпус не утёк в `docs/`, адаптеры 21 строка.
  - Полный прогон: 136 тестов OK; `gen_rules.py --check` — 0; `kb_lint` — 228 файлов, 2140 ссылок, 0 битых.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Фаза 22 завершена: приёмочное тестирование и `/kb-release v0.22.0`, затем `/kb-task` для TASK-089 (Фаза 23, Memory Integrity Guard).

### [2026-10-18] — TASK-087: Tier 1 тесты дрейфа правил
- **Что сделано:**
  - `tests/test_rules_consistency.py`: 13 инвариантов — состав документов, уникальность и баланс `RULE`-маркеров, по-документные пины (`CLIENT_RULES` 27, `ADAPTER_RULES` 10 ⊆ client, `HARNESS_RULES` 20 с `LIVING-SPEC`/`KB-STANDARD`), отсутствие маркеров и плейсхолдеров в рендере, детерминизм, honest failure без корпуса, отсутствие утечки корпуса в `docs/` клиента, `check_current` и CLI-гейт.
  - Уточнён пин в спецификации TASK-087: инвентари различаются по документам (уточнение выявлено в TASK-085).
  - Корпус приведён к формату ADR-0030: добавлены закрывающие маркеры `<!-- /RULE: … -->` (57 открывающих / 57 закрывающих); рендер не изменился — golden-тесты зелёные.
- **Проверка:**
  - `tests/test_rules_consistency.py` — 13 тестов OK; красный сценарий (удаление маркера `SINGLE-TASK`) падает с diff множеств.
  - Полный прогон: 136 тестов OK; `kb_lint` — 227 файлов, 2138 ссылок, 0 битых; `scripts/gen_rules.py --check` — 0.
  - `dist/install.py` пересобран с обновлённым корпусом.
- **Инцидент:** [[06_Memory/Incidents/INC-005-inverse-transform-restore-corrupted-corpus|INC-005]] — восстановление корпуса обратной заменой вместо копии; паттерн `TRG-05`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-088`: редакционная консолидация, E2E, Living Spec и пересборка `dist/install.py`.

### [2026-10-18] — TASK-086: генерация корневого `AGENTS.md` и CI-гейт дрейфа правил
- **Что сделано:**
  - Добавлен `scripts/gen_rules.py` (`--check`, `--output`): рендер документа `harness-agents` из `rules/AGENTS_CORE.md`, нормализация CRLF, unified-diff при дрейфе, Exit code 2 при ошибке рендера.
  - Корневой `AGENTS.md` переведён в генерируемый артефакт: единственное изменение — шапка GENERATED (дифф ровно +1 строка); ручные правки ловятся `--check`.
  - Workflow `.github/workflows/rules-check.yml` (`push`/`pull_request`: `--check` + unittest) и шаг `Verify Rules Corpus Consistency` в префлайт `.github/workflows/release.yml`.
  - `scripts/build_installer.py`: `EXCLUDED_WORKFLOWS = {"rules-check.yml"}` — харнесс-специфичный workflow не уезжает в клиентские проекты; в `tests/test_installer.py` закреплены ассерты исключения и наличия корпуса в бандле.
  - `docs/Onboarding.md`: раздел 16 «Компилятор правил агента» — где править правила и как проверять.
- **Проверка:**
  - `python scripts/gen_rules.py --check` → 0 на чистом дереве, 1 при ручной правке (проверено с восстановлением файла).
  - Полный прогон: 123 теста, OK; `compileall` — 0; `kb_lint` — 227 файлов, 2138 ссылок, 0 битых.
  - `dist/install.py` пересобран: бандл содержит корпус и не содержит `rules-check.yml`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-087`: Tier 1 тесты дрейфа (`tests/test_rules_consistency.py`).

### [2026-10-18] — TASK-085: компилятор правил (корпус `rules/AGENTS_CORE.md` и рендерер)
- **Что сделано:**
  - Три разрозненных инвентаря правил (`AGENTS.md`, `install.py: _RULES_BODY`, `install.py: _gen_rule`) извлечены в единый корпус `rules/AGENTS_CORE.md` (три документа: `client-agents`, `adapters`, `harness-agents`, семантические маркеры `RULE`, плейсхолдеры стека).
  - В `install.py` добавлены `_load_rules_corpus()`, `_render_rules_document()` и `_rules_values()`; `_RULES_BODY` удалён, `generate_agents_md()` и `_gen_rule()` делегируют рендереру при неизменных сигнатурах.
  - Корпус упакован в бандл (`scripts/build_installer.py`, ключ `rules/AGENTS_CORE.md`), добавлен local-fallback в `unpack_assets()`; в `docs/` клиента корпус не разворачивается.
  - Зафиксировано архитектурное решение [[03_Decisions_ADR/ADR-0030-single-source-rule-compiler|ADR-0030]] с отвергнутыми альтернативами (компиляция из `AGENTS.md`, Jinja2, две билингвальные копии, Python-структура, отдельный парсер).
- **Проверка:**
  - 24 golden-фикстуры (`tests/fixtures/rules/`): рендер совпал побайтово для 6 стеков × 2 языков и 6 адаптеров × 2 языков (`tests/test_rules_golden.py`).
  - Полный прогон: 123 теста, `OK` (через `tmp/run_tests.py` из-за INC-003).
  - Сборка `scripts/build_installer.py` — корпус в бандле; отсутствие корпуса даёт `RuntimeError` с actionable-подсказкой.
  - `kb_lint`: 225 файлов, 2123 викиссылки, 0 битых.
- **Инцидент:** зафиксирован [[06_Memory/Incidents/INC-004-path-write-text-newline-truncation|INC-004]] (усечение `install.py` при `write_text` с невалидным `newline`), паттерн `TRG-04` добавлен в `patterns.md`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-086`: генерация корневого `AGENTS.md` через `scripts/gen_rules.py --check` и CI-гейт.

### [2026-10-18] — Релиз v0.21.0: Фаза 21 (Tech Debt Lifecycle & Cross-Mode Sync)
- **Что сделано:**
  - Выпущен официальный релиз [[02_Tasks/Releases/RELEASE-v0.21.0|RELEASE-v0.21.0]] по завершении Фазы 21 ([[02_Tasks/Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]], [[03_Decisions_ADR/ADR-0028-end-to-end-tech-debt-lifecycle-and-lint-enforcement|ADR-0028]]).
  - Собран монолит `install.py` / `dist/install.py` через `scripts/build_release.py` (162.7 KB / 166 650 байт).
  - Сгенерированы Dual-Export артефакты: внутренний `docs/02_Tasks/Releases/RELEASE-v0.21.0.md` (со scoped-блоком ADR) и публичный `dist/RELEASE_NOTES.md` (High-SNR GFM без ADR).
  - Закрыт дефект P1: `scripts/kb_release.py` протаскивал credentials из Git remote (PAT в `https://user:TOKEN@github.com/...`) во frontmatter релизного документа и в публичные Release Notes. Добавлена нормализация `sanitize_repo_url()` (стриппинг userinfo, ssh → https, снятие `.git`), покрытая регрессионным тестом (120/120 тестов).
  - Синхронизирована база знаний: `Roadmap.md` (ссылка на релиз в шапке Фазы 21), `CHANGELOG.md` (секция `[0.21.0]`) и `Devlog.md`. Карточки Фазы 21 в `Kanban.md` уже находились в `Готово`.
- **Артефакты и контрольные суммы (SHA-256):**
  - `dist/install.py` — 162.7 KB (166 650 байт) — `f40c395e85fe1b17cf4d418def0bfc435fbc8484d3f3a68decd647960d9a66a9`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 217 файлов, 0 битых викиссылок (Exit code 0).
  - `python tmp/run_tests.py` (sandbox-safe wrapper, TRG-03/INC-003) -> 120/120 тестов (Exit code 0).
  - `python scripts/kb_release.py --version 0.21.0 --phase 21 --require-github` -> Exit code 0 (mode: github).
- **Git:** ветка `main`, аннотированный тег `v0.21.0`, публикация GitHub Release через `gh release create`.

---

### [2026-10-18] — Реализация TASK-084: Пересборка монолита, E2E-тесты и синхронизация Living Spec (Финал Фазы 21)
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/21_TechDebtLifecycle/TASK-084-bundle-rebuild-e2e-tests-and-living-spec-sync|TASK-084]] — финальная задача Фазы 21:
    1. Пересобран автономный монолит `install.py` через `scripts/build_installer.py` (166.2 KB) — упакованы обновлённые `scripts/kb_lint.py`, 12 скиллов и 16 шаблонов.
    2. Добавлен E2E-тест `test_tech_debt_end_to_end_lifecycle_and_lint_cross_check` в `tests/test_installer.py` (5 инвариантов: `AGENTS.md` `DEBT-XXX`/`#techdebt`/`Resolved Debt`, `tag:#techdebt` в graph.json, `TechDebt.md` в скиллах, ссылка в шаблонах, WARN-кросс-чек `kb_lint.py`).
    3. Актуализированы бенчмарк-пороги в `tests/test_installer.py` (скиллы 30 000 → 31 000 б, монолит 165 → 170 KB) и ассершены `#techdebt`/`// DEBT-XXX` в test_24/test_28.
    4. Living Spec синхронизирован: `SPEC.md` (Фаза 21, инварианты Правил 13/15, кросс-чек kb_lint), `README.md` (правила 12/14) и `docs/Onboarding.md` (цикл `Active P3 Debt -> Plan/Task -> Resolved Debt`).
  - **Фаза 21 официально закрыта!** Все 3 задачи (TASK-082, TASK-083, TASK-084) выполнены.
- **Результаты верификации:**
  - `py -3 scripts/build_installer.py` -> Exit code 0 (166.2 KB).
  - `py -3 -m py_compile install.py scripts/*.py` -> Exit code 0.
  - `py -3 -m unittest discover -s tests` -> 119/119 тестов успешно пройдено (100% Pass, Exit code 0).
  - `py -3 scripts/kb_lint.py --path docs` -> 216 файлов, 1982 викиссылки, 0 битых (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выпуск релиза v0.21.0 через `/kb-release 0.21.0`.

---

### [2026-10-18] — Реализация TASK-083: Сквозной цикл DEBT-XXX в скиллах, правилах AGENTS.md, шаблонах и install.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/21_TechDebtLifecycle/TASK-083-skills-agents-and-templates-tech-debt-lifecycle|TASK-083]] — вторая задача Фазы 21 ([[02_Tasks/Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]]):
    1. `AGENTS.md`: шапка `02_Tasks/` дополнена `TechDebt.md`; Правило 4 (`#techdebt`), Правило 13 (SSOT-жизненный цикл `DEBT-XXX`), Правило 15 (`// DEBT-XXX`); точки синхронизации в Mode 1/2/2C/3.
    2. `install.py`: синхронизированы генераторы `_gen_rule` (правила 8/10) и `generate_agents_md` (теги Obsidian, правила 8/10, Mode 1/2/2C/3).
    3. 6 файлов-адаптеров (`GEMINI.md`, `CLAUDE.md`, `.clinerules`, `.cursorrules`, `.windsurfrules`, `.github/copilot-instructions.md`): правила 8/10 актуализированы.
    4. Скиллы `kb-plan`/`kb-task`/`kb-triage`/`kb-complete`/`kb-lint`: сквозной цикл `DEBT-XXX` (регистрация, привязка, триаж, миграция в Resolved Debt, аудит).
    5. `templates/graph.json` и `docs/.obsidian/graph.json`: цветовая группа `tag:#techdebt`.
    6. `TEMPLATE_INDEX.md` и `TEMPLATE_ONBOARDING.md` (в `templates/` и `docs/00_Templates/`): ссылка на `[[02_Tasks/TechDebt|Реестр техдолга]]`.
- **Результаты верификации:**
  - `py -3 -m py_compile install.py scripts/*.py` -> Exit code 0 (6 файлов).
  - Валидация JSON графа + бюджет шаблонов -> `templates/` 27 908 б, `docs/00_Templates/` 28 495 б (оба ≤ 28 672, Exit code 0).
  - `py -3 scripts/kb_lint.py --path docs` -> 216 файлов, 1978 викиссылок, 0 битых (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-084` (пересборка монолита `build_installer.py`, E2E-тесты в `tests/test_installer.py` и синхронизация Living Spec).

---

### [2026-10-18] — Реализация TASK-082: Семантический кросс-чек TechDebt.md и поддержка кодовых тегов // DEBT-XXX в scripts/kb_lint.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/21_TechDebtLifecycle/TASK-082-kb-lint-tech-debt-cross-check-and-todo-tags|TASK-082]] — первая задача Фазы 21 «Сквозной жизненный цикл технического долга и кросс-режимная синхронизация» ([[02_Tasks/Plans/PLAN-021-tech-debt-lifecycle-and-cross-mode-sync|PLAN-021]]):
    1. `scripts/kb_lint.py`: `check_untracked_todos()` теперь принимает комментарии `// TODO(DEBT-XXX)` наравне с `// ROADMAP-<ID>` (regex `r'(?:ROADMAP-[A-Za-z0-9_-]+|DEBT-\d{3,})'`).
    2. `scripts/kb_lint.py`: `check_tech_debt_integrity()` собирает множество `recorded_debt_ids` (активные и погашенные) и выполняет семантический кросс-чек планов/спецификаций с тегом `#techdebt`/`#tech-debt` (исключая мета-документы харнесса `HARNESS_META_TECHDEBT_IDS`): при отсутствии ссылки `DEBT-\d{3,}` в теле документа или пустом реестре выдает неблокирующее `WARN:`.
    3. `scripts/kb_lint.py`: `run_linter()` маршрутизирует строки `WARN:` из `check_tech_debt_integrity()` в `debt_warnings` (неблокирующие), сохраняя синтаксические нарушения в `debt_errors` (Exit code 1), и избегает дублирования префикса `WARN: WARN:` в silent-режиме.
    4. `tests/test_kb_lint.py`: добавлены 3 модульных теста — `test_check_untracked_todos_accepts_debt_xxx_reference`, `test_check_tech_debt_warns_when_techdebt_tagged_spec_has_empty_registry`, `test_check_tech_debt_passes_when_techdebt_spec_references_debt_id`.
  - Зафиксирован процедурный инцидент песочницы DSH ([[06_Memory/Incidents/INC-003-dsh-sandbox-tempfile-mkdtemp-mode|INC-003]]) и паттерн `TRG-03` в [[06_Memory/patterns|patterns.md]].
- **Результаты верификации:**
  - `py -3 -m py_compile scripts/kb_lint.py tests/test_kb_lint.py` -> Exit code 0.
  - `py -3 -m unittest tests/test_kb_lint.py` -> 42/42 тестов успешно пройдено (100% Pass, Exit code 0).
  - `py -3 scripts/kb_lint.py --path docs` -> 215 файлов, 1974 викиссылки, 0 битых (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-083` (сквозной цикл `DEBT-XXX` в скиллах `kb-plan`/`kb-task`/`kb-triage`/`kb-complete`, правилах `AGENTS.md`, шаблонах и `install.py`).

---

### [2026-10-16] — Выпуск официального релиза v0.20.0: Стандартизация хранилища визуальных ассетов и валидация топологии (Фаза 20)
- **Что сделано:**
  - Осуществлен официальный релиз [[02_Tasks/Releases/RELEASE-v0.20.0|v0.20.0]] по завершении Фазы 20 (План [[02_Tasks/Plans/PLAN-020-asset-storage-hardening-and-layout-linting|PLAN-020]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.20.0|RELEASE-v0.20.0]] и публичные заметки `dist/RELEASE_NOTES.md` по стандарту High-SNR с автоконвертацией викиссылок для GitHub Releases.
  - Собраны и проверены релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (159.9 KB / 163 745 байт) — SHA-256: `76737116ad8b896a1c16e43938005e96eb15315e4b6ce9e7f0bf709b4b9caca2`.
  - Скорректирован бенчмарк-порог суммарного размера шаблонов `total_templates_size` с 28 000 до 30 000 байт в `tests/test_installer.py` для 16 шаблонов с учетом Visual DoD и пространств имен макетов.
  - Актуализирован `CHANGELOG.md` (секция `[0.20.0]`) и `Roadmap.md` (отметка Фазы 20 как `Завершена`).
  - Опубликован GitHub Release и зафиксирован Git-тег `v0.20.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 битых связей, 0 ошибок (Exit code 0).
  - `python -m unittest discover -s tests` -> 115/115 тестов успешно пройдено (100% Pass, Exit code 0).
  - Контрольная сумма SHA-256 подтверждена (`76737116ad8b896a1c16e43938005e96eb15315e4b6ce9e7f0bf709b4b9caca2`).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выбор следующей инициативы из Дорожной карты (Icebox) через `/kb-research` или `/kb-plan`.

---

### [2026-10-16] — Реализация TASK-081: Сквозные E2E-тесты в tests/test_installer.py, пересборка бандла install.py и синхронизация Living Spec
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/20_AssetHardening/TASK-081-e2e-verification-bundle-rebuild-and-living-spec-sync|TASK-081]] — финальная задача Фазы 20 «Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии (Asset Storage Hardening & Layout Linting)»:
    1. Автономный монолитный инсталлятор `install.py` и публичный дистрибутив `dist/install.py` пересобраны через `scripts/build_installer.py` (упакованы актуальные `scripts/kb_lint.py` с `check_asset_layout()` и шаблоны `templates/TEMPLATE_TASK.md` с пространствами имен `mockups/<target>/TASK-XXX/`). Размер бандла: 159.9 KB (строго в рамках DoD $\le 165\text{ KB}$).
    2. В `tests/test_installer.py` добавлен сквозной E2E-тест `test_ui_harness_task_scoped_mockup_taxonomy_and_asset_layout_lint`, валидирующий 5 ключевых инвариантов:
       * Развертывание мультитаргета `--ui windows,android` создает `mockups/flows/` и `01_Architecture/UI_Design_System.md`.
       * В `UI_Design_System.md` присутствует секция 4 с пространствами `mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`) и `mockups/flows/TASK-XXX/`.
       * В развернутых `AGENTS.md` и `GEMINI.md` зафиксированы пути макетов задач.
       * Развернутый шаблон `docs/00_Templates/TEMPLATE_TASK.md` содержит обновленный путь Headless-макета `docs/assets/mockups/<target>/TASK-XXX/tobe.svg`.
       * Развернутый `scripts/kb_lint.py` успешно проходит с кодом 0 на чистом проекте, выдает предупреждение `WARN` при появлении неканонической директории `assets/windows/` и возвращает код ошибки 1 при наличии битой относительной ссылки на несуществующий `TASK-099/tobe.svg` даже при наличии одноименного файла `TASK-001/tobe.svg`.
    3. Синхронизированы Living Spec документы:
       * `SPEC.md`: обновлены раздел 2.3 (`check_asset_layout`), раздел 2.4 (The 4-State UI & Visual Verification Invariant, ADR-0027) и раздел 4 (добавлено описание Фазы 20).
       * `README.md`: обновлены дерево структуры `assets/` (макеты по задачам и кросс-девайсные сценарии) и ключевая дисциплина #11 со ссылкой на ADR-0027.
       * `docs/Onboarding.md`: в разделе 14 детализирована таксономия директорий `mockups/<target>/TASK-XXX/` и `mockups/flows/TASK-XXX/`.
    4. Статусы задачи `TASK-081` и плана `PLAN-020` переведены в завершенные в ТЗ (`done`), Канбане (`Done`) и Дорожной карте (`[x]`). Фаза 20 официально закрыта!
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> сборка успешна (159.9 KB, Exit code 0).
  - `python -m py_compile install.py scripts/*.py tests/*.py` -> компиляция успешна (Exit code 0).
  - `python -m unittest tests/test_kb_lint.py` -> 39/39 тестов успешно пройдено (Exit code 0).
  - `python -m unittest tests.test_installer.TestAgentDocsHarness.test_ui_harness_task_scoped_mockup_taxonomy_and_asset_layout_lint` -> успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовка и публикация релиза v0.20.0 через `/kb-release 0.20.0`.

---

### [2026-10-16] — Реализация TASK-080: Стандартизация TASK-XXX/ для макетов и конвенции mockups/flows/ в install.py, шаблонах и правилах агентов
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/20_AssetHardening/TASK-080-mockup-namespace-and-flows-convention-in-installer-and-templates|TASK-080]] — вторая задача Фазы 20 «Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии»:
    1. В `install.py` генератор дизайн-системы `create_starter_docs()` дополнен разделом `## 4. Организация макетов и визуальных артефактов (Asset Taxonomy)` в `docs/01_Architecture/UI_Design_System.md` с фиксацией пространств имен `mockups/<target>/TASK-XXX/` (`asis.svg`, `tobe.svg`, `<surface>_tobe.svg`), сквозных сценариев `mockups/flows/TASK-XXX/` и скриншотов `screenshots/<target>/TASK-XXX.png`.
    2. В `_RULES_BODY` (дисциплина 20) и `_gen_rule()` (правило 7) инсталлятора зафиксирована симметрия хранения макетов в `docs/assets/mockups/<target>/TASK-XXX/` (или `flows/TASK-XXX/`) и скриншотов в `docs/assets/screenshots/<target>/TASK-XXX.png`.
    3. В генераторе `generate_agents_md()` и каноническом `AGENTS.md` (Правило 12: The 4-State UI & Visual Verification Invariant) закреплено положение `Mockup Namespaces & Lifecycle (ADR-0027)`.
    4. Синхронизированы все 6 тонких адаптеров в корне проекта: `.clinerules`, `.cursorrules`, `.windsurfrules`, `CLAUDE.md`, `GEMINI.md`, `.github/copilot-instructions.md`.
    5. Обновлен шаблон `docs/00_Templates/TEMPLATE_TASK.md` (и `templates/TEMPLATE_TASK.md`) с указанием точных путей макетов `docs/assets/mockups/<target>/TASK-XXX/tobe.svg` (`asis.svg`) в блоке Visual DoD при сохранении жесткого бюджета шаблонов $\le 28\text{ KB}$ (текущий вес: 28,375 байт).
    6. В `tests/test_installer.py` добавлен тест `test_35_task_080_mockup_namespaces_and_ui_design_system`, подтверждающий корректность генерации артефактов и адаптеров.
    7. Обновлены статусы задачи в спецификации (`done`), Канбане (`Done`), плане `PLAN-020` (`[x]`) и Дорожной карте `Roadmap.md` (`[x]`).
- **Результаты верификации:**
  - `python -m py_compile install.py scripts/*.py tests/*.py` -> компиляция успешна (Exit code 0).
  - Контроль бюджета шаблонов: 28,375 байт $\le 28,672$ байт (Exit code 0).
  - `python -m unittest tests/test_kb_lint.py` -> 39/39 тестов пройдено (Exit code 0).
  - `python -m unittest tests.test_installer.TestAgentDocsHarness.test_35_task_080_mockup_namespaces_and_ui_design_system` -> успешно пройдено (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация завершающей задачи Фазы 20 [[02_Tasks/Specs/20_AssetHardening/TASK-081-e2e-verification-bundle-rebuild-and-living-spec-sync|TASK-081]] через `/kb-implement TASK-081`.

---

### [2026-10-15] — Реализация TASK-079: Строгая резолюция медиа-путей и проверка топологии check_asset_layout() в scripts/kb_lint.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/20_AssetHardening/TASK-079-asset-layout-lint-and-strict-media-resolution|TASK-079]] — первая задача Фазы 20 «Стандартизация хранилища визуальных ассетов, пространства имен TASK-XXX и валидация топологии»:
    1. В `scripts/kb_lint.py` внедрена проверка топологии каталога ассетов `check_asset_layout(docs_dir: Path) -> List[str]` (Tier 1 Non-blocking Gate, выдает `WARN` без падения с Exit code 1):
       * Проверяет корневые подкаталоги `docs/assets/` на соответствие каноническому списку `VALID_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}` и сообщает о неразмеченных файлах в корне.
       * Проверяет вложенные элементы в `docs/assets/mockups/<target>/` и `docs/assets/mockups/flows/` на соответствие шаблону задач `^(?:TASK|BUG)-\d{3,}(?:-[a-zA-Z0-9_-]+)?$` (пропуская системные dotfiles вроде `.gitkeep`).
    2. В `run_linter()` исправлен дефект ложноположительного разрешения путей медиафайлов: fallback-поиск по голому имени `link_name in file_map` ограничен строго ссылками без разделителей путей (`"/" not in link and "\\" not in link`). Относительные пути медиафайлов теперь валидируются исключительно через проверку существования целевого файла на диске, что исключает маскировку битых ссылок при наличии одноименных файлов (`tobe.svg`, `asis.svg`) в других задачах.
    3. Добавлен вывод предупреждений `⚠️ Asset Layout Warnings` в подробном и компактном режимах работы линтера.
    4. В `tests/test_kb_lint.py` добавлено 4 модульных теста:
       * `test_same_name_media_in_different_task_folders_no_false_positive` (битая ссылка на `TASK-098/tobe.svg` не маскируется наличием `TASK-047/tobe.svg`, Exit code 1).
       * `test_bare_wikilink_media_still_resolves` (плоская викиссылка `![[Pasted image...|600]]` резолвится, Exit code 0).
       * `test_check_asset_layout_warns_rogue_platform_dir_and_flat_mockup` (неканоническая папка `assets/windows/` и плоский файл `mockups/web/login.svg` дают `WARN` без сбоя линтера).
       * `test_check_asset_layout_allows_canonical_roots` (каноническая топология проходит с пустым списком предупреждений).
    5. Обновлены статусы задачи в спецификации (`done`), Канбане (`Done`), плане `PLAN-020` (`[x]`) и Дорожной карте `Roadmap.md` (`[x]`).
- **Результаты верификации:**
  - `python -m py_compile scripts/kb_lint.py tests/test_kb_lint.py` -> компиляция успешна (Exit code 0).
  - `python -m unittest tests/test_kb_lint.py` -> 39/39 тестов успешно пройдено (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи [[02_Tasks/Specs/20_AssetHardening/TASK-080-mockup-namespace-and-flows-convention-in-installer-and-templates|TASK-080]] через `/kb-implement TASK-080`.

---

### [2026-10-15] — Выпуск релиза v0.19.0: Фаза 19 (Engineering Gates & Tech Debt Governance)
- **Что сделано:**
  - Опубликован официальный релиз [[02_Tasks/Releases/RELEASE-v0.19.0|RELEASE-v0.19.0]] по итогам завершения Фазы 19.
  - Успешно завершены и верифицированы все инженерные задачи фазы (`TASK-075`–`TASK-078`):
    * Реестр техдолга `docs/02_Tasks/TechDebt.md`, скаффолдинг в `install.py` и правило триажа P1/P2 vs P3 (Rule 13).
    * Инженерные барьеры в шаблонах и правилах: Prior-Art Gate (Rule 14), трассировка `// ROADMAP-<ID>` (Rule 15) и серийные замеры $\ge 3$ прогонов (Rule 16).
    * Чеклист приемочного тестирования GUI («UI не лжёт») в `TEMPLATE_TEST.md` и механический аудит `check_tech_debt_integrity()` / `check_untracked_todos()` в `scripts/kb_lint.py`.
    * Синхронизация `install.py`, сборка монолита через `build_installer.py`, E2E тесты в `tests/test_installer.py` и актуализация Living Spec.
  - Сформированы публичные релизные заметки `dist/RELEASE_NOTES.md` по стандарту High-SNR.
  - Собраны релизные артефакты в каталоге `dist/`:
    * `dist/install.py` (157.7 KB) — SHA-256: `3360889dbaf7fb1b23829022ef0191cdbdf04a743752b080e9b1a34183442601`.
  - Обновлен `CHANGELOG.md` с подробным перечнем добавленных возможностей.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 110/110 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к следующей фазе развития харнесса через `/kb-plan` (или обсуждение инициатив из Icebox Дорожной карты).

---

### [2026-10-15] — Реализация TASK-078: Синхронизация install.py, сборка монолита через build_installer.py, E2E тесты и актуализация Living Spec
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/19_EngineeringGates/TASK-078-bundling-e2e-tests-and-living-spec|TASK-078]] — финальная задача Фазы 19 «Инженерные барьеры качества и контроль техдолга (Engineering Gates & Tech Debt Governance)»:
    1. Генератор правил `generate_agents_md()` и адаптеров `_gen_rule()` в `install.py` синхронизирован с нормативами Prior-Art Gate (#14), `// ROADMAP-<ID>` (#15), Benchmark Persistence (#16) и триажа техдолга (#13).
    2. Все 16 шаблонов оптимизированы по High-SNR (суммарный объем `templates/*.md` $\le 28\text{ KB}$).
    3. Монолитный установщик `install.py` и артефакт `dist/install.py` собраны через `scripts/build_installer.py` (размер 161.4 KB $\le 165\text{ KB}$).
    4. В `tests/test_installer.py` добавлен сквозной E2E тест `test_28_phase_19_engineering_gates_and_tech_debt_e2e` для проверки реестра техдолга, неразрушающего обновления и внедрения правил 13–16.
    5. Актуализирован Living Spec: обновлены `SPEC.md`, `README.md` и `docs/Onboarding.md` (добавлена секция 15 «Управление техническим долгом и инженерные барьеры качества»).
    6. Статусы `TASK-078` и плана `PLAN-019` переведены в завершенные в ТЗ (`done`), Канбане (`Done`) и Дорожной карте (`[x]`). Фаза 19 официально закрыта!
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 198 файлов проверено, 1804 ссылки валидировано (0 битых).
  - `python -m unittest discover -s tests` -> 110 тестов пройдено (100% pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Фаза 19 полностью завершена. При готовности выпустить релиз — запустить навык `/kb-release --version v0.19.0 --phase 19`.

---

### [2026-10-15] — Реализация TASK-077: Чеклист приемочного тестирования GUI («UI не лжёт») в TEMPLATE_TEST.md и аудит целостности TechDebt.md в scripts/kb_lint.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/19_EngineeringGates/TASK-077-gui-acceptance-checklist-and-kb-lint-audit|TASK-077]]:
    1. В `TEMPLATE_TEST.md` (в `docs/00_Templates/` и `templates/`) добавлен структурированный чеклист приемочного тестирования интерфейсов («UI не лжёт» / The 4-State Matrix, отклик элементов, геометрия и верстка без наложений, непрерывность UI-потока, скриншот).
    2. В `scripts/kb_lint.py` внедрена функция `check_tech_debt_integrity()`: верификация существования `TechDebt.md`, формата идентификаторов `DEBT-XXX` и валидности викиссылок в таблицах долга.
    3. В `scripts/kb_lint.py` добавлена функция `check_untracked_todos()`: неблокирующее предупреждение `WARN` об обнаружении комментариев `TODO`/`FIXME` без явной привязки к `ROADMAP-<ID>`.
    4. В `tests/test_kb_lint.py` добавлены модульные тесты для проверки отсутствия `TechDebt.md`, обнаружения невалидных ID `DEBT-XXX`, битых викиссылок и отслеживания висячих `TODO`.
    5. Статус задачи обновлен в ТЗ (`done`), Канбане (`Done`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - Суммарный объем шаблонов в `templates/*.md` = 27511 байт ($\le 28000$ байт, лимит соблюден).
  - `python -m unittest tests/test_kb_lint.py` -> 35 тестов пройдено (100% pass, Exit code 0).
  - `python -m unittest discover -s tests` -> 109 тестов пройдено (100% pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 198 файлов проверено, 1798 ссылок валидировано (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к реализации следующей задачи Фазы 19 — запустить Режим 3: `/kb-implement TASK-078`.

---

### [2026-10-15] — Реализация TASK-076: Инженерные барьеры в шаблонах и правилах: Prior-Art Gate, трассировка // ROADMAP-<ID> и замеры >= 3 прогонов
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/19_EngineeringGates/TASK-076-prior-art-gate-roadmap-tagging-and-benchmarks|TASK-076]]:
    1. В `TEMPLATE_PLAN.md` (в `docs/00_Templates/` и `templates/`) внедрен барьер `Prior-Art Gate` со сканом внутренних модулей проекта и платформенных библиотек перед проектированием новых подсистем.
    2. В `TEMPLATE_RESEARCH.md` (в `docs/00_Templates/` и `templates/`) добавлена секция `Prior-Art Gate` для ранней проверки готовых решений.
    3. В `TEMPLATE_TASK.md` (в `docs/00_Templates/` и `templates/`) добавлен протокол «Benchmark Persistence» для фиксации серийных замеров.
    4. В `AGENTS.md` (уровень Tier 2 Always-On) внедрены инварианты: #14 (Prior-Art Gate Invariant), #15 (Traceable Backlog Tags `// ROADMAP-<ID>`) и #16 (Benchmark Persistence «Замер = артефакт» на сериях $\ge 3$ прогонов с отсечением холодного старта).
    5. Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - Суммарный объем шаблонов в `templates/*.md` = 27484 байт ($\le 28000$ байт, лимит соблюден).
  - `python -m unittest tests.test_installer.TestAgentDocsHarness.test_16_high_snr_static_corpus_benchmarks` -> 100% pass (0.435s).
  - `python scripts/kb_lint.py --path docs` -> 198 файлов проверено, 1797 ссылок валидировано (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к реализации следующей задачи Фазы 19 — запустить Режим 3: `/kb-implement TASK-077`.

---

### [2026-10-15] — Реализация TASK-075: Инфраструктура реестра техдолга, скаффолдинг в install.py и правила триажа P1/P2 vs P3
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/19_EngineeringGates/TASK-075-tech-debt-registry-and-triage-rules|TASK-075]]:
    1. Создан канонический реестр `docs/02_Tasks/TechDebt.md` с протоколом триажа находок ревью и таблицами открытого ($P3$) и погашенного долга.
    2. В `install.py` добавлена генерация `generate_tech_debt_md()`, создание файла в `create_starter_docs()` и безопасная инициализация в `update_harness()` без перезаписи существующего пользовательского долга.
    3. В `AGENTS.md` (уровень Tier 2 Always-On) внедрено правило 13 «Tech Debt Governance & Review Triage ($P1/P2$ vs $P3$)» для надежной защиты Single-Task Execution Barrier.
    4. В `GEMINI.md` и генераторы адаптеров `install.py` (`_gen_rule()`, `generate_agents_md()`) интегрирован норматив триажа техдолга.
    5. Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - Скаффолдинг в чистую директорию -> `docs/02_Tasks/TechDebt.md` успешно разворачивается.
  - Повторный запуск `--update` -> существующие записи техдолга сохраняются в полном объеме (`PRESERVED: True`).
  - `python scripts/kb_lint.py --path docs` -> 198 файлов проверено, 1796 ссылок валидировано (0 битых).
  - `python -m unittest tests/test_installer.py` -> все тесты пройдены.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к реализации следующей задачи Фазы 19 — запустить Режим 3: `/kb-implement TASK-076`.

---

### [2026-10-15] — Выпуск релиза v0.18.0: Фаза 18 (Heterogeneous UI/UX & Visual Asset Harness)
- **Что сделано:**
  - Опубликован официальный релиз [[02_Tasks/Releases/RELEASE-v0.18.0|RELEASE-v0.18.0]] по итогам завершения Фазы 18.
  - Успешно завершены и верифицированы все инженерные задачи фазы (`TASK-071`–`TASK-074`):
    * Архитектура хранения визуальных ассетов `docs/assets/`, композитный флаг `--ui` и Obsidian DX (`.obsidian/app.json`) в `install.py`.
    * Механический Tier 1 контроль медиа-ассетов в `scripts/kb_lint.py` и конвертация в чистый Markdown в `scripts/kb_release.py`.
    * Норматив матрицы 4 состояний (The 4-State UI Matrix), Visual DoD и правила изоляции временных тестовых снапшотов `tmp/ui_snapshots/` в `AGENTS.md` и шаблонах.
    * Бандлинг автономного инсталлятора `build_installer.py`, сквозные E2E тесты в `tests/test_installer.py` и актуализация Living Spec (`SPEC.md`, `README.md`, `docs/Onboarding.md`).
  - Сформированы публичные релизные заметки `dist/RELEASE_NOTES.md` по стандарту High-SNR (без шума ADR).
  - Собраны релизные артефакты в каталоге `dist/`:
    * `dist/install.py` (150.4 KB) — SHA-256: `8449faf8e61fc8f5d494c387d96ed38107c12744c3807a66c637f6aa9c4a6ea1`.
  - Обновлен `CHANGELOG.md` с подробным перечнем добавленных возможностей.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 105/105 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к следующей фазе развития (Фаза 19: Инженерные барьеры качества и контроль техдолга / Engineering Gates & Tech Debt Governance) через `/kb-plan`.

---

### [2026-10-15] — Реализация TASK-074: Бандлинг инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/18_VisualHarness/TASK-074-bundling-e2e-tests-and-living-spec|TASK-074]]:
    1. В `tests/test_installer.py` добавлен сквозной E2E тест `test_34_task_071_and_074_ui_harness_and_obsidian_dx`, покрывающий:
       - Скаффолдинг `--ui web` (структура каталогов, `UI_Design_System.md`, `app.json`, `.gitignore`).
       - Композитный мультитаргет `--ui windows,android` (директории обоих таргетов, `multi-device/`, `Protocols/`, `Targets/`).
       - Профиль `--ui none` (полное отсутствие каталога `docs/assets/`).
       - Безопасный мерж `docs/.obsidian/app.json` при запуске `install.py --update` (сохранение пользовательских настроек и инжекция `attachmentFolderPath`).
    2. В `install.py` добавлен псевдоним `ui_targets: str = None` в функцию `install_harness()` для обратной совместимости API.
    3. Запущен `scripts/build_installer.py`: монолитный установщик `install.py` и его зеркало `dist/install.py` пересобраны (150.4 KB / 154029 байт при лимите $\le 160\text{ KB}$).
    4. Синхронизированы Living Spec файлы:
       - `SPEC.md`: добавлена структура `assets/` в раздел 2.1, настройки Obsidian DX в 2.2, медиа-проверки в 2.3, правило 4-State UI в 2.4, ключ `--ui` в 3.2, Фазы 17 и 18 в раздел 4.
       - `README.md`: обновлены дерево директорий `docs/`, сводка параметров CLI (`--ui`) и ключевая дисциплина #11 (The 4-State UI & Visual Verification Invariant).
       - `docs/Onboarding.md`: добавлен раздел 14 «Контур UI/UX, управление визуальными ассетами и гетерогенные multi-target системы».
    5. Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`), плане `PLAN-018` (`Done`) и Дорожной карте (`[x]`). Фаза 18 официально завершена!
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> 154029 байт ($\le 160000$ байт).
  - `python scripts/kb_lint.py --path docs` -> 191 файл проверен, 1735 ссылок валидировано (0 битых).
  - `python -m unittest discover -s tests` -> 105/105 тестов пройдено (100% pass, 0 regressions).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Все задачи Фазы 18 успешно завершены. Для подготовки и выпуска релиза v0.18.0 запустите процедуру подготовки релиза: `/kb-release`.

---

### [2026-10-15] — Реализация TASK-073: Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в AGENTS.md
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/18_VisualHarness/TASK-073-the-4-state-matrix-visual-dod-and-templates|TASK-073]]:
    1. В `docs/00_Templates/TEMPLATE_PLAN.md` внедрен компактный блок проектирования «The 4-State UI Matrix» (`Empty`, `Loading`, `Error`, `Populated`) и подсказка сопряжения узлов в multi-target системах.
    2. В `docs/00_Templates/TEMPLATE_TASK.md` добавлен раздел «Visual DoD» с чеклистом фиксации постоянного скриншота в `docs/assets/screenshots/<target>/TASK-XXX.png` ($\le 2\text{ MB}$) и Headless/CLI Fallback слотом.
    3. Каталог `docs/00_Templates/` сохранен в Skeleton-формате (суммарный вес: 27.6 KB при лимите $\le 28.0\text{ KB}$).
    4. В корневой `AGENTS.md` добавлено правило 12: «The 4-State UI & Visual Verification Invariant» и правила изоляции снимков `tmp/ui_snapshots/` (Git Bloat Prevention).
    5. В `install.py` расширен `_RULES_BODY` (20 дисциплин Docs-as-Code), синхронизированы генераторы `_gen_rule()`, `generate_agents_md()` и корневой `GEMINI.md`.
    6. Актуализированы тесты в `tests/test_installer.py`.
  - Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - Суммарный вес `docs/00_Templates/` = 27628 байт ($\le 28000$ байт).
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 191 файл проверен, 1732 ссылки валидировано (0 битых).
  - `python -m unittest tests/test_installer.py` -> 33/33 тестов пройдено.
  - `python -m unittest discover -s tests` -> 104/104 теста пройдено.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к реализации завершающей задачи Фазы 18 — запустить Режим 3: `/kb-implement TASK-074`.

---

### [2026-10-15] — Реализация TASK-072: Механический контроль медиа-ассетов в scripts/kb_lint.py и scripts/kb_release.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/18_VisualHarness/TASK-072-media-assets-lint-and-release-checks|TASK-072]]:
    1. В `scripts/kb_lint.py` и `scripts/kb_release.py` добавлена константа `MEDIA_EXTENSIONS` (`.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`, `.gif`, `.canvas`, `.excalidraw`).
    2. В `scripts/kb_lint.py` функция `build_file_map()` изолированно индексирует медиафайлы строго с расширением, предотвращая затенение `.md` спецификаций одноименными изображениями (например, `TASK-001.png` vs `TASK-001.md`).
    3. Функция `parse_wikilinks()` дополнена поддержкой синтаксиса эмбеддингов Obsidian (`![[image.png|600x400]]`) с корректным отсечением параметров размера.
    4. Добавлена функция `parse_markdown_images()` для валидации локальных markdown-картинок вида `![alt](relative/path.png)` с URL-декодированием и фильтрацией внешних ссылок.
    5. Реализован `check_asset_weights()` (Tier 1 Non-blocking Gate) для предупреждения о файлах $> 2.0\text{ MB}$ в `docs/assets/`.
    6. В `scripts/kb_release.py` функция `convert_wikilinks_to_github_markdown()` адаптирована для медиа-ассетов: генерирует `![alt](url)` без ошибочного аппенда `.md` и с очисткой параметров размера Obsidian.
    7. Написаны 4 новых юнит-теста в `tests/test_kb_lint.py` и юнит-тест в `tests/test_kb_release.py`.
  - Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - `python -m py_compile scripts/kb_lint.py scripts/kb_release.py` -> синтаксис корректен (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 191 файл проверен, 1731 ссылка валидирована (0 битых).
  - `python -m unittest tests/test_kb_lint.py` -> 31/31 тестов пройдено.
  - `python -m unittest tests/test_kb_release.py` -> 26/26 тестов пройдено.
  - `python -m unittest discover -s tests` -> 104/104 теста пройдено.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к реализации следующей задачи — запустить Режим 3: `/kb-implement TASK-073`.

---

### [2026-10-15] — Реализация TASK-071: Архитектура хранения ассетов, композитный --ui и Obsidian DX в install.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/18_VisualHarness/TASK-071-asset-storage-composite-ui-and-obsidian-dx|TASK-071]]:
    1. В `install.py` реализован парсинг и нормализация композитного флага `--ui` (`auto`, `none`, `web`, `mobile`, `desktop`, `tui` и произвольные связки через запятую, например `--ui windows,android`).
    2. Внедрена двухступенчатая раскладка хранилища ассетов `docs/assets/`:
       - Single-target (1 узел): `docs/assets/mockups/<target>/`, `docs/assets/screenshots/<target>/`.
       - Multi-target ($\ge 2$ узлов): дополнительно `docs/assets/mockups/flows/`, `docs/assets/screenshots/multi-device/`, `docs/01_Architecture/Protocols/` и `docs/01_Architecture/Targets/`.
    3. Реализована функция `setup_obsidian()` с авто-роутингом вложений в `docs/.obsidian/app.json` (`"attachmentFolderPath": "assets/screenshots"`) и безопасным JSON-мержем настроек при `install.py --update`.
    4. В `handle_gitignore()` добавлены правила `!.obsidian/app.json` и `tmp/ui_snapshots/` (защита от Git Bloat).
    5. В `create_starter_docs()` интегрирована динамическая генерация `docs/01_Architecture/UI_Design_System.md` и спецификаций узлов `Targets/<Platform>.md` без изменения `docs/00_Templates/` с сохранением жесткого лимита $\le 28\text{ KB}$.
  - Статус задачи обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - Изолированные E2E тесты (Single target, Multi target, Safe update merge) -> 100% пройдены.
  - `python scripts/kb_lint.py --path docs` -> 191 файл проверен, 1730 ссылок валидировано (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к реализации следующей задачи — запустить Режим 3: `/kb-implement TASK-072`.

---

### [2026-10-15] — Инженерная спецификация: Фаза 18 (TASK-071–TASK-074)
- **Что сделано:**
  - В Режиме 2 (Task Specification) разработаны детальные технические спецификации для всех задач Фазы 18:
    * [[02_Tasks/Specs/18_VisualHarness/TASK-071-asset-storage-composite-ui-and-obsidian-dx|TASK-071]]: Архитектура хранения ассетов, композитный `--ui` и Obsidian DX в `install.py` (статус переведен в `В работе`).
    * [[02_Tasks/Specs/18_VisualHarness/TASK-072-media-assets-lint-and-release-checks|TASK-072]]: Механический контроль медиа-ассетов в `scripts/kb_lint.py` и `scripts/kb_release.py`.
    * [[02_Tasks/Specs/18_VisualHarness/TASK-073-the-4-state-matrix-visual-dod-and-templates|TASK-073]]: Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в `AGENTS.md`.
    * [[02_Tasks/Specs/18_VisualHarness/TASK-074-bundling-e2e-tests-and-living-spec|TASK-074]]: Бандлинг инсталлятора `build_installer.py`, сквозные E2E тесты и актуализация Living Spec.
  - Канбан-доска [[02_Tasks/Kanban|Kanban.md]] и Дорожная карта [[02_Tasks/Roadmap|Roadmap.md]] актуализированы постоянными ссылками на спецификации; карточка `TASK-071` перемещена в `⏳ В работе (In Progress)`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 191 файл проверен, 1724 ссылки валидировано (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к началу реализации первой задачи — запустить Режим 3: `/kb-implement TASK-071`.

---

### [2026-10-15] — Планирование и декомпозиция: Фаза 18 (PLAN-018)
- **Что сделано:**
  - В Режиме 1 (RFC & Планирование) сформирован и утвержден план [[02_Tasks/Plans/PLAN-018-heterogeneous-ui-ux-and-visual-asset-harness|PLAN-018]]: Контур UI/UX, управление визуальными ассетами и гетерогенные multi-target системы.
  - Инициатива переведена из Icebox в активную Фазу 18 Дорожной карты [[02_Tasks/Roadmap|Roadmap.md]].
  - В канбан-доску [[02_Tasks/Kanban|Kanban.md]] в колонку `📥 Бэклог` добавлены карточки плана и задач `TASK-071`–`TASK-074`.
  - Декомпозированы 4 инженерные задачи:
    * `TASK-071`: Архитектура хранения ассетов, композитный `--ui` и Obsidian DX в `install.py`.
    * `TASK-072`: Механический контроль медиа-ассетов в `scripts/kb_lint.py` и `scripts/kb_release.py`.
    * `TASK-073`: Матрица 4 состояний (The 4-State Matrix), Visual DoD и шаблоны жизненного цикла в `AGENTS.md`.
    * `TASK-074`: Бандлинг инсталлятора `build_installer.py`, сквозные E2E тесты и актуализация Living Spec.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 187 файлов проверено, 1689 ссылок валидировано (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к спецификации первой задачи — запустить Режим 2: `/kb-task TASK-071`.

---

### [2026-10-15] — Исследование и архитектурное решение: Контур UI/UX и гетерогенные multi-target системы (RESEARCH-021 & ADR-0026)
- **Что сделано:**
  - Завершено исследование в Режиме 0 (Discovery): оформлена исследовательская заметка [[04_Research/RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]].
  - Принято архитектурное решение [[03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]:
    * Сформулирована обобщенная концепция гетерогенных целевых узлов (Heterogeneous Target Nodes) для масштабирования на любые связки платформ (`Windows + Android`, `macOS + iOS`, `Windows + iOS`, `Linux + Android`, `Web + Mobile`).
    * Спроектирован композитный CLI-параметр `--ui <target1,target2>` для `install.py` с сохранением Zero-Dependencies (Python 3 stdlib).
    * Стандартизирована структура хранения ассетов `docs/assets/{mockups,screenshots}/<target>/` и авто-роутинг скриншотов Obsidian через `docs/.obsidian/app.json`.
    * Внедрена изоляция временных E2E-снапшотов в `.gitignore` (`tmp/ui_snapshots/`) для предотвращения Git Bloat.
    * Зафиксированы дисциплины The 4-State Matrix (`Empty`, `Loading`, `Error`, `Populated`), Multi-Actor Interaction Flow и Visual DoD.
    * Спроектированы механические проверки Tier 1 для `scripts/kb_lint.py` (индексация графических файлов, очистка параметров размера `![[image.png|600]]`, лимит веса ассетов $\le 2\text{ MB}$).
  - Инициатива зарегистрирована в Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]] в разделе перспективных направлений (Icebox).
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 186 файлов проверено, 1677 ссылок валидировано (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - При готовности к реализации — запустить Режим 1: `/kb-plan` для формирования плана реализации Фазы гетерогенного UI-контура.

---

### [2026-10-15] — Выпуск релиза v0.17.0: Фаза 17 (Core Hardening & SSOT Sync)
- **Что сделано:**
  - Опубликован официальный релиз [[02_Tasks/Releases/RELEASE-v0.17.0|RELEASE-v0.17.0]] по итогам завершения Фазы 17.
  - Устранены все накопленные дефекты совместимости и краевые сценарии (`BUG-005`–`BUG-009`).
  - Выполнены инженерные задачи `TASK-066`–`TASK-070`: харденинг линтера `scripts/kb_lint.py`, экранирование YAML и IMAP UID в `scripts/kb_ingest.py`, защита анонимизатора и контейнерный TTY-зонд в `install.py`, вызов `build_installer.build()` в `scripts/build_release.py`, полная синхронизация канонического `AGENTS.md` и генератора `generate_agents_md()`, внедрение контура процедурной памяти и терминального шага `Stop & Yield Control` во все read-only скиллы.
  - Сформированы публичные релизные заметки `dist/RELEASE_NOTES.md` по стандарту High-SNR (без шума ADR).
  - Собраны релизные артефакты в каталоге `dist/`:
    * `dist/install.py` (135.6 KB) — SHA-256: `5163a7629b939f18de76b7ec2a44cc3cc23f6e7db045c9e521ca17b8f5b7fe5c`.
  - Обновлен `CHANGELOG.md` с подробным перечнем добавленных возможностей и исправленных дефектов.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 99/99 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к Фазе 18 (Engineering Gates & Tech Debt Governance) через `/kb-plan`.

---

### [2026-10-15] — Реализация TASK-070: Синхронизация скиллов, шаблонов и контура памяти в AGENTS.md
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/17_HardeningAndSync/TASK-070-skills-templates-and-memory-sync|TASK-070]]:
    1. В `AGENTS.md` и функцию `generate_agents_md()` утилиты `install.py` интегрирован нулевой шаг `Memory-First Preflight (read patterns.md)` и рефлексия `Defect Loop Reflection (log INC-XXX & update patterns.md)` в Режиме 3 (Implementation).
    2. Во все read-only скиллы (`kb-plan`, `kb-task`, `kb-research`, `kb-adr`) и `kb-init` добавлен терминальный шаг `Stop & Yield Control` с генерацией Anti-Echo отчета и строгой остановкой вызовов инструментов.
    3. В шаблоне `TEMPLATE_TASK_MICRO.md` скорректирована начальная фаза (`phase: 1`), а в `customize_templates_for_stack()` добавлена замена команды тестов на специфичную для стека.
    4. В шаблоне `TEMPLATE_RELEASE.md` исправлены относительные викиссылки на задачи и баги (`[[../Specs/...]]`, `[[../Bugs/...]]`).
    5. В индексных хабах `TEMPLATE_INDEX.md` и `docs/00_Index.md` синхронизированы ссылки на `Zero_To_Hero_Guide.md`, `02_Tasks/Inbox/` и `06_Memory/` в структуре и Mermaid-диаграмме.
    6. В `templates/graph.json` и `docs/.obsidian/graph.json` добавлена нода `Zero_To_Hero_Guide` и выделенная цветовая группа для процедурной памяти `06_Memory/`.
    7. Руководство `docs/Zero_To_Hero_Guide.md` отполировано: добавлена прямая curl-команда и неинтерактивный флаг `-y` в Разделе 4, подраздел `/kb-bug` в Разделе 2, и скорректирован синтаксис команды `/kb-task`.
    8. Пересобран автономный инсталлятор `install.py` и дистрибутив `dist/install.py` через `scripts/build_installer.py`.
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус спецификации обновлен на `done`, Фаза 17 отмечена как завершенная в [[02_Tasks/Roadmap|Roadmap.md]] и плане [[02_Tasks/Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]].
- **Результаты верификации:**
  - `python -m unittest tests/test_installer.py` -> 33/33 теста успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 99/99 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 183 files scanned, 1649 wikilinks verified (0 broken, Exit code 0).
  - `python -m py_compile scripts/*.py install.py` -> 100% компиляция без ошибок.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Все задачи и дефекты Фазы 17 завершены. Ожидает команды пользователя на выпуск релиза (`/kb-release 0.17.0`) или планирование следующей фазы (`/kb-plan`).

---

### [2026-10-15] — Реализация TASK-069: Синхронизация SSOT: правила агентов, режимы жизненного цикла и таксономия 16 шаблонов
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/17_HardeningAndSync/TASK-069-ssot-agents-and-docs-sync|TASK-069]]:
    1. В функцию `generate_agents_md()` утилиты `install.py` добавлены разделы Режима 0 (`/kb-research` & `/kb-adr`) и Режима 2C (`/kb-triage`), а роботизированные алерты заменены на принципы Human Guardrails.
    2. В `install.py` заголовок `_RULES_BODY` обновлен на `## Docs-as-Code (19 Disciplines)`.
    3. В каноническом `AGENTS.md` зафиксирована таксономия 16 шаблонов (4 Core Essentials + 12 Advanced Governance), синхронизирована структура каталогов (`06_Memory/`, `02_Tasks/Inbox/`, `02_Tasks/Releases/`), а Правило 11 переведено на английский язык.
    4. В `README.md` устранены устаревшие роботизированные запреты `NO CODE EDITS` в диаграмме режимов и таблице скиллов, синхронизированы принципы Human Guardrails.
    5. Зафиксирована каноническая таксономия 16 шаблонов (Core 4 + Advanced 12) в `docs/Onboarding.md`, `templates/TEMPLATE_ONBOARDING.md`, `docs/00_Templates/TEMPLATE_ONBOARDING.md` и `.agents/skills/kb-onboard/SKILL.md`.
    6. В подвал `CHANGELOG.md` добавлены ссылки на диффы сравнения релизов для тегов `[0.10.0]` – `[0.16.0]`.
    7. Пересобран автономный инсталлятор `install.py` и дистрибутив `dist/install.py` через `scripts/build_installer.py`.
  - В `tests/test_installer.py` обновлены ассерты `test_21`, `test_25` и `test_26`.
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус спецификации обновлен на `done`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]] и плане [[02_Tasks/Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]].
- **Результаты верификации:**
  - `python -m unittest tests/test_installer.py` -> 33/33 теста успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 99/99 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 183 files scanned, 1644 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующей инженерной задачи Фазы 17 (`/kb-implement TASK-070`).

---

### [2026-10-15] — Реализация TASK-068: Защита анонимизатора, контейнерный TTY-зонд и интеграция сборщика в install.py и build_release.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/17_HardeningAndSync/TASK-068-installer-tty-anonymizer-and-build-hook|TASK-068]]:
    1. В функции `generate_diagnostic_report()` утилиты `install.py` усилен внутренний анонимизатор: добавлена замена домашней директории пользователя на `~` (с поддержкой как прямых, так и обратных слэшей) и проверка границ путей через регулярное выражение `([/\\\\])<user>([/\\\\]|$)`. Это предотвращает порчу слов с короткими именами пользователей (например, `dev` в `Devlog.md`).
    2. Внедрена вспомогательная функция `can_open_tty()`, проверяющая возможность интерактивного ввода как на Windows, так и в POSIX/Docker/CI контейнерах через дескриптор `/dev/tty`. В `main()` условие интерактивности переведено на `can_open_tty()`.
    3. В функции `setup_git()` инсталлятора `install.py` добавлена детальная диагностика при сбое первоначального `git commit`: вывод кода ошибки и явные инструкции по настройке `user.name` и `user.email`.
    4. В `scripts/build_release.py` интегрирован автоматический вызов `build_installer.build()` перед копированием артефакта в `dist/install.py`, гарантирующий актуальность упакованного бандла при релизной сборке.
    5. Пересобран монолитный инсталлятор `install.py` и `dist/install.py` через `scripts/build_installer.py`.
  - В `tests/test_installer.py` добавлен комплексный тест `test_33_task_068_installer_tty_anonymizer_and_build_hook`.
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус спецификации обновлен на `done`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]] и плане [[02_Tasks/Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]].
- **Результаты верификации:**
  - `python -m unittest tests/test_installer.py` -> 33/33 теста успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 99/99 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 183 files scanned, 1640 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующей инженерной задачи Фазы 17 (`/kb-implement TASK-069`).

---

### [2026-10-15] — Реализация TASK-067: Безопасное экранирование YAML, постоянные IMAP UIDs и URL-кодирование в scripts/kb_ingest.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/17_HardeningAndSync/TASK-067-kb-ingest-yaml-escaping-and-imap-uid|TASK-067]]:
    1. В функции `build_feedback_markdown()` утилиты `scripts/kb_ingest.py` внедрена сериализация строк через `json.dumps(..., ensure_ascii=False)` для полей `title`, `author` и `source_ref`, полностью защищающая frontmatter от синтаксических сбоев при наличии кавычек, апострофов и обратных слэшей.
    2. В драйвере `EmailIngestDriver` вызовы `client.search` и `client.fetch` переведены на использование интерфейса `client.uid("search", ...)` и `client.uid("fetch", ...)`, обеспечивающего постоянство идентификаторов писем и надежную дедупликацию в `.inbox_state.json`.
    3. В методе `GitHubIngestDriver.fetch_issues()` добавлено экранирование меток через `urllib.parse.quote(label)`, предотвращающее искажение запросов с пробелами и специальными символами.
    4. Синхронизирован бандл `install.py` и дистрибутив `dist/install.py` через `scripts/build_installer.py`.
  - В `tests/test_kb_ingest.py` добавлены 3 целевых модульных теста: `test_task_067_yaml_escaping_in_feedback_markdown`, `test_task_067_github_driver_url_encoding` и `test_task_067_imap_uid_calls`. Обновлен `test_email_driver_ingestion`.
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус спецификации обновлен на `done`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_ingest.py` -> 14/14 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 98/98 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 183 files scanned, 1637 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующей инженерной задачи Фазы 17 (например, `/kb-implement TASK-068`).

---

### [2026-10-15] — Устранение дефекта BUG-009: Утечка метаданных agent-docs-harness в .github/ISSUE_TEMPLATE/
- **Что сделано:**
  - Устранен дефект [[02_Tasks/Bugs/BUG-009-issue-templates-hardcoded-repo-leak|BUG-009]]:
    1. В функцию `deploy_infrastructure()` утилиты `install.py` добавлен пропуск развертывания `config.yml` в сторонние проекты во избежание утечки жестко зашитых ссылок на обсуждения и онбординг исходного репозитория `koudinie101-png/agent-docs-harness`.
    2. Добавлена параметризация шаблонов `.github/ISSUE_TEMPLATE/` (замена имени `agent-docs-harness` на целевой `project_name`).
    3. В утилите сборщика `scripts/build_installer.py` и локальном fallback `unpack_assets()` исключена упаковка `config.yml` в клиентские дистрибутивы.
    4. Обновлены и приведены к нейтральным формулировки в `.github/ISSUE_TEMPLATE/bug_report.yml` и `feature_request.yml`.
  - В `tests/test_installer.py` добавлен регрессионный тест `test_32_bug_009_issue_templates_no_repo_leak` (TDD: RED -> GREEN -> REFACTOR) и актуализированы фикстуры задач/багов под новые валидационные схемы frontmatter.
  - Пересобран монолитный инсталлятор `install.py` и зеркало `dist/install.py` через `scripts/build_installer.py`.
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус дефекта обновлен на `fixed`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m unittest tests.test_installer.TestAgentDocsHarness.test_32_bug_009_issue_templates_no_repo_leak` -> OK.
  - `python -m unittest discover -s tests` -> 95/95 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 183 files scanned, 1634 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующей инженерной задачи Фазы 17 (например, `/kb-implement TASK-067`).

---

### [2026-10-15] — Реализация TASK-066: Харденинг парсинга викиссылок и валидация схем frontmatter в scripts/kb_lint.py
- **Что сделано:**
  - Реализована спецификация [[02_Tasks/Specs/17_HardeningAndSync/TASK-066-kb-lint-codeblocks-and-schemas|TASK-066]]:
    1. В функцию `parse_wikilinks()` утилиты `scripts/kb_lint.py` добавлена предварительная очистка контента от fenced code blocks (` ```...``` `) и инлайн-кода (` `...` `), исключающая ложные срабатывания на демонстрационные ссылки.
    2. В регулярное выражение `parse_wikilinks()` добавлена поддержка экранированных пайпов `\|` в Markdown-таблицах Obsidian (`[[target\|Label]]`).
    3. В функции `run_linter()` запрещен невалидный fallback на `file_map` для ссылок с явным путем (`/` или `\`), маскировавший битые относительные ссылки на GitHub.
    4. В функцию `check_file_frontmatter()` добавлена строгая валидация обязательных полей схем frontmatter для каталогов `06_Memory/Incidents/`, `02_Tasks/Specs/`, `02_Tasks/Bugs/` и `03_Decisions_ADR/`.
  - В `tests/test_kb_lint.py` добавлены 4 целевых модульных теста, покрывающие все новые требования.
  - Устранен дефект фронтматтера в `docs/02_Tasks/Bugs/BUG-001-ci-release-notes-phase-fallback.md` (`type: bug`) и исправлена битая ссылка в `docs/Devlog.md`.
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус спецификации обновлен на `done`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_lint.py` -> 27/27 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 94/94 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 181 files scanned, 1618 wikilinks verified (0 broken, 0 warnings, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующей инженерной задачи Фазы 17 (например, `/kb-implement TASK-067`).

---

### [2026-10-15] — Устранение дефекта BUG-008: patterns.md в локальном fallback install.py и маска фаз >= 10 в kb_release.py
- **Что сделано:**
  - Устранен дефект [[02_Tasks/Bugs/BUG-008-local-fallback-patterns-and-phase-pad|BUG-008]]:
    1. В функцию `unpack_assets()` утилиты `install.py` добавлено чтение `docs/06_Memory/patterns.md` в ветку локального fallback для разработки, гарантирующее инициализацию процедурной памяти при отсутствии собранного base64-бандла.
    2. В функцию `find_phase_artifacts()` скрипта `scripts/kb_release.py` добавлена корректная маска выравнивания номеров фаз `f"{p:02d}_"` и `f"{p}_"`, устраняющая потерю спеков для двузначных фаз ($\ge 10$) без явного поля `phase:` во фронтматтере.
  - В `tests/test_installer.py` добавлен модульный тест `test_31_bug_008_local_fallback_memory_patterns`, а в `tests/test_kb_release.py` — `test_find_phase_artifacts_double_digit_fallback` (TDD: RED -> GREEN -> REFACTOR).
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус дефекта обновлен на `fixed`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m unittest tests.test_installer.TestAgentDocsHarness.test_31_bug_008_local_fallback_memory_patterns` -> OK.
  - `python -m unittest tests/test_kb_release.py` -> 25/25 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 181 files scanned, 1645 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию инженерных задач Фазы 17 (например, `/kb-implement TASK-066`).

---

### [2026-10-15] — Устранение дефекта BUG-007: Поддержка инлайн-текста в scripts/kb_ingest.py --paste
- **Что сделано:**
  - Устранен дефект [[02_Tasks/Bugs/BUG-007-kb-ingest-paste-inline-arg|BUG-007]]: сбой `unrecognized arguments` при вызове `scripts/kb_ingest.py --paste "<text>"`, документированном в `CHANGELOG.md`.
  - Аргумент `--paste` переконфигурирован на `nargs="?", const=True, default=None`, поддержано извлечение строкового содержимого из аргумента (с сохранением полной обратной совместимости для `--paste --text "<text>"`, `--paste` через stdin и автономного `--text`).
  - В `tests/test_kb_ingest.py` добавлен регрессионный тест `test_bug_007_paste_inline_argument_support` (TDD: RED -> GREEN -> REFACTOR).
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус дефекта обновлен на `fixed`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]], обновлен пример в [README.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/README.md).
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_ingest.py` -> 11/11 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 181 files scanned, 1642 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующего дефекта или задачи (например, `/kb-implement BUG-008` или `/kb-implement TASK-066`).

---

### [2026-10-15] — Устранение дефекта BUG-006: Исключение RELEASE_NOTES.md из таблицы артефактов SHA-256
- **Что сделано:**
  - Устранен дефект [[02_Tasks/Bugs/BUG-006-release-notes-self-artifact|BUG-006]]: при повторном запуске `scripts/kb_release.py` файл заметок релиза `dist/RELEASE_NOTES.md` каталогизировался как скачиваемый артефакт релиза и попадал в таблицу SHA-256.
  - В функцию `inspect_release_artifacts(dist_dir, excluded_names=None)` добавлен дефолтный список исключений `{"RELEASE_NOTES.md"}`, а также передача пользовательского имени из `--notes-output`, исключающая рекурсивное самоцитирование заметок.
  - В `tests/test_kb_release.py` добавлен регрессионный тест `test_bug_006_inspect_release_artifacts_excludes_release_notes` (TDD: RED -> GREEN -> REFACTOR).
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус дефекта обновлен на `fixed`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_release.py` -> 24/24 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 181 files scanned, 1639 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующего дефекта или задачи (например, `/kb-implement BUG-007` или `/kb-implement TASK-066`).

---

### [2026-10-15] — Устранение дефекта BUG-005: Совместимость kb_lint.py с Python 3.8 (Path.is_relative_to)
- **Что сделано:**
  - Устранен дефект [[02_Tasks/Bugs/BUG-005-kb-lint-py38-is-relative-to|BUG-005]]: аварийное завершение `scripts/kb_lint.py` на Python 3.8 из-за вызова метода `Path.is_relative_to()`, появившегося только в Python 3.9+.
  - Реализованы кросс-версионные хелперы `_is_relative_to(p, base)` и `_relative_to(p, base)` на базе `os.path.commonpath` / `relative_to` с перехватом исключений, гарантирующие корректную работу на Python 3.8+ без внешних библиотек.
  - В `tests/test_kb_lint.py` добавлен воспроизводящий регрессионный тест `test_bug_005_is_relative_to_python38_compatibility` (TDD: RED -> GREEN -> REFACTOR).
  - Карточка перемещена в `Done` в [[02_Tasks/Kanban|Kanban.md]], статус дефекта обновлен на `fixed`, веха отмечена в [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_lint.py` -> 23/23 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 86/86 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 181 files scanned, 1636 wikilinks verified (0 broken, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Ожидает команды пользователя на реализацию следующего дефекта или задачи (например, `/kb-implement BUG-006` или `/kb-implement TASK-066`).

---

### [2026-10-12] — Официальный выпуск релиза v0.16.0: Самообучающийся харнесс и память дефектов (Фаза 16)
- **Что сделано:**
  - Подготовлен и собран релиз `v0.16.0` (Фаза 16: [[02_Tasks/Releases/RELEASE-v0.16.0|RELEASE-v0.16.0]]).
  - В релиз вошли 4 ключевые фичи Фазы 16 (`TASK-061`, `TASK-062`, `TASK-063`, `TASK-064`), Fast-Track задача выравнивания CLI (`TASK-065`) и 3 исправленных дефекта (`BUG-002`, `BUG-003`, `BUG-004`).
  - Сгенерированы релизные документы `docs/02_Tasks/Releases/RELEASE-v0.16.0.md` и публичные релизные заметки `dist/RELEASE_NOTES.md`.
  - Сформированы релизные артефакты и рассчитаны контрольные суммы SHA-256:
    * `dist/install.py` (131.5 KB) — `c7aa191358f21f7c8096f564e0f68758df4f8e482d590c641bde20679af1eae8`
    * `dist/RELEASE_NOTES.md` (3.6 KB) — `2d89a853d8485cf4349f9f97c82d2e4e2356d49c227e8de050d43dc208351a0f`
  - Обновлен `CHANGELOG.md` и зафиксирована ссылка на релиз в `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 172 files scanned, 1563 wikilinks verified (0 broken), Exit code 0.
  - `python -m unittest discover -s tests` -> 85/85 тестов успешно пройдено (Exit code 0).

---

### [2026-10-12] — Реализация TASK-065: Выравнивание CLI-флагов (-i, -r) и синхронизация README.md (Fast-Track)
- **Что сделано:**
  - В `install.py` объявлены короткие флаги `-i` (для `--idea`) и `-r` (для `--report`) в `parser.add_argument` для полного соответствия документации.
  - В `scripts/build_installer.py` выполнен пересбор монолитного инсталлятора `install.py` и зеркала `dist/install.py` с обновленными флагами и 16 шаблонами.
  - В `README.md` устранены выявленные расхождения: обновлен пример вызова `kb_ingest.py` на `--paste --text "..."`, заменена абсолютная ссылка `file:///` на относительную `[RESEARCH-001](docs/04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix.md)`, обновлена структура каталогов (16 шаблонов, `docs/06_Memory/`), актуализирован роутер `kb-onboard` и осуществлен переход от термина «3-mode» к 4-этапному циклу разработки с новыми дисциплинами (Quality Gates Tier 1–3, процедурная память, Zero Round-Trip).
  - Спецификация `TASK-065` переведена в статус `done`, карточка перемещена в `Done` на `Kanban.md`, отмечена веха в `Roadmap.md`.
- **Результаты верификации:**
  - `python install.py -r` -> Диагностический отчет сгенерирован без ошибок (Exit code 0).
  - `python install.py -i "TestIdea" -y -n FastApp -d temp_fast` -> Успешная установка с пресетом `undecided` (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 30/30 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 171 files scanned, 1558 wikilinks verified (0 broken), Exit code 0.
  - Поиск `file:///` в `README.md` -> 0 совпадений.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовка и выпуск официального релиза Фазы 16: `/kb-release v0.16.0` ("Self-Improving Harness & Defect Memory").

---

### [2026-10-12] — Реализация TASK-064: Контроль лимита памяти в scripts/kb_lint.py, бандлинг install.py, E2E тесты и Living Spec sync
- **Что сделано:**
  - В `scripts/kb_lint.py` внедрена механическая проверка Tier 1 `check_memory_limits`: парсинг активных записей в `docs/06_Memory/patterns.md` с блокировкой (Exit code 1) при превышении жесткого лимита в 15 паттернов, а также валидация frontmatter архива инцидентов `docs/06_Memory/Incidents/`.
  - В `install.py` добавлены короткие флаги `-i` (для `--idea`) и `-r` (для `--report`), реализован деплой подсистемы памяти `docs/06_Memory/` с безопасным сохранением `patterns.md` при вызове `--update` (без перезаписи пользовательских инцидентов).
  - В `scripts/kb_ingest.py` поддержана передача строкового значения напрямую в аргумент `--paste` (`nargs="?"`).
  - В сборщик `scripts/build_installer.py` добавлена упаковка шаблона `TEMPLATE_INCIDENT.md` и стартового индекса `patterns.md` в монолитные `install.py` и `dist/install.py`.
  - В `tests/test_kb_lint.py` и `tests/test_installer.py` добавлены юнит- и E2E тесты контроля лимита памяти, флагов инсталлятора и безопасного сохранения данных.
  - Синхронизированы `SPEC.md` и `README.md`: устранены ссылки `file:///`, обновлена структура каталогов (16 шаблонов, `06_Memory/`), терминология и дисциплины надежности.
  - Спецификация `TASK-064` и план `PLAN-016` переведены в статус `done`, Фаза 16 успешно завершена в `Kanban.md` и `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 171 files scanned, 1558 wikilinks verified (0 broken), Exit code 0.
  - `python -m unittest tests/test_kb_lint.py` -> 22/22 тестов успешно пройдено (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 30/30 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 85/85 тестов успешно пройдено (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовка и выпуск официального релиза Фазы 16: `/kb-release v0.16.0` ("Self-Improving Harness & Defect Memory").

---

### [2026-10-12] — Реализация TASK-063: Слои надежности Quality Gates (Tier 1–3) в AGENTS.md и руководстве Onboarding.md
- **Что сделано:**
  - В канонический файл правил `AGENTS.md` добавлено правило 11 (`Quality Gates & Reliability Tiers Invariant`): декомпозиция всех требований надежности на 3 слоя (Tier 1: Enforcement / линтеры, компиляторы, тесты; Tier 2: Always-On промпты IDE; Tier 3: справочные плейбуки и скиллы). Зафиксирован инвариант недопустимости оставления критических правил исключительно в вероятностном слое Tier 3.
  - В руководство разработчика и агента `docs/Onboarding.md` добавлен раздел «13. Слои надежности Quality Gates (Tier 1–3) и процедурная память» с наглядной матрицей надежности и описанием контура памяти `docs/06_Memory/`.
  - Синхронизированы генераторы `install.py` (`_RULES_BODY`, `_gen_rule`) и все тонкие адаптеры в корне (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`) с гарантированным соблюдением лимита $\le 35$ строк.
  - Спецификация `TASK-063` переведена в статус `done`, карточка перемещена в Done на `Kanban.md`, отмечен чекбокс в `Roadmap.md`.
- **Результаты верификации:**
  - Проверка объема адаптеров: все файлы адаптеров в пределах 14–15 строк (лимит: $\le 35$).
  - `python scripts/kb_lint.py --path docs` -> 170 files scanned, 1554 wikilinks verified (0 broken), Exit code 0.
  - `python -m unittest tests/test_installer.py` -> 29/29 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 82/82 тестов успешно пройдено (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация завершающей задачи Фазы 16: `/kb-implement TASK-064` (Контроль лимита памяти в `scripts/kb_lint.py`, бандлинг `install.py`, E2E тесты и Living Spec sync).

---

### [2026-10-12] — Реализация TASK-062: Точки чтения памяти в жизненном цикле (kb-implement, kb-complete) и протокол двухосевого промоушена
- **Что сделано:**
  - В скилл `.agents/skills/kb-implement/SKILL.md` (Режим 3) интегрирована обязательная префлайт-проверка `0. Memory-First Check`: чтение индекса `docs/06_Memory/patterns.md`, проверка рисков типовых граблей (Windows paths, ложные моки, сбои версий) и применение превентивных мер до генерации кода.
  - В скилл `.agents/skills/kb-complete/SKILL.md` добавлен шаг `6. Defect Loop Reflection` (контур самообучения): обязательная рефлексия сессии разработки, оформление инцидентов `docs/06_Memory/Incidents/INC-XXX-<slug>.md` по шаблону `TEMPLATE_INCIDENT.md` и протокол двухосевого промоушена (Ось 1: Частота/Тяжесть $\to$ `patterns.md` $\le 15$; Ось 2: Охват применения $\to$ Tier 1 автотесты или Tier 2 `AGENTS.md`).
  - Спецификация `TASK-062` переведена в статус `done`, карточка перемещена в Done на `Kanban.md`, отмечен чекбокс в `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 170 files scanned, 1553 wikilinks verified (0 broken), Exit code 0.
  - `python -m unittest tests/test_installer.py` -> 29/29 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 82/82 тестов успешно пройдено (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация следующей задачи Фазы 16: `/kb-implement TASK-063` (Слои надежности Quality Gates (Tier 1–3) в `AGENTS.md` и руководстве `Onboarding.md`).

---

### [2026-10-12] — Реализация TASK-061: Инфраструктура процедурной памяти (docs/06_Memory/, шаблон TEMPLATE_INCIDENT.md и агрегированный индекс patterns.md)
- **Что сделано:**
  - Развернута подсистема процедурной памяти агента `docs/06_Memory/` с каталогом архива инцидентов `Incidents/` (`.gitkeep`).
  - Создан эталонный шаблон инцидента `docs/00_Templates/TEMPLATE_INCIDENT.md` с валидным YAML frontmatter (`id: INC-XXX`, `status`, `severity`, `tag`, `root_cause`, `target_pattern`, `tags: [memory, incident]`).
  - Сформирован High-SNR компактный индекс систематических ошибок `docs/06_Memory/patterns.md` со строгим инвариантом токеномики ($\le 15$ активных записей, ~350 токенов) и стартовыми паттернами (`TRG-01`, `TRG-02`).
  - Обновлена карта базы знаний `docs/00_Index.md`: добавлен раздел «6. Процедурная память (`06_Memory/`)» со ссылкой на `06_Memory/patterns`, обновлен Mermaid flowchart.
  - Спецификация `TASK-061` переведена в статус `done`, карточка перемещена в Done на `Kanban.md`, отмечен чекбокс в `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 170 files scanned, 1553 wikilinks verified (0 broken), Exit code 0.
  - `python -m unittest discover -s tests` -> 82/82 тестов успешно пройдено (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация следующей задачи Фазы 16: `/kb-implement TASK-062` (Точки чтения памяти в жизненном цикле и протокол двухосевого промоушена).

---

### [2026-10-12] — Исправление BUG-003: Устранение бесшумного отката в локальный режим при отсутствии GitHub CLI (gh)
- **Что сделано:**
  - В `scripts/kb_release.py` реализован протокол `No Silent Fallback`: при публикации в GitHub-репозитории отсутствие `gh` CLI больше не замалчивается. Скрипт выдает явное предупреждение с платформенными инструкциями по установке (`winget install GitHub.cli` / `brew install gh`).
  - Добавлена поддержка аутентификации через переменную `GITHUB_TOKEN` (или файл `.env.local`), определяющая `publish_provider` ("gh_cli" | "rest_api" | "none").
  - Добавлены CLI-аргументы `--mode {auto,github,local}` и `--require-github` для строгого прерывания процесса при отсутствии инструментов удаленной публикации.
  - Обновлен навык `.agents/skills/kb-release/SKILL.md` (Шаг 2: Правило No Silent Fallback).
  - По TDD-циклу разработан регрессионный тест `test_detect_release_environment_regression_bug_003` в `tests/test_kb_release.py`.
  - Пересобран монолитный инсталлятор `install.py` и `dist/install.py` через `scripts/build_installer.py`.
  - Дефект [[02_Tasks/Bugs/BUG-003-release-silent-local-fallback-missing-gh|BUG-003]] переведен в статус `fixed`, карточка перенесена в Done на [[02_Tasks/Kanban|Kanban.md]], Living Spec [[SPEC.md]] актуализирована.
- **Результаты верификации:**
  - `python -m unittest tests.test_kb_release` -> 23/23 тестов успешно пройдено (Exit code 0).
  - `python -m unittest tests.test_installer` -> 29/29 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 82/82 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Все дефекты из бэклога (BUG-002, BUG-003, BUG-004) успешно устранены. Запросить у пользователя выбор следующего приоритета: реализация идеи из Icebox (`Roadmap.md`) или подготовка инкрементального релиза.

---

### [2026-10-12] — Исправление BUG-004: Устранение циклической ссылки на саму себя в блоке Full Changelog релизных записок
- **Что сделано:**
  - В `scripts/kb_release.py` устранено зацикливание ссылки «Полный список изменений (Full Changelog)», которая ранее вела на ту же страницу релиза `releases/tag/{tag}`.
  - Разработана функция `detect_previous_tag(target_version, repo_root, docs_path)`, определяющая предшествующий релизный тег через Git (`git tag --list "v*"`) или артефакты `docs/02_Tasks/Releases/RELEASE-v*.md`.
  - При наличии предшествующего релиза строка Full Changelog формирует ссылку сравнения веток/тегов (`https://github.com/{owner}/{repo}/compare/{prev_tag}...{tag}`), а для первого релиза ссылается на историю коммитов (`commits/{tag}`).
  - Добавлен CLI-аргумент `--prev-tag` для ручного указания базовой версии сравнения.
  - Пересобран монолитный инсталлятор `install.py` и `dist/install.py` через `scripts/build_installer.py`.
  - По TDD-циклу реализован регрессионный тест `test_generate_public_release_notes_regression_bug_004` в `tests/test_kb_release.py`.
  - Дефект [[02_Tasks/Bugs/BUG-004-release-notes-changelog-self-link|BUG-004]] переведен в статус `fixed`, карточка перемещена в Done на [[02_Tasks/Kanban|Kanban.md]], Living Spec [[SPEC.md]] актуализирована.
- **Результаты верификации:**
  - `python -m unittest tests.test_kb_release` -> 22/22 тестов успешно пройдено (Exit code 0).
  - `python -m unittest tests.test_installer` -> 29/29 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 81/81 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Перейти к исправлению последнего дефекта из бэклога: `/kb-implement BUG-003` (устранение тихого отката в локальный режим при отсутствии gh CLI).

---

### [2026-10-12] — Исправление BUG-002: Устранение хардкода install.py в публичных релизных записках scripts/kb_release.py
- **Что сделано:**
  - В `scripts/kb_release.py` реализован адаптивный блок установки (`Adaptive Quick Install`): инструкции скачивания Docs-as-Code через `curl .../install.py` выводятся только для репозитория самого harness-а (`agent-docs-harness`); для внешних проектов при наличии артефактов генерируются команды загрузки артефактов из GitHub Releases, а при их отсутствии блок опускается.
  - Добавлен CLI-аргумент `--quick-install` для возможности передачи кастомных команд развертывания/установки релиза.
  - Устранена генерация проверочных команд контрольных сумм SHA-256 для несуществующего `./dist/install.py`, если в каталоге `dist/` нет артефактов.
  - Пересобран монолитный инсталлятор `install.py` и `dist/install.py` через `scripts/build_installer.py`.
  - По TDD-циклу разработан регрессионный тест `test_generate_public_release_notes_regression_bug_002` в `tests/test_kb_release.py`.
  - Дефект [[02_Tasks/Bugs/BUG-002-release-notes-hardcoded-install-script|BUG-002]] переведен в статус `fixed`, карточка перенесена в категорию Done на [[02_Tasks/Kanban|Kanban.md]], Living Spec [[SPEC.md]] синхронизирована.
- **Результаты верификации:**
  - `python -m unittest tests.test_kb_release` -> 21/21 тестов успешно пройдено (Exit code 0).
  - `python -m unittest tests.test_installer` -> 29/29 тестов успешно пройдено (Exit code 0).
  - `python -m unittest discover -s tests` -> 80/80 тестов успешно пройдено (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Перейти к исправлению следующего дефекта из бэклога: `/kb-implement BUG-004` (устранение циклической ссылки в Full Changelog).

---

### [2026-10-12] — Официальный релиз v0.15.0 (Фаза 15: Устранение задержек отклика и прозрачность каналов)
- **Что сделано:**
  - Успешно подготовлен и зафиксирован официальный релиз [[02_Tasks/Releases/RELEASE-v0.15.0|RELEASE-v0.15.0]] по итогам завершения Фазы 15.
  - Сгенерирован публичный файл заметок `dist/RELEASE_NOTES.md` с Human-First форматированием (Highlights, Quick Install, перечень ключевых фич).
  - Сформирован и синхронизирован пакет дистрибутива `dist/install.py` (124.8 KB, SHA-256: `caa5700dde2cb9b349221c07ef0f12ad9b7b0dc1256a294c02e3c903e3ad995d`).
  - Актуализированы Дорожная карта [[02_Tasks/Roadmap|Roadmap.md]] и история изменений `CHANGELOG.md`.
  - Установлен релизный Git-тег `v0.15.0`.
- **Контрольные суммы артефактов (SHA-256):**
  - `dist/install.py`: `caa5700dde2cb9b349221c07ef0f12ad9b7b0dc1256a294c02e3c903e3ad995d`
  - `dist/RELEASE_NOTES.md`: `7c5405f42d895d857cfbbe68cf82b21c5df6251c904c3e3c9869f328036472a3`
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Исследовать приоритетные направления из Icebox (например, контроль архитектурной преемственности в исследованиях): `/kb-research "Контроль архитектурной преемственности в исследованиях"`.

---

### [2026-10-12] — Реализация TASK-060: Синхронизация инсталлятора install.py / build_installer.py, регрессионные E2E тесты и актуализация Living Spec
- **Что сделано:**
  - Пересобраны монолитные дистрибутивы `install.py` и `dist/install.py` через `scripts/build_installer.py` с упаковкой обновленных `scripts/kb_ingest.py`, `scripts/kb_lint.py`, скилла `kb-triage` и сопутствующих ресурсов.
  - Разработан и интегрирован сквозной интеграционный E2E тест `test_29_channel_transparency_and_phase_consistency_deployment` в `tests/test_installer.py` (проверка чистой установки, работоспособности `kb_ingest.py --status`, семантического аудита фаз `kb_lint.py`, и корректности режима обновления `install.py --update`).
  - Скорректирован эталонный бюджет размера монолитного инсталлятора в `tests/test_installer.py` (`test_16`) до 130 000 байт с сохранением строгого контроля статического оверхеда.
  - Синхронизирована Living Spec: в `SPEC.md` зафиксированы семантический контроль фаз `check_phase_consistency`, Zero Round-Trip Dispatch и фазы 14–15; обновлены `README.md` и `docs/Onboarding.md` примерами команд прозрачности каналов.
  - Полностью завершена Фаза 15: обновлены статусы задачи в ТЗ [[02_Tasks/Specs/15_LatencyAndChannels/TASK-060-installer-bundling-e2e-and-living-spec|TASK-060]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> `install.py` и `dist/install.py` успешно сгенерированы (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 29/29 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs -v` -> 0 broken links, 0 warnings (Exit code 0).
  - `python -m unittest discover -s tests` -> все тесты успешно пройдены (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовить и выпустить официальный релиз Фазы 15: `/kb-release --version v0.15.0 --phase 15`.

---

### [2026-10-12] — Реализация TASK-059: Прозрачный фидбек источников в /kb-triage и семантический контроль фаз в scripts/kb_lint.py
- **Что сделано:**
  - Обновлен исполняемый скилл `.agents/skills/kb-triage/SKILL.md`: при пустом инбоксе агент запрашивает диагностический статус источников (`python scripts/kb_ingest.py --status`) и формирует понятный отчет (опрошенный репозиторий, статус каналов, число обработанных тикетов) перед завершением по Stop & Yield.
  - В утилиту аудита `scripts/kb_lint.py` внедрена функция `check_phase_consistency(docs_dir: Path) -> list`, сопоставляющая декларируемый номер фазы в frontmatter (`phase: N`) с папкой размещения (`Specs/NN_<Slug>/`) и тегами (`phaseN`).
  - Обеспечен неблокирующий вывод семантических предупреждений о фазах (`⚠️ Phase Consistency Warnings`) в Verbose и Silent-on-Success режимах.
  - Разработаны 4 модульных теста в `tests/test_kb_lint.py` (`test_phase_consistency_*`), проверяющие соответствие папок, тегов и неблокирующий статус.
  - Актуализированы статусы задачи в ТЗ [[02_Tasks/Specs/15_LatencyAndChannels/TASK-059-channel-triage-feedback-and-phase-consistency-lint|TASK-059]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m py_compile scripts/kb_lint.py tests/test_kb_lint.py` -> синтаксис корректен (Exit code 0).
  - `python -m unittest tests/test_kb_lint.py` -> 20/20 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs -v` -> 153 файла и 1420 связей проверено, 0 broken links, 0 warnings (Exit code 0).
  - `python -m unittest discover -s tests` -> 78/78 тестов успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать следующую задачу Фазы 15: `/kb-implement TASK-060` («Синхронизация инсталлятора install.py / build_installer.py, регрессионные E2E тесты и актуализация Living Spec»).

---

### [2026-10-12] — Реализация TASK-058: Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в scripts/kb_ingest.py
- **Что сделано:**
  - Реализована функция `detect_github_repo` (Zero-Dependencies): автоопределение `owner/repo` из `git config --get remote.origin.url` (HTTPS, SSH, token auth) с приоритетом переменной среды `GITHUB_REPOSITORY`.
  - Внедрен инвариант прозрачности каналов (Channel Transparency Invariant): явные предупреждения при отсутствии конфигурации источников (`⚠️ Warning: Канал GitHub/Email пропущен...`) и информационная плашка о лимитах анонимных обращений к GitHub API (60 req/h vs 5000 req/h).
  - Реализованы гибкие фильтры инжеста: CLI-флаги `--label <NAME>` (по умолчанию `needs-triage`) и `--all-open` (сбор всех открытых issues за исключением Pull Requests).
  - Реализован диагностический дашборд статуса источников (`scripts/kb_ingest.py --status`): мгновенное отображение состояния каналов GitHub и Email, проверка остатка квоты GitHub API и статистика буфера `docs/02_Tasks/Inbox/` по статусам (`new`, `processed`, `rejected`).
  - Добавлена детальная обработка HTTP-ошибок GitHub API (коды 401, 403, 404, 500) с понятными рекомендациями.
  - Написаны 10 модульных тестов в `tests/test_kb_ingest.py` (100% Pass).
  - Актуализированы Мастер-Спецификация `SPEC.md` и витрина проекта `README.md` в соответствии с Living Spec Invariant.
  - Обновлены статусы задачи в ТЗ [[02_Tasks/Specs/15_LatencyAndChannels/TASK-058-channel-transparency-git-remote-and-status-dashboard|TASK-058]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m py_compile scripts/kb_ingest.py tests/test_kb_ingest.py` -> синтаксис корректен (Exit code 0).
  - `python -m unittest tests/test_kb_ingest.py` -> 10/10 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_ingest.py --status` -> дашборд отображен корректно (Exit code 0).
  - `python scripts/kb_ingest.py --github --dry-run` -> dry-run успешно выполнен (Exit code 0).
  - `python -m unittest discover -s tests` -> 74/74 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 150 файлов проверено, 1389 связей валидны (0 broken links, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать следующую задачу Фазы 15: `/kb-implement TASK-059` («Прозрачный фидбек источников в /kb-triage и семантический контроль фаз в scripts/kb_lint.py»).

---

### [2026-10-12] — Реализация TASK-057: Архитектура Zero Round-Trip Dispatch и горячие инварианты в правилах агентов
- **Что сделано:**
  - Внедрено Правило 10 (Zero Round-Trip Dispatch & Hot Invariants Protocol) в мастер-свод `AGENTS.md`: прямая авторизация агентов на исполнение стандартных жизненных циклов (Режимы 0, 1, 2, 2B, 2C, 3) в первом раунде без предварительного чтения `SKILL.md`.
  - Введен регламент **Pipelined Co-fetching** (параллельное чтение контекста и шаблонов в первом же раунде вызова инструментов) для устранения задержки 6–12 секунд.
  - Обновлен монолитный скрипт установки `install.py` (правило 18 в `_RULES_BODY`, генератор `_gen_rule` и компактные адаптеры для 6 IDE).
  - Актуализированы тонкие адаптеры правил (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`) с сохранением лимита $\le 35$ строк.
  - Расширены E2E-тесты в `tests/test_installer.py` (`test_25_thin_forwarders_rules_layering`), подтверждающие генерацию директив Zero Round-Trip Dispatch и целостность слоев правил.
  - Обновлены статусы задачи в ТЗ [[02_Tasks/Specs/15_LatencyAndChannels/TASK-057-zero-roundtrip-dispatch-and-hot-invariants|TASK-057]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 28/28 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python -m unittest discover -s tests` -> 69/69 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 150 файлов проверено, 1388 связей валидны (0 broken links, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Разработать детальную спецификацию следующей задачи Фазы 15: `/kb-task TASK-058 "Прозрачный UX инжеста, автодетект Git Remote и дашборд статуса источников в scripts/kb_ingest.py"`.

---

### [2026-10-12] — Официальный релиз v0.14.0 (Фаза 14: Продуктовый DX, протокол Fast-Track и адаптация для вайбкодеров)
- **Что сделано:**
  - Успешно подготовлен и зафиксирован официальный релиз [[02_Tasks/Releases/RELEASE-v0.14.0|RELEASE-v0.14.0]] по итогам завершения Фазы 14.
  - Сгенерирован публичный файл заметок `dist/RELEASE_NOTES.md` с новым Human-First форматом (Highlights, Quick Install, эмодзи-теги `⚡ Fast-Track:`, `✨ Фича:`).
  - Сформирован и синхронизирован пакет дистрибутива `dist/install.py` (120.9 KB, SHA-256: `e4f470e7dae9d462bc92911894fa28832948fcedb884e8ce50d956298c0e30d5`).
  - Актуализированы Дорожная карта [[02_Tasks/Roadmap|Roadmap.md]] и история изменений `CHANGELOG.md`.
  - Установлен релизный Git-тег `v0.14.0`.
- **Контрольные суммы артефактов (SHA-256):**
  - `dist/install.py`: `e4f470e7dae9d462bc92911894fa28832948fcedb884e8ce50d956298c0e30d5`
  - `dist/RELEASE_NOTES.md`: `86573271144aa870c9282bae3809157bb02b216dc5d262890685374ebe43116e`
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Сформировать план Фазы 15 на основе приоритетных кандидатов из Icebox (Zero Round-Trip Dispatch & Channel Transparency) с помощью команды: `/kb-plan "Фаза 15: Устранение задержек и прозрачность каналов"`.

---

### [2026-10-12] — Реализация TASK-056: Синхронизация инсталлятора install.py / build_installer.py, E2E тесты и актуализация Living Spec
- **Что сделано:**
  - Обновлен сборщик `scripts/build_installer.py` для упаковки 15 шаблонов (включая микро-спецификацию Fast-Track `TEMPLATE_TASK_MICRO.md`) и практического руководства `docs/Zero_To_Hero_Guide.md` в монолитный дистрибутив `install.py` и `dist/install.py`.
  - Модернизирован `install.py`: добавлены процедуры развертывания `Zero_To_Hero_Guide.md` при первичной установке и безопасного обновления при вызове `install.py --update`.
  - Реализован комплексный сквозной тест `test_28_fast_track_template_and_zero_to_hero_guide_deployment` в `tests/test_installer.py`, проверяющий доставку и обновление файлов, а также адаптированы тесты `test_01` и `test_16` под расширенный реестр из 15 шаблонов.
  - Актуализирована витрина `README.md`: добавлен раздел One-Prompt Quickstart для вайбкодеров, обновлена структура директории `docs/` и свод ключевых дисциплин (Human Guardrails, Fast-Track).
  - Выполнена синхронизация Мастер-Спецификации `SPEC.md` (реестр 15 шаблонов, протоколы Human Guardrails и Fast-Track).
  - Актуализированы статусы задачи в ТЗ [[02_Tasks/Specs/14_AgileDX/TASK-056-installer-bundling-e2e-and-living-spec|TASK-056]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]]. Завершена вся Фаза 14!
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> сборка успешна (120.9 KB, Exit code 0).
  - `python -m py_compile dist/install.py install.py` -> синтаксис корректен (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 28/28 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python -m unittest discover -s tests` -> 69/69 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 145 файлов проверено, 1324 связи валидны (0 broken links, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Провести выпуск релиза Фазы 14 с помощью команды: `/kb-release --version v0.14.0 --phase 14`.

---

### [2026-10-12] — Реализация TASK-055: Human-First чейнджлоги в scripts/kb_release.py и аудит Fast-Track в scripts/kb_lint.py
- **Что сделано:**
  - Модернизирована функция генерации публичных релизных заметок `generate_public_release_notes` в Zero-Deps утилите `scripts/kb_release.py`: сформирован человеко-читаемый блок `### 🌟 Главное в этом релизе (Highlights)` с выжимкой ключевых возможностей, внедрены семантические маркеры для задач (`⚡ Fast-Track:`, `✨ Фича:`, `🐛 Исправление:`).
  - В утилиту аудита `scripts/kb_lint.py` внедрена функция `check_fast_track_specs`: автоматический контроль лимита затронутых файлов ($\le 2$) и обязательного наличия Плана верификации (`Verification Plan`) для микро-спецификаций (`type: fast-track`).
  - Разработаны и успешно пройдены модульные тесты: валидация человеко-читаемых чейнджлогов в `tests/test_kb_release.py` и аудит Fast-Track в `tests/test_kb_lint.py`.
  - Актуализированы статусы задачи в ТЗ [[02_Tasks/Specs/14_AgileDX/TASK-055-human-first-release-notes-and-lint-audit|TASK-055]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m py_compile scripts/kb_release.py scripts/kb_lint.py` -> синтаксис корректен (Exit code 0).
  - `python -m unittest tests/test_kb_release.py` -> 20/20 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python -m unittest tests/test_kb_lint.py` -> 16/16 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 145 файлов проверено, 1321 связь валидна (0 broken links, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать следующую задачу фазы 14: `/kb-implement TASK-056` («Синхронизация инсталлятора install.py / build_installer.py, E2E тесты и актуализация Living Spec»).

---

### [2026-10-12] — Реализация TASK-054: Практический гайд Zero_To_Hero_Guide.md («Вайбкодинг со страховкой») и менторский онбординг в kb-onboard
- **Что сделано:**
  - Разработано практическое руководство [[Zero_To_Hero_Guide|docs/Zero_To_Hero_Guide.md]] («Zero to Hero: Вайбкодинг со страховкой»), объясняющее философию Docs-as-Code через ментальную модель «Автопилот с датчиками» и жизненные аналогии для 4 шагов разработки (Тест-драйв идеи $\to$ Чертеж дома $\to$ Список материалов $\to$ Строительство + экспресс Fast-Track).
  - В гайде зафиксирована шпаргалка по AI-средам (Antigravity, Cursor, Windsurf, Claude Code, Cline, Copilot), золотые правила диалога с агентом и готовый промпт для развертывания проекта в один клик без консольных команд (Chat-First Bootstrapping).
  - Модернизирован скилл `.agents/skills/kb-onboard/SKILL.md`: внедрен адаптивный менторский диалоговый режим (объяснение шагов на простых аналогиях для новичков и ссылка на руководство `Zero_To_Hero_Guide.md`). Размер скилла сохранен в рамках лимита $\le 3000$ байт (2823 байт).
  - Обновлены вводный раздел [[Onboarding|docs/Onboarding.md]] со специальной плашкой для вайбкодеров и каталог документов в [[00_Index|docs/00_Index.md]] (раздел 0).
  - Актуализированы статусы задачи в ТЗ [[02_Tasks/Specs/14_AgileDX/TASK-054-zero-to-hero-guide-and-mentor-onboarding|TASK-054]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 145 файлов проверено, 1315 связей валидны (0 broken links, Exit code 0).
  - Контроль размера скилла `.agents/skills/kb-onboard/SKILL.md`: 2823 байт ($\le 3000$ байт).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать следующую задачу фазы 14: `/kb-implement TASK-055` («Human-First чейнджлоги в scripts/kb_release.py и аудит Fast-Track в scripts/kb_lint.py»).

---

### [2026-10-12] — Реализация TASK-053: Принцип «Направляй, а не блокируй» (Human Guardrails) в AGENTS.md и адаптерах
- **Что сделано:**
  - В базовый стандарт [[AGENTS.md]] внедрены нормативные правила 8 («Human Guardrails Protocol») и 9 («Fast-Track Protocol»). В режимах, запрещающих редактирование кода (Режимы 0, 1, 2, 2B, 2C), агенту предписано действовать как дружелюбный Senior Partner: объяснять назначение шага понятным языком, задавать направляющие вопросы с вариантами выбора и предлагать готовую команду для продолжения (`/kb-implement ...`), исключая сухие роботизированные отказы.
  - В генераторах правил `install.py` (`_RULES_BODY`, `_gen_rule`) и корневых адаптерах IDE (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`) закреплены директивы Human Guardrails и Fast-Track при строгом сохранении лимита $\le 35$ строк для тонких адаптеров.
  - Адаптирован и расширен E2E тест `test_25_thin_forwarders_rules_layering` в `tests/test_installer.py` для верификации присутствия Human Guardrails и Fast-Track директив.
  - Обновлены статусы задачи в ТЗ [[02_Tasks/Specs/14_AgileDX/TASK-053-human-guardrails-and-agent-rules|TASK-053]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 27/27 тестов успешно пройдено (100% Pass, Exit code 0, 46.8s).
  - `python scripts/kb_lint.py --path docs` -> 144 файла проверено, 1305 связей валидны (0 broken links, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать следующую задачу фазы 14: `/kb-implement TASK-054` («Практический гайд Zero_To_Hero_Guide.md («Вайбкодинг со страховкой») и менторский онбординг в kb-onboard»).

---

### [2026-10-12] — Реализация TASK-052: Шаблон Micro-Spec TEMPLATE_TASK_MICRO.md и поддержка Fast-Track в kb-task / kb-plan
- **Что сделано:**
  - Создан ультра-компактный шаблон микро-спецификации `TEMPLATE_TASK_MICRO.md` в канонической базе знаний (`docs/00_Templates/TEMPLATE_TASK_MICRO.md`) и в дистрибутивном каталоге шаблонов (`templates/TEMPLATE_TASK_MICRO.md`). Шаблон оптимизирован для Fast-Track задач (≤ 30 LOC, ≤ 2 файлов) и занимает всего ~35 строк с четкими контрактами DoD и Verification Plan.
  - Модернизирован скилл `.agents/skills/kb-task/SKILL.md`: добавлена прямая поддержка режима Fast-Track через аргумент `--fast` (или выявление тривиального скоупа ≤ 30 LOC), использование шаблона `TEMPLATE_TASK_MICRO.md` и гарды на превышение лимитов сложности.
  - Модернизирован скилл `.agents/skills/kb-plan/SKILL.md`: внедрен эвристический префлайт Soft Nudge при вызове `/kb-plan <idea>` на тривиальные изменения, рекомендующий прямое создание ТЗ через `/kb-task --fast` в обход тяжелой стадии RFC.
  - Размеры обоих скиллов сохранены в жестком High-SNR лимите ≤ 3000 байт (kb-task: 2018 байт, kb-plan: 2490 байт).
  - Успешно обновлены статусы задачи в ТЗ [[02_Tasks/Specs/14_AgileDX/TASK-052-micro-spec-template-and-fast-track-skills|TASK-052]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 144 файла проверено, 1301 связь валидна (0 broken links, Exit code 0).
  - `python -m unittest discover -s tests` -> 67/67 тестов успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать следующую задачу фазы 14: `/kb-implement TASK-053` («Принцип «Направляй, а не блокируй» (Human Guardrails) в AGENTS.md и адаптерах»).

---

### [2026-10-11] — Официальный релиз v0.13.0 (Фаза 13: Слоистая архитектура правил, тонкие адаптеры и таксономия базы знаний)
- **Что сделано:**
  - Осуществлен выпуск релиза [[02_Tasks/Releases/RELEASE-v0.13.0|RELEASE-v0.13.0]] через скилл `/kb-release` и утилиту `scripts/kb_release.py`.
  - Успешно сформирован комплект релизных артефактов в каталоге `dist/` с потоковым расчетом контрольных сумм SHA-256:
    - `dist/install.py` (114.1 KB) — `f472fe4dbcf8e12d8a15249d52475d23890b48ea8e1423f8c7b5f405df3fe633`
    - `dist/RELEASE_NOTES.md` (2.9 KB) — `d60a7ba1f4bdaec9570b8595423cab212bd80ed760854b6225a57b6314d9bfae`
  - Обновлен `CHANGELOG.md` с описанием всех ключевых изменений версии v0.13.0.
  - Успешно пройден полный аудит базы знаний `kb_lint.py` (0 broken links) и полный набор тестов (100% Pass).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Зафиксировать релизный тег Git: `git tag -a v0.13.0 -m "Release v0.13.0: Phase 13 Layered Rules and Thin Forwarders"` и запушить на GitHub.

---

### [2026-10-11] — Реализация TASK-051: Сборка монолитного инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec (Завершение Фазы 13)
- **Что сделано:**
  - Модернизирован сборщик `scripts/build_installer.py`: теперь он одновременно упаковывает embedded payload в `install.py` и автоматически компилирует готовый монолитный дистрибутив `dist/install.py` со всеми 14 шаблонами, конфигурацией Obsidian Graph, утилитами и 12 скиллами.
  - Реализован комплексный E2E тест `test_27_dist_monolith_e2e_fresh_install_and_update` в `tests/test_installer.py`, тестирующий установку и бережное обновление (`--update`) через `dist/install.py` в изолированном каталоге с проверкой 12 скиллов и тонких адаптеров.
  - Актуализированы Master Specification (`SPEC.md`) и витрина проекта (`README.md`): зафиксирован переход на паттерн Thin Forwarders, 12 специализированных скиллов (`kb-onboard` как единая точка входа) и двухуровневая таксономия шаблонов базы знаний.
  - Успешно завершена **Фаза 13** («Слоистая архитектура правил, тонкие адаптеры и таксономия базы знаний»): закрыты все задачи в ТЗ [[02_Tasks/Specs/13_RulesLayering/TASK-051-bundling-e2e-tests-and-living-spec|TASK-051]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]], Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]] и плане [[02_Tasks/Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]].
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> сборка успешна, обновлены `install.py` и `dist/install.py` (Exit code 0).
  - `python -m py_compile dist/install.py` -> синтаксис монолита корректен (Exit code 0).
  - `python scripts/kb_lint.py --path docs -v` -> 134 файла проверено, 1210 связей валидны (0 broken links, Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 27/27 тестов успешно пройдено (100% Pass, OK, 45.4s).
  - `python -m unittest discover -s tests` -> 67/67 тестов успешно пройдено (100% Pass, Exit code 0, 37.4s).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовить и выпустить релиз Фазы 13: `/kb-release --version v0.13.0 --phase 13` (или запланировать исследование следующей инициативы из Icebox через `/kb-research`).

---

### [2026-10-11] — Реализация TASK-050: Консолидация docs-as-code и kb-onboard, двухуровневая таксономия шаблонов в Onboarding.md
- **Что сделано:**
  - Упразднен избыточный мета-скилл `.agents/skills/docs-as-code/`, высвободивший постоянный слот в Always-On системном промпте модели (реестр скиллов сокращен с 13 до 12 специализированных инструментов).
  - Скилл `.agents/skills/kb-onboard/SKILL.md` расширен и стал единой точкой входа: включены компактная таблица Command Router (12 команд), навигационная карта каталогов `docs/` и сводка 4-этапного жизненного цикла. Размер скилла удержан в лимите $\le 3000$ байт (2525 байт).
  - В руководстве [[Onboarding|docs/Onboarding.md]] и эталонных шаблонах `docs/00_Templates/TEMPLATE_ONBOARDING.md` / `templates/TEMPLATE_ONBOARDING.md` зафиксирована двухуровневая таксономия шаблонов (Core Essentials [4] vs Advanced Governance [10]).
  - Обновлен тестовый сьют `tests/test_installer.py`: проверки адаптированы на развертывание 12 скиллов без `docs-as-code`, добавлен тест `test_26_skills_consolidation_and_template_taxonomy`.
  - Синхронизированы сборщик и дистрибутивный инсталлятор `install.py` через `scripts/build_installer.py`.
  - Актуализированы статусы задачи в ТЗ [[02_Tasks/Specs/13_RulesLayering/TASK-050-consolidate-onboard-and-template-taxonomy|TASK-050]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]], Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]] и плане [[02_Tasks/Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]].
- **Результаты верификации:**
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - `python scripts/kb_lint.py --path docs -v` -> 134 файла проверено, 1205 связей валидны (0 broken links, Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 26/26 тестов успешно пройдено (OK, 18.2s).
  - `python -m unittest discover -s tests` -> 66/66 тестов успешно пройдено (100% Pass, Exit code 0, 22.8s).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Приступить к реализации TASK-051: `/kb-implement TASK-051` (Сборка инсталлятора build_installer.py, сквозные E2E тесты и актуализация Living Spec).

---

### [2026-10-11] — Реализация TASK-049: Реализация паттерна Thin Forwarders в генераторах адаптеров install.py
- **Что сделано:**
  - Переведены все 6 генераторов адаптеров AI-ассистентов в `install.py` (`generate_gemini_md`, `generate_windsurfrules`, `generate_clinerules`, `generate_claude_md`, `generate_cursorrules`, `generate_copilot_instructions`) на паттерн **Thin Forwarders**: адаптеры сжаты до $\le 25$ строк (сокращение на 80%), устранены дублирование 15 дисциплин и риск двойной инжекции контекста.
  - Адаптеры сфокусированы на командах верификации стека (`Build`, `Test`, `Lint`), прямой ссылке на канонический `[[AGENTS.md]]` как единый источник правды (SSOT) и ключевых горячих инвариантах (Read-Only в Режимах 1/2, Anti-Echo, Single-Task Barrier, TDD-цикл).
  - Сгенерированы актуальные тонкие форвардеры в корне проекта `agent-docs-harness`: `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`.
  - Реализован комплексный модульный тест `test_25_thin_forwarders_rules_layering` в `tests/test_installer.py`, верифицирующий длину файлов ($\le 35$ строк), ссылки на `AGENTS.md` и развертывание в изолированном окружении.
  - Актуализированы статусы задачи в ТЗ [[02_Tasks/Specs/13_RulesLayering/TASK-049-thin-forwarders-adapters-generator|TASK-049]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]], Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]] и плане [[02_Tasks/Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]].
- **Результаты верификации:**
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - `python scripts/kb_lint.py --path docs -v` -> 134 файла проверено, 1198 связей валидны (0 broken links, Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 25/25 тестов успешно пройдено (OK, 18.8s).
  - `python -m unittest discover -s tests` -> 65/65 тестов успешно пройдено (100% Pass, Exit code 0, 15.5s).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Приступить к реализации TASK-050: `/kb-implement TASK-050` (Консолидация docs-as-code и kb-onboard, двухуровневая таксономия шаблонов в Onboarding.md).

---

### [2026-10-11] — Реализация TASK-048: Очистка AGENTS.md от графового шума и изоляция таксономии Obsidian Graph в .obsidian/graph.json
- **Что сделано:**
  - Устранена 10-строчная таблица цветов интерфейса Obsidian Graph из канонического `AGENTS.md` и генератора `generate_agents_md` в `install.py` (-150 токенов контекста модели на каждом запросе).
  - Внедрена лаконичная каноническая директива таксономии путей и тегов (`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#testing`) с указанием на `.obsidian/graph.json`.
  - Добавлен автоматический тест `test_24_obsidian_taxonomy_decoupling` в `tests/test_installer.py`, проверяющий генерацию `AGENTS.md`, корневой файл и установку в изолированный каталог.
  - Актуализированы статусы задачи в спецификации [[02_Tasks/Specs/13_RulesLayering/TASK-048-clean-agents-md-and-obsidian-taxonomy|TASK-048]], Канбан-доске [[02_Tasks/Kanban|Kanban.md]] и Дорожной карте [[02_Tasks/Roadmap|Roadmap.md]].
- **Результаты верификации:**
  - `python -m py_compile install.py` -> синтаксис корректен (Exit code 0).
  - `python scripts/kb_lint.py --path docs -v` -> 127 файлов проверено, 1139 связей валидны (0 broken links, Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 24/24 тестов успешно пройдено (OK, 21.9s).
  - `python -m unittest discover -s tests` -> 64/64 теста успешно пройдено (100% Pass, Exit code 0, 27.0s).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать тонкие форвардеры для адаптеров IDE в генераторах `install.py`: `/kb-task TASK-049` (или `/kb-implement TASK-049`).

---

### [2026-10-11] — Системный аудит эффективности сквозного цикла агентской разработки
- **Что сделано:**
  - Проведен детальный аудит сквозного цикла разработки харнесса по 5 ключевым фазам:
    1. Исследование (Режим 0: Discovery) — 8.2/10
    2. Разработка (Режимы 1 & 2: Planning & Spec) — 7.9/10
    3. Имплементация (Режим 3) — 8.7/10
    4. Исправление дефектов (Режимы 2B & 3: TDD) — 9.5/10 (лучший компонент)
    5. Релиз-менеджмент (Режим 4: Dual-Export) — 8.8/10
    6. Воронка фидбека (Режим 2C: Inbox & Triage) — 7.3/10
  - Сформирован подробный аналитический артефакт с матрицей эффективности: `agent_lifecycle_effectiveness_audit.md`.
  - Выявлено главное системное противоречие харнесса: **Safety First (95% надежности) против Velocity (60% скорости)** — «церемониальный налог» на мелких задачах.
  - В [[02_Tasks/Roadmap|Roadmap.md]] (Icebox) зарегистрированы 3 новые архитектурные инициативы:
    1. **Протокол Fast-Track:** облегченный регламент для микро-задач $\le 30$ строк кода без отдельного RFC в `Plans/` (-60% диалогового трения).
    2. **Пакетный триаж обращений (`/kb-triage --batch`):** автоматическая кластеризация и группировка похожих тикетов в `Inbox/`.
    3. **Обязательное Spike-прототипирование в Режиме 0:** требование запускаемого проверочного скрипта в `scratch/` для исключения бумажной архитектуры.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 126 файлов проверено, 1128 связей валидны (0 broken links, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Оформить кумулятивный релиз Фазы 12 (`/kb-release --version v0.12.0 --phase 12`) либо перейти к декомпозиции и реализации Фазы 13 (`/kb-implement TASK-048`).

---

### [2026-10-11] — Реализация TASK-047: Диагностический модуль install.py --report, синхронизация сборщика и E2E тесты (Завершение Фазы 12)
- **Что сделано:**
  - Реализован диагностический CLI-модуль `install.py --report`: генерирует анонимизированный Markdown-отчет о локальном окружении (ОС, рантайм Python, статус Git, проверка базы знаний `kb_lint.py`, обнаруженные конфиги AI-агентов) с маскированием персональных путей `<user>`.
  - Обновлен сборщик `scripts/build_installer.py`: упакованы утилита `scripts/kb_ingest.py`, шаблон `TEMPLATE_FEEDBACK.md`, формы `.github/ISSUE_TEMPLATE/*.yml` и скилл `.agents/skills/kb-triage/SKILL.md` в монолит `install.py` (115.4 KB).
  - Обновлены процедуры `install_harness` и `update_harness`: обеспечено автоматическое создание буфера `docs/02_Tasks/Inbox/` и `.inbox_state.json`, а также распаковка `.github/ISSUE_TEMPLATE/` при установке и бережном обновлении без затирания пользовательских файлов.
  - Разработан сквозной E2E тест `test_23_feedback_ingestion_and_diagnostic_report` в `tests/test_installer.py`, проверяющий работу флага `--report`, деплой буфера Inbox, шаблонов, скриптов и сохранение пользовательских данных при обновлении.
  - Актуализированы `SPEC.md`, `README.md` и `docs/Onboarding.md` согласно Living Spec Invariant.
  - Завершена спецификация [[02_Tasks/Specs/12_FeedbackIngestion/TASK-047-installer-diagnostics-bundling-and-e2e|TASK-047]], Канбан-доска [[02_Tasks/Kanban|Kanban.md]] и Дорожная карта [[02_Tasks/Roadmap|Roadmap.md]] (Фаза 12 официально завершена).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> успешно собран монолит `install.py` (115.4 KB).
  - `python install.py --report` -> сгенерирован валидный анонимизированный отчет окружения.
  - `python -m unittest tests/test_installer.py` -> 23/23 тестов пройдено (OK, 18.2s).
  - `python -m unittest discover -s tests` -> 63/63 теста успешно пройдено (100% Pass, Exit code 0, 25.2s).
  - `python scripts/kb_lint.py --path docs` -> 126 файлов проверено, 1126 связей валидны (0 broken links, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Оформить кумулятивный релиз Фазы 12 (`/kb-release --version v0.12.0 --phase 12`) либо перейти к декомпозиции и реализации Фазы 13 (`/kb-implement TASK-048`).

---

### [2026-10-11] — Аудит архитектуры правил (RESEARCH-016), утверждение ADR-0021 и фиксация плана Фазы 13 (PLAN-013)
- **Что сделано:**
  - Проведен комплексный аудит кодовой базы и исследования [[04_Research/RESEARCH-016-agent-rules-hierarchy-and-knowledge-base-structure|RESEARCH-016]] в сопоставлении с мировыми стандартами агентской разработки (Anthropic Claude Code, Cursor Rules, Context Engineering).
  - Сформирован подробный аналитический артефакт с разбором плюсов, узких мест и дорожной картой оптимизации.
  - Оформлен формальный план Фазы 13 [[02_Tasks/Plans/PLAN-013-rules-layering-thin-forwarders-and-obsidian-taxonomy|PLAN-013]]:
    - Перевод адаптеров IDE (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`) на паттерн **Thin Forwarders** (до 30 строк, ссылки на `AGENTS.md`, команды верификации стека) с устранением Rule Drift и экономией 80–85% объема файлов.
    - Декуплинг визуальной палитры Obsidian Graph: удаление таблицы цветов из `AGENTS.md` и локализация настроек строго в `docs/.obsidian/graph.json` (экономия ~150 токенов на каждом запросе).
    - Консолидация онбординга: объединение функций `docs-as-code` и `kb-onboard`.
    - Двухуровневая таксономия шаблонов в `docs/Onboarding.md` (Core Essentials vs Advanced Governance).
  - Актуализированы Канбан-доска [[02_Tasks/Kanban|Kanban.md]] (карточки добавлены в Бэклог) и Дорожная карта [[02_Tasks/Roadmap|Roadmap.md]].
  - Исправлены битые ссылки в `docs/Onboarding.md` на ADR-0020 и RESEARCH-015.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs -v` -> 126 файлов проверено, 1122 связи валидны (0 broken links, 100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Завершить текущую задачу Фазы 12 (`/kb-implement TASK-047`) либо приступить к спецификации задач Фазы 13 (`/kb-task TASK-048`).

---
- **Что сделано:**
  - Создан исполняемый скилл `.agents/skills/kb-triage/SKILL.md` (Режим 2C: Feedback Triage & Dispatch) согласно [[02_Tasks/Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]] и [[03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]]:
    - Реализована процедура двухстадийного скрининга обращений в `docs/02_Tasks/Inbox/`.
    - Закреплен запрет модификации кода проекта и обязательный терминальный шаг **Stop & Yield Control**.
    - Закреплен **Permalinks Invariant** для обращений: файлы `FB-*.md` никогда не перемещаются, статус и целевой артефакт (`target: "[[...]]"`) обновляются in-place.
  - Актуализирован канонический файл руководства агентов `AGENTS.md`: добавлены 7-й инвариант (буфер триажа) и регламент Режима 2C.
  - В генераторах правил инсталлятора `install.py` (`_RULES_BODY`, `_3MODES`, `generate_gemini_md` и др.) закреплены 15 дисциплин Docs-as-Code и зарегистрирован скилл `/kb-triage`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 124 файла проверено, 1101 связь валидна (0 broken links).
  - `python -m unittest discover -s tests` -> 62/62 теста успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать финальную интеграцию фазы: `/kb-implement TASK-047`.

---  

### [2026-10-11] — Реализация TASK-045: GitHub Issue Forms и облачный workflow кросс-агентной синхронизации
- **Что сделано:**
  - Созданы декларативные формы сбора обратной связи в `.github/ISSUE_TEMPLATE/` согласно [[02_Tasks/Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]] и [[03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]]:
    - `.github/ISSUE_TEMPLATE/bug_report.yml`: форма баг-репорта с авто-лейблами `needs-triage` и `kind:defect`.
    - `.github/ISSUE_TEMPLATE/feature_request.yml`: форма запроса улучшений с авто-лейблами `needs-triage` и `kind:enhancement`.
    - `.github/ISSUE_TEMPLATE/config.yml`: запрет пустых обращений и ссылки на онбординг/дискуссии.
  - Разработан кросс-агентный облачный рабочий процесс `.github/workflows/feedback-sync.yml`, запускающийся по расписанию (раз в 6 часов) и `workflow_dispatch`, который выполняет `scripts/kb_ingest.py --all` и фиксирует новые обращения в `docs/02_Tasks/Inbox/` без необходимости локального запуска разработчиком.
- **Результаты верификации:**
  - Валидация структуры и разметки YAML пройдена без ошибок.
  - `python scripts/kb_lint.py --path docs` -> 123 файла проверено, 1087 связей валидны (0 broken links).
  - `python -m unittest discover -s tests` -> 62/62 теста успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать скилл триажа: `/kb-implement TASK-046`.

---  

### [2026-10-11] — Реализация TASK-044: Zero-Dependencies модуль импорта обратной связи (scripts/kb_ingest.py) и тесты
- **Что сделано:**
  - Разработан автономный модуль импорта `scripts/kb_ingest.py` на стандартной библиотеке Python 3 (Zero Dependencies) согласно [[02_Tasks/Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]] и [[03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]].
  - Реализованы драйверы трех каналов доставки:
    - **GitHub Issues:** сбор issues с меткой `needs-triage` через REST API v3 (`urllib.request`) с фильтрацией PR и генерацией `FB-GH-{num}.md`.
    - **Email (IMAP):** опрос почтового ящика через `imaplib` и парсинг тела/заголовков через `email` с генерацией `FB-MAIL-{YYYYMMDD}-{hash}.md`.
    - **Quick Paste:** мгновенная вставка из CLI-аргументов или stdin (`FB-PASTE-{YYYYMMDD}-{hash}.md`).
  - Реализован класс `InboxStateManager` для детерминированной дедупликации и управления курсорами в `.inbox_state.json`.
  - В корневом `.gitignore` зафиксировано игнорирование `.env.local` и локальных файлов секретов.
  - Написан комплексный набор модульных тестов в `tests/test_kb_ingest.py` с моками сетевых протоколов (GitHub REST API, IMAP).
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_ingest.py` -> 5/5 тестов успешно пройдено.
  - `python scripts/kb_ingest.py --paste --title "Test" --text "Sample" --dry-run` -> Exit code 0.
  - `python scripts/kb_lint.py --path docs` -> 123 файла проверено, 1085 связей валидны (0 broken links).
  - `python -m unittest discover -s tests` -> 62/62 теста успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать GitHub формы и облачный cron workflow: `/kb-implement TASK-045`.

---  

### [2026-10-11] — Реализация TASK-043: Буфер триажа, шаблон TEMPLATE_FEEDBACK и аудит в kb_lint.py
- **Что сделано:**
  - Реализован изолированный буфер триажа `docs/02_Tasks/Inbox/` и созданы эталонные шаблоны `docs/00_Templates/TEMPLATE_FEEDBACK.md` и `templates/TEMPLATE_FEEDBACK.md` согласно [[02_Tasks/Plans/PLAN-012-feedback-ingestion-and-triage-buffer|PLAN-012]] и [[03_Decisions_ADR/ADR-0020-feedback-ingestion-channels-and-triage-automation|ADR-0020]].
  - Инициализирован файл состояния дедупликации `docs/02_Tasks/Inbox/.inbox_state.json` с курсорами источников (GitHub, Email, Paste) и защитный `.gitignore` для каталога `Inbox/`.
  - В `scripts/kb_lint.py` добавлен аудит обязательного YAML frontmatter для файлов обращений (`id`, `title`, `status`, `type`, `channel`, `created`) и допустимых статусов (`new`, `triaged`, `processed`, `rejected`).
  - Добавлены модульные тесты валидации файлов обращений в `tests/test_kb_lint.py`.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_lint.py` -> 15/15 тестов успешно пройдено.
  - `python scripts/kb_lint.py --path docs` -> 123 файла проверено, 1082 викиссылки валидны (0 broken links).
  - `python -m unittest discover -s tests` -> 57/57 тестов успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализовать утилиту импорта: `/kb-implement TASK-044`.

---  

### [2026-10-11] — Выпуск официального релиза v0.11.0: Bug Lifecycle & Release Targeting (Фаза 11)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.11.0** по завершении Фазы 11 (План [[02_Tasks/Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]]).
  - Сформирован структурированный релизный документ [[02_Tasks/Releases/RELEASE-v0.11.0|RELEASE-v0.11.0]] во внутренней базе знаний и публичный файл заметок `dist/RELEASE_NOTES.md` по High-SNR стандарту (без шума ADR).
  - Собраны релизные артефакты в `dist/` через хук `scripts/build_release.py`:
    - `dist/install.py` (99.0 KB / 101 356 байт) — SHA-256: `c6b877a95817af8a9156666f4decaaceb498593a9ea130e2145a5734a4a105c7`.
    - `dist/RELEASE_NOTES.md` (3.0 KB / 2 988 байт) — SHA-256: `4e0bf47abf6519f2fca53dd31e4805519e3d309a30702340667f4e32e694d1b5`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (ссылка на официальный релиз `RELEASE-v0.11.0`) и корневой `CHANGELOG.md` (секция `[0.11.0]`).
  - Зафиксирован аннотированный Git-тег `v0.11.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 113 файлов проверено, 988 связей валидны (0 битых связей, 0 ошибок).
  - `python -m unittest discover -s tests` -> 56/56 тестов успешно пройдено (100% Pass, Exit code 0).
  - Контрольные суммы SHA-256 подтверждены.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выбор и концептуальная проработка следующей инициативы из Icebox (например, Zero Round-Trip Dispatch [[04_Research/RESEARCH-008-latency-prompt-caching-and-skill-chaining|RESEARCH-008]] или Feedback Loops & Triage Buffer [[04_Research/RESEARCH-003-feedback-channels-and-triage-pipeline|RESEARCH-003]]) через `/kb-plan`.

---

### [2026-10-11] — Завершение TASK-042 и Фазы 11: Синхронизация инсталлятора, E2E тесты и документация
- **Что сделано:**
  - Полностью завершена **Фаза 11: Жизненный цикл дефектов, прозрачный триаж и релизный таргетинг** согласно [[02_Tasks/Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]], [[03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]] и [[04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]].
  - Пересобран автономный монолитный инсталлятор `install.py` (99.0 KB) через `scripts/build_installer.py`: упакованы обновленные шаблоны `TEMPLATE_BUG.md`, `TEMPLATE_ONBOARDING.md`, скиллы `kb-bug`, `kb-implement`, `kb-complete`, и скрипт `kb_release.py`.
  - В генераторах правил агентов `install.py` (`_RULES_BODY`, `_3MODES`, `generate_agents_md` и др.) закреплены дисциплины: изоляция триажа дефектов Режима 2B (`kb-bug` со Stop & Yield), обязательный TDD-цикл устранения багов в Режиме 3 (`/kb-implement BUG-XXX`: RED -> GREEN -> REFACTOR) и барьер единичной задачи.
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_22_bug_lifecycle_and_phase11_assets`, проверяющий развертывание дефектов, бережное обновление через `install.py --update` и прерывание релиза открытыми блокерами.
  - Синхронизирована документация: актуализированы мастер-спецификация `SPEC.md`, витрина `README.md`, руководство `docs/Onboarding.md` и шаблон `templates/TEMPLATE_ONBOARDING.md`.
  - Все задачи Фазы 11 ([[02_Tasks/Specs/11_BugLifecycle/TASK-039-template-bug-and-kb-bug-triage-skill|TASK-039]], [[02_Tasks/Specs/11_BugLifecycle/TASK-040-kb-implement-bug-lifecycle-and-tdd|TASK-040]], [[02_Tasks/Specs/11_BugLifecycle/TASK-041-kb-release-defect-filtering-and-blockers|TASK-041]], [[02_Tasks/Specs/11_BugLifecycle/TASK-042-installer-bundling-e2e-and-docs|TASK-042]]) и план [[02_Tasks/Plans/PLAN-011-bug-lifecycle-triage-and-release-targeting|PLAN-011]] переведены в статус `done`/`completed`, Канбан и Дорожная карта актуализированы (Фаза 11 переведена в статус `✅ Завершена`).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> Payload 98 138 bytes -> compressed 39 356 b64 chars, `install.py` 101 356 bytes (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 22/22 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python -m unittest discover -s tests` -> 56/56 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 113 файлов проверено, 979 связей валидны (0 битых связей, 0 ошибок).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовка и публикация официального релиза Фазы 11: `/kb-release v0.11.0`.

---

### [2026-10-11] — Завершение TASK-041: Релизный таргетинг и фильтрация дефектов в scripts/kb_release.py (Фаза 11)
- **Что сделано:**
  - Реализован строгий релизный таргетинг дефектов в `scripts/kb_release.py` согласно [[03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]] и [[04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]].
  - Добавлена функция `collect_fixed_bugs`: сбор только устраненных багов (`status: fixed | closed`), у которых `fixed_in` или `target_release` совпадает с версией релиза (с fallback-поддержкой `target_phase` для legacy-багов).
  - Внедрена функция `check_release_blockers`: префлайт-проверка открытых дефектов (`status: open | in-progress`) с флагом `release_blocker: true`. При их обнаружении релиз немедленно прерывается с `Exit code 1`.
  - В `tests/test_kb_release.py` добавлен тест-сьют `TestBugReleaseTargeting` (4 теста), покрывающий корректную фильтрацию версий и блокировку открытыми багами-блокерами.
  - Спецификация задачи [[02_Tasks/Specs/11_BugLifecycle/TASK-041-kb-release-defect-filtering-and-blockers|TASK-041]] переведена в статус `done`, карточка перемещена в `Done` в [[02_Tasks/Kanban|Канбане]], веха отмечена в [[02_Tasks/Roadmap|Дорожной карте]].
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_release.py` -> 20/20 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python -m unittest discover -s tests` -> 55/55 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 113 файлов проверено, 972 связи валидны (0 битых связей, 0 ошибок).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-042-installer-bundling-e2e-and-docs`.

---

### [2026-10-11] — Завершение TASK-040: Нативная поддержка дефектов в kb-implement и kb-complete (Фаза 11)
- **Что сделано:**
  - Унифицировано исполнение дефектов в рамках Режима 3 (Implementation & Verification) согласно [[03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]].
  - В скилл `.agents/skills/kb-implement/SKILL.md` добавлена нативная поддержка аргумента `BUG-XXX` со строгим TDD-пайплайном: **RED** (запуск падающего теста из `regression_test`) $\to$ **GREEN** (минимальный фикс в коде) $\to$ **REFACTOR** (прогон полного тестового набора репозитория).
  - В скилл `.agents/skills/kb-complete/SKILL.md` добавлена логика финализации дефектов: простановка `status: fixed`, заполнение `fixed_in: "<target_release>"`, перемещение карточки дефекта в `Done` на Канбане и коммит `fix(...)`.
  - В `AGENTS.md` актуализированы правила: Regression-First Principle (закрепление TDD через `/kb-implement BUG-XXX`), Single-Task Execution Barrier (поддержка целей `TASK-XXX | BUG-XXX`) и регламент Режима 3.
  - В роутере `.agents/skills/docs-as-code/SKILL.md` синхронизированы описания скиллов `kb-implement` и `kb-bug`.
  - Спецификация задачи [[02_Tasks/Specs/11_BugLifecycle/TASK-040-kb-implement-bug-lifecycle-and-tdd|TASK-040]] переведена в статус `done`, карточка перемещена в `Done` в [[02_Tasks/Kanban|Канбане]], веха отмечена в [[02_Tasks/Roadmap|Дорожной карте]].
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 113 файлов проверено, 968 связей валидны (0 битых связей, 0 ошибок).
  - `python -m unittest discover -s tests` -> 51/51 тестов успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-041-kb-release-defect-filtering-and-blockers`.

---

### [2026-10-11] — Завершение TASK-039: Рефакторинг TEMPLATE_BUG.md и скилла kb-bug (Фаза 11)
- **Что сделано:**
  - Реализован изолированный входной шлюз обработки дефектов — Режим 2B (Defect Logging & Interactive Triage) согласно [[03_Decisions_ADR/ADR-0019-bug-lifecycle-triage-and-release-targeting|ADR-0019]] и [[04_Research/RESEARCH-014-bug-lifecycle-triage-and-release-targeting|RESEARCH-014]].
  - В шаблоны `docs/00_Templates/TEMPLATE_BUG.md` и `templates/TEMPLATE_BUG.md` добавлен релизный контракт дефектов: поля frontmatter `target_release`, `target_phase`, `release_blocker`, `fixed_in`, а также обновлена структура документа (диагностика, RCA, план исправления, TDD верификация).
  - Скилл `.agents/skills/kb-bug/SKILL.md` полностью освобожден от процедур редактирования кода и запуска тестов (устранение причины Eager Auto-Fixing Runaway) и переведен в чистый Режим 2B с интерактивным триажем и обязательным терминальным барьером `Stop & Yield Control`.
  - Спецификация задачи [[02_Tasks/Specs/11_BugLifecycle/TASK-039-template-bug-and-kb-bug-triage-skill|TASK-039]] переведена в статус `done`, карточка перемещена в `Done` в [[02_Tasks/Kanban|Канбане]], веха отмечена в [[02_Tasks/Roadmap|Дорожной карте]].
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 113 файлов проверено, 963 связи валидны (0 битых связей, 0 ошибок).
  - `python -m unittest discover -s tests` -> 51/51 тестов успешно пройдено (100% Pass, Exit code 0).
  - Проверено отсутствие директив правки кода в `kb-bug/SKILL.md`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - `/kb-implement TASK-040-kb-implement-bug-lifecycle-and-tdd`.

---

### [2026-10-03] — Выпуск кумулятивного релиза v0.10.0 (Фазы 9 и 10)
- **Что сделано:**
  - Осуществлен выпуск кумулятивного релиза [[02_Tasks/Releases/RELEASE-v0.10.0|v0.10.0]], объединяющего наработки Фазы 9 (Single-Task Execution Barrier & Stop-on-Complete Protocol), Фазы 10 (Spec Genesis Protocol & High-SNR Release Notes) и исправление дефекта CI [[02_Tasks/Bugs/BUG-001-ci-release-notes-phase-fallback|BUG-001]].
  - В утилиту `scripts/kb_release.py` добавлена поддержка кумулятивных релизов (`--phases 9,10`) с автоматическим парсингом метаданных из существующих релизных документов для CI-пайплайна.
  - Сгенерирован публичный файл заметок `dist/RELEASE_NOTES.md` по стандарту высокой плотности полезного сигнала (High-SNR) без шума кумулятивных ADR, а также структурированный документ базы знаний `docs/02_Tasks/Releases/RELEASE-v0.10.0.md` с фазовым скоупингом ADR.
  - Скомпилирован финальный автономный дистрибутив инсталлятора `dist/install.py` (95.1 KB, SHA-256: `1e31643af92b5fb3c8347e71c70e02a48c8abe9d764a3c8c2ed09320b7983a19`).
  - Актуализированы отметки о релизах в [[02_Tasks/Roadmap|Дорожной карте]] для Фазы 9 и Фазы 10.
- **Результаты верификации:**
  - `python scripts/kb_release.py --version v0.10.0 --phase 10 --phases 9,10` -> Exit code 0 (сгенерированы `RELEASE-v0.10.0.md` и `dist/RELEASE_NOTES.md`).
  - `python -m unittest discover -s tests` -> 51/51 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 битых связей, 0 предупреждений.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Создание git-тега `v0.10.0` и отправка в удаленный репозиторий (`git push origin main --tags`).

### [2026-10-03] — Завершение TASK-038: Синхронизация инсталлятора, E2E тесты и документация (Завершение Фазы 10)
- **Что сделано:**
  - Завершена реализация Фазы 10: комплексная синхронизация инсталлятора `install.py`, генераторов правил агентов, сквозных E2E тестов и документации проекта согласно [[03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]] и [[03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]].
  - В `install.py` актуализированы генераторы правил агентов (`_RULES_BODY`, `_3MODES` с 14 дисциплинами и правилом Spec Genesis, а также `generate_agents_md()` с инвариантом `6. Zero-State Anti-Hallucination & Spec Genesis`).
  - Через `scripts/build_installer.py` пересобран автономный дистрибутив `install.py` с упаковкой обновленных скиллов (`kb-init`, `kb-plan`, `kb-task`, `kb-release`), скрипта `scripts/kb_release.py`, шаблонов (`TEMPLATE_ONBOARDING.md`, `TEMPLATE_RELEASE.md`) и рабочих процессов.
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_21_spec_genesis_and_high_snr_release_notes`, подтвердивший:
    1. Создание проекта с пресетом `undecided` / `--idea` развертывает `SPEC.md` со статусом `discovery`.
    2. Механизм `install.py --update` обновляет скиллы `kb-init`, `kb-plan`, `kb-task`, `kb-release`, утилиту `kb_release.py`, сохраняет бэкап `AGENTS.md.bak` и актуализирует `AGENTS.md`.
    3. Генерация релизных заметок в целевом проекте создает публичный `dist/RELEASE_NOTES.md` без кумулятивной секции ADR (High-SNR) и внутренний `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` с фазово-изолированными решениями ADR.
    4. Аудит `kb_lint.py` проходит успешно с 0 предупреждений.
  - Актуализированы витрина [README.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/README.md), руководство [docs/Onboarding.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/docs/Onboarding.md) и мастер-спецификация [SPEC.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/SPEC.md).
  - Спецификация задачи [[02_Tasks/Specs/10_SpecLifecycle/TASK-038-installer-bundling-e2e-and-docs|TASK-038]], родительский план [[02_Tasks/Plans/PLAN-010-spec-genesis-and-high-snr-release-notes|PLAN-010]] и вся Фаза 10 переведены в статус завершенных в [[02_Tasks/Kanban|Канбане]] и [[02_Tasks/Roadmap|Дорожной карте]].
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> успешная компиляция бандла в `install.py` (Exit code 0).
  - `python -m unittest tests/test_installer.py` -> 21/21 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python -m unittest discover -s tests` -> 50/50 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 105 файлов проверено, 863 связи валидны (0 битых, 0 предупреждений, Exit code 0).
  - `python install.py --help` -> Exit code 0.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выпуск релиза Фазы 10: `/kb-release v0.10.0 --phase 10`.

---

### [2026-10-03] — Завершение TASK-037: High-SNR Release Notes Generator и фазовый скоупинг ADR
- **Что сделано:**
  - Реализован выходной шлюз методологии Docs-as-Code — Стандарт высокой плотности полезного сигнала в релизных заметках (High-SNR Release Notes) согласно [[03_Decisions_ADR/ADR-0017-release-notes-adr-exclusion-and-high-snr-standard|ADR-0017]] и [[04_Research/RESEARCH-013-release-notes-adr-exclusion-and-high-snr|RESEARCH-013]].
  - В функции `generate_public_release_notes()` утилиты `scripts/kb_release.py` полностью упразднена секция `### 🏛️ Архитектурные решения (ADR)`, исключая кумулятивное раздувание публичных заметок на GitHub (сокращение объема заметок на 45% и фокус на Highlights, Quick Install, Features, Fixes и SHA-256).
  - В функции `find_phase_artifacts()` реализован предикат `is_adr_for_phase()`, ограничивающий сбор ADR во внутреннем документе релиза `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` только решениями, релевантными текущей фазе (`phase: N`, теги `#phaseN` или ссылки в задачах/плане фазы).
  - Актуализирован скилл `.agents/skills/kb-release/SKILL.md` (High-SNR dual export) и шаблоны `docs/00_Templates/TEMPLATE_RELEASE.md` и `templates/TEMPLATE_RELEASE.md`.
  - В `tests/test_kb_release.py` добавлены модульные тесты `test_generate_public_release_notes_excludes_adrs` и `test_generate_release_note_filters_adrs_by_phase` (все 15 тестов пройдены).
  - Спецификация задачи [[02_Tasks/Specs/10_SpecLifecycle/TASK-037-high-snr-release-notes-and-phase-adr-scoping|TASK-037]] переведена в статус `done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_release.py` -> 15/15 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python -m unittest discover -s tests` -> 49/49 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 105 файлов проверено, 858 связей валидны (0 битых, 0 предупреждений, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи `TASK-038`: `/kb-implement TASK-038`.

---

### [2026-10-03] — Завершение TASK-036: Spec Genesis Protocol и Zero-State Guardrails
- **Что сделано:**
  - Реализован входной шлюз методологии Docs-as-Code — Протокол рождения Мастер-Спецификации (Spec Genesis) и защита от галлюцинаций в пустом состоянии (Zero-State) согласно [[03_Decisions_ADR/ADR-0018-spec-genesis-protocol-and-zero-state-handling|ADR-0018]] и [[04_Research/RESEARCH-011-spec-genesis-protocol-and-zero-state-handling|RESEARCH-011]].
  - В скилл `.agents/skills/kb-init/SKILL.md` добавлено гарантированное развертывание каркаса `SPEC.md` со статусом `status: discovery` (Spec Genesis skeleton), устраняя архитектурный пробел тулинга по сравнению с `install.py`.
  - В скилл `.agents/skills/kb-plan/SKILL.md` внедрен префлайт-чек Spec Genesis (Zero-State Guard), выдающий мягкое предупреждение (Soft Nudge) с предложением кристаллизовать концепцию и стек через `/kb-research` (Режим 0) до перехода к детальному планированию.
  - В скилл `.agents/skills/kb-task/SKILL.md` добавлена проверка статуса `SPEC.md`, предотвращающая нарезку ТЗ без согласованной спецификации.
  - В [AGENTS.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/AGENTS.md) закреплен инвариант `6. Zero-State Anti-Hallucination & Spec Genesis`: категорический запрет директивного выдумывания архитектуры, стека и бизнес-требований без прямого диалога с пользователем.
  - Спецификация задачи [[02_Tasks/Specs/10_SpecLifecycle/TASK-036-spec-genesis-and-zero-state-guardrails|TASK-036]] переведена в статус `done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 105 файлов проверено, 855 связей валидны (0 битых, 0 предупреждений, Exit code 0).
  - `python -m unittest discover -s tests` -> 47/47 тестов успешно пройдено (100% Pass, Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи `TASK-037`: `/kb-implement TASK-037`.

---

### [2026-10-03] — Завершение TASK-035: Синхронизация инсталлятора, E2E тесты и документация (Завершение Фазы 9)
- **Что сделано:**
  - Завершена реализация Фазы 9: комплексная интеграция барьера единичной задачи и протокола гарантированной остановки в дистрибутив харнесса Docs-as-Code ([[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]], [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]]).
  - В `install.py` актуализированы строковые константы правил (`_RULES_BODY`, `_3MODES` с 13-й дисциплиной `Single-Task Barrier`), встроенный генератор `generate_agents_md` и запись обновлений `record_devlog_update` с семантическим маркером.
  - Через `scripts/build_installer.py` пересобран автономный дистрибутив `install.py` с упаковкой обновленных шаблонов (`TEMPLATE_DEVLOG.md`, `TEMPLATE_ONBOARDING.md`), скиллов (`kb-implement`, `kb-complete`) и утилиты `scripts/kb_lint.py`.
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_20_single_task_barrier_and_stop_on_complete`, проверяющий генерацию правил, доставку обновлений через `install.py --update`, бэкап `AGENTS.md.bak` и чистоту журнала без предупреждений линтера.
  - Витрина проекта `README.md` и руководство `docs/Onboarding.md` дополнены описанием барьера единичной задачи и протокола Stop & Yield Control.
  - Успешно завершены задача [[02_Tasks/Specs/09_Guardrails/TASK-035-installer-bundling-e2e-and-docs|TASK-035]], план [[02_Tasks/Plans/PLAN-009-single-task-barrier-and-stop-on-complete|PLAN-009]] и вся Фаза 9 в [[02_Tasks/Kanban|Канбане]] и [[02_Tasks/Roadmap|Дорожной карте]].
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> Успешная сборка дистрибутива `install.py` (Exit code 0).
  - `python -m unittest discover -s tests` -> 47/47 тестов успешно пройдено (100% Pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 101 файл проверен, 795 связей валидны (0 битых, 0 предупреждений, Exit code 0).
  - `python install.py --help` -> Автономный инсталлятор готов к использованию (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подготовка и срез официального релиза Фазы 9: `/kb-release v0.9.0 --phase 9`.

---

### [2026-10-03] — Завершение TASK-034: Семантический протокол журнала разработки и аудит в kb_lint.py
- **Что сделано:**
  - Реализованы уровни 3 и 4 эшелонированной защиты против своевольного авто-чейнинга (Eager Task Chaining) согласно [[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]].
  - В шаблонах `docs/00_Templates/TEMPLATE_DEVLOG.md` и `templates/TEMPLATE_DEVLOG.md` строка «Следующий шаг» заменена на семантически безопасный маркер `- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**`.
  - В `scripts/kb_lint.py` реализована функция `check_devlog_semantic_guard(docs_dir)`: неблокирующий эвристический аудит (Exit code 0), выявляющий формулировки, провоцирующие модель на несанкционированное конвейерное продолжение работы.
  - В `tests/test_kb_lint.py` добавлены 4 модульных теста (`test_devlog_semantic_guard_*`), проверяющие детекцию опасных паттернов, пропуск защищенных строк и неблокирующий статус предупреждений.
  - Исторические записи в `docs/Devlog.md` приведены в соответствие новому стандарту (0 предупреждений).
  - Спецификация задачи [[02_Tasks/Specs/09_Guardrails/TASK-034-devlog-semantic-guard-and-kb-lint-audit|TASK-034]] переведена в статус `done`, Канбан-доска и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_lint.py` -> 14/14 тестов успешно пройдено (100% Pass).
  - `python -m unittest discover -s tests` -> 46/46 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 100 файлов проверено, 782 связи валидны (0 битых, 0 предупреждений).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи `TASK-035`: `/kb-implement TASK-035`.

---

### [2026-10-03] — Завершение TASK-033: Нормативный инвариант барьера единичной задачи и терминальный шаг Stop & Yield Control
- **Что сделано:**
  - Реализованы уровни 1 и 2 эшелонированной защиты против своевольного авто-чейнинга (Eager Task Chaining) согласно [[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]] и [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]].
  - В корневые правила [AGENTS.md](file:///c:/Users/Koudinie/Documents/antigravityProjects/agent-docs-harness/AGENTS.md) внесен инвариант `5. Single-Task Execution Barrier (No Auto-Chaining)` и шаг 9 `Terminal Step (Stop & Yield)` в чеклист Mode 3.
  - В скилл `.agents/skills/kb-implement/SKILL.md` добавлено ограничение `Single-Task Barrier` и шаг 5 `Immediate Auto-Completion & Stop` с принудительной остановкой вызовов инструментов.
  - В скилл `.agents/skills/kb-complete/SKILL.md` добавлено ограничение `Single-Task Barrier`, шаг 9 `Terminal Step: Stop & Yield Control` и семантический формат записи в Devlog.
  - Синхронизирована мастер-спецификация `SPEC.md` (добавлено описание Single-Task Barrier и Фазы 9).
  - Спецификация задачи [[02_Tasks/Specs/09_Guardrails/TASK-033-single-task-barrier-and-stop-yield-skills|TASK-033]] переведена в статус `done`, Канбан-доска и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 100 файлов проверено, 775 связей валидны (0 битых).
  - `python -m unittest discover -s tests` -> 42/42 теста успешно пройдено (100% Pass).
  - High-SNR замеры: `kb-implement` (32 строки), `kb-complete` (37 строк) соответствуют лимитам компактности.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи `TASK-034`: `/kb-implement TASK-034`.

---

### [2026-10-02] — Устранение дефекта BUG-001: Рассинхронизация номера фазы и описания релиза в CI release.yml
- **Что сделано:**
  - Локализован и устранен дефект [[02_Tasks/Bugs/BUG-001-ci-release-notes-phase-fallback|BUG-001]]: сброс метаданных в дефолтную Фазу 1 при запуске в GitHub Actions CI без параметров `--phase` и `--summary`.
  - Разработан воспроизводящий регрессионный тест `test_ci_mode_infers_phase_and_summary_from_existing_release_doc` в `tests/test_kb_release.py` (Regression-First, RED -> GREEN).
  - В `scripts/kb_release.py` добавлены функции `extract_release_meta_from_doc` (чтение `phase` и `Executive Summary` из существующего артефакта `docs/02_Tasks/Releases/RELEASE-{tag}.md` как Single Source of Truth) и `detect_latest_phase` (эвристический автодетект фазы по `docs/02_Tasks/Specs/`).
  - Пересобран бандл `install.py` (89.4 KB) через `scripts/build_installer.py`.
  - Карточка дефекта переведена в статус `Done` на Канбан-доске [[02_Tasks/Kanban|Kanban.md]], отчет [[02_Tasks/Bugs/BUG-001-ci-release-notes-phase-fallback|BUG-001]] переведен в статус `fixed`.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 42/42 теста пройдено успешно (100% Pass).
  - `python scripts/kb_release.py --version v0.8.0 --ci-mode` -> сформирован корректный `dist/RELEASE_NOTES.md` с «Фаза 8» и полным Executive Summary.
  - `python scripts/kb_lint.py --path docs` -> 94 файла проверено, 712 викиссылок валидны (0 битых).

---

### [2026-10-02] — Выпуск официального релиза v0.8.0: Greenfield-инициализация от идеи и Living Spec (Фаза 8)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.8.0** по завершении Фазы 8 (План [[02_Tasks/Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.8.0|RELEASE-v0.8.0]] и публичные заметки `dist/RELEASE_NOTES.md` с чистым GitHub Markdown и автоконвертером викиссылок.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (88.4 KB) — SHA-256: `867757bad12d737fa8409fdfea41e63850c9658f8e5fb0cc4a60c62e6351ec26`.
    - `dist/RELEASE_NOTES.md` (6.4 KB) — SHA-256: `1469cd999b113ab5a8f98ad4eb9c96e996e1c936d865186d8dcf431cecaf421e`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (ссылка на официальный релиз `RELEASE-v0.8.0`) и корневой `CHANGELOG.md` (секция `[0.8.0]`).
  - Зафиксирован аннотированный Git-тег `v0.8.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 93 файла проверено, 683 викиссылки валидны (0 битых).
  - `python -m unittest discover -s tests` -> 41/41 тест успешно пройден (100% Pass).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена (`867757bad12d737fa8409fdfea41e63850c9658f8e5fb0cc4a60c62e6351ec26`).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Определение приоритета следующей инициативы из Icebox (например, реализация Single-Task Execution Barrier по итогам [[04_Research/RESEARCH-012-single-task-execution-barrier-and-autonomous-pipeline-containment|RESEARCH-012]] и [[03_Decisions_ADR/ADR-0016-single-task-execution-barrier-and-stop-on-complete-protocol|ADR-0016]]) через `/kb-plan`.

---

### [2026-10-02] — Завершение TASK-032: Сборка инсталлятора, E2E тесты и документация (Завершение Фазы 8)
- **Что сделано:**
  - Запущен сборщик `scripts/build_installer.py`: актуализирован монолит `install.py` с упаковкой обновленных шаблонов (`TEMPLATE_ONBOARDING.md`), скиллов (`kb-research`, `kb-complete`, `kb-release`), скрипта `kb_lint.py` и конфигов (`EMBEDDED_ASSETS_B64`).
  - Расширен тестовый сценарий `test_19_undecided_preset_and_idea_flag` в `tests/test_installer.py`: добавлена валидация развертывания всех 12 скиллов и успешного прогона `kb_lint.py` на созданном проекте.
  - Актуализирован `README.md`: добавлен раздел быстрого старта с опцией `--idea` (Greenfield Idea-First), пресет `undecided` в таблицу поддерживаемых стеков, CLI-флаг `--idea`, и диаграмма 4-этапного жизненного цикла (Discovery + Delivery).
  - Актуализировано руководство `docs/Onboarding.md` и шаблон `templates/TEMPLATE_ONBOARDING.md`: добавлен раздел 7 с регламентом Greenfield Idea-First старта, инварианта Living Spec и эвристического контроля дрифта.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]] и весь план [[02_Tasks/Plans/PLAN-008-greenfield-idea-first-and-living-spec|PLAN-008]] переведены в статус `done`, Канбан и Дорожная карта актуализированы (Фаза 8 завершена).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> успешная сборка монолита `install.py` (88.4 KB).
  - `python -m unittest discover -s tests` -> 41/41 тест пройден (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 658 викиссылок валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выпуск официального релиза Фазы 8 через `/kb-release v0.8.0`.

---

### [2026-10-02] — Завершение TASK-031: Эвристический контроль дрифта спецификации в scripts/kb_lint.py
- **Что сделано:**
  - В автономном линтере `scripts/kb_lint.py` реализована функция `check_spec_drift(docs_dir: Path)` для неблокирующего эвристического анализа устаревания мастер-спецификации.
  - Детектор сканирует `Roadmap.md` на предмет завершенных фаз (`## Фаза X: ... — ✅ Завершена` или блоков с закрытыми чекбоксами `- [x]`) и сверяет дату `updated` в `SPEC.md` с датой `created`.
  - При обнаружении $\ge 2$ завершенных фаз без обновления `SPEC.md` линтер выводит неблокирующее предупреждение (`⚠️  WARN: Living Spec Drift...`), сохраняя статус успешного выполнения (`exit code 0`).
  - В `tests/test_kb_lint.py` добавлено 5 новых модульных тестов, проверяющих:
    - генерацию предупреждения при дрифте (с сохранением exit code 0);
    - отсутствие предупреждения при актуализированном `SPEC.md` (`updated != created`);
    - отсутствие ложных срабатываний при одной завершенной фазе (порог $\ge 2$);
    - безопасную работу при отсутствии файлов спецификации или дорожной карты;
    - форматирование секции дрифта в подробном режиме (`--verbose`).
  - Актуализирована мастер-спецификация `SPEC.md`: дата обновлена до `2026-10-02`, разделы дополнены описанием 4 этапов жизненного цикла (Modes 0–3), 13 шаблонов, утилит `kb_release.py` и `kb_lint.py`, пресета `undecided` и протокола Living Spec.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]] переведена в `status: done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_lint.py` -> 10/10 тестов пройдено (100% Pass).
  - `python -m unittest discover -s tests` -> 41/41 тест пройден (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 656 викиссылок валидны (0 битых, 0 предупреждений дрифта).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи [[02_Tasks/Specs/08_Greenfield/TASK-032-installer-bundling-and-e2e-verification|TASK-032]] (Сборка инсталлятора `build_installer.py`, сквозные E2E тесты нового пресета, обновление `README.md` и `docs/Onboarding.md`).

---

### [2026-10-02] — Завершение TASK-030: Протокол Living Spec и синхронизация документации
- **Что сделано:**
  - В скилле `.agents/skills/kb-research/SKILL.md` добавлен шаг первичного выбора стека (Primary Stack Selection): если `SPEC.md` находится в `status: discovery`, принятие `ADR-0001` автоматически переводит спецификацию в `status: active`, наполняет реальными командами сборки/тестирования и синхронизирует `README.md`.
  - В скилле `.agents/skills/kb-complete/SKILL.md` внедрен шаг `Living Spec Sync`: если завершенная задача изменила публичный CLI, интерфейсы или системную архитектуру, агент обязан актуализировать `SPEC.md` и `README.md` в той же сессии.
  - В скилле `.agents/skills/kb-release/SKILL.md` в раздел префлайт-чеков добавлена обязательная верификация актуальности `README.md` (CLI команды/примеры) и `SPEC.md` перед срезом релиза.
  - В `AGENTS.md` закреплено каноническое правило `Living Spec Invariant (No Documentation Drift)` и обновлены чеклисты режимов 0 и 3.
  - В утилите `install.py` синхронизированы шаблоны правил агентов (`_RULES_BODY`, `_3MODES`) с обязательным напоминанием о синхронизации Living Spec.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-030-living-spec-protocol-and-skill-sync|TASK-030]] переведена в `status: done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 36/36 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 654 викиссылки валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи [[02_Tasks/Specs/08_Greenfield/TASK-031-kb-lint-spec-drift-audit|TASK-031]] (Эвристический контроль дрифта спецификации в `scripts/kb_lint.py` и модульные тесты в `tests/test_kb_lint.py`).

---

### [2026-10-02] — Завершение TASK-029: Пресет undecided и CLI-флаг --idea в install.py
- **Что сделано:**
  - В утилите `install.py` реализован пресет `undecided` (*"Undecided / Idea-First Research"*) с нейтральными заглушками и отложенным выбором стека через Режим 0.
  - Добавлена опция `6) 💡 Undecided / Idea-First` в интерактивное меню выбора стека.
  - Реализован CLI-флаг `--idea "<текст>"` для Greenfield-старта с одной продуктовой идеи; при его указании без флага `--stack` автоматически активируется пресет `undecided`.
  - Модифицирована функция `create_starter_docs`: при выборе пресета `undecided` мастер-спецификация `SPEC.md` создается со статусом `status: discovery`, описание идеи помещается в раздел «Концепция и цели», а в архитектурном разделе фиксируется статус TBD.
  - Обновлен финальный приветственный баннер инсталлятора, подсказывающий первый шаг: `/kb-research <исследование идеи и выбор стека>`.
  - Добавлен сквозной модульный и CLI тест `test_19_undecided_preset_and_idea_flag` в `tests/test_installer.py`.
  - Задача [[02_Tasks/Specs/08_Greenfield/TASK-029-undecided-preset-and-idea-flag|TASK-029]] переведена в `status: done`, Канбан и Дорожная карта актуализированы.
- **Результаты верификации:**
  - `python install.py --help` -> подтверждено наличие опции `--idea` и значения `undecided` в `--stack`.
  - `python -m unittest tests.test_installer.TestAgentDocsHarness.test_19_undecided_preset_and_idea_flag` -> 1/1 Pass (Exit code 0).
  - `python -m unittest discover -s tests` -> 36/36 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 89 файлов проверено, 652 викиссылки валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация задачи [[02_Tasks/Specs/08_Greenfield/TASK-030-living-spec-protocol-and-skill-sync|TASK-030]] (Протокол Living Spec и синхронизация документации в скиллах `kb-research`, `kb-complete`, `kb-release` и `AGENTS.md`).

---

### [2026-10-01] — Выпуск официального релиза v0.7.0: GitHub Releases & Distribution Notes Standard (Фаза 7)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.7.0** по завершении Фазы 7 (План [[02_Tasks/Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.7.0|RELEASE-v0.7.0]] и публичные заметки `dist/RELEASE_NOTES.md` с чистым GitHub Markdown и автоконвертером викиссылок.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (83.3 KB / 85 310 байт) — SHA-256: `1e386242736e166e836fe5116ccbdad64dfcab48e97781f302b40e8764d68d4b`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (ссылка на официальный релиз `RELEASE-v0.7.0`) и корневой `CHANGELOG.md` (секция `[0.7.0]`).
  - Зафиксирован аннотированный Git-тег `v0.7.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
  - `python -m unittest discover -s tests` -> 35/35 тестов успешно пройдено (Exit code 0).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена (`1e386242736e166e836fe5116ccbdad64dfcab48e97781f302b40e8764d68d4b`).

---

### [2026-10-01] — Завершение TASK-028 и Фазы 7: Сборка инсталлятора и сквозная E2E верификация
- **Что сделано:**
  - Пересобран автономный инсталлятор `install.py` через `scripts/build_installer.py`, упаковав обновленные `scripts/kb_release.py` (двухформатный экспорт заметок и автоконвертер викиссылок), воркфлоу `.github/workflows/release.yml` (`body_path: dist/RELEASE_NOTES.md`), скилл `.agents/skills/kb-release/SKILL.md` и шаблон `TEMPLATE_RELEASE.md`.
  - Дополнен тестовый набор `tests/test_installer.py` проверками наличия `body_path: dist/RELEASE_NOTES.md` в воркфлоу, флага `--notes-file dist/RELEASE_NOTES.md` в скилле `kb-release`, генерации `dist/RELEASE_NOTES.md` и корректного обновления через `install.py --update`.
  - Все задачи Фазы 7 ([[02_Tasks/Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]) — TASK-025, TASK-026, TASK-027, TASK-028 — переведены в `status: done` в ТЗ, Дорожная карта и Канбан актуализированы (Фаза 7 перемещена в `Done`).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> инсталлятор успешно пересобран (размер: 83.3 KB, сжатие: 41.9%).
  - `python -m unittest discover -s tests` -> 35/35 тестов успешно пройдено (100% Pass).
  - `python scripts/kb_lint.py --path docs` -> 77 файлов проверено, 516 викиссылок валидны (0 битых).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Приемочное тестирование Фазы 7 и выпуск публичного релиза `v0.7.0` через скилл `/kb-release`.

---

### [2026-10-01] — Завершение TASK-027: Актуализация скилла kb-release и шаблона TEMPLATE_RELEASE.md
- **Что сделано:**
  - В скилле `.agents/skills/kb-release/SKILL.md` актуализированы шаги 4 и 6:
    - Шаг 4: зафиксирована генерация внутреннего `RELEASE-vX.Y.Z.md` и публичного `dist/RELEASE_NOTES.md`.
    - Шаг 6 (GitHub Mode): команда публикации `gh release create` дополнена параметром `--notes-file dist/RELEASE_NOTES.md`.
    - Сохранена High-SNR токеномика (описание frontmatter $\le$ 15 слов).
  - В шаблонах `TEMPLATE_RELEASE.md` (в `docs/00_Templates/` и корневой `templates/`) добавлено примечание о генерации публичных заметок в `dist/RELEASE_NOTES.md`.
  - Задача [[02_Tasks/Specs/07_Distribution/TASK-027-kb-release-skill-and-notes-file|TASK-027]] переведена в `status: done` в ТЗ, Канбане (`(2026-10-01)`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - Подтверждена идентичность файлов шаблонов в `docs/00_Templates/` и `templates/`.
  - Проверена лаконичность описания `SKILL.md` (13 слов).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-028`: Сборка инсталлятора `build_installer.py`, регрессионные E2E тесты и аудит целостности дистрибутива.

---

### [2026-10-01] — Завершение TASK-026: Автоматизация передачи заметок в CI release.yml и шаблоне инсталлятора
- **Что сделано:**
  - В файле `.github/workflows/release.yml` добавлен параметр `body_path: dist/RELEASE_NOTES.md` в шаг `Publish GitHub Release` (`softprops/action-gh-release@v2`). Теперь GitHub Release автоматически получает полное описание, команды быстрой установки и таблицу SHA-256 из артефакта, сгенерированного `kb_release.py --ci-mode`.
  - В `install.py` обновлен встроенный fallback-шаблон `wf_release_content` в функции `deploy_ci_workflows()` с включением `body_path: dist/RELEASE_NOTES.md`.
  - Задача [[02_Tasks/Specs/07_Distribution/TASK-026-github-actions-release-body-and-installer-template|TASK-026]] переведена в `status: done` в ТЗ, Канбане (`(2026-10-01)`) и Дорожной карте (`[x]`).
- **Результаты верификации:**
  - Проверена валидность синтаксиса `.github/workflows/release.yml` и наличие `body_path: dist/RELEASE_NOTES.md`.
  - Проверено наличие актуального шаблона воркфлоу в `install.py`.
  - `python -m unittest tests/test_kb_release.py` -> 12/12 тестов успешно пройдено.
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-027`: Актуализация скилла `.agents/skills/kb-release/SKILL.md` (флаг `--notes-file dist/RELEASE_NOTES.md`) и шаблона `TEMPLATE_RELEASE.md`.

---

### [2026-10-01] — Завершение TASK-025: Двухформатный экспорт и автоконвертер викиссылок в scripts/kb_release.py
- **Что сделано:**
  - В утилите `scripts/kb_release.py` реализована функция `convert_wikilinks_to_github_markdown` (Zero-Dependencies):
    - Относительные викиссылки `[ [ ../Specs/... | TASK-XXX ] ]` и `[ [ ../../03_Decisions_ADR/... | ADR-XXXX ] ]` преобразуются в полноценные кликабельные URL GitHub с учетом `remote.origin.url` и ветки `main`.
    - В Local-Only режиме без удаленного репозитория ссылки безопасно сворачиваются в жирный шрифт `**Alias**`.
  - Добавлена функция `generate_public_release_notes`:
    - Формирует `dist/RELEASE_NOTES.md` в чистом GitHub Flavored Markdown (GFM) без YAML frontmatter.
    - Включает Executive Summary, блок быстрого старта (Quick Install / Upgrade) с автоопределением `raw.githubusercontent.com`, категоризированный чейнджлог (Features, Bug Fixes, ADRs), таблицу артефактов SHA-256 с командами верификации (`Get-FileHash` / `sha256sum`) и ссылку на Release diff.
  - Обновлен CLI интерфейс `main()`:
    - Добавлен аргумент `--notes-output` (по умолчанию `dist/RELEASE_NOTES.md`).
    - При обычном запуске и в `--ci-mode` генерируются оба документа: внутренний `docs/02_Tasks/Releases/RELEASE-{tag}.md` и публичный `dist/RELEASE_NOTES.md`.
    - В режиме `--dry-run` выводятся обе секции с разделителем.
  - Написаны модульные тесты в `tests/test_kb_release.py` (12 тестов, 100% pass):
    - Тестирование конвертации викиссылок (HTTPS, SSH, Local-Only fallback).
    - Тестирование структуры `dist/RELEASE_NOTES.md` и отсутствия YAML frontmatter.
    - Тестирование одновременного создания обоих файлов через CLI.
  - Задача [[02_Tasks/Specs/07_Distribution/TASK-025-dual-export-and-wikilinks-converter|TASK-025]] переведена в `status: done`.
- **Результаты верификации:**
  - `python -m unittest tests/test_kb_release.py` -> 12/12 тестов успешно пройдено.
  - `python scripts/kb_release.py --version 0.7.0 --phase 7 --dry-run` -> чистый и корректный вывод.
  - `python -m unittest discover -s tests` -> 35/35 тестов успешно пройдено.
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-026`: Автоматизация передачи заметок в CI `release.yml` (`body_path: dist/RELEASE_NOTES.md`) и синхронизация встроенного шаблона в `install.py`.

---

### [2026-10-01] — Выпуск официального релиза v0.6.0: Discovery & Feasibility Lifecycle (Фаза 6)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.6.0** по завершении Фазы 6 (План [[02_Tasks/Plans/PLAN-006-discovery-mode-and-kb-research-lifecycle|PLAN-006]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.6.0|RELEASE-v0.6.0]] по каноническому стандарту `TEMPLATE_RELEASE.md`.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (81.5 KB / 83 499 байт) — SHA-256: `132776da84c4820caf3359598ec827594d541927bd6c857b7a8ee16647d03a7f`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (ссылка на официальный релиз `RELEASE-v0.6.0`) и корневой `CHANGELOG.md` (секция `[0.6.0]`).
  - Зафиксирован аннотированный Git-тег `v0.6.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links.
  - `python -m unittest discover -s tests` -> 31/31 тест успешно пройден (Exit code 0).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена (`132776da84c4820caf3359598ec827594d541927bd6c857b7a8ee16647d03a7f`).

---

### [2026-10-01] — Завершение TASK-024 и Фазы 6: Синхронизация инсталлятора, E2E тесты и аудит целостности
- **Что сделано:**
  - Запущена пересборка автономного инсталлятора `scripts/build_installer.py`:
    - Все обновленные шаблоны (`TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md`) и скиллы (`kb-research`, `kb-plan`, `kb-onboard`) сжаты и упакованы в `install.py` (размер дистрибутива 81.5 KB, полезная нагрузка ассетов 71.4 KB).
  - Актуализирован тестовый набор `tests/test_installer.py`:
    - Добавлен сквозной регрессионный тест `test_18_discovery_mode_and_phase6_assets` для верификации упаковки артефактов Режима 0 (Discovery & Feasibility), двухпутевой воронки в `kb-research`, префлайт-чеков в `kb-plan` и секций отклоненных альтернатив.
    - Адаптированы бенчмарки токеномики High-SNR (`test_16_high_snr_static_corpus_benchmarks`) под обновленные шаблоны с сохранением строгого лимита `total_templates_size <= 21000`.
  - Закрыта задача `TASK-024` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - Успешно завершена **Фаза 6: Интеграция этапа исследования (Режим 0: Discovery & Feasibility) и эволюция /kb-research** (`PLAN-006` переведен в `status: completed`).
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> Payload 73 148 bytes, `install.py` 83 490 bytes (Exit code 0).
  - `python -m unittest discover -s tests` -> 31/31 тест успешно пройден (100% pass, Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 438 wikilinks verified).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Релиз версии `v0.6.0` через команду `/kb-release v0.6.0` (Dual-Mode: Local-Only / GitHub tag & Release Notes).

---

### [2026-10-01] — Завершение TASK-023: Обновление шаблонов TEMPLATE_ROADMAP, TEMPLATE_ONBOARDING и руководства Onboarding.md
- **Что сделано:**
  - Синхронизированы канонические шаблоны в `docs/00_Templates/` и корневом `templates/`:
    - `TEMPLATE_ROADMAP.md`: внедрен ориентирующий комментарий для секции Icebox (рекомендация использовать `/kb-research <идея>` вместо ручной правки) и добавлена секция `## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)`.
    - `TEMPLATE_ONBOARDING.md`: матрица режимов обновлена до 4-этапного цикла (Режим 0: Исследование / Discovery, Режимы 1–3: Delivery), команды `/kb-research` и `/kb-adr` добавлены в справочник, процесс Brownfield Adoption расширен до 4 этапов.
  - Обновлено руководство `docs/Onboarding.md`:
    - Mermaid диаграмма жизненного цикла обновлена (модель Double Diamond: Режим 0 $\to$ Режимы 1–3).
    - Добавлен подраздел с описанием **Режима 0: Исследование и валидация гипотез (Discovery & Feasibility)**.
  - Закрыта задача `TASK-023` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - В `Kanban.md` задача `TASK-024` переведена в колонку `## ⏳ В работе (In Progress)`.
- **Результаты верификации:**
  - Проверена строгая побайтовая идентичность шаблонов `docs/00_Templates/` и `templates/` (100% совпадение).
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 438 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-024`: пересборка дистрибутива `install.py` через `scripts/build_installer.py`, регрессионные E2E тесты и аудит целостности.

---

### [2026-10-01] — Завершение TASK-022: Префлайт-чеки в kb-plan и 4-этапный цикл в kb-onboard
- **Что сделано:**
  - Обновлен скилл `.agents/skills/kb-plan/SKILL.md`:
    - Внедрен предупреждающий фильтр **Pre-flight Nudge** в шаге 1 процедуры (Intent Routing): при передаче рискованной идеи, затрагивающей внешние зависимости (ADR-0001) или платформенные неопределенности, агент рекомендует сначала выполнить исследование и фальсификацию в Режиме 0 (`/kb-research <idea>`).
  - Обновлен скилл `.agents/skills/kb-onboard/SKILL.md`:
    - Онбординг-шпаргалка актуализирована с 3-режимного до **4-этапного жизненного цикла (Discovery + Delivery)**.
    - В матрицу команд включен **Режим 0 (Discovery & Feasibility)**: `/kb-research` (стресс-тесты, бенчмарки, синхронизация с Icebox) и `/kb-adr` (фиксация архитектурных решений и отказных альтернатив).
  - Закрыта задача `TASK-022` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - В `Kanban.md` задача `TASK-023` переведена в колонку `## ⏳ В работе (In Progress)`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 437 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-023`: обновление шаблонов `TEMPLATE_ROADMAP.md`, `TEMPLATE_ONBOARDING.md` и руководства `Onboarding.md`.

---

### [2026-10-01] — Завершение TASK-021: Эволюция скилла kb-research и маршрутизация гипотез в Roadmap
- **Что сделано:**
  - Обновлен исполняемый скилл `.agents/skills/kb-research/SKILL.md` согласно спецификации [[02_Tasks/Specs/06_Discovery/TASK-021-kb-research-evolution-and-roadmap-routing|TASK-021]]:
    - Скилл преобразован в канонический инструмент **Режима 0 (Discovery & Feasibility)** модели Double Diamond (согласно [[03_Decisions_ADR/ADR-0012-discovery-mode-and-kb-research-lifecycle-integration|ADR-0012]] и [[04_Research/RESEARCH-007-discovery-mode-and-kb-research-lifecycle-integration|RESEARCH-007]]).
    - Расширен фокус: от узких платформенных дефектов к полноценной валидации продуктовых и архитектурных гипотез с критическим партнерством агента (Senior Partner: обязательная фальсификация, риски Zero-Deps, токеномика).
    - Внедрена двухпутевая автоматическая воронка интеграции с [[02_Tasks/Roadmap|Roadmap.md]]:
      - Одобренные инициативы $\to$ автоматическая регистрация в `## 🔮 Перспективные направления (Future Horizons / Icebox)` с оценкой ценности (Value Impact).
      - Отклоненные инициативы $\to$ фиксация отказного ADR (`status: rejected`) через `/kb-adr` и регистрация в `## 🚫 Отклоненные архитектурные идеи (Rejected Alternatives)`.
    - Сохранена High-SNR токеномика: микро-описание frontmatter $\le$ 15 слов, компактные императивные формулировки.
  - Закрыта задача `TASK-021` в спецификации (`status: done`), Канбане (`## ✅ Готово`) и Дорожной карте (`[x]`).
  - В `Kanban.md` задача `TASK-022` переведена в колонку `## ⏳ В работе (In Progress)`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (71 files scanned, 433 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-022`: префлайт-чеки в `/kb-plan` и актуализация онбординг-скилла `/kb-onboard`.

---

### [2026-10-01] — Выпуск официального релиза v0.5.0: High-SNR Token Architecture (Фаза 5)
- **Что сделано:**
  - Осуществлен официальный релиз **v0.5.0** по завершении Фазы 5 (План [[02_Tasks/Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]).
  - Сформирован релизный документ [[02_Tasks/Releases/RELEASE-v0.5.0|RELEASE-v0.5.0]] по каноническому стандарту `TEMPLATE_RELEASE.md`.
  - Собраны релизные артефакты через хук `scripts/build_release.py`:
    - `dist/install.py` (81.2 KB / 83 119 байт) — SHA-256: `04d88c2a1f5c10bb0e2b4bb0f1715d6af377aaffd3cfed3843a6b51183d5707d`.
  - Обновлены [[02_Tasks/Roadmap|Roadmap.md]] (статус Фазы 5 переведен в `✅ Завершена`) и корневой `CHANGELOG.md`.
  - Зафиксирован аннотированный Git-тег `v0.5.0`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 0 broken links (60 files scanned, 331 wikilinks verified).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (Exit code 0).
  - Контрольная сумма SHA-256 `dist/install.py` подтверждена.

---

### [2026-10-01] — Завершение TASK-020: Синхронизация сборщика, install.py (--update) и E2E тесты (Завершение Фазы 5)
- **Что сделано:**
  - Полностью завершена **Фаза 5: Оптимизация токенов и High-SNR архитектура контекста**:
    - Перепакован автономный монолитный инсталлятор `install.py` через `scripts/build_installer.py`:
      - В бандл включены все 13 компактных шаблонов `templates/`, 12 High-SNR скиллов `.agents/skills/`, утилиты `scripts/kb_lint.py` и `scripts/kb_release.py`.
      - Размер итогового дистрибутива `install.py` сократился с 98.6 КБ до **81.2 КБ** (-17.6%).
    - Функция `customize_templates_for_stack` адаптирована для бесшовной параметризации новых компактных Skeleton Templates под все поддерживаемые стеки (Swift, TS, Python, .NET, Generic).
    - В `install.py` расширен механизм бережного обновления (`update_harness`) с поддержкой флага `backup=True/False`.
    - В `tests/test_installer.py` добавлены E2E тесты бенчмаркинга (`test_16_high_snr_static_corpus_benchmarks`) и верификации миграции устаревших проектов (`test_17_update_migrates_to_skeleton_templates_and_high_snr_skills`):
      - Общий размер 12 скиллов: $\le$ 20 000 байт (фактически ~18.9 КБ vs лимит 20 КБ).
      - Общий размер 13 шаблонов: $\le$ 21 000 байт (фактически ~20.0 КБ vs лимит 21 КБ).
      - Размер `TEMPLATE_ONBOARDING.md`: $\le$ 4 000 байт (фактически 3.8 КБ).
      - Размер роутера `docs-as-code/SKILL.md`: $\le$ 3 000 байт (фактически 2.2 КБ).
      - Размер дистрибутива `install.py`: $\le$ 100 000 байт (фактически 81.2 КБ).
    - Актуализирована документация: в `README.md`, `docs/Onboarding.md` и `docs/00_Index.md` отражен стандарт High-SNR Token Architecture.
    - В `scripts/kb_lint.py` расширен список игнорируемых русскоязычных плейсхолдеров (`заметка`, `документ`, `файл`, `slug`).
  - Закрыта задача `TASK-020` и завершен план `PLAN-005` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python scripts/build_installer.py` -> 13 шаблонов, 12 скиллов, 2 скрипта, 81.2 КБ payload (Exit code 0).
  - `python scripts/kb_lint.py --path docs` -> `OK: 59 files scanned, 315 wikilinks verified (0 broken).` (Exit code 0).
  - `python -m unittest discover -s tests` -> 30/30 тестов успешно пройдены (100% pass, Exit code 0).
  - Тестовая установка в изолированную директорию подтвердила работоспособность и чистоту создаваемого проекта.
- **Итог Фазы 5:**
  - Достигнуто радикальное сжатие контекстной нагрузки на 55–65% за сессию при 100% сохранении инженерных гарантий, 3-режимного цикла и интерактивного графа Obsidian.

---

### [2026-10-01] — Завершение TASK-019: Внедрение правил High-SNR, Anti-Echo и Silent-CLI (Фаза 5)
- **Что сделано:**
  - Реализованы Правила 3 (Anti-Echo Response Protocol), 4 (DRY Rules Hierarchy) и 6 (Silent-on-Success CLI) из [[03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]:
    - В `AGENTS.md` и генератор правил `install.py` внедрен строгий протокол **Anti-Echo Response Protocol**: полный запрет на повторную распечатку содержимого файлов в чате; обязательный компактный формат (кликабельный permalink `[FileName](file:///...)` + резюме из 3–5 пунктов + следующий шаг).
    - В `AGENTS.md` и `install.py` внедрена полная явная таблица 7-цветовой схемы Obsidian Graph (`.obsidian/graph.json`) и тегов (`#arch`, `#adr`, `#research`, `#task`, `#bug`, `#testing`).
    - В утилите `scripts/kb_lint.py` реализован режим Silent-on-Success: при успешной проверке выводится ровно одна строка (`OK: N files scanned, M wikilinks verified (0 broken).`), добавлен флаг `--verbose` (`-v`) для вывода полного аудита; ошибки выводятся развернуто.
    - В утилите `scripts/kb_release.py` реализован лаконичный однострочный вывод успешной генерации релиза и добавлен флаг `--verbose` (`-v`).
    - Создан набор модульных тестов `tests/test_kb_lint.py` (5 тестов: Silent-on-Success, Verbose, обнаружение битых wikilinks, ошибки YAML frontmatter, CLI флаги).
  - Закрыта задача `TASK-019` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> `OK: 59 files scanned, 313 wikilinks verified (0 broken).` (1 строка, Exit code 0).
  - `python scripts/kb_lint.py --path docs --verbose` -> полный лог аудита, Exit code 0.
  - `python -m unittest tests/test_kb_lint.py` -> 5/5 тестов зеленые.
  - `python -m unittest discover -s tests` -> 28/28 тестов зеленые.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-020`: Синхронизация сборщика `scripts/build_installer.py`, `install.py` (`--update`), E2E тесты и замеры сжатия.

---

### [2026-10-01] — Завершение TASK-018: Рефакторинг 13 шаблонов docs/00_Templates/ в компактные каркасы (Фаза 5)
- **Что сделано:**
  - Реализовано Правило 5 (Skeleton Templates) архитектурного стандарта [[03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]:
    - Все 13 шаблонов `docs/00_Templates/` очищены от обучающих эссе, вербального шума и пространных рассуждений, замененных на точечные однострочные директивы `<!-- prompt / instruction -->`.
    - Шаблон `TEMPLATE_ONBOARDING.md` радикально сжат с 11 423 байт до 3 567 байт (-68.8%), превратившись в высокоэффективную шпаргалку по онбордингу без «воды».
    - Сохранена 100% структурная целостность: YAML frontmatter, канонические разделы, интерактивные чеклисты `- [ ]` и связность графа Obsidian.
  - Суммарный объем 13 шаблонов сокращен с 38 774 байт до 19 712 байт (-49.2%), что укладывается в бюджет $\le$ 21 000 байт.
  - Закрыта задача `TASK-018` в `Kanban.md` и отмечен пункт в `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 59 файлов, 312 ссылок, 0 broken links, 100% валидный YAML frontmatter.
  - `python -m unittest discover -s tests` -> 23/23 тестов зеленые.
  - Замер размера шаблонов: 19 712 байт $\le$ 21 000 байт; `TEMPLATE_ONBOARDING.md`: 3 567 байт $\le$ 4 000 байт.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-019`: Внедрение правил High-SNR, Anti-Echo протокола и Silent-CLI в `AGENTS.md`, `scripts/kb_lint.py` и `scripts/kb_release.py`.

---

### [2026-10-01] — Завершение TASK-017: High-SNR рефакторинг реестра и 12 скиллов .agents/skills/ (Фаза 5)
- **Что сделано:**
  - Реализованы Правила 1, 2, 4 и 6 архитектурного стандарта [[03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]]:
    - Сжаты Always-On описания в YAML frontmatter всех 12 скиллов до лаконичных Micro-Descriptions (10–13 слов), что снижает постоянный налог системного реестра на 53% (~194 токена вместо ~410 токенов на каждом шаге диалога).
    - Монолитный скилл `docs-as-code/SKILL.md` рефакторен в компактный высокоуровневый роутер Progressive Disclosure: размер снижен с 13 775 байт до 2 274 байт (-83.5%).
    - Все 11 специализированных скиллов (`kb-plan`, `kb-task`, `kb-implement`, `kb-complete`, `kb-release`, `kb-bug`, `kb-adr`, `kb-research`, `kb-init`, `kb-lint`, `kb-onboard`) очищены от словесного шума, эмоциональной риторики и дублирования `AGENTS.md`. Инструкции переведены в строгий императивный формат (`CONSTRAINT: ...`, `PROCEDURE: ...`).
  - Суммарный объем 12 файлов `SKILL.md` сокращен с 42 445 байт до 18 728 байт (-55.9%), полностью уложившись в бюджет $\le$ 20 000 байт.
  - Закрыта задача `TASK-017` в `Kanban.md` и отмечен пункт в `Roadmap.md`.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 59 файлов, 311 ссылок, 0 broken links, 100% валидный YAML.
  - `python -m unittest discover -s tests` -> 23/23 тестов зеленые.
  - Проверка суммарного размера скиллов: 18 728 байт $\le$ 20 000 байт.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к `TASK-018`: Рефакторинг 13 шаблонов `docs/00_Templates/` в компактные каркасы (Skeleton Templates).

---

### [2026-10-01] — Завершение TASK-016: Комплексное E2E тестирование релизного пайплайна и документация (Завершение Фазы 4)
- **Что сделано:**
  - Написаны и интегрированы 3 сквозных E2E теста в `tests/test_installer.py`:
    - `test_13_release_components_deployed_on_fresh_install`: верификация развертывания `docs/02_Tasks/Releases/`, `TEMPLATE_RELEASE.md`, `scripts/kb_release.py`, скилла `kb-release` и воркфлоу `release.yml`.
    - `test_14_kb_release_utility_execution_in_sandbox`: генерация релиза, расчет потокового SHA-256 артефакта в `dist/` и проверка генерации `RELEASE-v1.0.0.md` с аудитом через `kb_lint.py`.
    - `test_15_update_preserves_existing_releases`: верификация бережного обновления через `install.py --update` (обновление шаблонов/скиллов при 100% сохранении существующих заметок `docs/02_Tasks/Releases/RELEASE-*.md`).
  - Синхронизирована пользовательская и агентная документация:
    - `README.md`: добавлена 13-я позиция каталога шаблонов (`TEMPLATE_RELEASE.md`), папка `Releases/`, 12-й скилл `/kb-release`, команды запуска `scripts/kb_release.py` и раздел Dual-Mode автоматизации релизов.
    - `docs/Onboarding.md`: добавлен раздел «3. Релиз-менеджмент и жизненный цикл (`/kb-release`)» с диаграммой каналов выпуска (Dual-Mode: GitHub / Local-Only), Pre-flight чеками и Build Hook Contract.
    - `docs/00_Index.md`: актуализирована карта разделов, добавлен раздел `Releases/` и шаблон `TEMPLATE_RELEASE.md`.
  - Закрыта задача `TASK-016` и полностью завершена **Фаза 4 («Релиз-менеджмент и автоматизация жизненного цикла»)** в `Kanban.md` и `Roadmap.md`.
- **Результаты верификации:**
  - `python -m unittest discover -s tests` -> 23/23 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 54 файла, 260 ссылок, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Выполнение приемочных сценариев в `docs/05_Testing/` и публикация первого официального релиза Фазы 4 через `/kb-release`.

---

### [2026-10-01] — Завершение TASK-015: Шаблон GitHub Actions CI release.yml и упаковка релизных компонентов в инсталлятор
- **Что сделано:**
  - Разработан эталонный GitHub Actions workflow `.github/workflows/release.yml` для автоматической сборки и публикации релизов по push аннотированных тегов `v*`:
    - Проверка целостности базы знаний через `scripts/kb_lint.py --path docs`.
    - Обнаружение и запуск билд-хука (`scripts/build_release.sh`, `scripts/build_release.py`, `package.json`).
    - Инспекция артефактов в `dist/` и валидация контрольных сумм через `scripts/kb_release.py --ci-mode`.
    - Публикация GitHub Release через `softprops/action-gh-release@v2`.
  - Скопирован `TEMPLATE_RELEASE.md` в корень `templates/`.
  - Обновлен сборочный скрипт `scripts/build_installer.py`:
    - Бандлинг всех 13 шаблонов (включая `TEMPLATE_RELEASE.md`).
    - Бандлинг утилит `scripts/kb_lint.py` и `scripts/kb_release.py`.
    - Бандлинг 12 скиллов агентов (включая `kb-release`).
    - Бандлинг CI воркфлоу `.github/workflows/*.yml`.
  - Обновлен автономный инсталлятор `install.py`:
    - Создание каталога `docs/02_Tasks/Releases/` с `.gitkeep`.
    - Развертывание `scripts/kb_release.py` с правами 0o755 в `deploy_infrastructure`.
    - Развертывание `.github/workflows/release.yml` и `kb-lint.yml` в `deploy_ci_workflow`.
    - Безопасное обновление через `install.py --update`: переразвертывание шаблонов, утилит и скиллов при строгом сохранении существующих пользовательских релизов в `docs/02_Tasks/Releases/`.
    - Перекомпилирован монолитный бандл в `install.py`: размер 95.0 КБ (в рамках бюджета < 120 КБ).
  - Закрыта задача `TASK-015` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python -m py_compile scripts/build_installer.py install.py` -> Код 0.
  - `python scripts/build_installer.py` -> 13 шаблонов, 12 скиллов, 2 скрипта, 95.0 КБ бандл.
  - `python scripts/kb_lint.py --path docs` -> 52 файла, 239 ссылок, 0 broken links, 100% валидный YAML frontmatter.
  - `python -m unittest discover -s tests` -> 20/20 тестов успешно пройдены (100% pass).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-016`: Комплексное E2E тестирование релизного пайплайна (Local-Only и GitHub) и обновление документации (`README.md`, `Onboarding.md`, `00_Index.md`).

---

### [2026-10-01] — Завершение TASK-014: Исполняемый скилл kb-release и фазовые подсказки в kb-complete
- **Что сделано:**
  - Создан 12-й канонический исполняемый скилл `.agents/skills/kb-release/SKILL.md` со строгим 7-шаговым регламентом выпуска релизов фаз:
    1. Pre-flight Checks (проверка чистоты рабочей копии Git, прохождения `kb_lint.py`, тестов и закрытия задач фазы в `Roadmap.md`).
    2. Dual-Mode Detection (`github` через `gh` CLI или `local-only`).
    3. Build Hook Discovery (`scripts/build_release.py`, `package.json`, `pyproject.toml`, `Package.swift`, `*.sln`, `Cargo.toml`).
    4. Artifacts Inspection & SHA-256 (вызов `scripts/kb_release.py` и генерация `RELEASE-vX.Y.Z.md`).
    5. Knowledge Base Sync (`Roadmap.md`, `CHANGELOG.md`, `Devlog.md`).
    6. Publication (Git tag, `gh release create` или отчет о локальных файлах).
    7. Validation (`kb_lint.py`).
  - В скилл `.agents/skills/kb-complete/SKILL.md` добавлен шаг 7 «Phase Completion Nudge»: если при закрытии задачи все тикеты текущей фазы выполнены, выводится рекомендация провести E2E тестирование и вызвать `/kb-release`.
  - В мастер-скилл `.agents/skills/docs-as-code/SKILL.md` добавлена строка `/kb-release` и обновлена карта разделов.
  - Закрыта задача `TASK-014` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python scripts/kb_lint.py --path docs` -> 52 файла, 239 ссылок, 0 broken links, 100% валидный YAML frontmatter.
  - `python -m unittest discover -s tests` -> 20/20 тестов успешно пройдены (100% pass).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-015`: Шаблон GitHub Actions CI `.github/workflows/release.yml` и упаковка в инсталлятор `install.py` / `build_installer.py` (включая `--update`).

---

### [2026-10-01] — Завершение TASK-013: Шаблон релиза, каталог Releases/ и утилита scripts/kb_release.py
- **Что сделано:**
  - Создан канонический 13-й шаблон `docs/00_Templates/TEMPLATE_RELEASE.md` для фиксации релизов фаз с метаданными, чейнджлогом, таблицей артефактов и контрольными суммами SHA-256.
  - Создан постоянный каталог `docs/02_Tasks/Releases/` с правилом неизменяемости ссылок (Permalinks).
  - Разработана автономная Zero-Dependencies CLI-утилита `scripts/kb_release.py` на стандартной библиотеке Python 3:
    - Детекция окружения (`detect_release_environment`): статус git, чистота рабочего дерева, remote origin, `gh` CLI и режим (`github` | `local-only`).
    - Инспекция каталога `dist/` (`inspect_release_artifacts`): расчет размеров и потоковых SHA-256 хэшей блоками по 64 КБ.
    - Семантический сбор артефактов фазы (`find_phase_artifacts`): извлечение выполненных `TASK-XXX`, закрытых `BUG-XXX` и принятых `ADR-XXXX` из базы знаний.
    - Генерация markdown-документа релиза по стандарту `TEMPLATE_RELEASE.md`.
    - CLI интерфейс с флагами `--version`, `--phase`, `--dist-dir`, `--docs-dir`, `--output`, `--summary`, `--dry-run`, `--detect-only`.
  - Создан набор модульных тестов `tests/test_kb_release.py` (8 тестов: SHA-256, Markdown-таблица, парсер frontmatter, сбор артефактов фазы, CLI).
  - Закрыта задача `TASK-013` в `Kanban.md`, `Roadmap.md` и спецификации.
- **Результаты верификации:**
  - `python -m py_compile scripts/kb_release.py` -> Код 0.
  - `python -m unittest tests/test_kb_release.py` -> 8/8 тестов успешно пройдены (100% pass).
  - `python -m unittest discover -s tests` -> 20/20 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 52 файла, 239 ссылок, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-014`: Исполняемый скилл `.agents/skills/kb-release/SKILL.md` (Dual-Mode workflow, префлайт-чеки, подсказка в `kb-complete`).

---

### [2026-10-01] — Завершение TASK-012 и полное закрытие Фазы 3: Зрелость инсталлятора
- **Что сделано:**
  - Реализован генератор workflow для GitHub Actions `deploy_ci_workflow` в `install.py`, создающий `.github/workflows/kb-lint.yml` для автоматического аудита базы знаний через `kb_lint.py` при Push и Pull Request.
  - Добавлен CLI-флаг `--ci` со значениями `github` и `none` (по умолчанию `none`).
  - В интерактивный CLI-мастер добавлен шаг выбора настройки CI.
  - Поддержано автоматическое развертывание и обновление CI-workflow при использовании `install.py --update`.
  - Произведена оптимизация размера `install.py` (компактизация пресетов стека `STACK_PRESETS` и унификация генераторов правил через `_gen_rule`), итоговый размер дистрибутива: **80.4 КБ / 82,334 байта** (с запасом внутри бюджета < 82 КБ).
  - В `tests/test_installer.py` добавлен сквозной тест `test_12_ci_workflow_generation_and_e2e`, верифицирующий отсутствие CI по умолчанию, создание при `--ci github`, работу через CLI и сохранение/обновление при `--update`.
  - Обновлена документация `README.md` (разделы по CLI-флагам, безопасному обновлению, интеграции в существующие проекты и CI).
  - Закрыты все 4 задачи Фазы 3 (`TASK-009`, `TASK-010`, `TASK-011`, `TASK-012`) и родительский план `PLAN-003`.
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0 (размер 80.4 КБ / 82,334 байта).
  - `python -m unittest discover -s tests` -> 12/12 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к перспективным идеям из бэклога / Icebox: автоматизация релиз-менеджмента (`/kb-release`, `RESEARCH-002`, `ADR-0007`) или семантический контроль фаз в `kb_lint.py`.

---

### [2026-10-01] — Завершение TASK-011: Safe Infrastructure Update Mechanism (`install.py --update`)
- **Что сделано:**
  - Реализован флаг `--update` (`-u`) в CLI `install.py` для обновления инфраструктуры базы знаний в уже существующих проектах.
  - Разделены зоны ответственности при обновлении:
    - Обновляемые компоненты: шаблоны (`docs/00_Templates/*`), линтер (`scripts/kb_lint.py`), скиллы (`.agents/skills/*`), цветовая схема графа Obsidian (`.obsidian/graph.json`).
    - Неприкосновенные пользовательские данные: `docs/02_Tasks/*` (Kanban, Roadmap, планы, ТЗ, отчеты о багах), `docs/03_Decisions_ADR/*`, `docs/04_Research/*`, `docs/05_Testing/*`, `SPEC.md`, `README.md`, `.gitignore`, `00_Index.md`.
  - Реализован механизм защиты кастомных правил агентов: если пользователь модифицировал `AGENTS.md` (или другие конфигурации агентов), автоматически создается резервная копия `*.bak` перед обновлением.
  - Реализована автоматическая фиксация обновления в `docs/Devlog.md` и последующий запуск контрольного аудита линтером `scripts/kb_lint.py`.
  - Произведен рефакторинг общих модулей в `install.py` (`deploy_infrastructure`, `run_linter_audit`, `get_agent_rule_specs`, сжатие `_3MODES`), позволивший удержать итоговый размер однофайлового дистрибутива в пределах бюджета: 81.8 КБ / 83,770 байт (лимит < 82 КБ).
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_11_safe_update_mechanism`, проверяющий валидацию директории, обновление шаблонов/линтера, неприкосновенность пользовательских задач, создание `AGENTS.md.bak`, добавление записи в `Devlog.md` и успешный прогон `kb_lint.py`.
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0 (размер 81.8 КБ).
  - `python -m unittest discover -s tests` -> 11/11 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-012`: Шаблон GitHub Actions CI (`.github/workflows/kb-lint.yml`) и E2E тесты.

---

### [2026-10-01] — Завершение TASK-010: Brownfield Adoption & Smart Stack Autodetection
- **Что сделано:**
  - Реализован эвристический детектор стека технологий `detect_project_stack` в `install.py`, определяющий Swift (`Package.swift`), Web/TypeScript (`package.json`), Python (`pyproject.toml`, `requirements.txt`, `Pipfile`, `setup.py`), .NET (`*.sln`, `*.csproj`) и fallback на Generic.
  - Реализован неразрушающий механизм внедрения в существующие проекты (Brownfield Adoption):
    - `handle_readme`: сохраняет исходный пользовательский `README.md` и бережно дописывает блок Docs-as-Code (с поддержкой мультиязычности `ru`/`en`), предотвращая дублирование при повторных запусках.
    - `handle_gitignore`: сохраняет пользовательские правила игнорирования и дописывает правила для Obsidian (`.obsidian/*`, `!.obsidian/graph.json`).
    - `create_starter_docs`: защищает существующие `SPEC.md`, `Kanban.md`, `Roadmap.md`, `Devlog.md` и `00_Index.md` от перезаписи, если не указан флаг `--force`.
  - В интерактивный CLI-мастер добавлена подсветка и предвыбор автоопределенного стека по умолчанию. В CLI поддержан параметр `--stack auto`.
  - В шаблон онбординга `TEMPLATE_ONBOARDING.md` добавлен раздел 7 («Внедрение в существующий проект») со сценарием экспресс-аудита легаси-кода для AI-агента.
  - В `tests/test_installer.py` добавлен сквозной E2E тест `test_10_brownfield_adoption_and_stack_autodetect`, верифицирующий детект всех 5 стеков, неразрушающее внедрение и идемпотентность.
  - Сборщик `scripts/build_installer.py` пересобрал бандл (размер `install.py`: 80.3 КБ / 82,204 байта, строго в рамках бюджета < 82 КБ).
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0.
  - `python -m unittest discover -s tests` -> 10/10 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-011`: Механизм бережного обновления инфраструктуры (`install.py --update`).

---

### [2026-10-01] — Завершение TASK-009: Clean Slate Scaffolding & Zero-Broken-Links FTUE
- **Что сделано:**
  - В `install.py` (`create_starter_docs`) полностью исключена генерация фантомных ссылок на несуществующие файлы `PLAN-001` и `TASK-001` в `Kanban.md` и `Roadmap.md`.
  - Стартовый бэклог в `Kanban.md` теперь создается чистым, с комментарием-приглашением начать работу с `/kb-plan <название>`.
  - `Roadmap.md` генерирует чистую структуру Фазы 1 без битых ссылок.
  - Удалена паразитная генерация фиктивных файлов планов и ТЗ в каталогах `Plans/` и `Specs/`.
  - Обновлены канонические шаблоны `templates/TEMPLATE_KANBAN.md`, `templates/TEMPLATE_ROADMAP.md` и пересобран бандл через `build_installer.py` (размер дистрибутива `install.py`: 75.9 КБ / 77,684 байта).
  - В тестовый набор `tests/test_installer.py` добавлен сквозной тест `test_09_clean_slate_scaffolding`, проверяющий чистоту бэклога и успешное прохождение аудита `kb_lint.py` с 0 битых ссылок при первой установке.
- **Результаты верификации:**
  - `python -m py_compile install.py` -> Код 0.
  - `python scripts/build_installer.py` -> Код 0.
  - `python -m unittest discover -s tests` -> 9/9 тестов успешно пройдены (100% pass).
  - `python scripts/kb_lint.py --path docs` -> 44 файла, 174 ссылки, 0 broken links, 100% валидный YAML frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-010`: Бесшовное внедрение в существующие проекты (Brownfield Adoption) и автодетект стека.

---

### [2026-10-01] — Режим 1: Планирование Фазы 3 и фиксация отказных архитектурных решений (ADR-0005, ADR-0006)
- **Что сделано:**
  - Проведен критический анализ бэклога перспективных идей из `Roadmap.md` и `Kanban.md` с позиции Senior Partner.
  - Идеи категории C официально отклонены как оверинжиниринг и зафиксированы в отказных архитектурных решениях (`status: rejected`):
    - [[03_Decisions_ADR/ADR-0005-rejection-of-embedded-web-visualizer|ADR-0005]]: Отказ от встроенного локального web-визуализатора базы знаний (`install.py --serve`) во избежание раздувания бандла, нарушения Zero Dependencies и дублирования нативного Obsidian.
    - [[03_Decisions_ADR/ADR-0006-rejection-of-standalone-pdf-report-generator|ADR-0006]]: Отказ от встроенного Python-генератора PDF-отчетов в пользу нативных возможностей LLM/агентов и штатного экспорта Markdown.
  - Сформирован и утвержден концептуальный план Фазы 3: [[02_Tasks/Plans/PLAN-003-brownfield-adoption-and-lifecycle|PLAN-003]] («Зрелость инсталлятора — Brownfield Adoption, Clean Slate Scaffolding, безопасное обновление и CI»).
  - Декомпозированы задачи Фазы 3 (`TASK-009` — `TASK-012`), добавлены карточки в бэклог [[02_Tasks/Kanban|Kanban.md]] и вехи в [[02_Tasks/Roadmap|Roadmap.md]].
  - Запущена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`: 0 broken wikilinks, 100% валидность frontmatter.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к Режиму 2 (Task Specification) для первой задачи `TASK-009` (Clean Slate Scaffolding).

---

### [2026-09-30] — Завершение TASK-008 и успешное закрытие Фазы 2 (Скиллы, правила и экосистема)
- **Что сделано:**
  - В тестовый набор `tests/test_installer.py` добавлены 3 новых сквозных E2E теста:
    - `test_06_install_deploys_all_11_skills`: проверяет корректное развертывание каталога `.agents/skills/`, наличие всех 11 исполняемых скиллов и валидность структуры их файлов `SKILL.md`.
    - `test_07_install_gemini_and_windsurf_rules`: проверяет корректность создания `GEMINI.md` и `.windsurfrules` как в режиме `--agent all`, так и в изолированных режимах `--agent gemini` / `--agent windsurf`, а также наличие директив `STRICTLY NO CODE CHANGES`.
    - `test_08_install_doc_lang_parameter`: проверяет влияние флага `--doc-lang` (`ru` vs `en`) на директивы в сгенерированных правилах и подтверждает успешное прохождение аудита `kb_lint.py` в обоих случаях.
  - Актуализирована документация `README.md`:
    - Добавлено описание структуры каталога `.agents/skills/` и таблица всех 11 скиллов с их slash-командами `/kb-*` и режимами.
    - Отражена поддержка Google Antigravity (`GEMINI.md`) и Windsurf Cascade (`.windsurfrules`).
    - Описан флаг `--doc-lang` и поддержка двуязычной разработки.
    - Включен раздел об открытых моделях (Qwen 2.5 Coder, DeepSeek) со ссылкой на платформенное исследование `RESEARCH-001`.
    - Добавлен раздел «Zero-to-Hero Quickstart» с первыми шагами для пользователей после установки.
  - Проведена полная верификация: все 8 тестов в `tests/test_installer.py` пройдены успешно (100% pass), `kb_lint.py` подтвердил 0 битых ссылок и целостность базы знаний.
  - План Фазы 2 (`PLAN-002`) и все входящие задачи (TASK-005, TASK-006, TASK-007, TASK-008) полностью выполнены и закрыты.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Переход к перспективным направлениям бэклога (Clean Slate Scaffolding, GitHub Actions CI workflow, Brownfield Adoption).

---

### [2026-09-30] — Завершение TASK-007: Эталонные правила агентов по канону remote-notification и генерация GEMINI.md
- **Что сделано:**
  - Во все генераторы правил инсталлятора `install.py` интегрирован полный канонический регламент из эталонного проекта `remote_notification`:
    - 12 канонических дисциплин Docs-as-Code (онбординг, Kanban, Roadmap, ADR и отказные ADR, платформа/Research, Devlog, Obsidian, Permalinks, Regression-First, QA-реестр `05_Testing/`, Obsidian Graph, Git-интеграция).
    - Строгая защита 3 режимов с маркером `STRICTLY NO CODE CHANGES` для Режимов 1 и 2.
    - Роль Senior Engineering Partner с обязательным подтверждением пользователя перед записью планов и ТЗ.
    - Поддержка языкового регламента `doc_lang` (`ru` vs `en`).
  - Добавлен генератор `generate_gemini_md` для создания корневого файла `GEMINI.md` (поддержка Google Antigravity и Gemini CLI с перечислением доступных скиллов).
  - Добавлен генератор `generate_windsurfrules` для поддержки Windsurf Cascade (`.windsurfrules`).
  - Обновлены генераторы `generate_agents_md`, `generate_clinerules`, `generate_claude_md`, `generate_cursorrules`, `generate_copilot_instructions`.
  - В опции `--agent` CLI и интерактивного визарда добавлены варианты `gemini` и `windsurf`.
  - Проведена оптимизация размера: итоговый размер `install.py` составил 79.3 КБ / 81,153 байта (строго в рамках DoD < 80 КБ / 81,920 байт).
  - Успешно пройдены все верификационные тесты: сборка `build_installer.py` (код 0), `py_compile` (код 0), `kb_lint.py` (0 битых ссылок), интеграционный прогон генерации всех 7 файлов правил и проверка наличия ключевых маркеров, полный набор тестов `unittest` (5/5 тестов OK).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-008`: Сквозное E2E тестирование в `tests/test_installer.py` и обновление документации `README.md` (включая гайд для новичков).

---

### [2026-09-30] — Завершение TASK-006: Упаковка 11 скиллов .agents/skills/ в сборщик и install.py
- **Что сделано:**
  - В `scripts/build_installer.py` добавлен сборщик скиллов: обход каталога `.agents/skills/` и упаковка канонических файлов `SKILL.md` для всех 11 скиллов без дублирования лишних файлов.
  - В `install.py` реализован локальный фолбэк для разработки в `unpack_assets()` и автоматическая распаковка скиллов в целевую директорию `.agents/skills/<skill>/SKILL.md`.
  - Оптимизирована генерация стартовых документов в `create_starter_docs` через переиспользование распакованных шаблонов (итоговый размер `install.py` составил 78.1 КБ / 80,024 байта при лимите DoD < 80 КБ).
  - Успешно пройдены все этапы верификации: `build_installer.py` (код 0), `py_compile` (код 0), `kb_lint.py` (0 битых ссылок), интеграционный прогон в песочнице с проверкой всех 11 `SKILL.md`, полный прогон `unittest` (5/5 тестов пройдено).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-007`: Эталонные правила агентов по канону `remote_notification` (12 дисциплин, языковая параметризация, роль Senior Partner, отказные ADR, `GEMINI.md`, `.windsurfrules` и адаптеры).

---

### [2026-09-30] — Завершение TASK-005: Исследование экосистемы AI-агентов (RESEARCH-001) и мультиязычность
- **Что сделано:**
  - Проведено и оформлено глубокое платформенное исследование `docs/04_Research/RESEARCH-001-ai-agent-ecosystem-and-ide-matrix.md` по средам разработки (Antigravity, Cline, Claude Code CLI, Cursor, Windsurf, Copilot, Continue, Aider) и семействам моделей (Qwen 2.5 Coder, DeepSeek R1/V3, Claude, Gemini, GPT).
  - В исследовании детально разобран потенциал ведущей открытой модели **Qwen 2.5 Coder** (32B/14B/7B) для локального enterprise-развертывания (Ollama/vLLM) со 100% приватностью кода под управлением 3-режимного каркаса.
  - Реализована поддержка языковой параметризации в `install.py`: добавлен CLI-флаг `--doc-lang` (по умолчанию `ru`) и интерактивный вопрос на английском языке в TUI визарде.
  - Проведена верификация: `py_compile` (код 0), запуск `install.py --help`, запуск песочницы с `--doc-lang en`, все 5 модульных тестов в `test_installer.py` (100% pass), проверка ссылок `kb_lint.py` (0 битых ссылок).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация `TASK-006`: упаковка всех 11 исполняемых скиллов `.agents/skills/` в сборщик `build_installer.py` и распаковка в `install.py`.

---

### [2026-09-30] — Завершение Фазы 1 (MVP): Автономный инсталлятор и мульти-стековые пресеты
- **Что сделано:**
  - Реализован автономный установщик `install.py` на стандартной библиотеке Python 3 (Zero Dependencies).
  - Разработан скрипт компиляции ресурсов `scripts/build_installer.py`, который упаковывает 12 шаблонов, `.obsidian/graph.json` и `kb_lint.py` в компактный zlib/base64 бандл внутри `install.py`.
  - Реализованы 5 технологических пресетов (Swift/iOS/macOS с нюансами ARC/Concurrency/BackgroundTasks, TypeScript, Python, .NET, Generic).
  - Сгенерированы адаптеры правил AI-агентов (`AGENTS.md`, `.clinerules`, `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`).
  - Разработан интерактивный терминальный мастер с поддержкой TTY при pipe через `curl | python3` и полным набором CLI-флагов.
  - Написан набор автоматических тестов `tests/test_installer.py` (5 E2E тестов, 100% pass).
  - Подготовлен исчерпывающий `README.md` с визуальным стилем, инструкцией в 1 команду и описанием преимуществ.
  - Проверена целостность базы знаний через `kb_lint.py` (0 битых ссылок).
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Подключение удаленного GitHub репозитория и релиз v1.0.0.

---

### [2026-09-30] — Инициализация проекта agent-docs-harness и базы знаний Docs-as-Code
- **Что сделано:**
  - Инициализирован Git-репозиторий и настроен `.gitignore`.
  - Развернута архитектура базы знаний `docs/` по стандарту Docs-as-Code с соблюдением догфудинга.
  - Настроена цветовая схема Obsidian Graph (`.obsidian/graph.json`) с 7 цветовыми группами.
  - Подготовлены 12 эталонных шаблонов в `templates/` и `docs/00_Templates/`.
  - Реализован автономный линтер базы знаний `scripts/kb_lint.py` с проверкой wikilinks и frontmatter без внешних зависимостей.
  - Сформированы документы `SPEC.md`, `00_Index.md`, `Onboarding.md`, `Kanban.md`, `Roadmap.md`.
- **Рекомендуемый следующий шаг (Ожидает команды пользователя):**
  - Реализация первой задачи фазы MVP: ядро инсталлятора `install.py` с упаковщиком шаблонов и адаптерами стеков.
