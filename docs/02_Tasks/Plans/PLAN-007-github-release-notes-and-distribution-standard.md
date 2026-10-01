---
id: PLAN-007
title: "Фаза 7: Стандарт оформления публичных релизов на GitHub и экспорт Release Notes"
status: completed
type: plan
phase: 7
created: 2026-10-01
updated: 2026-10-01
tags:
  - plan
  - phase7
  - release
  - release-notes
  - github-releases
  - distribution
  - supply-chain-security
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 📋 План: PLAN-007 — Фаза 7: Стандарт оформления публичных релизов на GitHub и экспорт Release Notes

> **ID:** PLAN-007  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #plan #phase7 #release #release-notes #github-releases #distribution #supply-chain-security  
> **Родительская спецификация:** [[../../SPEC|SPEC.md]]  
> **Канбан:** [[../Kanban|Канбан-доска]]  
> **Связанные исследования и ADR:** [[../../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005: Лучшие практики оформления релизов на GitHub]], [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010: Стандарт оформления публичных релизов на GitHub]], [[../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007: Архитектура релиз-менеджмента]], [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]], [[../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009: High-SNR Token Architecture]]  

---

## 1. Контекст и цели (Problem & Goals)

### Проблема
В ходе публикации релиза `v0.5.0` на GitHub обнаружено, что:
1. Релиз на GitHub создался с прикрепленным файлом `install.py`, но с **пустым описанием** (Release Notes отсутствуют). Воркфлоу `.github/workflows/release.yml` не передавал параметр `body_path` или `body` в действие `softprops/action-gh-release@v2`.
2. Локальный документ `docs/02_Tasks/Releases/RELEASE-v0.5.0.md` содержит YAML frontmatter и относительные викиссылки Obsidian (`[[...]]`), которые в веб-интерфейсе GitHub отображаются как некрасивый серый код и сломанный некликабельный синтаксис.
3. Релиз без заметок и таблицы контрольных сумм SHA-256 порождает риски безопасности (Supply Chain Security), лишает подписчиков репозитория информации об изменениях и не содержит команд быстрой установки/обновления (`curl ... | python3`).

### Цель Фазы 7
Реализовать стандарт публичного релизного сопровождения согласно [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]] и [[../../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005]]:
1. Внедрить **двухформатный экспорт (Dual-Format Export)** в `scripts/kb_release.py`:
   - Внутренний сводный документ базы знаний: `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` (с YAML frontmatter и викиссылками).
   - Публичные релизные заметки: `dist/RELEASE_NOTES.md` (чистый GFM без frontmatter, кликабельные веб-ссылки репозитория, таблица SHA-256, сниппет верификации `Get-FileHash` и команды быстрой установки).
2. Разработать функцию очистки/преобразования синтаксиса `convert_wikilinks_to_github_markdown` без сторонних зависимостей (Python 3 stdlib).
3. Настроить передачу `body_path: dist/RELEASE_NOTES.md` в воркфлоу `.github/workflows/release.yml` и обновить встроенный шаблон в `install.py`.
4. Актуализировать скилл `.agents/skills/kb-release/SKILL.md` для автоматического использования `--notes-file dist/RELEASE_NOTES.md` при публикации через GitHub CLI (`gh`).
5. Провести пересборку инсталлятора через `scripts/build_installer.py`, покрыть функционал тестами в `tests/test_kb_release.py` и верифицировать отсутствие регрессий.

---

## 2. Обсуждение и ключевые решения (Q&A / Discussion)

* **Q1: Почему генерируются два файла (`RELEASE-vX.Y.Z.md` и `dist/RELEASE_NOTES.md`), а не один универсальный?**
  * **Решение (согласно [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]):** У них принципиально разные потребители. Файл в `docs/` оптимизирован для графа знаний Obsidian (требует frontmatter, wikilinks, чекбоксы DoD). Публичный файл в `dist/` оптимизирован для веб-интерфейса GitHub Releases и подписчиков (требует чистый Markdown, абсолютные ссылки на коммиты/файлы репозитория и команды запуска).
* **Q2: Как преобразовывать викиссылки без тяжелых внешних парсеров?**
  * **Решение (согласно [[../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]):** Используется регулярное выражение на стандартной библиотеке Python `re`. Ссылки вида `[[path/to/spec|TASK-017]]` трансформируются в `[TASK-017](https://github.com/<owner>/<repo>/blob/main/docs/path/to/spec.md)`. Если `remote_url` не определен (Local-Only режим), ссылки безопасно схлопываются в `**TASK-017**`.
* **Q3: Как исключить человеческий фактор при релизе через CLI?**
  * **Решение:** В скилле `kb-release` в шаге публикации GitHub CLI команда явно фиксируется как `gh release create vX.Y.Z dist/* --notes-file dist/RELEASE_NOTES.md`.

---

## 3. Архитектурное влияние и риски (Architectural Impact & Risks)

* **Затрагиваемые компоненты:**
  * `scripts/kb_release.py` — функции `convert_wikilinks_to_github_markdown`, `generate_public_release_notes`, флаги CLI (`--notes-output`, автогенерация в `dist/`).
  * `.github/workflows/release.yml` — добавление параметра `body_path: dist/RELEASE_NOTES.md`.
  * `.agents/skills/kb-release/SKILL.md` — обновление шагов 4 и 6 (генерация заметок и вызов `gh release create --notes-file`).
  * `install.py` и `scripts/build_installer.py` — обновление встроенного шаблона `release.yml`, пересборка бандла.
  * `tests/test_kb_release.py` — юнит-тесты на генерацию `dist/RELEASE_NOTES.md` и конвертацию ссылок.
* **Оценка рисков и соблюдение стандартов:**
  * Принцип Zero Dependencies строго соблюдается — все манипуляции со строками и ссылками выполняются силами stdlib.
  * Безопасность цепочки поставок (Supply Chain Security) усиливается благодаря обязательному присутствию хэшей SHA-256 прямо в теле публичного релиза.

---

## 4. Высокоуровневая декомпозиция (Task Breakdown)

- [x] **TASK-025:** Двухформатный экспорт и автоконвертер викиссылок в `scripts/kb_release.py`, модульные тесты в `tests/test_kb_release.py`.
- [x] **TASK-026:** Автоматизация передачи заметок в `.github/workflows/release.yml` (`body_path: dist/RELEASE_NOTES.md`) и синхронизация встроенного шаблона в `install.py`.
- [x] **TASK-027:** Актуализация скилла `.agents/skills/kb-release/SKILL.md` (флаг `--notes-file dist/RELEASE_NOTES.md` и Dual-Export шаги).
- [x] **TASK-028:** Сборка инсталлятора `build_installer.py`, регрессионные E2E тесты (`test_installer.py`, `test_kb_release.py`) и аудит `kb_lint.py`.

---

## 5. Критерии приемки плана (Definition of Done для Режима 1)

- [x] Концепция согласована с пользователем (Режим 1: READ-ONLY, без изменения кода).
- [x] Опирается на завершенное исследование [[../../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005]] и принятый стандарт [[../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]].
- [x] Создан файл плана `docs/02_Tasks/Plans/PLAN-007-github-release-notes-and-distribution-standard.md`.
- [x] Инициатива промоутирована из Icebox в Фазу 7 в `docs/02_Tasks/Roadmap.md`.
- [x] Задачи `TASK-025` — `TASK-028` добавлены в `docs/02_Tasks/Kanban.md` в колонку `📥 Бэклог`.
- [x] Пройдена проверка целостности базы знаний через `python scripts/kb_lint.py --path docs`.
