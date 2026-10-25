---
id: TASK-106
title: "Принять правило PLAIN-LANGUAGE: ADR, свежесть бандла и бюджет"
status: in-progress
type: task
phase: 29
component:
  - rules
  - docs
  - tests
  - installer
parent_plan: "[[../../Roadmap|Roadmap.md (Фаза 29)]]"
created: 2026-10-25
updated: 2026-10-25
tags:
  - task/spec
  - phase29
  - rules
  - docs
  - installer
kanban: "[[../../Kanban|Канбан-доска]]"
---

# 🛠️ Спецификация: TASK-106 — Принять правило `PLAIN-LANGUAGE`

> **ID:** TASK-106 | **Статус:** К реализации (Режим 2)  
> **Фаза:** 29 | **Канбан:** [[../../Kanban|Канбан]]  
> **Источник изменения:** прямой запрос пользователя в параллельной сессии («вне фазового плана» по записи в `Devlog.md` от 2026-10-25)  
> **Состояние:** реализация **уже лежит в рабочем дереве** некоммитнутой (40 файлов); задача принимает её, добавляет запись решения и Tier 1-страж, а не переписывает заново

---

## 1. Цель задачи

В рабочем дереве обнаружен завершённый, но не закоммиченный набор изменений: правило Tier 2 `PLAIN-LANGUAGE` добавлено в корпус `rules/AGENTS_CORE.md` (client #25, harness #17, adapters #11), перегенерированы `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md` и 24 golden-фикстуры, обновлены `tests/test_rules_consistency.py` (адаптеры 10 → 11), `SPEC.md` §2.4, `README.md` §4, `docs/Onboarding.md` §17, `CHANGELOG.md`, `docs/Devlog.md`; бандл пересобран — `install.py` = `dist/install.py` = **179 979 B**.

Изменение по существу корректно и покрыто тестами, но у него нет трёх вещей, без которых оно не считается принятым:

1. **Записи решения** — правило уровня Tier 2 меняет тон всех ответов агента, это архитектурное решение, а не косметика (нет `ADR-XXXX`).
2. **Стража свежести бандла** — ровно этот класс дрейфа мы уже поймали: корпус обновили, `AGENTS.md`/бандл отстали, CI покраснел. Нужен Tier 1-тест, который проверяет правило в **установленной** копии, а не только в репозитории.
3. **Безопасного бюджета** — 21 байт запаса (`179 979` при лимите `180 000`) означает, что любая следующая правка шаблона или корпуса немедленно валит гейт. Это не запас, а растяжка.

## 2. Затрагиваемые файлы и скоуп символов

* `[NEW]` `docs/03_Decisions_ADR/ADR-0033-plain-language-contract.md`:
  - `ADR-0033` — контекст (пользователь-не-разработчик, жаргон как барьер), решение (Tier 2-правило в трёх документах, scope = только чат), отклонённые альтернативы (жаргон по умолчанию; «Technical details» первым блоком; снисходительный тон), последствия (тон, границы с `docs/` и кодом).
* `[MODIFY]` `tests/test_installer.py`:
  - `TestAgentDocsHarness.test_36_task_106_installed_rules_contain_plain_language()` — E2E: установка в temp-каталог, в установленных `AGENTS.md` и `CLAUDE.md` присутствует `Plain-Language Contract`; страж против «корпус обновлён, бандл отстал».
  - `TestAgentDocsHarness.test_16_high_snr_static_corpus_benchmarks()` — бюджет установщика `180000` → `182000` с комментарием-обоснованием (21 B запаса после Фазы 29).
* `[MODIFY]` `CHANGELOG.md`:
  - строка про лимиты: заменить «limits unchanged (180 000 …), 21 B of headroom» на новое значение бюджета и причину.
* `[MODIFY]` `docs/02_Tasks/Roadmap.md`, `docs/02_Tasks/Kanban.md`, `docs/Devlog.md` — стандартная синхронизация (последние два — на шаге `/kb-complete`).
* **Уже в рабочем дереве и принимаются как есть** (не переписываются): `rules/AGENTS_CORE.md`, 7 сгенерированных файлов правил, 24 фикстуры `tests/fixtures/rules/*`, `tests/test_rules_consistency.py`, `SPEC.md` §2.4, `README.md` §4, `docs/Onboarding.md` §17, `install.py` / `dist/install.py` (пересобранный бандл).

## 3. Детали реализации

### 3.1. ADR-0033 (структура)

* **Контекст:** пользователь харнесса — не обязательно разработчик; существующие правила требуют технической точности, но не регулируют **тон** объяснений; в чате это давало жаргон, пути файлов и стек-трейсы вместо ответа на вопрос.
* **Решение:** Tier 2-правило `PLAIN-LANGUAGE` в трёх документах корпуса (client #25, harness #17, adapters #11); scope — только чат: код, коммиты и `docs/` сохраняют техническую точность; структура ответа «результат → смысл → одно действие», ошибки «причина → следствие → исправление», необязательный блок «Technical details».
* **Отклонено:** жаргон по умолчанию (барьер входа); «Technical details» первым блоком (закапывает результат); снисходительный тон («just», «simply», «obviously») — простота не равна упрощению; распространение правила на `docs/`/код (потеря точности).
* **Последствия:** тон обязателен во всех ответах агента; правило механически проверяется инвентарём `tests/test_rules_consistency.py` (Tier 1) и наличием маркера в установленной копии (новый тест §2); «вне фазового плана» — исключение, зафиксированное в Devlog.

### 3.2. Страж свежести бандла

```python
def test_36_task_106_installed_rules_contain_plain_language(self):
    """TASK-106: installed rule files must carry the Tier 2 PLAIN-LANGUAGE rule."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        target = Path(tmp_dir) / "PlainLanguageApp"
        target.mkdir()
        install.install_harness(
            target_dir=target, project_name="PlainLanguageApp", stack_key="python",
            agent_choice="all", git_choice="none", force=True,
        )
        agents_md = (target / "AGENTS.md").read_text(encoding="utf-8")
        claude_md = (target / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("Plain-Language Contract", agents_md)
        self.assertIn("Plain-Language Contract", claude_md)
```

Тест падает, если корпус изменили, а `install.py` не пересобрали — то есть ровно на том дрейфе, который случился в этой итерации.

### 3.3. Бюджет

`179 979 B` при лимите `180 000` → **21 B**. Пере-базировать до `182 000` (запас ~2 KB, как было до Фазы 27), обоснование в комментарии `test_16`: бюджет монолита — про вес дистрибутива, а не про токены контекста; 21 B не позволяют ни одной правки без красного гейта. Токен-бюджеты шаблонов (30 000) и скиллов (31 000) не затрагиваются. Пересборка бандла **не требуется** (меняются только тесты и `CHANGELOG`).

### 3.4. Порядок коммита

Один коммит `feat(rules): adopt PLAIN-LANGUAGE contract with ADR and bundle freshness guard (TASK-106)`, включающий и унаследованный набор из §2, и новые файлы. Коммит выполняется с **явным перечислением путей** (`git add <paths…>`), без `git add -A`: в общем рабочем дереве широкий stage уже один раз захватил чужие файлы (инцидент, который логируется в `/kb-complete`).

## 4. План верификации (Verification Plan)

- [ ] `python scripts/gen_rules.py --check` → `OK: AGENTS.md matches rules/AGENTS_CORE.md`.
- [ ] `python -m unittest tests.test_rules_consistency tests.test_rules_golden` → все OK (инвентарь 11 адаптеров, 24 фикстуры).
- [ ] `python -m unittest tests.test_installer.TestAgentDocsHarness.test_36_task_106_installed_rules_contain_plain_language` → OK (страж работает).
- [ ] Негативная проверка стража: временно вернуть старое содержимое бандла невозможно без пересборки; вместо этого проверить, что тест читает **установленный** `AGENTS.md` (а не файл репозитория) — ревью кода теста.
- [ ] Полный набор: `python scripts/run_tests_sandbox.py` → **184 теста OK** (183 + 1 новый).
- [ ] Размер бандла: `install.py` = `dist/install.py` = 179 979 B ≤ 182 000 B; `test_16` зелёный.
- [ ] `python scripts/kb_lint.py --path docs` → 0 битых ссылок, 0 `WARN`.
- [ ] `git status --porcelain` пуст после коммита (никаких `??`/`M` не осталось).
- [ ] Замеры $\ge 3$ прогонов: не применимы (статический байтовый бюджет, детерминированная пересборка).

### Visual DoD (для задач с GUI/TUI):

Не применимо: правило меняет тон ответов и документацию, пользовательской поверхности нет.

## 5. Критерии готовности (DoD)

- [ ] `ADR-0033` создан (`status: accepted`) с контекстом, решением, отклонёнными вариантами и последствиями.
- [ ] Новый Tier 1-страж проверяет правило в **установленной** копии и зелёный.
- [ ] Бюджет установщика `180000` → `182000` с обоснованием; `CHANGELOG.md` обновлён; бандл не повреждён.
- [ ] Унаследованный набор (корпус, 7 файлов правил, 24 фикстуры, тест-инвентарь, `SPEC`/`README`/`Onboarding`) закоммичен без изменений по существу.
- [ ] Полный набор тестов зелёный; `kb_lint` — 0 битых; рабочее дерево чистое.
- [ ] На шаге `/kb-complete`: Devlog дополнен ссылкой на эту задачу и ADR; зафиксирован инцидент «широкий `git add -A` в общем дереве» (Tier 2-память).
