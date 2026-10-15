# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.16.0] - 2026-10-12

### Added
- **Self-Improving Harness & Procedural Memory Subsystem** (ADR-0025, RESEARCH-020):
  - Procedural memory structure `docs/06_Memory/` with incident archive `Incidents/`.
  - Canonical incident template `TEMPLATE_INCIDENT.md` (`INC-XXX`).
  - High-SNR aggregated memory index `docs/06_Memory/patterns.md` strictly limited to $\le 15$ active patterns (~350 tokens) to guard agent context economy.
- **Quality Gates & Reliability Tiers (Tier 1–3)**:
  - Formally codified Quality Gates invariant (Rule 11) in `AGENTS.md` and synced into thin IDE adapters: Tier 1 (Enforcement: linters/tests), Tier 2 (Always-On prompt invariants), Tier 3 (Playbook skills).
  - Detailed reliability tier matrix in `docs/Onboarding.md`.
- **Lifecycle Memory Integration & Dual-Axis Promotion**:
  - `0. Memory-First Check` preflight in `/kb-implement` (Mode 3).
  - `6. Defect Loop Reflection` and incident promotion protocol in `/kb-complete`.
- **Mechanical Quality Gate in `scripts/kb_lint.py`**:
  - `check_memory_limits`: audits `docs/06_Memory/patterns.md` ensuring $\le 15$ active patterns (Exit code 1 on breach) and validates frontmatter in `docs/06_Memory/Incidents/`.
- **CLI Enhancements & Fast-Track**:
  - Added `-i` (for `--idea`) and `-r` (for `--report`) short CLI flags in `install.py` (TASK-065).
  - Added support for inline text parameter in `scripts/kb_ingest.py --paste "<text>"`.

### Fixed
- **BUG-002**: Eliminated hardcoded `install.py` deployment instructions in public release notes (`scripts/kb_release.py`) for third-party consumers.
- **BUG-003**: Replaced silent local fallback with actionable warnings and installation instructions when GitHub CLI (`gh`) is missing or unauthenticated.
- **BUG-004**: Fixed changelog self-link in release notes generator to construct proper comparison diff URL (`compare/vPREV...vCURR`).
- Fixed documentation discrepancies, updated 16-template registry, and eliminated developer absolute paths (`file:///`) from `README.md`.

### Changed
- Re-bundled standalone installer `install.py` and `dist/install.py` (131.5 KB) packaging 16 templates and procedural memory assets with safe-retention update logic.

## [0.15.0] - 2026-10-12

### Added
- Zero Round-Trip Dispatch & Hot Invariants architecture (ADR-0013, RESEARCH-008): eliminates `view_file` latency on standard lifecycle modes (0, 1, 2, 2B, 2C, 3) and slash commands, speeding up first-turn response by 2.5–3x.
- Pipelined Co-fetching Protocol for bundled reference reading during initialization turns.
- User-Centric Ingestion & Channel Transparency in `scripts/kb_ingest.py` (ADR-0024, RESEARCH-019):
  - Zero-Dependencies git remote autodetection (`detect_github_repo`) from `remote.origin.url`.
  - Channel Transparency Invariant: explicit warnings for unconfigured or skipped sources and GitHub API rate-limit guidance.
  - Flexible ingestion filtering: CLI flags `--label <NAME>` and `--all-open`.
  - Diagnostics status dashboard: `scripts/kb_ingest.py --status` showing channel health, rate limit quota, and inbox ticket distribution.
- Source transparency and diagnostics in `/kb-triage`: actionable diagnostics report via `kb_ingest.py --status` when inbox buffer is empty.
- Phase consistency audit in `scripts/kb_lint.py`: semantic validation (`check_phase_consistency`) matching frontmatter `phase: N` with folder structure (`Specs/NN_<Slug>/`) and tags (`phaseN`).
- Comprehensive E2E installer test `test_29_channel_transparency_and_phase_consistency_deployment` in `tests/test_installer.py`.

### Changed
- Re-bundled standalone installer `install.py` and `dist/install.py` (124.8 KB) packaging updated ingestion, linter, and triage skills with migration support.
- Synchronized `SPEC.md`, `README.md`, and `docs/Onboarding.md` with Zero Round-Trip Dispatch, phase consistency rules, and channel transparency commands.

## [0.14.0] - 2026-10-12

