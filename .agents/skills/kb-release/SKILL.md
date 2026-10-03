---
name: kb-release
description: "Release cut: pre-flight checks, dist/ build hook, SHA-256, RELEASE notes, git tag."
---

# /kb-release — Release Cut & Publication

Use when the user runs `/kb-release <vX.Y.Z>` to finalize a development phase and package artifacts.

## 🚨 Constraints
* **Explicit Trigger Only:** Releases are NEVER triggered implicitly or automatically.
* **Pre-flight Gate:** Prohibited if git working tree is dirty, phase tasks are incomplete, or `kb_lint.py` fails.
* **Zero Dependencies:** Uses only standard library Python 3 (`scripts/kb_release.py`), native Git, and `gh` CLI.

## Procedure
1. **Pre-flight Checks:**
   - Run `python scripts/kb_lint.py --path docs` (0 broken links).
   - Run project test suites.
   - Verify `git status` is clean.
   - Verify all tasks of the target phase are marked `[x]` in `docs/02_Tasks/Roadmap.md`.
   - Verify Living Spec & README: `README.md` contains actual CLI commands and `SPEC.md` reflects current architecture.
2. **Environment & Mode Detection:**
   - Detect mode: `github` (remote origin on GitHub + `gh` CLI available) or `local-only`.
3. **Execute Build Hook:**
   - Trigger build hook targeting `dist/` (e.g., `scripts/build_release.py`, package manager build script).
   - If no hook exists, fallback to clean Source Release.
4. **Generate Release Document (Dual-Export & High-SNR):**
   - Run `python scripts/kb_release.py --version X.Y.Z --phase N`.
   - Generates internal `docs/02_Tasks/Releases/RELEASE-vX.Y.Z.md` (scoped ADRs for current phase) and public `dist/RELEASE_NOTES.md` (High-SNR clean GFM: Highlights, Quick Install, Features, Fixes, SHA-256 table; strictly excludes ADR block).
5. **Sync Knowledge Base:**
   - Mark phase as completed in `docs/02_Tasks/Roadmap.md`.
   - Prepend release section to `CHANGELOG.md`.
   - Append entry with SHA-256 checksums to `docs/Devlog.md`.
6. **Publish:**
   - **GitHub Mode:** commit docs, create annotated tag `vX.Y.Z`, push main and tags, create release with `gh release create vX.Y.Z dist/* --notes-file dist/RELEASE_NOTES.md`.
   - **Local-Only Mode:** commit docs, create tag `vX.Y.Z`, display local artifact paths and SHA-256 hashes in chat.
7. **Final Verification:**
   - Run `python scripts/kb_lint.py --path docs` to confirm link integrity.
