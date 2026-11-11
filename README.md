# Research Writing Skill

A skill for **Claude** and **Codex** that helps researchers plan, write, review and analyze scientific work (articles, technical reports, undergraduate theses, master's dissertations, PhD theses and research proposals) following a structured scientific writing guideline.

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

**Citation styles:** ABNT (NBR 6023 and NBR 10520:2023), ACM, IEEE, APA 7, Vancouver, Springer LNCS, Chicago (author-date) and Harvard.

**Languages:** the skill answers in the user's language and writes the manuscript in the manuscript's language (e.g., English or Portuguese).

**Integrity:** the skill never fabricates references, data or statistics. Where information is missing it uses placeholders such as `[CITATION NEEDED]` and `[DATA PENDING]` and lists them at the end.

## Installation

### Claude Code (plugin via marketplace)
```text
/plugin marketplace add adrianosantospb/Research-and-Writing-skill
/plugin install research-writing@research-writing-skill
```

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
│   └── analysis/             # review rubric and paper analysis
├── assets/templates/         # outlines, paper card, comparative table, review report, experimental plan
└── scripts/check_manuscript.py   # heuristic checks (.md, .tex, .txt)
.claude-plugin/marketplace.json   # Claude Code plugin installation
scripts/install.sh · scripts/build_zip.sh
evals/evals.json · tests/
```
Content that goes beyond the original guideline is labeled **[EXTENSION]**.

## Automatic checks
```bash
python3 skills/research-writing/scripts/check_manuscript.py manuscript.md --type article   # or --type thesis
python3 -m unittest discover tests
```
The script uses only the Python standard library. Convert .docx or .pdf to text first (e.g., `pandoc file.docx -o file.md`). Its output is a set of **hints** to verify, not a verdict.

## License
MIT. See [LICENSE](LICENSE).
