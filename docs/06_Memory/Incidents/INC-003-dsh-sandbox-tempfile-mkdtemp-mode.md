---
id: INC-003
title: "DSH Windows Sandbox: tempfile.mkdtemp mode 0o700 blocks child creation in tests"
status: active
type: incident
severity: high
tag: platform
root_cause: "os.mkdir 0o700 DACL under DSH sandbox denies child writes"
target_pattern: "TRG-03"
created: 2026-10-18
updated: 2026-10-18
tags:
  - memory
  - incident
---

# ⚠️ Инцидент: INC-003 — DSH Windows Sandbox: tempfile.mkdtemp mode 0o700 blocks child creation

> **Тег:** #memory #incident | **Тяжесть:** high | **Статус:** active  
> **Паттерн в базе:** `TRG-03` | **Задача:** `TASK-082`

---

## 1. Контекст и симптом
При запуске `py -3 -m unittest tests/test_kb_lint.py` под Windows-песочницей DSH все тесты падали в `setUp` с `PermissionError: [WinError 5] Access is denied` на `self.docs_dir.mkdir(...)` внутри каталога, созданного `tempfile.mkdtemp()`.

## 2. Корневая причина (Root Cause)
`tempfile.mkdtemp()` вызывает `os.mkdir(name, 0o700)`. Под Windows-песочницей DSH режим `0o700` приводит к DACL, запрещающей процессу создание дочерних каталогов/файлов (и даже `os.chmod`). `os.mkdir(name, 0o777)` работает нормально. На Linux/CI проблема не воспроизводится.

## 3. Защитное действие (Corrective Action)
Прогонять тестовые наборы через обёртку, патчащую `tempfile.mkdtemp` на `os.mkdir(name, 0o777)` (или иной permissive-режим), и перенаправлять временный каталог (`TMP`/`TEMP`) внутрь рабочей директории. Паттерн промотирован в `patterns.md` как `TRG-03`.
