[![Buy Me a Coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/adrianoneg0)

# Research Writing Skill

A skill for **Claude** and **Codex** that helps researchers plan, write, review, analyze and edit scientific work (articles, technical reports, undergraduate theses, master's dissertations, PhD theses and research proposals) following a structured scientific writing guideline. It also proofreads and refines academic text in **Brazilian Portuguese, Spanish, French and English**.

> ### Personal note
> This skill brings together the way I learned to structure and write scientific research during my years as a graduate student. That approach evolved during my time as a university professor and researcher, until it became the guideline you find here. I share it hoping it helps whoever is writing their own work.
>
> — **Adriano Araujo Santos, PhD**

## What the skill does

| Mode | Purpose | Example request |
|---|---|---|
| 1. Plan | Document structure by type (article, report, undergraduate thesis, dissertation, thesis, proposal) | "Outline my dissertation on…" |
| 2. Draft a section | Writes or improves a section following the guideline rules | "Write the Introduction, separating the business problem from the technical problem" |
| 3. Review a manuscript | Section-by-section audit with rule IDs, cross-section coherence and priorities | "Review my paper against the guideline" |
| 4. Analyze research | 4-part card per paper (overview, contributions, relationship to the proposal, gaps) + comparative table with the proposal as the last row | "Analyze these papers for my related work" |
| 5. Classify methodology | Area, nature, objectives, procedures, object and approach, written as continuous prose | "Classify my research methodology" |
| 6. Experimental planning | H0/H1 hypotheses, variables, design, instrumentation and threats to validity | "Help me plan my experiment" |
| 7. Academic editing | Proofreading, humanization, stylistic refinement and native-level editing in pt-BR, es, fr and en, at three levels, preserving the author's style | "Proofread my abstract", "Improve the writing of this section" |

**Citation styles:** ABNT (NBR 6023 and NBR 10520:2023), ACM, IEEE, APA 7, Vancouver, Springer LNCS, Chicago (author-date) and Harvard.

**Languages:** the skill answers in the user's language and writes or edits the manuscript in the manuscript's language.

**Integrity:** the skill never fabricates references, data or statistics. Where information is missing it uses placeholders such as `[CITATION NEEDED]` and `[DATA PENDING]` and lists them at the end.

## Academic editing (mode 7)

Mode 7 improves the *language* of existing text without changing its *content*. It is an extension of the original guideline; every editing rule is labeled **[EXTENSION]**.

### What it covers
| Module | What it does |
|---|---|
| Academic proofreading | Grammar, syntax, spelling, punctuation, tense consistency, agreement, prepositions and articles, academic conventions. It corrects errors without rewriting correct sentences. |
| Academic humanization | Natural sentence construction, fluency, lexical and syntactic variety, natural transitions, less repetition and fewer formulaic phrases. It never introduces deliberate errors and never tries to evade AI detectors. |
| Native-level multilingual editing | Language profiles for **Brazilian Portuguese**, **Spanish** (Spain and Latin America), **French** (France, Canada, Belgium, Switzerland) and **English** (US and UK). |
| Stylistic refinement | Vocabulary precision, sentence and paragraph restructuring, coherence and cohesion, consistent terminology, academic register. |
| Writing fingerprint preservation | Keeps the author's vocabulary, sentence complexity, voice, formality and preferred terms, so different authors do not end up sounding the same. |

### Editing levels
| Level | Name | What changes |
|---|---|---|
| 1 | Proofreading | Errors only; structure and style untouched |
| 2 | Academic enhancement (**default**) | Level 1 + naturalness, clarity, fluency, vocabulary and style, keeping meaning and argument |
| 3 | Deep academic editing | Level 2 + sentence and paragraph restructuring where it improves clarity |

### Integrity guarantees (rules E1–E11)
Editing never changes numbers, statistics, citation markers, equations, code, URLs, technical terms, quotations or the strength of claims, and it adds no new content. Ambiguous passages are flagged as `[AUTHOR CHECK: …]` instead of being guessed. The script `check_edit_preservation.py` compares the original and edited versions and reports any protected content that changed.

### How to ask
| You want | Example request |
|---|---|
| Proofreading (Level 1) | "Proofread this abstract — errors only." · "Revise só a gramática deste parágrafo." · "Corrige la ortografía y la gramática." · "Corrigez les fautes sans changer le style." |
| Humanization / enhancement (Level 2) | "Make this section read more naturally." · "Melhore a escrita desta seção." · "Mejora la redacción de este párrafo." |
| Deep academic editing (Level 3) | "Deep edit the Discussion for clarity and flow." · "Faça uma edição profunda da Introdução." · "Réécrivez en profondeur cette section." |
| A regional variant | "Edit in British English." · "Use español de México." · "Révisez selon les conventions du Québec (fr-CA)." · "Português do Brasil." |
| Keep your voice | "Improve it, but keep my first person plural and my long sentences." |

Without a level, the skill uses Level 2. Without a variant, it infers one from the text (pt-BR, fr-FR and en-US are the defaults; for Spanish it asks when there are no cues) and states the assumption.

### How it works with the other modes
- **Draft (2) → Edit (7):** write a section by the guideline, then polish its language.
- **Review (3):** the review reports language-quality findings by category, without rewriting, and suggests an editing level.
- **Analyze research (4):** paper cards and tables are not "humanized"; only your own synthesis text is proofread.
- **Citation styles:** reference formatting stays with the citation-style files; editing never reformats references.

## Installation

### Claude Code and Codex (script)
```bash
git clone https://github.com/adrianosantospb/Research-and-Writing-skill.git
cd Research-and-Writing-skill
scripts/install.sh            # Claude Code (~/.claude/skills) + Codex (~/.agents/skills)
scripts/install.sh --claude   # Claude Code only
scripts/install.sh --codex    # Codex only
scripts/install.sh --project /path/to/project   # project scope (.claude/skills and .agents/skills)
```
By default the script creates a symlink, so `git pull` updates the skill. Use `--copy` to copy the files instead. Older Codex versions read `~/.codex/skills`; in that case, copy `skills/research-writing` there.

### claude.ai (web/desktop app)
```bash
scripts/build_zip.sh   # creates dist/research-writing.zip
```
Then upload the .zip in **Settings → Capabilities → Skills**.

### Usage
- **Claude:** just ask (e.g., "review my paper against the guideline"). The skill is triggered by its description. In Claude Code you can also call `/research-writing`.
- **Codex:** ask normally or invoke it explicitly with `$research-writing`.

## Repository structure
```text
skills/research-writing/
├── SKILL.md                  # router: context, modes and invariant rules
├── agents/openai.yaml        # Codex metadata (ignored by Claude)
├── references/
│   ├── guideline-original.md # original guideline (source of truth)
│   ├── core-rules.md         # rules with IDs (R01–R33, C1–C8, I1–I5, W1–W5)
│   ├── sections/             # guidance per section
│   ├── methodology-taxonomy.md · experimental-planning.md · threats-to-validity.md
│   ├── document-types/       # article, report, undergraduate thesis, dissertation, thesis, proposal
│   ├── extensions/           # objectives/RQs, theoretical foundation, systematic review, qualitative, ethics/AI, title
│   ├── citation-styles/      # abnt, acm, ieee, apa, vancouver, lncs, chicago, harvard
│   ├── analysis/             # review rubric and paper analysis
│   └── writing/              # mode 7: editing workflow, proofreading, humanization, stylistic refinement,
│       └── language-profiles/ #   fingerprint preservation; portuguese-brazilian, spanish, french, english
├── assets/templates/         # outlines, paper card, comparative table, review and editing reports, experimental plan
└── scripts/
    ├── check_manuscript.py       # structural heuristic checks (.md, .tex, .txt) in en/pt/es/fr
    └── check_edit_preservation.py # compares original vs. edited text for protected content
.claude-plugin/marketplace.json   # Claude Code plugin installation
scripts/install.sh · scripts/build_zip.sh
evals/evals.json · evals/editing-evals.json · tests/
```
Content that goes beyond the original guideline is labeled **[EXTENSION]**.

## Automatic checks
```bash
# Structural signals (sections, roadmap paragraph, results in Method, hypotheses, threats, contributions…)
python3 skills/research-writing/scripts/check_manuscript.py manuscript.md --type article          # or --type thesis
python3 skills/research-writing/scripts/check_manuscript.py manuscrito.md --lang pt-BR            # auto, en, pt, es, fr or a regional tag

# Did an edit preserve numbers, citations, equations, code and URLs? (exit code 1 if something changed)
python3 skills/research-writing/scripts/check_edit_preservation.py original.md edited.md --level 2

python3 -m unittest discover tests
```
Both scripts use only the Python standard library. Convert .docx or .pdf to text first (e.g., `pandoc file.docx -o file.md`).
Their output is a set of **structural hints**, not a verdict. **They do not check grammar, spelling or style**; linguistic proofreading is done by the skill itself (mode 7). Section headings and structural patterns are recognized in English, Portuguese, Spanish and French, and the language is detected automatically.

## License
MIT. See [LICENSE](LICENSE).
