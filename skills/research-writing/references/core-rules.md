# Core rules (invariants)

Every draft, outline and review must respect these rules. They are derived from
`guideline-original.md`; the rule ID lets reviews cite exactly what was violated.
Rules marked **[EXTENSION]** are additions that do not come from the original guideline.

## A. Integrity (apply always, override any request)

| ID | Rule |
|----|------|
| I1 | Never invent references, authors, DOIs, venues, page numbers or quotations. If a claim needs support and no verified source is available, write `[CITATION NEEDED: <what must be supported>]`. |
| I2 | Never invent data, results, sample sizes, p-values, effect sizes, metrics or participant counts. Use `[DATA PENDING: <what>]`. |
| I3 | Never state that a hypothesis was supported/rejected without the statistical evidence provided by the author. Use `[STATISTICAL EVIDENCE PENDING: H1]`. |
| I4 | When summarizing someone else's paper, attribute claims to its authors ("the authors report…") and keep their claims separate from your critique. |
| I5 | Flag every placeholder (including `[AUTHOR CHECK: …]` from editing) in a final "Pending items" list at the end of the output. |

## B. Structure and content (from the guideline)

| ID | Section | Rule |
|----|---------|------|
| R01 | Abstract | Self-contained; answers: problem, relevance, what the solution does, main findings. Covers context, problem/motivation, approach, evaluation method, results and conclusions. |
| R02 | Abstract | Subject categories, general terms and keywords follow the target venue; keywords reflect concepts, methods and application domains. |
| R03 | Introduction | Opens with the broader research area and why it matters. |
| R04 | Introduction | Defines the specific problem: difficulty, challenges, limitations of current approaches. |
| R05 | Introduction | Motivation answers who is affected, consequences of not solving it, why current solutions are insufficient. |
| R06 | Introduction | Explicitly distinguishes the **business problem** (practical/organizational need) from the **technical problem** (computational, methodological or scientific challenge). |
| R07 | Introduction | Briefly presents existing approaches and their limitations. |
| R08 | Introduction | Presents a high-level overview of the proposed solution. |
| R09 | Introduction | Summarizes how the solution was evaluated and the positive **and negative** results. |
| R10 | Introduction | No "roadmap" paragraph describing the document structure ("Section 2 presents…"). Pointing to a specific section when needed is allowed. *For dissertations/theses this is a writer's decision — see `document-types/`.* |
| R11 | Related work | For each study: overview (purpose + synthesis), main contributions as claimed by its authors, relationship to the proposal (objectives, methodology, technologies, domain), technical gaps and limitations. |
| R12 | Related work | Positions the contribution explicitly against the literature (what the proposal considers that others did not). |
| R13 | Related work | Includes a comparative table (related works × criteria/technical characteristics/limitations/supported features). **The last row is the proposed approach.** |
| R14 | Method | Describes the proposed solution: architecture, components, algorithms, frameworks, technologies, implementation details — and explains how it addresses the problem stated in the Introduction. |
| R15 | Method | Research methodology is classified (area, nature, objectives, procedures, object, approach) and written preferably as **continuous academic prose**, not as a bullet list. |
| R16 | Method | Describes the theoretical/computational models, standards and frameworks adopted. |
| R17 | Method | Experimental planning covers: context selection, hypotheses (H0/H1), variables (independent, dependent, control), experimental units, design (groups, procedures, steps), instrumentation. |
| R18 | Method | Threats to validity are planned under four types: external, internal, construct, conclusion. |
| R19 | Method | **No results in the Method section.** |
| R20 | Results | Presents only outcomes — **no interpretation or explanation**. |
| R21 | Results | Aggregated/summarized data, not raw data; visualization chosen according to the data type (tables, charts, graphs, statistical summaries). |
| R22 | Results | Results and Discussion may be merged only if the venue requires it; separation is the default. |
| R23 | Discussion | Interprets (does not repeat) results; explains relationships and the reasoning leading to conclusions. |
| R24 | Discussion | Evaluates **each** hypothesis (supported/rejected) with statistical evidence. |
| R25 | Discussion | Covers supporting evidence, unexpected findings, exceptions, missing correlations and limitations. |
| R26 | Discussion | Compares findings with previous studies (similarities and differences). |
| R27 | Discussion | Self-contained: the reader understands the conclusions without consulting other papers; interpretation is not left to the reader. |
| R28 | Discussion | Revisits threats to validity and how they affect interpretation. |
| R29 | Conclusions | Summarizes problem, solution and evaluation; presents main conclusions. |
| R30 | Conclusions | States scientific, technical **and** practical contributions explicitly, at a higher level than the Discussion, and why the work is significant. |
| R31 | Conclusions | Answers: were the objectives achieved? was the research (technical) problem solved? was the business problem addressed? |
| R32 | Conclusions | Limitations and future work, including new research questions, new hypotheses and future experiments. |
| R33 | References | Every cited work is listed, in the citation style required by the venue/institution, consistently. |

