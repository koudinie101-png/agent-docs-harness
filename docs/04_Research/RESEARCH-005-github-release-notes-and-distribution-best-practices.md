---
id: RESEARCH-005
title: "Лучшие практики оформления релизов на GitHub (Release Notes & Distribution) и их интеграция в Docs-as-Code харнесс"
status: completed
created: 2026-10-01
updated: 2026-10-01
tags:
  - research
  - release-management
  - github-releases
  - release-notes
  - changelog
  - docs-as-code
  - supply-chain-security
related_tasks: []
related_adrs:
  - "[[../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]]"
  - "[[../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007: Release Management]]"
---

# 🔬 Исследование: Лучшие практики оформления релизов на GitHub и автоматизация Release Notes

> **Теги:** #research #release-management #github-releases #release-notes #changelog #docs-as-code #supply-chain-security  
> **Связанный канбан:** [[../02_Tasks/Kanban|Канбан-доска]]  
> **Связанная дорожная карта:** [[../02_Tasks/Roadmap|Дорожная карта]]  
> **Связанные ADR:** [[../03_Decisions_ADR/ADR-0001-zero-dependencies-python-stdlib|ADR-0001: Zero Dependencies]], [[../03_Decisions_ADR/ADR-0007-release-management-dual-mode-and-build-hook|ADR-0007: Архитектура релиз-менеджмента]]  

---

## 1. Контекст, проблема и проверяемые гипотезы

### 1.1. Контекст и выявленная проблема
В ходе инспекции первого опубликованного релиза репозитория (`v0.5.0` на GitHub) было обнаружено, что:
1. Релиз на GitHub создался с прикрепленным файлом `install.py`, но **с полностью пустым описанием (отсутствуют Release Notes)**.
2. При этом внутри локальной базы знаний Docs-as-Code был сформирован подробнейший документ `docs/02_Tasks/Releases/RELEASE-v0.5.0.md` с обзором фазы, ссылками на задачи, ADR и таблицей хэшей SHA-256.
3. Корневая причина рассинхронизации найдена в файле `.github/workflows/release.yml`:
   ```yaml
   - name: Publish GitHub Release
     uses: softprops/action-gh-release@v2
     with:
       name: Release ${{ github.ref_name }}
       draft: false
       prerelease: false
       files: |
         dist/*
   ```
   Действие `softprops/action-gh-release` не получило параметра `body_path` или `body`. В результате GitHub опубликовал «голый» тег с бинарником, проигнорировав подготовленную документацию.
4. Дополнительная проблема: документ `RELEASE-v0.5.0.md` содержит внутренние относительные викиссылки Obsidian (`[ [ ../Specs/... | TASK-017 ] ]`), которые в веб-интерфейсе GitHub Releases не распознаются и выглядят как сломанный синтаксис.

### 1.2. Проверяемые гипотезы
* **Гипотеза 1 (Критичность Release Notes для open-source и безопасности):** Релиз без содержательных заметок (Release Notes) в современной разработке воспринимается как непрофессиональный, опасный (Supply Chain Security) или заброшенный. Release Notes обязательны для прозрачности, доверия пользователей и доставки обновлений.
* **Гипотеза 2 (Разделение форматов — Internal Vault vs External GitHub):** Внутренний релизный документ в `docs/02_Tasks/Releases/` (с викиссылками для графа Obsidian) и публичный релиз на GitHub преследуют разные цели. Необходима автоматическая генерация публичного файла `dist/RELEASE_NOTES.md` в чистом GitHub Flavored Markdown (GFM) с внешними URL и инструкцией по установке.
* **Гипотеза 3 (Интеграция в CI и утилиту `kb_release.py`):** Добавление в `scripts/kb_release.py` флага экспорта публичных заметок и привязка `body_path: dist/RELEASE_NOTES.md` в `.github/workflows/release.yml` гарантирует 100% автоматическую публикацию релизов с красивым описанием без ручного вмешательства.

---

## 2. Анализ лучших практик индустрии (Industry Standards for GitHub Releases)

### 2.1. Зачем нужны Release Notes? (Критический анализ)

