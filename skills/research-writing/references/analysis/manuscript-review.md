# Mode 3 — Manuscript review rubric

Goal: evaluate the author's manuscript against the guideline and give actionable, prioritized feedback. Output with `assets/templates/review-report.md`.

## Procedure
1. **Identify** document type, language, venue/institution, citation style. Load the matching `document-types/` file.
2. **Automatic signals** (optional): `python3 scripts/check_manuscript.py <file> --type <article|thesis> --lang <pt|en>`. Treat its output as hints to verify, not verdicts.
3. **Section-by-section review** — for each section, rate each applicable rule:
   - **Meets** — present and adequate.
   - **Partial** — present but incomplete/weak (say what is missing).
   - **Missing** — absent.
   - **N/A** — not applicable to this document type (say why).
4. **Cross-section coherence** — check C1–C8 from `core-rules.md`; build the traceability chain: business problem → technical problem → objectives/RQs → hypotheses → method → results → discussion → conclusions.
5. **Integrity check** — citations without references and vice versa (C8); suspicious statistics (p-values without test, "significant" without test); claims with no support → mark `[CITATION NEEDED]`.
6. **Style** — W1–W5 (consistency, acronyms, figure references, hedging).
7. **Prioritize** — classify each issue:
   - **Critical**: would likely cause rejection/failure (missing evaluation, no hypotheses evaluated, results mixed with method, no gap/positioning, fabricated-looking data).
   - **Major**: weakens the work substantially (no business/technical distinction, table without proposal row, threats not revisited).
   - **Minor**: presentation, style, formatting.
8. **Report** — every issue has: location (section/paragraph/line or quote ≤ 15 words), rule ID, problem, concrete fix (rewrite suggestion when short).

## Section checklist (rule IDs)
| Section | Rules |
|---|---|
| Abstract & keywords | R01, R02, C7 |
| Introduction | R03–R10 (R10 depends on type and writer's decision) |
| Related work | R11–R13, C6 |
| Method | R14–R19, C1, C2 |
| Results | R20–R22, C3 |
| Discussion | R23–R28, C2–C4 |
| Conclusions | R29–R32, C5 |
| References | R33, C8 |
| Extensions (theses etc.) | objectives/RQs mapping, theoretical foundation, ethics, data availability, AI disclosure |

## Tone
Direct and constructive, as a careful advisor: start with the 2–3 main strengths, then issues by priority. Never rewrite the whole manuscript unless asked; offer to draft specific fixes.
