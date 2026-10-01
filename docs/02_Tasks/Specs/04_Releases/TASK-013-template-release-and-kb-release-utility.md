---
id: TASK-013
title: "Канонический шаблон TEMPLATE_RELEASE.md, каталог docs/02_Tasks/Releases/ и утилита scripts/kb_release.py"
status: in-progress
type: task
phase: 4
component:
  - templates
  - release
  - tooling
  - cli
parent_plan: "[[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase4
  - component/templates
  - component/release
  - component/tooling
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-013 — Канонический шаблон TEMPLATE_RELEASE.md, каталог Releases/ и утилита scripts/kb_release.py

> **ID:** TASK-013  
> **Статус:** В работе (Режим 2)  
> **Теги:** #task/spec #phase4 #component/templates #component/release #component/tooling  
> **Родительский план:** [[../../Plans/PLAN-004-release-management-and-lifecycle-automation|PLAN-004]]  
> **Связанные ADR и исследования:** [[../../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]], [[../../../04_Research/RESEARCH-002-release-management-and-github-automation|RESEARCH-002]], [[../../../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Создать фундамент релиз-менеджмента в соответствии с [[../../../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007]]:
1. Разработать канонический шаблон `docs/00_Templates/TEMPLATE_RELEASE.md` для фиксации релизов фаз с поддержкой метаданных, чейнджлога и таблицы артефактов с SHA-256.
2. Создать директорию постоянного хранения релизов `docs/02_Tasks/Releases/` с правилом неизменяемости ссылок (Permalinks).
3. Разработать автономную Zero-Dependencies CLI-утилиту `scripts/kb_release.py` на стандартной библиотеке Python 3, реализующую:
   - Детекцию среды (GitHub vs Local-Only, проверка Git working tree, remote origin, наличие и авторизацию `gh` CLI).
   - Инспекцию каталога `dist/` и вычисление размеров и контрольных сумм SHA-256 блоками по 64 КБ.
   - Семантическую агрегацию артефактов фазы (`TASK-XXX`, `BUG-XXX`, `ADR-XXXX`) из базы знаний.
   - Генерацию форматированного markdown-документа релиза по шаблону.
4. Разработать unit-тесты `tests/test_kb_release.py` для тестирования функций утилиты.

---

## 2. Затрагиваемые файлы и компоненты

* `[NEW]` `docs/00_Templates/TEMPLATE_RELEASE.md` — канонический 13-й шаблон базы знаний Docs-as-Code.
* `[NEW]` `docs/02_Tasks/Releases/.gitkeep` — каталог для постоянного хранения релизных документов `RELEASE-vX.Y.Z.md`.
* `[NEW]` `scripts/kb_release.py` — автономный скрипт автоматизации релиза (Zero External Dependencies).
* `[NEW]` `tests/test_kb_release.py` — unit-тесты для функций `kb_release.py`.

---

## 3. Детали технической реализации

### 3.1. Структура `docs/00_Templates/TEMPLATE_RELEASE.md`

Шаблон релиза должен содержать стандартизированный YAML frontmatter и markdown-секторы:

```markdown
---
id: RELEASE-v[X.Y.Z]
title: "Релиз v[X.Y.Z]: [Название релиза / Фазы]"
version: "[X.Y.Z]"
phase: [N]
status: completed # completed | draft
date: YYYY-MM-DD
git_tag: "v[X.Y.Z]"
github_release_url: "" # Заполняется при публикации на GitHub
mode: "github" # github | local-only
artifacts:
  - name: "[artifact.ext]"
    path: "dist/[artifact.ext]"
    size: "[Размер]"
    sha256: "[SHA-256]"
tags:
  - release
  - changelog
  - v[X.Y.Z]
kanban: "[[../Kanban|Канбан-доска]]"
roadmap: "[[../Roadmap|Дорожная карта]]"
---

# 🚀 Релиз v[X.Y.Z]: [Название релиза / Фазы]

> **Версия:** v[X.Y.Z]  
> **Фаза:** [N]  
> **Дата:** YYYY-MM-DD  
> **Режим публикации:** [GitHub Release | Local-Only Package]  
> **Git Tag:** `v[X.Y.Z]`  
> **Дорожная карта:** [[../Roadmap|Дорожная карта]]  

---

## 📋 Обзор релиза (Executive Summary)
[Краткое резюме ключевой ценности и изменений, вошедших в данный выпуск]

---

## 🚀 Что нового (Release Notes)

### ✨ Новые возможности (Features)
- [[Specs/0N_Phase/TASK-XXX-slug|TASK-XXX]]: Краткое описание реализованной функциональности.

### 🐛 Исправленные дефекты (Bug Fixes)
- [[Bugs/BUG-XXX-slug|BUG-XXX]]: Описание устраненной проблемы и RCA.

### 🏛️ Архитектурные решения (ADR)
- [[../../03_Decisions_ADR/ADR-XXXX-slug|ADR-XXXX]]: Архитектурное новшество или стандарт.

---

## 📦 Релизные артефакты и контрольные суммы (SHA-256)

| Файл | Размер | Контрольная сумма (SHA-256) | Расположение |
| :--- | :--- | :--- | :--- |
| `example.zip` | 1.25 MB | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `dist/example.zip` |

---

## 🔍 Инструкция по проверке целостности артефакта

```bash
# Проверка в PowerShell (Windows)
Get-FileHash -Path dist/example.zip -Algorithm SHA256

# Проверка в Bash / macOS / Linux
sha256sum dist/example.zip
# или
shasum -a 256 dist/example.zip
```
```

---

### 3.2. Архитектура и сигнатуры `scripts/kb_release.py`

Скрипт разрабатывается без сторонних библиотек (только `sys`, `os`, `hashlib`, `subprocess`, `shutil`, `re`, `argparse`, `pathlib`).

```python
"""
scripts/kb_release.py — Zero-Dependencies Release Automation Utility for Docs-as-Code.
"""
from pathlib import Path
from typing import Dict, List, Any, Optional

def detect_release_environment(repo_root: Path) -> Dict[str, Any]:
    """
    Определяет возможности текущего окружения:
    - has_git: bool (наличие git и работа внутри репозитория)
    - is_clean: bool (отсутствие незакоммиченных изменений)
    - has_remote: bool (наличие remote origin)
    - remote_url: Optional[str]
    - is_github: bool (remote указывает на github.com)
    - has_gh_cli: bool (наличие утилиты gh)
    - gh_authenticated: bool (результат gh auth status == 0)
    - mode: "github" | "local-only"
    """
    pass

def inspect_release_artifacts(dist_dir: Path) -> List[Dict[str, str]]:
    """
    Сканирует dist_dir, игнорируя скрытые файлы.
    Для каждого файла вычисляет размер (KB/MB) и SHA-256 хеш чанками по 64 КБ.
    Возвращает список словарей: [{"name": str, "path": str, "size": str, "sha256": str}].
    """
    pass

def find_phase_artifacts(docs_dir: Path, phase_num: int) -> Dict[str, List[Dict[str, str]]]:
    """
    Сканирует базу знаний docs/ и собирает:
    - tasks: ТЗ фазы docs/02_Tasks/Specs/ со статусом done/completed или атрибутом phase: phase_num.
    - bugs: баг-репорты docs/02_Tasks/Bugs/ со статусом resolved/closed.
    - adrs: принятые ADR docs/03_Decisions_ADR/ со статусом accepted.
    Возвращает структурированные метаданные с permalinks.
    """
    pass

def generate_release_markdown(
    version: str,
    phase_num: int,
    env_info: Dict[str, Any],
    artifacts: List[Dict[str, str]],
    phase_data: Dict[str, List[Dict[str, str]]],
    summary: str = ""
) -> str:
    """
    Формирует готовое тело документа RELEASE-vX.Y.Z.md по стандарту TEMPLATE_RELEASE.md.
    """
    pass

def main() -> int:
    """
    CLI точка входа:
    Аргументы:
      --version <X.Y.Z> (обязательный)
      --phase <N> (обязательный)
      --docs-dir <path> (по умолчанию docs)
      --dist-dir <path> (по умолчанию dist)
      --output <path> (по умолчанию docs/02_Tasks/Releases/RELEASE-v{version}.md)
      --dry-run (вывод в stdout без записи на диск)
    """
    pass
```

---

## 4. План верификации (Verification Plan)

### Сборка и синтаксис:
- [ ] Проверка синтаксиса `scripts/kb_release.py`:
  ```bash
  python -m py_compile scripts/kb_release.py
  ```
  *(Ожидаемый код завершения: 0)*

### Автоматические тесты:
- [ ] Запуск специализированных unit-тестов:
  ```bash
  python -m unittest tests/test_kb_release.py
  ```
  *(Ожидаемый результат: все тесты зеленые, 100% pass)*
- [ ] Проверка хэширования SHA-256: сравнение программного расчета `inspect_release_artifacts` с эталонным `hashlib.sha256()`.
- [ ] Проверка детекции окружения: mock-тесты вызовов `git` и `gh`.

### Интеграционная проверка базы знаний:
- [ ] Запуск линтера Docs-as-Code:
  ```bash
  python scripts/kb_lint.py --path docs
  ```
  *(Ожидаемый результат: 0 broken wikilinks, валидный YAML frontmatter)*

---

## 5. Критерии готовности (Definition of Done)

- [ ] Создан файл `docs/00_Templates/TEMPLATE_RELEASE.md` со всеми полями метаданных и таблицей артефактов.
- [ ] Создан каталог `docs/02_Tasks/Releases/` с `.gitkeep`.
- [ ] Реализован скрипт `scripts/kb_release.py` без внешних зависимостей.
- [ ] Скрипт корректно формирует релизный документ с расчетом SHA-256 для файлов в `dist/`.
- [ ] Написаны и проходят тесты в `tests/test_kb_release.py`.
- [ ] Линтер `kb_lint.py` подтверждает 0 ошибок в базе знаний.
