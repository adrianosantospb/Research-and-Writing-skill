# [EXTENSION] Mode 7 — Multilingual academic editing (workflow)

Entry point for proofreading, humanization, stylistic refinement and native-level editing of existing text.
Integrity rules **E1–E11** (`../core-rules.md`) apply to every step. This file decides *what* to load; the module files say *how*.

## Step 1 — Identify the language
1. Detect the language of the body text (not of quotations, the second-language abstract, or the reference list).
   Supported profiles: **Brazilian Portuguese, Spanish, French, English**.
2. Mixed documents: edit each part in its own language (e.g., Portuguese body + English abstract → `portuguese-brazilian.md` for the body, `english.md` for the abstract). Never translate unless asked.
3. If the language is unsupported, apply the general modules only and say that no native-level profile exists for it.
4. If a shell is available, `python3 scripts/check_manuscript.py <file> --lang auto` reports the detected language.

## Step 2 — Fix the regional variant
Explicit user/venue preference always wins ("edit in British English", "español de México", "français du Québec").
Otherwise infer from cues in the text, and state the assumption in the report:

| Language | Default | Variants and typical cues |
|---|---|---|
| Portuguese | pt-BR | pt-PT only on request (cues: *facto*, *equipa*, *registo*, enclisis after subject). This skill's profile is pt-BR; for pt-PT, apply it with the European spelling/usage noted by the user. |
| Spanish | infer; ask if no cue | es-ES (*vosotros*, *ordenador*, *coche*, « » quotes) · es-419 / es-MX / es-AR etc. (*ustedes* only, *computadora*, *carro/auto*) |
| French | fr-FR | fr-CA (OQLF typography and vocabulary: *courriel*, *clavardage*), fr-BE, fr-CH |
| English | en-US | en-GB (*colour*, *analyse*, single quotes, *-ise* or Oxford *-ize*); follow the venue's house style |

Never mix variants inside one document; unify to the chosen one and report it.

## Step 3 — Choose the editing level
**Default: Level 2** when the user does not specify.

| Level | Name | Modules | Allowed changes | Not allowed |
|---|---|---|---|---|
| 1 | **Proofreading** | `academic-proofreading.md` + language profile | Grammar, spelling, punctuation, agreement, tense, prepositions/articles, typography of the profile | Rewording correct sentences; reordering; style changes |
| 2 | **Academic enhancement** *(default)* | Level 1 + `academic-humanization.md` + `stylistic-refinement.md` (sentence level) | Natural phrasing, word choice, transitions, removing repetition, splitting/merging sentences | Reordering paragraphs; changing argument structure |
| 3 | **Deep academic editing** | Level 2 + `stylistic-refinement.md` (paragraph level) | Restructuring sentences and paragraphs, reordering sentences within a section, improving argument flow and cohesion | Changing claims, evidence, results or conclusions; moving content between IMRaD sections without telling the author |

`authorial-style-preservation.md` applies at **all** levels (strictest at Level 1).

Map user wording to levels:
- "proofread", "revisar gramática", "corregir ortografía", "relire / corriger les fautes" → **Level 1**
- "improve", "make it more natural/fluent", "humanize", "melhorar a escrita", "mejorar la redacción", "améliorer le style" → **Level 2**
- "deep edit", "rewrite for clarity", "reestruturar", "reescribir a fondo", "réécrire en profondeur", "native-level editing of the whole paper" → **Level 3**
If the wording is ambiguous between two levels, pick the lower one and offer the higher.

## Step 4 — Profile the author
Before changing anything, build the short style profile described in `authorial-style-preservation.md`.

## Step 5 — Edit
- Load the language profile (`language-profiles/<language>.md`) and the modules for the level.
- Work section by section for long documents; keep a running glossary of the author's terms to stay consistent across chunks.
- Protect, and never edit: citations, equations, code, numbers, table cells, figure content, URLs/DOIs, quoted text, reference list (E1–E3, E8).
- Flag ambiguity as `[AUTHOR CHECK: …]` instead of guessing (E7).

## Step 6 — Verify and report
1. Self-check against E1–E11.
2. If a shell is available and the original and edited texts can be saved as files, run
   `python3 scripts/check_edit_preservation.py original.txt edited.txt` and fix any reported change in numbers, citations, equations or URLs.
3. Deliver with `assets/templates/editing-report.md`:
   - **Level 1**: edited text + change log table (original → correction → category). For short texts, show inline changes.
   - **Level 2**: edited text + summary of change types + notable changes (max ~10) + flags.
   - **Level 3**: edited text + summary of structural changes (what moved/merged/split and why) + flags. Offer a Level 1 pass if the author wants a lighter version.
   - Always: language/variant used, level, preservation check result, and `[AUTHOR CHECK]` list.
4. Deliver long texts as a file in the author's format (Markdown, LaTeX source with commands untouched, or .docx via the available document tools — tracked changes when the author asks).

## Interaction with the other modes
| Mode | How editing integrates |
|---|---|
| 2 Draft a section | After drafting, an optional Level 2 pass in the manuscript language. The draft already follows the profile; do not over-polish placeholders. |
| 3 Review manuscript | Review reports *language quality* findings (Level 1 detection, categories and examples) but does not rewrite; offer mode 7 as a next step. |
| 4 Analyze research | Cards and tables are not "humanized"; only Level 1 corrections on the user's own synthesis text. |
| 5 / 6 | Methodology and experimental-plan prose may get a Level 2 pass on request. |
| Citation styles | Reference formatting stays with `../citation-styles/`; editing never reformats references. |
| Translation | Not a module of this skill. If the user asks for translation, translate faithfully, then apply the target-language profile at Level 1–2, keeping E1–E11. |

## AI-use disclosure
Editing with an AI assistant may need to be declared; point to `../extensions/ethics-data-and-ai-disclosure.md` when the author is preparing a submission. Never present the editing as a way to hide AI use (E9).
