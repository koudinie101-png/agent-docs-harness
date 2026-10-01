---
id: TASK-026
title: "Автоматизация передачи заметок в CI release.yml и синхронизация встроенного шаблона"
status: planned
type: task
phase: 7
component:
  - ci
  - automation
  - installer
parent_plan: "[[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]"
created: 2026-10-01
updated: 2026-10-01
tags:
  - task/spec
  - phase7
  - component/ci
  - component/automation
  - component/installer
  - release
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация задачи: TASK-026 — Автоматизация передачи заметок в CI и шаблоне инсталлятора

> **ID:** TASK-026  
> **Статус:** К реализации (Режим 2)  
> **Теги:** #task/spec #phase7 #component/ci #component/automation #component/installer #release  
> **Родительский план:** [[../../Plans/PLAN-007-github-release-notes-and-distribution-standard|PLAN-007]]  
> **Связанные исследования и ADR:** [[../../../04_Research/RESEARCH-005-github-release-notes-and-distribution-best-practices|RESEARCH-005]], [[../../../03_Decisions_ADR/ADR-0010-github-release-notes-and-public-distribution-standard|ADR-0010]]  
> **Канбан:** [[../../Kanban|Канбан-доска]]  

---

## 1. Цель задачи

Устранить рассинхронизацию между генерацией релизных заметок и их публикацией на GitHub в автоматическом пайплайне:
1. **GitHub Actions CI (`.github/workflows/release.yml`):** Добавить параметр `body_path: dist/RELEASE_NOTES.md` в действие `softprops/action-gh-release@v2`, гарантируя, что создаваемый GitHub Release содержит полное описание, проверочные контрольные суммы и команды установки.
2. **Шаблон в `install.py`:** Обновить строковую переменную `wf_release_content` в функции `deploy_ci_workflows()` инсталлятора, чтобы при установке без распаковки бандла создавался актуальный воркфлоу с `body_path`.

---

## 2. Затрагиваемые файлы и компоненты

* `[MODIFY]` `.github/workflows/release.yml` — добавление `body_path: dist/RELEASE_NOTES.md` в шаг `Publish GitHub Release`.
* `[MODIFY]` `install.py` — обновление встроенного шаблона воркфлоу `release.yml`.

---

## 3. Детали реализации

### Контракт `.github/workflows/release.yml`

```yaml
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
          body_path: dist/RELEASE_NOTES.md
          files: |
            dist/*
```

### Контракт встроенного шаблона в `install.py`

В функции `deploy_ci_workflows(target_dir: Path, assets: Optional[Dict[str, str]] = None)`:
```python
        # 2. release.yml
        ...
        wf_release_content = (
            ...
            "      - name: Publish GitHub Release\n"
            "        uses: softprops/action-gh-release@v2\n"
            "        if: startsWith(github.ref, 'refs/tags/')\n"
            "        with:\n"
            "          name: Release ${{ github.ref_name }}\n"
            "          draft: false\n"
            "          prerelease: false\n"
            "          body_path: dist/RELEASE_NOTES.md\n"
            "          files: |\n"
            "            dist/*\n"
        )
```

---

## 4. План верификации (Verification Plan)

- [ ] Синтаксис CI: валидация структуры `.github/workflows/release.yml`.
- [ ] Проверка шаблона в инсталляторе: поиск строки `body_path: dist/RELEASE_NOTES.md` в `install.py`.
- [ ] Линтер базы знаний: `python scripts/kb_lint.py --path docs` (0 broken links).

---

## 5. Критерии готовности (DoD)

- [ ] В `.github/workflows/release.yml` и встроенном шаблоне `install.py` зафиксирован параметр `body_path: dist/RELEASE_NOTES.md`.
- [ ] Статус обновлен в ТЗ (`Выполнено`), Канбане (`Done`) и Дорожной карте (`[x]`).
- [ ] Запись добавлена в `docs/Devlog.md`.
