# Changelog

## [1.1.0] — 2026-11-10
### Added
- Mode 7 — multilingual academic editing [EXTENSION]: `references/writing/` with the editing workflow (`multilingual-editing.md`), academic proofreading, academic humanization, stylistic refinement, writing fingerprint preservation, and language profiles for Brazilian Portuguese, Spanish, French and English (with regional variants).
- Three editing levels: 1 Proofreading, 2 Academic enhancement (default), 3 Deep academic editing.
- Editing-integrity rules E1–E11 in `core-rules.md`; `[AUTHOR CHECK: …]` placeholder.
- `assets/templates/editing-report.md`; language-quality section in the review report.
- `scripts/check_edit_preservation.py` (numbers, citations, equations, code, URLs).
- `check_manuscript.py`: Spanish and French headings and patterns, automatic language detection, `--lang auto|en|pt|es|fr|<regional tag>`.
- Tests for Spanish and French manuscripts, language selection and edit preservation in four languages; `evals/editing-evals.json`.
### Changed
- `SKILL.md` description and routing (mode 2 vs. mode 7); review rubric points to the editing modules for language quality.
### Unchanged
- Original guideline, modes 1–6, citation styles and all v1.0 behavior of `check_manuscript.py` (two-argument `run_checks`, `--lang pt|en|auto`).

## [1.0.0] — 2026-11-10
### Added
- `research-writing` skill compatible with Claude (Claude Code, claude.ai) and Codex (Agent Skills standard).
- Source guideline converted to `references/guideline-original.md` and rule catalog `core-rules.md`.
- Six modes: plan, draft section, review manuscript, analyze research (related work), classify methodology, experimental planning.
- Document types: article, technical report, TCC, dissertation, thesis, research proposal.
- Extensions: objectives and research questions, theoretical foundation, systematic review, qualitative/mixed methods, ethics/data/AI disclosure, title.
- Citation styles: ABNT, ACM, IEEE, APA 7, Vancouver, Springer LNCS, Chicago author-date, Harvard.
- Templates, heuristic checker `check_manuscript.py` with tests, evaluation prompts, Claude Code marketplace manifest, install and zip scripts.
