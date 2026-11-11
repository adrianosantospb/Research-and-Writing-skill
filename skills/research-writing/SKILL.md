---
name: research-writing
description: Plan, write, review, analyze and edit scientific work (articles, reports, TCC, dissertations, theses, proposals) with a structured guideline. Use to outline or draft sections, plan experiments, review a manuscript, analyze papers for related work, or proofread, humanize and refine academic text in Portuguese (BR), Spanish, French or English at three editing levels, preserving the author's style. Supports ABNT, ACM, IEEE, APA, Vancouver, LNCS, Chicago, Harvard.
license: MIT
metadata:
  author: Adriano Araujo Santos
  version: "1.1.0"
---

# Research Writing

Helps researchers plan, write, review, analyze and edit scientific documents following the author's guideline
(`references/guideline-original.md`, the source of truth). Content beyond it is labeled **[EXTENSION]**.

## Non-negotiable rules
Read `references/core-rules.md` before producing any manuscript text or review. Above all:
- **Never fabricate** references, data, statistics, results or quotations. Use placeholders:
  `[CITATION NEEDED: …]`, `[DATA PENDING: …]`, `[STATISTICAL EVIDENCE PENDING: …]`, `[MISSING FIELD: …]`,
  and end the output with a **Pending items** list.
- Results contain no interpretation; Method contains no results; Discussion interprets and evaluates every hypothesis.
- Introduction separates the **business problem** from the **technical problem**.
- Related Work: 4-part analysis per study; comparative table whose **last row is the proposal**.
- Research methodology is written as continuous prose.
- Conclusions state scientific, technical and practical contributions and answer whether objectives, the research problem and the business problem were addressed.
- When editing existing text, follow the editing-integrity rules **E1–E11**: never change numbers, citations, equations, technical terms or the meaning/strength of claims; flag ambiguity as `[AUTHOR CHECK: …]`; never optimize text to evade AI detectors.

## Step 1 — Establish the context (ask only what is missing)
1. **Document type**: article, technical report, TCC/monograph, dissertation, thesis, research proposal/qualification.
2. **Language** of the manuscript (answer the user in their language; write the manuscript in its language).
3. **Target venue or institution** and **citation style**.
4. **Stage**: idea, outline, partial draft, full draft.
For dissertations/theses, also ask whether the program expects an "Organization of the work" paragraph at the end of the Introduction — **the writer decides** (the guideline forbids it for articles).

## Step 2 — Pick the mode

| User intent | Mode | Load |
|---|---|---|
| "Structure / outline / plan my paper or thesis" | **1. Plan** | `references/document-types/<type>.md`, `assets/templates/article-outline.md` or `thesis-outline.md` |
| "Write the Introduction / Method / …", "fix the content/structure of a section" | **2. Draft a section** | `references/sections/<section>.md` (+ related refs listed in it) |
| "Review / evaluate / check my manuscript" | **3. Review manuscript** | `references/analysis/manuscript-review.md`, `assets/templates/review-report.md`, `scripts/check_manuscript.py` |
| "Analyze these papers / build related work / comparison table" | **4. Analyze research (related work)** | `references/analysis/paper-analysis.md`, `assets/templates/related-work-card.md`, `assets/templates/comparative-table.md` |
| "Classify my research methodology" | **5. Classify methodology** | `references/methodology-taxonomy.md` |
| "Plan my experiment / hypotheses / threats" | **6. Experimental planning** | `references/experimental-planning.md`, `references/threats-to-validity.md`, `assets/templates/experimental-plan.md` |
| "Proofread / correct grammar", "humanize / make it more natural", "improve the writing / style", "deep edit", "native-level English/Spanish/French/Portuguese" | **7. Academic editing** [EXTENSION] | `references/writing/multilingual-editing.md` first; it says which other `references/writing/` files to load |
| Citation or reference formatting | (any mode) | `references/citation-styles/<style>.md` |

Modes can chain (e.g., 4 → 2 to write Related Work from the analyzed papers; 6 → 2 to write §3.4; 2 → 7 to polish a draft).
**Mode 2 vs. 7**: if the request changes *what* a section contains (missing elements, structure per the guideline), use mode 2; if it only changes *how* existing text is written (language, fluency, style), use mode 7. When both are asked, do mode 2 first, then mode 7.

## Mode procedures

**1. Plan** — Build the outline for the document type. Under each heading, list the guideline elements to cover and the questions the author must answer. Mark which information is already available and which is missing.

**2. Draft a section** — Collect the inputs listed in the section file; ask for the missing essentials (max 3–5 questions) or proceed with placeholders if the user prefers. Draft, then run the section's self-check and list unmet rule IDs.

**3. Review manuscript** — If the manuscript is a file and a shell is available, run
`python3 scripts/check_manuscript.py <file> [--type article|thesis] [--lang auto|en|pt|es|fr]` (accepts .md, .txt, .tex; convert .docx/.pdf to text first) for automatic signals. Then perform the full rubric review (judgment cannot be replaced by the script). Output with `assets/templates/review-report.md`: per-section status (Meets / Partial / Missing), issues with location + rule ID + concrete fix, cross-section coherence (C1–C8), and prioritized actions.

**4. Analyze research** — For each paper supplied (PDF, text, link, or abstract), fill a related-work card with the 4 parts (overview, claimed contributions, relationship to the user's proposal, gaps). Ask for the user's proposal summary first if unknown — parts 3 and 4 depend on it. Then consolidate the comparative table (last row = proposal) and, if asked, write the Related Work prose. Only analyze papers provided or retrieved and verified; state when the analysis is based on the abstract only.

**5. Classify methodology** — Classify on the six dimensions with justification, check consistency, write the paragraph(s) as prose.

**6. Experimental planning** — Walk through context, hypotheses (H0/H1), variables, units, design, instrumentation, threats; produce the plan and, if asked, the §3.4 text.

**7. Academic editing** [EXTENSION] — Follow `references/writing/multilingual-editing.md`: identify the language and regional variant, choose the level (**1 Proofreading**, **2 Academic enhancement — default**, **3 Deep academic editing**), profile the author's style, load only the modules that level needs, edit, verify preservation (`scripts/check_edit_preservation.py original edited` when a shell is available) and report with `assets/templates/editing-report.md`. Load only the language profile of the text being edited.

## Extensions (load when relevant)
- `references/extensions/objectives-and-research-questions.md` — objectives, RQs (theses, proposals).
- `references/extensions/theoretical-foundation.md` — theory chapter (theses/dissertations/TCC).
- `references/extensions/systematic-review.md` — survey/review research (PRISMA, Kitchenham).
- `references/extensions/qualitative-and-mixed-methods.md` — non-experimental designs.
- `references/extensions/ethics-data-and-ai-disclosure.md` — ethics committee (CEP/IRB), data availability, AI-use statement.
- `references/extensions/title.md` — titles.

## Output conventions
- Manuscript text in the manuscript language; explanations to the user in the user's language.
- Prefer delivering long manuscripts as files (Markdown or LaTeX as the user prefers); short sections inline.
- Always finish drafts/reviews with **Pending items** (placeholders) and **Unmet rules** (IDs), when any.
