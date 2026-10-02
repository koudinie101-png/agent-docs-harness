# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.8.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.8.0
[0.7.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.7.0
[0.6.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.6.0
[0.5.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.5.0