| Фактор | Что происходит БЕЗ Release Notes | Как решают качественные Release Notes |
| :--- | :--- | :--- |
| **Доверие и безопасность (Trust & Security)** | Пользователь видит бинарник `install.py` без объяснений. Возникает подозрение на вредоносный код или сломанный билд. | Четкий перечень изменений, таблица контрольных сумм SHA-256 для проверки скачанного файла. |
| **Уведомления подписчиков (Watchers)** | Пользователи GitHub, подписавшиеся на *Releases Only*, получают пустые email-письма без информации. | Подписчики получают в почту содержательный дайджест новых фичей и исправлений. |
| **Обратная совместимость (Breaking Changes)** | Пользователи обновляются вслепую и сталкиваются с поломками окружения. | Выделенный блок с инструкцией по миграции (Migration Guide). |
| **Быстрый старт (Quick Install)** | Пользователю приходится возвращаться в README в поисках команды установки. | Прямо в релизе приведена однострочная команда запуска (`curl ... \| python3`). |

---

### 2.2. Анатомия эталонного описания релиза на GitHub

Анализ ведущих open-source проектов (VS Code, Fastlane, Docker, Ripgrep, Tauri) показывает устойчивый золотой стандарт структуры:

```markdown
# 🚀 Release v0.5.0 — High-SNR Token Architecture

> 💡 **Executive Summary:** Краткое резюме главной ценности релиза простыми словами для людей (2-3 предложения).

---

### ⚡ Быстрый старт / Обновление (Quick Install)
```bash
# Новая установка
curl -fsSL https://raw.githubusercontent.com/owner/repo/main/install.py | python3

# Обновление существующего проекта
python install.py --update
```

---

### ✨ Новые возможности (Features)
* **High-SNR рефакторинг скиллов:** сжатие Always-On описаний в системном промпте на 53% ([#24](url)).
* **Компактные каркасы шаблонов:** облегчение 13 шаблонов docs/ до Skeleton Templates ([#25](url)).
* **Протокол Anti-Echo:** устранение дублирования созданных файлов в ответах чата.

### 🐛 Исправления ошибок (Bug Fixes)
* Устранены проблемы с кодировкой UTF-8 на консолях Windows при выводе таблиц.

### 🏛️ Ключевые архитектурные решения (ADR)
* [ADR-0009: High-SNR Token Architecture](https://github.com/owner/repo/blob/main/docs/03_Decisions_ADR/ADR-0009.md).

---

### 📦 Контрольные суммы артефактов (SHA-256 Checksums)

| Файл | Размер | Контрольная сумма SHA-256 |
| :--- | :--- | :--- |
| `install.py` | 81.2 KB | `04d88c2a1f5c10bb0e2b4bb0f1715d6af377aaffd3cfed3843a6b51183d5707d` |

**Верификация в PowerShell:**
```powershell
Get-FileHash -Algorithm SHA256 ./dist/install.py
```

---
**Полный список изменений (Full Changelog):** https://github.com/owner/repo/compare/v0.4.0...v0.5.0
```

---

## 3. Практические эксперименты и прототипы

### 3.1. Эксперимент 1: Преобразование Obsidian Wikilinks в чистый Markdown

Во внутреннем документе `docs/02_Tasks/Releases/RELEASE-v0.5.0.md` ссылки хранятся в формате:
`- [[../Specs/05_TokenOptimization/TASK-017-skills-high-snr-refactoring|TASK-017]]: Описание...`

В веб-интерфейсе GitHub Releases это отображается как некликабельный сырой текст `[ [ ... | ... ] ]`.

Напишем функцию очистки/конвертации для `scripts/kb_release.py`:

```python
import re

def convert_wikilinks_to_github_markdown(text: str, repo_url: str = "", branch: str = "main") -> str:
    """
    Конвертирует внутренние викиссылки Obsidian в GitHub Markdown:
    - [ [ path/to/file | Title ] ] -> [Title](repo_url/blob/branch/docs/path/to/file.md) (если repo_url задан)
    - [ [ path/to/file | Title ] ] -> **Title** (если repo_url пуст)
    - [ [ Title ] ] -> **Title**
    """
    def replace_wikilink(match):
        target = match.group(1).strip()
        alias = match.group(2).strip() if match.group(2) else target
        
        # Если есть remote URL, формируем красивую ссылку на GitHub
        if repo_url and not target.startswith("http"):
            clean_target = target.lstrip("./").lstrip("../")
            if not clean_target.endswith(".md"):
                clean_target += ".md"
            full_url = f"{repo_url.rstrip('/')}/blob/{branch}/docs/{clean_target}"
            return f"[{alias}]({full_url})"
        
        # Иначе возвращаем жирный текст без сломанных скобок
        return f"**{alias}**"

    pattern = r"\[\[([^\|\]]+)(?:\|([^\]]+))?\]\]"
    return re.sub(pattern, replace_wikilink, text)
```

