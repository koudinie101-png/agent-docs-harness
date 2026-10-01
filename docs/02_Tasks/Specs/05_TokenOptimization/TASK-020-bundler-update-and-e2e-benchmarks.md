---
id: TASK-020
title: "Синхронизация сборщика scripts/build_installer.py, install.py (--update), E2E тесты и замеры сжатия"
status: done
type: task
phase: 5
component:
  - installer
  - bundler
  - lifecycle
  - e2e
  - benchmarks
parent_plan: "[[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase5
  - component/installer
  - component/bundler
  - component/lifecycle
  - component/e2e
  - component/benchmarks
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-020 — Синхронизация сборщика, install.py (--update) и E2E тесты

> **ID:** TASK-020  
> **Статус:** Выполнено (2026-10-01)  
> **Теги:** #task/spec #phase5 #component/installer #component/bundler #component/lifecycle #component/e2e #component/benchmarks  
> **Родительский план:** [[../../Plans/PLAN-005-high-snr-token-optimization|PLAN-005]]  
> **Связанные ADR и исследования:** [[../../../04_Research/RESEARCH-004-token-efficiency-and-context-compression|RESEARCH-004]], [[../../../03_Decisions_ADR/ADR-0009-high-snr-token-architecture-and-context-efficiency|ADR-0009]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]], [[../../../03_Decisions_ADR/ADR-0002-self-contained-installer-bundling|ADR-0002]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Завершить Фазу 5 интеграцией и сквозной верификацией High-SNR артефактов в дистрибутиве харнесса:
1. **Перепаковка монолитного инсталлятора `install.py`:**
   * Запустить сборочный скрипт `scripts/build_installer.py`, упаковывающий оптимизированные скиллы `.agents/skills/`, компактные шаблоны `docs/00_Templates/` и правила `AGENTS.md` в Base64/Gzip бандл `install.py`.
2. **Верификация механизма обновления (`install.py --update`):**
   * Убедиться, что режим `--update` штатно обновляет скиллы и шаблоны до компактных High-SNR версий в проектах ранних фаз без затирания пользовательских задач и логов.
3. **Регрессионные E2E тесты и бенчмаркинг в `tests/test_installer.py`:**
   * Расширить набор тестов проверками физического размера развернутых скиллов и шаблонов.
   * Добавить программный ассерт на максимальный объем статического корпуса:
     - Общий вес 12 скиллов $\le$ 20 000 байт (сокращение с 42.4 КБ).
     - Общий вес 13 шаблонов $\le$ 21 000 байт (сокращение с 38.8 КБ).
4. **Обновление документации:**
   * Отразить стандарт High-SNR и принципы контекстной токеномики в `README.md`, `docs/Onboarding.md` и `docs/00_Index.md`.
5. **Финальный аудит базы знаний:**
   * Прогон `python scripts/kb_lint.py --path docs` с подтверждением нулевого количества ошибок и сломанных ссылок.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `scripts/build_installer.py` — упаковка оптимизированных ресурсов в `install.py`.
* `[MODIFY]` `install.py` — сгенерированный автономный инсталлятор (сжатый бандл).
* `[MODIFY]` `tests/test_installer.py` — тесты развертывания, обновления и бенчмарки размера.
* `[MODIFY]` `README.md` — обновление описания возможностей (High-SNR Token Architecture).
* `[MODIFY]` `docs/Onboarding.md` — синхронизация с компактным форматом онбординга.
* `[MODIFY]` `docs/00_Index.md` — актуализация ссылок и архитектурных правил.

---

## 3. Детали технической реализации

### 3.1. Тесты бенчмарков в `tests/test_installer.py`

```python
def test_high_snr_static_corpus_benchmarks(self):
    """Проверяет, что суммарный объем скиллов и шаблонов укладывается в бюджет токенов ADR-0009."""
    skills_dir = os.path.join(self.temp_dir, ".agents", "skills")
    templates_dir = os.path.join(self.temp_dir, "docs", "00_Templates")
    
    total_skills_size = sum(
        os.path.getsize(os.path.join(root, f))
        for root, _, files in os.walk(skills_dir)
        for f in files if f.endswith(".md")
    )
    total_templates_size = sum(
        os.path.getsize(os.path.join(root, f))
        for root, _, files in os.walk(templates_dir)
        for f in files if f.endswith(".md")
    )
    
    self.assertLessEqual(total_skills_size, 20000, f"Skills size exceeded budget: {total_skills_size} bytes")
    self.assertLessEqual(total_templates_size, 21000, f"Templates size exceeded budget: {total_templates_size} bytes")
```

---

## 4. План верификации (Verification Plan)

### Сборка и тесты:
- [x] Пересборка инсталлятора: `python scripts/build_installer.py` (Exit code 0, размер 81.2 КБ).
- [x] Запуск полного набора unit и E2E тестов:
  ```powershell
  python -m unittest discover -s tests
  ```
  *Критерий:* 100% тестов пройдены успешно (30/30 тестов, Exit code 0).
- [x] Проверка чистого развертывания в изолированной директории:
  ```powershell
  python install.py --target-dir ./test_sandbox --non-interactive --stack python --force
  ```
  *Критерий:* песочница создана, все скиллы и шаблоны компактные, тесты внутри песочницы проходят.
- [x] Проверка линтера: `python scripts/kb_lint.py --path docs` (0 broken links, Exit code 0).

---

## 5. Критерии готовности (Definition of Done)

- [x] Инсталлятор `install.py` пересобран с обновленными бандлами ресурсов.
- [x] Механизм `install.py --update` подтвержден тестами.
- [x] Бенчмарки подтверждают сокращение объема скиллов ($\le$ 20 КБ) и шаблонов ($\le$ 21 КБ).
- [x] Документация (`README.md`, `docs/Onboarding.md`, `docs/00_Index.md`) актуализирована.
- [x] Все тесты `tests/` проходят успешно.