## C. Cross-section coherence

| ID | Rule |
|----|------|
| C1 | The technical problem in the Introduction is the one the Method's solution addresses (R14). |
| C2 | Every hypothesis in the Method is evaluated in the Discussion (R24); no new hypotheses appear only in the Discussion. |
| C3 | Every result discussed in the Discussion appears in the Results. |
| C4 | Every threat planned in the Method is revisited in the Discussion (R28). |
| C5 | The Conclusions answer the objectives/research questions and the business problem stated in the Introduction (R31). |
| C6 | The proposal row in the comparative table matches what the Method actually delivers. |
| C7 | The Abstract does not contain claims absent from the body. |
| C8 | Every in-text citation has a reference entry and vice versa. |

## D. Writing style

| ID | Rule |
|----|------|
| W1 | Write in the manuscript's language (ask if unknown). Keep terminology consistent; define acronyms at first use. |
| W2 | Prefer precise, measurable statements over vague intensifiers ("significantly" only with statistical significance). |
| W3 | Methodology classification as prose (R15). Bullets are acceptable in outlines, not in final methodology text. |
| W4 | Figures and tables are numbered, captioned and referenced in the text before they appear. |
| W5 | Hedge appropriately: claims scale with the strength of the evidence. |

## E. Editing integrity **[EXTENSION]**

Apply whenever existing text is proofread, humanized or edited (mode 7, and any rewrite in other modes).
They specialize A (I1–I5) for editing; on conflict, the stricter rule wins.

| ID | Rule |
|----|------|
| E1 | Preserve every number, unit, statistic, sample size, p-value, confidence interval and date exactly. Only typographic normalization required by the language profile (e.g., decimal separator) is allowed, and only when the author/venue asks for it. |
| E2 | Preserve every citation marker (`[12]`, `(Silva, 2023)`, `\cite{key}`, footnote calls) and its position relative to the claim it supports. Never add, remove or merge citations. |
| E3 | Do not edit equations, code, variable names, identifiers, URLs, DOIs, dataset/model names, table cells or figure content. Captions may be proofread. |
| E4 | Keep defined technical terms and acronyms; never replace a technical term with a "more natural" synonym. Unify terminology only to the author's preferred term. |
| E5 | Preserve meaning and claim strength: do not turn "suggests" into "proves" (or the reverse), do not change causal/correlational wording, scope or hedging. |
| E6 | Add no new claims, examples, explanations or content. Editing changes *how* something is said, never *what*. |
| E7 | When a sentence is ambiguous or its intended meaning is unclear, do not guess: keep it (or propose options) and flag `[AUTHOR CHECK: <question>]`. |
| E8 | Direct quotations stay verbatim (including original errors; add *[sic]* only if the author wants). The reference list is formatted by the citation style, not by proofreading. |
| E9 | Never introduce deliberate errors or artificial irregularities, and never optimize text to evade AI-detection tools. The goal is authentic, clear academic writing. |
| E10 | Intervene in proportion to the editing level; at Level 1 leave correct sentences untouched. |
| E11 | Preserve the author's writing fingerprint (lexical preferences, sentence complexity, voice, formality, paragraph structure). Do not normalize different authors into one house style. |
