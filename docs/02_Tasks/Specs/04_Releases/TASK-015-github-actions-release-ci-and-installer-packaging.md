---
id: TASK-015
title: "Шаблон GitHub Actions CI release.yml и упаковка релизных компонентов в install.py"
status: planned
type: task
phase: 4
component:
  - ci
  - installer
  - packaging
  - update
parent_plan: "[[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase4
  - component/ci
  - component/installer
  - component/packaging
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-015 — Шаблон GitHub Actions CI release.yml и упаковка релизных компонентов в инсталлятор

> **ID:** TASK-015  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase4 #component/ci #component/installer #component/packaging  
> **Родительский план:** [[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]  
> **Связанные ADR:** [[../../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]], [[../../../03_Decisions_ADR/ADR-0002-self-contained-installer-bundling|ADR-0002]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

1. Разработать эталонный шаблон автоматической сборки и публикации релизов в GitHub Actions: `.github/workflows/release.yml`, активируемый при пуше аннотированных тегов `v*`.
2. Интегрировать новый шаблон релиза `TEMPLATE_RELEASE.md`, каталог `docs/02_Tasks/Releases/`, утилиту `scripts/kb_release.py` и скилл `kb-release` в монолитный инсталлятор `install.py` и сборочный скрипт `scripts/build_installer.py`.
3. Обеспечить бережное обновление инфраструктуры релиз-менеджмента через команду `python install.py --update`:
   - Обновление шаблона `TEMPLATE_RELEASE.md`, скрипта `scripts/kb_release.py` и скилла `.agents/skills/kb-release/`.
   - Строгий запрет на затирание или изменение существующих пользовательских релизов в `docs/02_Tasks/Releases/`.
4. Добавить в интерактивный CLI-мастер `install.py` и флаги командной строки поддержку настройки релизного CI-пайплайна (`--ci github`).

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `.github/workflows/release.yml` — эталонный CI workflow для публикации релизов на GitHub.
* `[MODIFY]` `scripts/build_installer.py` — упаковка новых компонентов в монолитный бандл:
  * Включение `TEMPLATE_RELEASE.md` в словарь встраиваемых шаблонов.
  * Включение `.agents/skills/kb-release/SKILL.md` в список скиллов.
  * Включение `scripts/kb_release.py` в состав генерируемых скриптов.
  * Включение шаблона `.github/workflows/release.yml`.
* `[MODIFY]` `install.py` — логика развертывания и обновления:
  * Создание каталога `docs/02_Tasks/Releases/`.
  * Развертывание `TEMPLATE_RELEASE.md`, `scripts/kb_release.py` и скилла `kb-release`.
  * Интеграция в метод безопасного обновления (`safe_update`).

---

## 3. Детали технической реализации

### 3.1. Эталонный GitHub Actions Workflow `.github/workflows/release.yml`

```yaml
name: Release Automation

on:
  push:
    tags:
      - 'v*'

permissions:
  contents: write

jobs:
  build-and-release:
    name: Build & Publish Release
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Verify Knowledge Base Integrity
        run: |
          python scripts/kb_lint.py --path docs

      - name: Execute Project Build Hook
        run: |
          if [ -f "scripts/build_release.sh" ]; then
            bash scripts/build_release.sh
          elif [ -f "scripts/build_release.py" ]; then
            python scripts/build_release.py
          elif [ -f "package.json" ]; then
            npm ci && npm run build
          fi

      - name: Inspect Artifacts & Verify Checksums
        id: release_meta
        run: |
          mkdir -p dist
          python scripts/kb_release.py --version ${{ github.ref_name }} --ci-mode

      - name: Publish GitHub Release
        uses: softprops/action-gh-release@v2
        if: startsWith(github.ref, 'refs/tags/')
        with:
          name: Release ${{ github.ref_name }}
          draft: false
          prerelease: false
          files: |
            dist/*
```

---

### 3.2. Обновление `scripts/build_installer.py`

В `build_installer.py`:
1. Ресурсная карта шаблонов расширяется шаблоном `TEMPLATE_RELEASE.md`.
2. Список встроенных скиллов расширяется директорией `kb-release`.
3. Скрипт `scripts/kb_release.py` упаковывается в код инсталлятора.
4. Контролируется размер генерируемого `install.py` (порог не более 120 КБ).

---

### 3.3. Обновление `install.py` (Clean Slate & `--update`)

1. **Новая установка:**
   - Создает `docs/02_Tasks/Releases/` с `.gitkeep`.
   - Записывает `TEMPLATE_RELEASE.md` в `docs/00_Templates/`.
   - Записывает `scripts/kb_release.py` в `scripts/`.
   - Записывает `.agents/skills/kb-release/SKILL.md`.
2. **Режим обновления (`install.py --update`):**
   - Перезаписывает `TEMPLATE_RELEASE.md`, `kb_release.py` и скилл `kb-release`.
   - **СТРОГО ПРОПУСКАЕТ** любые пользовательские файлы в `docs/02_Tasks/Releases/RELEASE-*.md`.

---

## 4. План верификации (Verification Plan)

### Сборка и синтаксис:
- [ ] Проверка синтаксиса `scripts/build_installer.py` и `install.py`:
  ```bash
  python -m py_compile scripts/build_installer.py install.py
  ```
  *(Exit code 0)*
- [ ] Пересборка монолитного инсталлятора:
  ```bash
  python scripts/build_installer.py
  ```
  *(Exit code 0, размер файла в пределах нормы)*

### Верификация целостности:
- [ ] Запуск `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (Definition of Done)

- [ ] Создан файл `.github/workflows/release.yml`.
- [ ] `build_installer.py` успешно упаковывает все релизные ресурсы.
- [ ] `install.py` генерирует каталог `docs/02_Tasks/Releases/` и разворачивает 12-й скилл.
- [ ] В режиме `--update` инфраструктура релиза обновляется без риска удаления существующих релизов.
- [ ] Сборщик инсталлятора работает без ошибок.
