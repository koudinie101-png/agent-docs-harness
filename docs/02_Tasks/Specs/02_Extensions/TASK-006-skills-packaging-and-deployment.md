---
id: TASK-006
title: "Упаковка 11 скиллов .agents/skills/ в сборщик build_installer.py и install.py"
status: done
type: task
phase: 2
component:
  - build
  - installer
  - skills
parent_plan: "[[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]"
created: 2026-09-30
updated: 2026-09-30
tags:
  - task/spec
  - phase2
  - component/build
  - component/installer
  - component/skills
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-006 — Упаковка 11 скиллов .agents/skills/ в сборщик build_installer.py и install.py

> **ID:** TASK-006  
> **Статус:** Выполнено (Режим 3)  
> **Теги:** #task/spec #component/build #component/installer #component/skills  
> **Родительский план:** [[../../Plans/PLAN-002-full-skills-and-agent-rules-integration|PLAN-002]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Обеспечить автоматическую упаковку всех 11 исполняемых скиллов из каталога `.agents/skills/` репозитория в монолитный бандл `install.py` с последующим их корректным развертыванием в целевом проекте пользователя при установке харнесса.

Список упаковываемых скиллов:
1. `docs-as-code` (главный справочник и стандарт)
2. `kb-plan` (Режим 1: Планирование / RFC)
3. `kb-task` (Режим 2: Формирование ТЗ)
4. `kb-implement` (Режим 3: Реализация ТЗ)
5. `kb-complete` (Режим 3: Завершение задачи и синхронизация)
6. `kb-bug` (Фиксация дефектов и Regression-First автотест)
7. `kb-adr` (Архитектурные решения и отказные ADR)
8. `kb-research` (Платформенные исследования и компромиссы)
9. `kb-lint` (Проверка целостности базы знаний)
10. `kb-onboard` (Онбординг разработчика и агента)
11. `kb-init` (Инициализация структуры в новом проекте)

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `scripts/build_installer.py` — добавление обхода `.agents/skills/`, упаковка канонических файлов `SKILL.md` каждого скилла в единый zlib/base64 бандл (исключая дублирующие локальные копии `resources/` и `scripts/`).
* `[MODIFY]` `install.py` — добавление распаковки ресурсов с префиксом `.agents/skills/` в целевой каталог `.agents/skills/<skill>/SKILL.md`.

---

## 3. Детали технической реализации

### 3.1. Сборщик `scripts/build_installer.py`:
```python
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"

# В функции bundle_assets():
if SKILLS_DIR.is_dir():
    skill_dirs = sorted([d for d in SKILLS_DIR.iterdir() if d.is_dir()])
    for sdir in skill_dirs:
        skill_md = sdir / "SKILL.md"
        if skill_md.is_file():
            rel_key = f".agents/skills/{sdir.name}/SKILL.md"
            assets[rel_key] = skill_md.read_text(encoding="utf-8")
            print(f"  • Bundled skill: {sdir.name}/SKILL.md ({len(assets[rel_key])} chars)")
```

### 3.2. Распаковщик в `install.py`:
```python
# В функции install_harness():
for rel_path, content in assets.items():
    if rel_path.startswith(".agents/skills/"):
        target_file = target_dir / rel_path
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")

print(f"✅ Deployed 11 AI agent skills (.agents/skills/).")
```

---

## 4. План верификации (Verification Plan)

### Сборка и тесты:
- [x] Запуск сборщика: `python scripts/build_installer.py` (код завершения 0, подтверждение включения 11 скиллов в логе).
- [x] Проверка синтаксиса `install.py`: `python -m py_compile install.py`.
- [x] Проверка базы знаний линтером: `python scripts/kb_lint.py --path docs`.

### Интеграционная проверка развертывания:
- [x] Тестовая установка в изолированный каталог:
  `python install.py -y --target-dir test_sandbox_skills --stack generic --agent generic --git none`
- [x] Проверка наличия всех 11 каталогов скиллов в `test_sandbox_skills/.agents/skills/` с непустыми `SKILL.md`.
- [x] Очистка временного каталога: `Remove-Item test_sandbox_skills -Recurse -Force`.

---

## 5. Критерии готовности (Definition of Done)

- [x] `scripts/build_installer.py` упаковывает ровно 11 файлов `SKILL.md`.
- [x] Размер `install.py` не превышает 80 КБ.
- [x] Инсталлятор корректно создает структуру `.agents/skills/<skill_name>/SKILL.md` в целевой директории.
- [x] Все пункты Плана верификации пройдены успешно.