**Результат:**
Входной текст: `- [ [ ../Specs/TASK-017 | TASK-017 ] ]: Описание задачи`  
Выходной текст на GitHub: `- [TASK-017](https://github.com/owner/repo/blob/main/docs/Specs/TASK-017.md): Описание задачи`  
Ссылки становятся кликабельными, а синтаксис — валидным GFM.

---

### 3.2. Эксперимент 2: Автоматизация передачи Release Notes в GitHub Actions

В файле `.github/workflows/release.yml` текущий блок публикации выглядит так:

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
          body_path: dist/RELEASE_NOTES.md # <--- КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ
          files: |
            dist/*
```

Когда `scripts/kb_release.py` создает файл `dist/RELEASE_NOTES.md` с чистым описанием, действию `action-gh-release` достаточно указать `body_path: dist/RELEASE_NOTES.md`.

---

## 4. Сравнительный анализ альтернатив (Trade-off Matrix)

| Подход | Плюсы | Минусы и риски | Вердикт |
| :--- | :--- | :--- | :--- |
| **1. Статус-кво: Пустой релиз (только файлы)** | Ноль усилий в CI | 🔴 Подозрительно для пользователей, нулевое описание, пустые уведомления подписчикам | Отклонено |
| **2. Встроенный генератор GitHub (`generate_release_notes: true`)** | Автоматически собирает список PR и коммитов | 🟡 Выводит сырые коммиты (`fix typo`, `wip`), не знает структуру Docs-as-Code, не включает SHA-256 | Недостаточно |
| **3. Ручное оформление через веб-интерфейс GitHub** | Красивое оформление человеком | 🔴 Человеческий фактор, забывчивость, разрыв автоматизации, рутина | Отклонено |
| **4. Dual-Export в `kb_release.py` + `body_path` в CI (Выбранный)** | Полный автопилот, семантический чейнджлог из ТЗ и ADR, проверенные SHA-256, красивые ссылки | 🟢 Требует один раз настроить экспорт `dist/RELEASE_NOTES.md` | **Рекомендовано** |

---

## 5. Отвергнутые подходы (Rejected Alternatives)

* ❌ **Отвергнуто: Использование файла `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` напрямую в качестве `body_path`:**  
  *Причина отказа:* Файл в `docs/` содержит YAML frontmatter (который отображается в релизе как некрасивый серый блок кода) и внутренние относительные викиссылки `[ [ ... ] ]`, ломающие веб-верстку GitHub. Публичный релизный файл должен генерироваться очищенным.
* ❌ **Отвергнуто: Исключительно нативный генератор заметок GitHub (`generate_release_notes`):**  
  *Причина отказа:* GitHub генерирует чейнджлог исключительно на основе заголовков PR и коммитов. В проектах Docs-as-Code первоисточником истины являются спецификации `TASK-XXX`, отчеты `BUG-XXX` и архитектурные решения `ADR-XXXX`. Нативный генератор упускает эту ценную информацию.

---

## 6. Выводы и план внедрения

### 6.1. Архитектурный стандарт релизного сопровождения
1. **Каждый релиз обязан иметь Release Notes:** Релизы без описания запрещены регламентом харнесса.
2. **Экспорт публичных заметок в `dist/RELEASE_NOTES.md`:**  
   Утилита `scripts/kb_release.py` при формировании релиза генерирует два артефакта:
   * Локальный сводный документ: `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` (для базы знаний Obsidian).
   * Публичные релизные заметки: `dist/RELEASE_NOTES.md` (чистый GFM без YAML frontmatter, с кликабельными ссылками на репозиторий, таблицей SHA-256 и быстрыми командами установки).
3. **CI-интеграция:** В `.github/workflows/release.yml` устанавливается параметр `body_path: dist/RELEASE_NOTES.md` (с fallback на `generate_release_notes: true`).
4. **Упаковка в инсталлятор `install.py`:** Шаблон `release.yml` в составе инсталлятора должен содержать эту настройку по умолчанию, чтобы все создаваемые проекты автоматически получали оформленные релизы.

### 6.2. Следующие шаги
1. Зафиксировать решение через **ADR-0010: GitHub Release Notes & Public Distribution Standard**.
2. Внести исправления в:
   * `scripts/kb_release.py` (генерация `dist/RELEASE_NOTES.md` и очистка викиссылок).
   * `.github/workflows/release.yml` (добавление `body_path: dist/RELEASE_NOTES.md`).
   * Шаблоны инсталлятора (`templates/release.yml` и сборщик).
3. При необходимости: обновить описание уже существующего релиза `v0.5.0` на GitHub через GitHub API или веб-интерфейс.
