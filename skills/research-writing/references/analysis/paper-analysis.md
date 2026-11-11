# Mode 4 — Analyzing research for Related Work

Implements the author's 4-part strategy (R11) and the comparative table (R13).

## Inputs
- The papers (PDF, text, DOI/link, or at least the abstract). Never analyze a paper you have not read or retrieved; never invent papers to complete the set (I1).
- A short description of the **user's proposal** (problem, approach, technologies, domain, evaluation). Parts 3 and 4 and the table depend on it — ask for it first if missing.
- Optional: the comparison criteria the user wants.

## Procedure
1. **Read each paper** focusing on: objective, method, technologies, dataset/participants, evaluation, results, stated limitations, future work.
2. **Fill one card per paper** (`assets/templates/related-work-card.md`):
   1. *Study overview* — purpose + 2–4 sentence synthesis.
   2. *Main contributions* — as claimed by the authors (attributed, not judged).
   3. *Relationship to the proposed work* — objectives, methodology, technologies, application domain: similar / different / partially.
   4. *Technical gaps and limitations* — (a) limitations admitted by the authors; (b) limitations identified by the analyst; (c) aspects the user's proposal considers that this work does not. Keep (a) and (b) separate.
   Add: full reference in the chosen style, evidence level (full text / abstract only), and quotes with page numbers if any.
3. **Derive comparison criteria** from the recurring gaps and from the proposal's distinctive features (5–8 criteria). Prefer objective, verifiable criteria.
4. **Build the comparative table** (`assets/templates/comparative-table.md`) — related works as rows, **proposal as the last row**, legend for markers, citation per row.
5. **Synthesis** — 1–2 paragraphs: what the field has solved, what remains open, and the precise gap the proposal fills (R12).
6. **Optional: write the Related Work section** (mode 2 with `sections/related-work.md`), grouping studies by theme.

## Also useful for
- Evaluating a research **project or proposal** someone else wrote: apply the 4-part card to it, then the manuscript-review rubric.
- Building a reading log during a literature review: one card per paper, kept in a file the user can extend.

## Quality checks
- Every card has all 4 parts (or states "not reported by the authors").
- The table criteria are explained and not cherry-picked; if the proposal does not satisfy a criterion, show it honestly.
- Proposal row claims match what the user actually built/plans (C6).