### Added
- Agile Docs-as-Code & Chat-First DX standard based on ADR-0022, ADR-0023, ADR-0015, and RESEARCH-018, RESEARCH-017, RESEARCH-010.
- Ultra-compact Micro-Spec template `TEMPLATE_TASK_MICRO.md` (~35 lines) and Fast-Track protocol (`kb-task --fast`, preflight nudge in `kb-plan`) for trivial changes ($\le 30$ LOC, $\le 2$ files) saving ~70% tokens.
- Human Guardrails protocol («Направляй, а не блокируй») in `AGENTS.md` and all 6 thin IDE adapters (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`).
- Practical developer guide `Zero_To_Hero_Guide.md` («Вайбкодинг со страховкой») introducing the "Autopilot with sensors" mental model and One-Prompt Chat-First bootstrapping.
- Mentor dialogue mode in `kb-onboard` skill with adaptive explanations for beginner vibe coders.
- Human-First release notes formatting (`Highlights`, emoji feature tags `⚡ Fast-Track:`, `✨ Фича:`, `🐛 Исправление:`) in `scripts/kb_release.py`.
- Automated Fast-Track complexity limits and Verification Plan audit (`check_fast_track_specs`) in `scripts/kb_lint.py`.
- Comprehensive E2E installer test `test_28_fast_track_template_and_zero_to_hero_guide_deployment` in `tests/test_installer.py`.

### Changed
- Re-bundled standalone installer `install.py` and `dist/install.py` (120.9 KB) packaging 15 templates and `Zero_To_Hero_Guide.md` with full `--update` migration support.
- Synchronized `SPEC.md`, `README.md`, `docs/Onboarding.md`, and `docs/00_Index.md` with the 15-template registry, Fast-Track, and Human Guardrails protocols.

## [0.13.0] - 2026-10-11

### Added
- Layered Rules Architecture & Thin Forwarders standard based on ADR-0021 and RESEARCH-016.
- Compact Thin Forwarders pattern in all 6 IDE adapter generators (`GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.github/copilot-instructions.md`) shrinking rules by 80% ($\le 25$ lines) and eliminating Double Prompt Injection.
- Decoupled Obsidian Graph taxonomy: interface color configuration isolated inside `.obsidian/graph.json`, saving ~150 prompt tokens per conversation turn.
- Consolidated Onboarding Hub (`kb-onboard`): absorbed command router, directory layout, and 4-stage lifecycle; decommissioned redundant `docs-as-code` meta-skill to free an Always-On slot in the system prompt registry (12 active skills).
- Two-Tier Template Taxonomy (Core Essentials [4] vs Advanced Governance [10]) in `docs/Onboarding.md` and `docs/00_Templates/TEMPLATE_ONBOARDING.md`.
- Automated build hook mirroring compiled standalone monolith into `dist/install.py` with full E2E regression coverage.

### Changed
- Re-bundled standalone installer `install.py` and `dist/install.py` (114.1 KB) with updated templates, skills, and thin forwarders.
- Synchronized `SPEC.md`, `README.md`, and `docs/Onboarding.md` with the 12-skill architecture and Thin Forwarders pattern.

## [0.11.0] - 2026-10-11

### Added
- Bug Lifecycle Architecture & Release Targeting standard based on ADR-0019 and RESEARCH-014.
- Isolated Mode 2B Defect Logging & Interactive Triage (`/kb-bug`) strictly prohibiting code modifications and enforcing Stop & Yield Control.
- Defect release contract metadata (`target_release`, `target_phase`, `release_blocker`, `fixed_in`, `regression_test`) in canonical `TEMPLATE_BUG.md`.
- Native bug resolution via Mode 3 (`/kb-implement BUG-XXX`) enforcing the strict TDD cycle (RED -> GREEN -> REFACTOR).
- Release defect filtering (`collect_fixed_bugs`) in `scripts/kb_release.py` scoping bug fixes strictly to the target release version.
- Pre-flight release blocker check (`check_release_blockers`) halting releases with Exit code 1 upon detecting open blockers.
- Comprehensive E2E installer test `test_22_bug_lifecycle_and_phase11_assets` in `tests/test_installer.py`.

### Changed
- Re-bundled standalone installer `install.py` (99.0 KB) with updated templates, skills, and release manager.
- Synchronized `SPEC.md`, `README.md`, `docs/Onboarding.md`, and agent rules with the 4-Stage Development Lifecycle.

## [0.10.0] - 2026-10-03

### Added
- Single-Task Execution Barrier & Stop-on-Complete Protocol based on ADR-0016 and RESEARCH-012.
- Spec Genesis Protocol & Zero-State Guardrails based on ADR-0018 and RESEARCH-011.
- High-SNR Release Notes Generator & Phase ADR Scoping based on ADR-0017 and RESEARCH-013.
- Cumulative multi-phase release packaging (`--phases`) in `scripts/kb_release.py`.

## [0.8.0] - 2026-10-02

### Added
- Greenfield initialization from verbal idea (Idea-First) based on ADR-0014 and RESEARCH-009.
- Undecided tech stack preset (`undecided`) and `--idea "<text>"` CLI parameter in `install.py` / `build_installer.py`.
- Dynamic generation of `SPEC.md` with `status: discovery` and preliminary architecture questions.
- Living Spec Invariant protocol embedded into `AGENTS.md` and skills (`kb-research`, `kb-complete`, `kb-release`).
- Automated crystallization of `SPEC.md` (`status: active`) and `README.md` upon completing Mode 0 Discovery research.
- Heuristic specification drift audit in `scripts/kb_lint.py` validating sync between `SPEC.md` and root `README.md`.
- Comprehensive unit and E2E regression tests in `tests/test_kb_lint.py` and `tests/test_installer.py` (41 passing tests).

### Changed
- Re-bundled standalone installer `install.py` with updated skills, templates, and drift linter (88.4 KB).

## [0.7.0] - 2026-10-01

### Added
- GitHub Releases & Distribution Notes Standard based on ADR-0010 and RESEARCH-005.
- Dual-export mechanism in `scripts/kb_release.py`: generates internal `RELEASE-vX.Y.Z.md` and public `dist/RELEASE_NOTES.md`.
- Zero-Dependencies wikilinks converter transforming `[[Target|Title]]` into standard GitHub Markdown URLs based on remote origin.
- GitHub Actions release automation with `body_path: dist/RELEASE_NOTES.md` in `.github/workflows/release.yml`.
- Synchronized fallback release workflow template in standalone `install.py`.
- Automated notes delivery via `--notes-file dist/RELEASE_NOTES.md` in `.agents/skills/kb-release/SKILL.md`.
- Canonical `TEMPLATE_RELEASE.md` updated with public release notes export guidelines.
- Extended regression test suite in `tests/test_installer.py` verifying release notes and CI workflow bundling.

### Changed
- Re-bundled standalone installer `install.py` with updated release script, templates, and CI workflows (83.3 KB, 41.9% compression).

## [0.6.0] - 2026-10-01

### Added
- Discovery & Feasibility Lifecycle (Mode 0) integration based on the Double Diamond model (ADR-0012, RESEARCH-007).
- Two-way automated outcome routing in `/kb-research` (Icebox registration for viable ideas vs Rejected ADRs for unviable ones).
- Pre-flight Nudge checks in `/kb-plan` suggesting Mode 0 research for high-risk proposals before planning.
- 4-stage lifecycle documentation in `/kb-onboard` and `docs/Onboarding.md` (Double Diamond: Mode 0 Discovery -> Modes 1-3 Delivery).
- Canonical `TEMPLATE_ROADMAP.md` updated with Icebox routing guidance and `## 🚫 Отклоненные архитектурные идеи` section.
- Canonical `TEMPLATE_ONBOARDING.md` updated with 4-stage lifecycle cheat-sheet and Brownfield adoption steps.
- Regression test `test_18_discovery_mode_and_phase6_assets` in `tests/test_installer.py`.

### Changed
- Re-bundled standalone installer `install.py` with updated templates and skills (81.5 KB payload).
- Maintained strict High-SNR token and byte limits across all updated skeleton templates (`total_templates_size <= 21000`).

## [0.5.0] - 2026-10-01

### Added
- High-SNR Token Architecture & Context Efficiency standard across all agent skills and templates.
- Micro-descriptions for all 12 AI agent skills in `.agents/skills/` (reducing description tax by 53%).
- Skeleton Templates for all 13 canonical templates in `docs/00_Templates/` (reducing template size by 49%).
- Anti-Echo Response Protocol in `AGENTS.md` and installer rules generators to eliminate redundant code echoing in chat.
- Obsidian Graph 7-color palette and tag mapping table explicitly documented in `AGENTS.md`.
- Silent-on-Success CLI mode for `scripts/kb_lint.py` and `scripts/kb_release.py` (with `--verbose` flags).
- Benchmark test suite in `tests/test_installer.py` verifying static corpus token and byte budgets.
- Build hook `scripts/build_release.py` packaging standalone `install.py` into `dist/install.py`.

### Changed
- Refactored `docs-as-code` skill from monolithic duplicate into a lightweight router (2.2 KB).
- Re-bundled and compressed standalone installer `install.py` down to 81.2 KB (-17.6%).
- Enhanced `install.py --update` with non-destructive updates and stack customization for skeleton templates.

[0.16.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.15.0...v0.16.0
[0.15.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.14.0...v0.15.0
[0.14.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.13.0...v0.14.0
[0.13.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.12.0...v0.13.0
[0.12.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/koudinie101-png/agent-docs-harness/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.8.0
[0.7.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.7.0
[0.6.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.6.0
[0.5.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.5.0
