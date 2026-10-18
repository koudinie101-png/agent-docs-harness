---
id: BUG-011
title: "Rules Check: test_05_git_local_setup зависит от глобальной Git identity (exit 128 на чистом runner)"
status: open
severity: high
type: bug
target_release: "v0.23.0"
target_phase: 22
release_blocker: true
fixed_in: null
regression_test: "tests/test_installer.py::test_05_git_local_setup"
created: 2026-10-18
updated: 2026-10-18
tags:
  - bug
  - defect
  - ci
  - tests
  - quality-gates
  - phase22
parent_spec: "[[../../SPEC|SPEC.md]]"
kanban: "[[../Kanban|Канбан-доска]]"
---

# 🐞 Дефект: BUG-011 — Rules Check: `test_05_git_local_setup` зависит от глобальной Git identity

> **ID:** BUG-011 | **Критичность:** High | **Статус:** open  
> **Релиз:** v0.23.0 | **Блокер:** Да  
> **Канбан:** [[../Kanban|Канбан-доска]] | **Спецификация:** [[../../SPEC|SPEC.md]]  

---

## 1. Симптомы и окружение
* **Симптом:** Job `Rules Corpus Guard` падает на шаге `Unit tests` с `AssertionError: 128 != 0` в `test_05_git_local_setup`. На машине разработчика тот же тест проходит.
* **Окружение:** GitHub Actions `ubuntu-latest`, Python 3.11, git 2.x. Чистый runner без `~/.gitconfig` и без `user.name`/`user.email`; локально глобальная identity настроена, поэтому дефект невидим.
* **Масштаб:** красный `main` на четырёх пушах подряд — `a3e8956`, `e19cce5`, `2788d7f`, `223e737` (прогоны [39109860347](https://github.com/koudinie101-png/agent-docs-harness/actions/runs/39109860347), [39110362897](https://github.com/koudinie101-png/agent-docs-harness/actions/runs/39110362897), [39111822882](https://github.com/koudinie101-png/agent-docs-harness/actions/runs/39111822882), [39112082267](https://github.com/koudinie101-png/agent-docs-harness/actions/runs/39112082267)).

## 2. Шаги воспроизведения (Repro Steps)
1. Взять окружение без глобальной Git identity (GitHub runner; локально — пустые `GIT_CONFIG_GLOBAL` и `GIT_CONFIG_SYSTEM`).
2. Выполнить `python -m unittest tests.test_installer.TestAgentDocsHarness.test_05_git_local_setup`.
3. Установщик создаёт `.git` и `.git/HEAD`, но `git commit` завершается с кодом 128 («Author identity unknown»); последующий `git log` тоже возвращает 128, и проверка `self.assertEqual(res.returncode, 0)` падает.

**Ожидаемое:** тест детерминированно проверяет генерацию initial commit независимо от глобального `git config` машины.
**Фактическое:** результат теста зависит от ambient-окружения; на чистом runner'е гейт всегда красный.

## 3. Диагностика (Логи, Стек-трейс)
```text
FAIL: test_05_git_local_setup (test_installer.TestAgentDocsHarness.test_05_git_local_setup)
AssertionError: 128 != 0
  File ".../tests/test_installer.py", line 220, in test_05_git_local_setup
    self.assertEqual(res.returncode, 0)

# Воспроизведено локально с пустым GIT_CONFIG_GLOBAL:
Author identity unknown
*** Please tell me who you are.
Run
  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
[exit 128]
```

## 4. Первопричина (Root Cause Analysis — RCA)
1. `setup_git()` намеренно деградирует при отсутствии identity: `git commit` вызывается без `-c user.name/user.email`, ошибка перехватывается, печатается подсказка, установка продолжается (`install.py`, строки 1001–1008).
2. Тест `test_05_git_local_setup` безусловно требует успешный `git log` (`tests/test_installer.py:220`), то есть кодирует предположение о наличии глобальной identity, не создавая её сам.
3. GitHub runner не имеет identity → коммита нет → `git log` возвращает 128. На dev-машине глобальный конфиг маскирует дефект.
4. **Системная причина:** тест не изолирован от окружения (`HOME`, `GIT_CONFIG_GLOBAL`, `GIT_CONFIG_SYSTEM`) и не имеет hermetic-профиля. Tier 1-гейт (`rules-check.yml`) зависит от конфигурации машины, поэтому невоспроизводим и непригоден как барьер.

## 5. План исправления
* `[MODIFY]` `tests/test_installer.py` — обернуть установку в `test_05_git_local_setup` в контекст с детерминированной identity (`GIT_AUTHOR_NAME/EMAIL`, `GIT_COMMITTER_NAME/EMAIL`) и изолированным конфигом (`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` → пустые файлы во временном каталоге, `GIT_CONFIG_NOSYSTEM=1`); `git log` проверять в том же окружении.
* `[NEW]` `tests/test_installer.py::test_05b_git_setup_without_identity_is_graceful` — зафиксировать продуктовый контракт деградации: без identity установка не падает, `.git/HEAD` создаётся, коммита нет, установщик печатает подсказку про identity.
* **Отклонено:** `git config --global user.name/user.email` в workflow — маскирует негерметичность; тест продолжит падать в Docker, форках и на чистых машинах.

## 6. Верификация (Regression-First)
- [ ] RED: `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM` указывают на пустые файлы, identity отсутствует → `test_05` падает с `128 != 0` (воспроизведено 2026-10-18).
- [ ] GREEN: после фикса тот же запуск проходит; тест зелёный и с настроенной, и с пустой глобальной identity.
- [ ] `test_05b` подтверждает graceful-деградацию без synthetic-коммита.
- [ ] `python -m unittest discover -s tests` и `python scripts/kb_lint.py --path docs` — 0 ошибок.
- [ ] Прогон `Rules Check` на GitHub Actions зелёный.

## 7. Влияние и принятые решения
* Красный гейт блокирует мёрж/релизные проверки и создаёт ложное впечатление сломанного продукта; сам установщик при этом ведёт себя корректно.
* **Продуктовое решение (по умолчанию):** не коммитить от синтетического имени. Identity — ответственность пользователя, установщик обязан явно предупреждать. Тест обязан моделировать это явно, а не наследовать конфиг машины.
