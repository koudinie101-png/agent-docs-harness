---
id: RESEARCH-022
title: "Укрепление контура визуальных ассетов (Asset Storage Hardening): Task-Scoped пространства имен (TASK-XXX/), жизненный цикл As-Is/To-Be и валидация лейаута в kb_lint.py"
status: completed
created: 2026-10-15
updated: 2026-10-15
tags:
  - research
  - ui-ux
  - assets
  - visual-harness
  - lint
  - quality-gates
related_tasks: []
related_adrs:
  - "[[../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]"
  - "[[../03_Decisions_ADR/ADR-0027-task-scoped-asset-namespaces-and-layout-linting|ADR-0027]]"
---

# 🔬 Исследование: Укрепление контура визуальных ассетов (Asset Storage Hardening): Task-Scoped пространства имен (`TASK-XXX/`), жизненный цикл As-Is/To-Be и валидация лейаута в `kb_lint.py`

> **Теги:** #research #ui-ux #assets #visual-harness #lint #quality-gates | **Канбан:** [[../02_Tasks/Kanban|Канбан]]  
> **Первоисточник:** [[../02_Tasks/Inbox/FB-GH-5|FB-GH-5 (GitHub Issue #5)]] | **Преемственность:** Развитие [[RESEARCH-021-heterogeneous-ui-ux-and-visual-asset-management|RESEARCH-021]] и [[../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]

---

## 1. Проблема и гипотезы

При промышленной эксплуатации контура визуальных ассетов (`VisualHarness`, [[../03_Decisions_ADR/ADR-0026-heterogeneous-ui-ux-and-visual-asset-management|ADR-0026]]) в многокомпонентных гетерогенных системах (`Windows Desktop + Android Companion`) вскрылись три структурные уязвимости хранения макетов в `docs/assets/`:

1. **Коллизия итеративных редизайнов («To-Be Drift» и нарушение Permalinks Principle):**
   - В базовой версии `ADR-0026` скриншоты верификации уже имели привязку к задаче (`docs/assets/screenshots/<target>/TASK-XXX.png`), тогда как каталог макетов `docs/assets/mockups/<target>/` оставался плоским (ориентированным на названия экранов, например `settings_screen_tobe.svg`).
   - Когда тот же экран подвергается повторному редизайну в следующей фазе (например, `TASK-047` внедряет экран настроек, а `TASK-098` адаптирует его под складные экраны и планшеты), перезапись `settings_screen_tobe.svg` **разрушает исторический визуальный контракт** закрытой спецификации `TASK-047` (нарушение Правила 1 `AGENTS.md` — *Permalinks & Historical Integrity Invariant*).
   - Попытка обходить перезапись через суффиксы версий (`settings_screen_tobe_v2.svg`, `settings_screen_tobe_final_new.svg`) порождает неконтролируемую энтропию имен.

2. **Гранулярность поверхностей (Target Component Granularity) и «дикие» корни (Rogue Roots):**
   - В реальных клиентах с 5–10 поверхностями (например, Windows: `TrayFlyout`, `ToastCards`, `ContextMenu`, `PairingModal`) разработчики и AI-агенты инстинктивно группируют векторные макеты в подпапки.
   - В отсутствие формального стандарта вложенности внутри `mockups/<target>/` агенты создают несанкционированные корневые папки напрямую в `docs/assets/<target>/<component>/` (например, `docs/assets/windows/tray_flyout/`), обходя каталог `mockups/`.

3. **Слепая зона и ложноположительное разрешение путей в `scripts/kb_lint.py`:**
   - В `scripts/kb_lint.py` присутствует проверка веса ассетов (`check_asset_weights()`), но отсутствует проверка топологии каталога `docs/assets/` (`check_asset_layout()`).
   - **Критическая находка при аудите кода `scripts/kb_lint.py` (строки 604–605 и 724–726):** при переходе на task-scoped папки (`mockups/android/TASK-047/tobe.svg` и `mockups/android/TASK-098/tobe.svg`) базовые имена файлов (`tobe.svg`, `asis.svg`, `sequence.svg`) совпадают между разными задачами. В текущей реализации `build_file_map()` регистрирует каждый медиафайл по голому имени `file_map[p.name] = p`, а `run_linter()` на строке 725 проверяет `if link_name in file_map:` **даже для ссылок с явным относительным путем**! В результате битая ссылка `![[../../../assets/mockups/android/TASK-098/tobe.svg]]` (когда файл в `TASK-098` забыли создать) **ложноположительно проходит проверку**, так как в `file_map` уже лежит `tobe.svg` от старой задачи `TASK-047`!

### Проверяемые гипотезы
* **H1 (Task-Scoped Symmetry):** Переход от плоского каталога `mockups/<target>/` к пространствам имен задач `docs/assets/mockups/<target>/TASK-XXX/` (и `BUG-XXX/` для UI-дефектов) устанавливает полную триаду симметрии: `Specs/.../TASK-XXX.md` $\leftrightarrow$ `mockups/<target>/TASK-XXX/` $\leftrightarrow$ `screenshots/<target>/TASK-XXX.png`.
* **H2 (As-Is / To-Be Lifecycle):** Хранение пары `asis.svg` и `tobe.svg` (либо `<surface>_asis.svg` / `<surface>_tobe.svg` для мульти-экранных задач) внутри `TASK-XXX/` превращает каждый редизайн в самодостаточный иммутабельный срез без мутации предыдущих задач.
* **H3 (Path-Strict Media Resolution + Layout Gate):** Устранение fallback-поиска по `link_name` для ссылок с разделителями пути (`/`, `\`) в `kb_lint.py` в сочетании с `check_asset_layout()` механически (Tier 1) блокирует ложноположительные совпадения одноименных `tobe.svg` и выявляет «дикие» папки в `docs/assets/`.

### Prior-Art Gate (Существующие решения и платформенные аналоги)
* **Внутренний аудит кодовой базы:**
  - `install.py` (`setup_ui_harness()`, строки 557–598): уже создает `docs/assets/mockups/<target>/`, `docs/assets/screenshots/<target>/`, а при `len(ui_targets) > 1` — `docs/assets/mockups/flows/` и `docs/assets/screenshots/multi-device/` с файлами `.gitkeep`.
  - `SPEC.md` (раздел 2.1), `README.md`, `CHANGELOG.md` и `docs/Onboarding.md`: помимо `mockups/` и `screenshots/`, в качестве канонических подкаталогов `docs/assets/` задокументированы `diagrams/` и `design/`.
  - `scripts/kb_lint.py` (`build_file_map()`, строки 598–610; `run_linter()`, строки 723–730; `check_asset_weights()`, строки 405–429): реализована индексация `MEDIA_EXTENSIONS` и проверка лимита 2 МБ. Для `.md` файлов на строке 728 уже действует защита `"/" not in link and "\\" not in link`, которая по упущению не была применена к ветке `MEDIA_EXTENSIONS` на строке 725.
* **Внешние аналоги:**
  - *Snapshot Testing (Playwright / Jest / Storybook Chromatic):* группировка визуальных эталонов по идентификатору теста/спецификации (`<spec-id>/<state>.png`), исключающая глобальные коллизии имен между сьютами.

---

## 2. Анализ механизмов и стресс-тест

### 2.1. Стресс-тест №1: Коллизия одноименных файлов (`tobe.svg`, `asis.svg`) в `kb_lint.py` и Obsidian

Проверим, что происходит в текущем `scripts/kb_lint.py`, если две задачи (`TASK-047` и `TASK-098`) используют канонические имена `asis.svg` и `tobe.svg` в своих папках:

1. **Перезапись в `file_map`:**
   В `build_file_map()` (строки 604–605):
   ```python
   file_map[p.name] = p
   file_map[p.name.lower()] = p
   ```
   При обходе `docs_dir.rglob("*")` ключ `file_map["tobe.svg"]` перезаписывается последним найденным файлом.
2. **Ложноположительный пропуск битых путей (False Negative Linter Bug):**
   В `run_linter()` (строки 724–726):
   ```python
   if link_ext in MEDIA_EXTENSIONS or "." in link_name:
       if link_name in file_map or link_name_lower in file_map or link in file_map ...:
           found = True
   ```
   Если в `TASK-098.md` указана ссылка с явным путем `![[../../../assets/mockups/android/TASK-098/tobe.svg]]`, но папка `TASK-098/` пуста или не создана:
   - Проверки `candidates` и `norm_path` возвращают `False`.
   - Линтер переходит в блок `if not found:` (строка 723), берет `link_name = "tobe.svg"`, находит его в `file_map` (от `TASK-047/tobe.svg`) и выставляет `found = True`!
   - **Вывод стресс-теста:** Без исправления строки 725 в `scripts/kb_lint.py` введение стандартных имен `asis.svg` / `tobe.svg` **опасно**, так как после первой же задачи линтер перестанет замечать отсутствующие макеты во всех последующих задачах!
3. **Защита от неоднозначных голых ссылок (`![[tobe.svg]]`):**
   Если в ссылке указан путь (`"/" in link or "\\" in link`), поиск в `file_map` должен выполняться **только по относительному пути** (`link` / `stripped_link`), но **не** по голому `link_name`.

### 2.2. Стресс-тест №2: Мульти-поверхностные задачи (Multi-Surface Tasks в рамках одного `TASK-XXX`)

В `FB-GH-5` справедливо отмечено, что целевая платформа может содержать 5–10 поверхностей (`TrayFlyout`, `ToastCards`, `ContextMenu`, `PairingModal`). Что если одна задача `TASK-047` одновременно затрагивает две поверхности (`TrayFlyout` и `PairingModal`)?
* Если жестко ограничить имена файлов внутри `TASK-XXX/` только строками `asis.svg` и `tobe.svg`, разработчик не сможет положить макеты двух разных окон в одну папку `TASK-047/`.
* **Решение:** Внутри `docs/assets/mockups/<target>/TASK-XXX/` разрешается как каноническая краткая нотация для одноэкранных задач (`asis.svg`, `tobe.svg`, `empty.svg`, `loading.svg`, `error.svg`, `populated.svg`), так и префиксная нотация с именем поверхности (`<surface>_asis.svg`, `<surface>_tobe.svg`, `<surface>_<state>.svg`, например `tray_flyout_tobe.svg`, `pairing_modal_tobe.svg`). Папка задачи `TASK-XXX/` выступает единым изолированным контейнером.

### 2.3. Стресс-тест №3: Топология корня `docs/assets/` и обратная совместимость

В `FB-GH-5` предлагалось ограничить верхний уровень `docs/assets/` только папками `mockups` и `screenshots`.
* **Фальсификация по кодовой базе:** Аудит `SPEC.md` (строка 53), `README.md` (строка 131), `CHANGELOG.md` (строка 28) и `docs/Onboarding.md` (строки 310–311) показал, что в стандарте уже узаконены 4 корневых каталога внутри `docs/assets/`: `mockups/`, `screenshots/`, `diagrams/` и `design/`.
* Если запретить `diagrams/` и `design/`, линтер выдаст ложные срабатывания на проектах, строго следующих `SPEC.md` и `Onboarding.md`.
* Кроме того, унаследованные хранилища могут содержать файлы верхнего уровня до миграции. Поэтому проверка `check_asset_layout(docs_dir)` должна работать в режиме **Non-Blocking Warning (`WARN`)** (аналогично `check_asset_weights` и `check_phase_consistency`), а нарушение целостности путей в ссылках — в режиме **Blocking Error (Exit code 1)**.

---

## 3. Практические замеры и прототип валидации

Ниже представлен эталонный алгоритм проверки топологии `check_asset_layout()` и строгого разрешения путей медиафайлов для `scripts/kb_lint.py` (Zero Dependencies, `pathlib` + `re`):

```python
ALLOWED_ASSET_ROOTS = {"mockups", "screenshots", "diagrams", "design"}
TASK_NAMESPACE_RE = re.compile(r"^(?:TASK|BUG)-\d{3,}(?:-[a-zA-Z0-9_-]+)?$", re.IGNORECASE)

def check_asset_layout(docs_dir: Path) -> List[str]:
    warnings: List[str] = []
    assets_dir = docs_dir / "assets"
    if not assets_dir.is_dir() and (docs_dir / "docs" / "assets").is_dir():
        assets_dir = docs_dir / "docs" / "assets"
    if not assets_dir.is_dir():
        return warnings

    for item in sorted(assets_dir.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir() and item.name.lower() not in ALLOWED_ASSET_ROOTS:
            rel_p = item.relative_to(docs_dir).as_posix() if _is_relative_to(item, docs_dir) else item.name
            warnings.append(
                f"WARN: Asset layout violation: rogue top-level directory '{rel_p}' in assets/. "
                f"Allowed roots: {sorted(ALLOWED_ASSET_ROOTS)}."
            )
        elif item.is_file():
            rel_p = item.relative_to(docs_dir).as_posix() if _is_relative_to(item, docs_dir) else item.name
            warnings.append(
                f"WARN: Asset layout violation: un-namespaced loose file '{rel_p}' at root of assets/."
            )

    mockups_dir = assets_dir / "mockups"
    if mockups_dir.is_dir():
        for target_dir in sorted(mockups_dir.iterdir()):
            if target_dir.name.startswith("."):
                continue
            if not target_dir.is_dir():
                rel_p = target_dir.relative_to(docs_dir).as_posix() if _is_relative_to(target_dir, docs_dir) else target_dir.name
                warnings.append(f"WARN: Asset layout violation: loose file '{rel_p}' in 'assets/mockups/'.")
                continue

            for entry in sorted(target_dir.iterdir()):
                if entry.name.startswith("."):
                    continue
                if not entry.is_dir() or not TASK_NAMESPACE_RE.match(entry.name):
                    rel_p = entry.relative_to(docs_dir).as_posix() if _is_relative_to(entry, docs_dir) else entry.name
                    warnings.append(
                        f"WARN: Asset layout violation: '{rel_p}' inside 'assets/mockups/{target_dir.name}/' "
                        f"must be a task-scoped directory matching 'TASK-XXX/' (or 'BUG-XXX/')."
                    )
    return warnings
```

И исправление строгости разрешения медиа-ссылок в `run_linter()`:
```python
if link_ext in MEDIA_EXTENSIONS or "." in link_name:
    if link in file_map or link.lower() in file_map or stripped_link in file_map or stripped_link.lower() in file_map:
        found = True
    elif "/" not in link and "\\" not in link and (link_name in file_map or link_name_lower in file_map):
        found = True
```

---

## 4. Сравнительный анализ (Trade-off Matrix)

| Вариант | Плюсы | Минусы и риски | Вердикт |
| :--- | :--- | :--- | :--- |
| **А. Плоский каталог по платформам (`mockups/<target>/<screen>_tobe.svg`)** *(Текущий в ADR-0026)* | Простые короткие пути на старте проекта (Фаза 1). | **To-Be Drift:** при повторном редизайне экрана перезапись ломает Permalinks старых ТЗ, а версионирование (`_v2`, `_final`) создает хаос. | **Отклонён (Устарел)** |
| **Б. Группировка по UI-компонентам (`mockups/<target>/<component>/tobe.svg`)** | Логичная группировка по окнам/виджетам (`tray_flyout/`, `settings/`). | Не решает проблему повторного редизайна того же компонента в будущих фазах; провоцирует создание `assets/<target>/<component>/`. | **Отклонён** |
| **В. Task-Scoped пространства имен (`mockups/<target>/TASK-XXX/{asis,tobe}.svg`) + Layout Gate + Strict Path Resolution** | 100% иммутабельность истории ТЗ (Permalinks), полная симметрия `Specs` $\leftrightarrow$ `mockups` $\leftrightarrow$ `screenshots`, поддержка `As-Is / To-Be`, механическая защита в `kb_lint.py`. | Требует создания подпапки `TASK-XXX/` для макетов задачи и запрета fallback-поиска по голому имени при наличии пути. | **Рекомендован (Выбран)** |

---

## 5. Отвергнутые варианты

* **Глобальное хранение «текущего состояния экранов» вне контекста задач (`docs/assets/current_screens/<target>/<screen>.svg`):**
  * *Причина отказа:* Дублирует реальный код приложения и быстро устаревает. В парадигме Docs-as-Code макет (`mockup`) — это проектный контракт конкретной задачи (`TASK-XXX`), а источником правды о текущем визуальном состоянии системы служат дизайн-система (`UI_Design_System.md`) и подтверждающие скриншоты выполненных задач (`screenshots/<target>/TASK-XXX.png`).
* **Блокирующая ошибка (Exit code 1) в `check_asset_layout()` на любые нестандартные файлы в `docs/assets/`:**
  * *Причина отказа:* Нарушает обратную совместимость при обновлении существующих проектов через `install.py --update` и мешает работе пользователя в Obsidian в момент вставки черновых скриншотов через `Ctrl+V` до их переименования. Формат `WARN` (как в `check_asset_weights()`) дает 100% видимость для AI-агента на этапе верификации Режима 3 без разрушения обратной совместимости, тогда как битые пути к макетам блокируются жестко (Exit code 1).
* **Жесткий запрет папок `diagrams/` и `design/` внутри `docs/assets/`:**
  * *Причина отказа:* Противоречит `SPEC.md`, `README.md` и `docs/Onboarding.md`, где `diagrams/` и `design/` уже задокументированы как легитимные разделы `docs/assets/`.

---

## 6. Выводы и правила

1. **Утвердить стандарт Task-Scoped Mockup Namespaces (`ADR-0027`, расширяющий `ADR-0026`):**
   - Все предварительные макеты и вайрфреймы размещаются строго внутри каталога задачи: `docs/assets/mockups/<target>/TASK-XXX/` (или `BUG-XXX/`) и `docs/assets/mockups/flows/TASK-XXX/`.
2. **Утвердить конвенцию жизненного цикла `As-Is / To-Be`:**
   - Для новых экранов (Greenfield UI): создается `tobe.svg` (и опционально файлы состояний `empty.svg`, `loading.svg`, `error.svg`, `populated.svg` либо префиксные `<surface>_tobe.svg`).
   - Для рефакторинга или редизайна существующего UI: в `TASK-XXX/` фиксируются оба состояния — `asis.svg` и `tobe.svg` без мутации старых задач.
3. **Укрепить механический контроль в `scripts/kb_lint.py` (Tier 1):**
   - Исправить ложноположительное срабатывание `run_linter()` для медиафайлов с путями (`/` или `\`), разрешив fallback по голому `link_name` только для ссылок без пути.
   - Внедрить `check_asset_layout(docs_dir: Path) -> List[str]` для контроля корней `docs/assets/` и неймспейсов `TASK-XXX/` внутри `mockups/`.
4. **Синхронизировать нормативную базу и шаблоны в следующей фазе:**
   - Обновить Правило 12 в `AGENTS.md` (и `_RULES_BODY` в `install.py`), `SPEC.md`, `README.md`, `docs/Onboarding.md`, `TEMPLATE_PLAN.md` и `TEMPLATE_TASK.md`.



