---
id: FB-GH-1
title: "Хардкод установки harness-а (`install.py`) в публичных релизных записках `scripts/kb_release.py`"
status: processed
type: feedback
channel: github
perceived_severity: s2
target: "[[../Bugs/BUG-002-release-notes-hardcoded-install-script]]"
created: 2026-10-03
updated: 2026-10-12
author: "koudinie101-png"
source_ref: "https://github.com/koudinie101-png/agent-docs-harness/issues/1"
tags:
  - feedback
  - inbox
---

# 📥 Обращение: FB-GH-1 — Хардкод установки harness-а (`install.py`) в публичных релизных записках `scripts/kb_release.py`

> **Источник:** Github (https://github.com/koudinie101-png/agent-docs-harness/issues/1) | **Статус:** processed  
> **Целевой артефакт:** [[../Bugs/BUG-002-release-notes-hardcoded-install-script|BUG-002]]  

---

## 1. Исходное сообщение
### Bug Report: Хардкод установки harness-а (`install.py`) в публичных релизных записках `scripts/kb_release.py`

**Проблема:**
В генераторе публичных релизных заметок (`scripts/kb_release.py`) в секцию `Quick Install` жестко зашит вызов `install.py` самого фреймворка `Docs-as-Code`:

```python
# scripts/kb_release.py, строки 754-762:
### ⚡ Быстрый старт / Обновление (Quick Install)
```bash
# Новая установка Docs-as-Code
curl -fsSL {raw_install_url} | python3

# Обновление существующего проекта
python install.py --update
```

**Почему это баг:**
1. **Leaky Abstraction:** В целевых проектах, использующих Docs-as-Code как шаблон документации (C#, Go, Rust, Kotlin, Web и т.д.), в корне репозитория нет файла `install.py`.
2. **Битые ссылки:** Пользователи проекта видят в GitHub Release команду `curl .../{repo}/main/install.py`, которая завершается с `HTTP 404 Not Found`.
3. **Неуместный контент:** Для сторонних приложений (десктоп, мобильные клиенты, библиотеки) призыв «Новая установка Docs-as-Code» вводит конечных пользователей в заблуждение.
4. **Неиспользуемый код:** На строке 742 объявлена переменная `first_art_name = artifacts[0]["name"] if artifacts else "install.py"`, которая нигде в шаблоне не используется.

**Предлагаемые решения:**
1. **Вариант А (Конфигурируемый):** Добавить в параметры генератора/конфиг поле `quick_install` (или флаг `--install-instructions`), а при его отсутствии генерировать нейтральный блок скачивания артефактов из таблицы `artifacts_table`.
2. **Вариант Б (Адаптивный):** Если артефакты присутствуют в `dist/` (например, `.apk`, `.exe`, `.zip`, `.whl`), предлагать их скачивание со ссылками на `releases/download/{tag}/{artifact}`, а блок установки Docs-as-Code отображать только если сам репозиторий является репозиторием `agent-docs-harness`.

## 2. Анализ и предварительный скрининг
- **Тип:** Дефект (Defect, S2/Medium).
- **Контекст:** Нарушение принципа изоляции harness-а от целевого репозитория; битая ссылка 404 при публикации релизов в сторонних проектах.

## 3. Решение по триажу
Конвертировано в баг-репорт [[../Bugs/BUG-002-release-notes-hardcoded-install-script|BUG-002]]. Реализация исправления через TDD-цикл.
