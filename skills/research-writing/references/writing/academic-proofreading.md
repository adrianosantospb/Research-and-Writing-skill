# [EXTENSION] Module A — Advanced academic proofreading (Level 1 core)

Goal: detect and correct linguistic errors **without rewriting correct sentences** (E10).
Language-specific rules live in `language-profiles/`; this file defines the procedure and categories.

## What to check (categories used in the change log)
| Code | Category | Examples of what to look for |
|---|---|---|
| GR | Grammar and syntax | missing/extra words, wrong clause structure, run-on sentences, dangling modifiers, fragments |
| SP | Spelling and orthography | typos, accents/diacritics, official spelling (VOLP for pt-BR, RAE/ASALE, Académie/OQLF, US/UK spelling), hyphenation |
| PU | Punctuation | comma between subject and verb, missing comma after long introductory clauses, semicolon/colon use, quotation marks, profile typography (spaces in French) |
| TE | Verb tense consistency | tense conventions per section (see profile), unjustified tense shifts, sequence of tenses |
| AG | Agreement | subject–verb, noun–adjective, gender/number, participle agreement |
| PA | Prepositions and articles | wrong preposition/government, article use, contractions (pt *de + o*), *a* + article (pt crase) |
| SC | Sentence construction | awkward word order that causes a real error or ambiguity (not mere preference) |
| CV | Academic grammatical conventions | numbers and units formatting, abbreviations (e.g./i.e.), capitalization of headings, acronym definition at first use, list parallelism |

## Procedure
1. Read the whole passage once before correcting (some "errors" are intentional terms).
2. Mark protected spans (E1–E3, E8): citations, equations, code, numbers, quotations, URLs, table cells, LaTeX commands, the reference list.
3. Correct only actual errors. A sentence that is grammatical and clear stays as is, even if you would phrase it differently.
4. For each correction record: location, original, correction, category code, short reason (one line).
5. When a correction depends on intended meaning (e.g., which noun a pronoun refers to), flag `[AUTHOR CHECK: …]` instead.
6. Check consistency at document level: spelling variant, number format, acronym forms, term capitalization, hyphenation of the same compound.
7. Do not change regional variant unless asked; unify only inconsistencies.

## Precision rules
- Do not "correct" accepted variants (e.g., *data are/data is* when the venue accepts both — just make it consistent).
- Do not apply prescriptive myths (e.g., never splitting infinitives in English, never starting a sentence with "And/But" — prefer consistency with the author and venue).
- Respect technical usage that differs from general dictionaries (e.g., "dataset", "fine-tuning", *treinamento* vs *treino* chosen by the author).
- LaTeX: edit only running text; keep `\cite{}`, `\ref{}`, `~`, math mode and macros untouched.

## Output (Level 1)
Edited text + change log (`assets/templates/editing-report.md`). For very long documents, a change log grouped by category with counts and representative examples, plus the full corrected file.
