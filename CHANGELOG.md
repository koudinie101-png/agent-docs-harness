# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

[0.5.0]: https://github.com/koudinie101-png/agent-docs-harness/releases/tag/v0.5.0
