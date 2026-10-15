---
id: TASK-068
title: "Защита анонимизатора, контейнерный TTY-зонд и интеграция сборщика в install.py и build_release.py"
status: done
type: task
phase: 17
component:
  - installer
  - release
parent_plan: "[[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]]"
created: 2026-10-14
updated: 2026-10-15
tags:
  - task/spec
  - phase17
  - installer
  - release
  - build
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-068 — Защита анонимизатора, контейнерный TTY-зонд и интеграция сборщика в install.py и build_release.py

> **ID:** TASK-068 | **Статус:** Выполнено  
> **Фаза:** 17 | **Релиз:** v0.17.0  
> **План:** [[../../Plans/PLAN-017-core-hardening-and-ssot-sync|PLAN-017]] | **Канбан:** [[../../Kanban|Канбан]]  

---

## 1. Цель задачи
Устранить краевые дефекты в инсталляторе и релизном пайплайне:
1. Защитить анонимизатор диагностического отчета `install.py --report` от порчи произвольных слов при наличии коротких системных логинов (`dev`, `git`, `py`).
2. Обеспечить корректную работу `install.py` в Docker-контейнерах и CI без управляющего терминала (проверка открытия `/dev/tty`).
3. Добавить информативную диагностику при сбое начального `git commit` в `setup_git()`.
4. Интегрировать автоматический вызов `build_installer.build()` внутри `scripts/build_release.py`, чтобы дистрибутив `dist/install.py` всегда содержал свежий бандл ассетов.

---

## 2. Затрагиваемые файлы
* `[MODIFY]` `install.py` — функции `generate_diagnostic_report()`, `setup_git()`, `main()`.
* `[MODIFY]` `scripts/build_release.py` — вызов генерации бандла перед упаковкой артефакта.
* `[MODIFY]` `tests/test_installer.py` — тесты анонимизатора, TTY-зонда и релизного билда.

---

## 3. Детали реализации

### 3.1. Защита границ путей в анонимизаторе `generate_diagnostic_report()`
```python
home_dir = str(Path.home())
def anonymize(text: str) -> str:
    # 1. Замена домашнего каталога целиком на '~'
    if home_dir and home_dir in text:
        text = text.replace(home_dir, "~")
    # 2. Замена логина строго с проверкой разделителей путей
    if current_user and len(current_user) > 1:
        # Регулярное выражение с границами разделителей путей / или \
        text = re.sub(r'([/\\\\])' + re.escape(current_user) + r'([/\\\\]|$)', r'\1<user>\2', text)
    return text
```
Это предотвращает замену подстрок в именах файлов (`Devlog.md` остается `Devlog.md`).

### 3.2. Надежный TTY-зонд для Linux/Docker/CI в `install.py`
```python
def can_open_tty() -> bool:
    if os.name == "nt":
        return sys.stdin.isatty()
    if sys.stdin.isatty():
        return True
    if os.path.exists("/dev/tty"):
        try:
            with open("/dev/tty", "r"):
                return True
        except (OSError, IOError):
            return False
    return False

# В main():
is_interactive = not args.non_interactive and can_open_tty()
```

### 3.3. Диагностика `git commit` в `setup_git()`
```python
res = subprocess.run([git_cmd, "commit", "-m", "feat: initialize docs-as-code harness"], cwd=str(target_dir), env=git_env, capture_output=True, text=True, encoding="utf-8", errors="replace")
if res.returncode == 0:
    print("✅ Created initial Git commit with Docs-as-Code harness (branch: main).")
else:
    print(f"⚠️ Git commit notice: Initial commit could not be created automatically (exit code {res.returncode}).")
    if "user.name" in res.stderr or "user.email" in res.stderr:
        print("   ℹ️ Configure Git identity: git config --global user.name 'Your Name' && git config --global user.email 'you@example.com'")
```

### 3.4. Интеграция сборки ассетов в `scripts/build_release.py`
```python
import scripts.build_installer as build_installer

def main() -> int:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    # Пересобрать бандл ассетов в install.py перед копированием в dist/
    print("Building embedded installer bundle...")
    build_installer.build()

    target = DIST_DIR / "install.py"
    shutil.copy2(INSTALL_PY, target)
    print(f"OK: Release artifact packaged at {target.as_posix()} ({target.stat().st_size} bytes).")
    return 0
```

---

## 4. План верификации (Verification Plan)
- [x] Автотесты: `pytest tests/test_installer.py` — 100% pass.
- [x] Тест анонимизатора: подача строки `C:/Users/dev/Documents/project/docs/Devlog.md` с `user='dev'` возвращает `~/Documents/project/docs/Devlog.md` или `.../<user>/.../Devlog.md` без искажения слова `Devlog`.
- [x] Тест TTY-зонда: вызов в окружении с закрытым или недоступным `/dev/tty` корректно определяет `is_interactive=False`.
- [x] Тест билда: вызов `python scripts/build_release.py` выполняет `build_installer.build()` и обновляет `dist/install.py`.

---

## 5. Критерии готовности (DoD)
- [x] Код написан строго по ТЗ без внешних зависимостей.
- [x] Все пункты Плана верификации пройдены.
- [x] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [x] Запись добавлена в `Devlog.md`.
