# Scientific Article and Report Writing Template (source guideline)

> **Source of truth.** This file is a faithful Markdown conversion of the author's guideline
> *"Article and Report Structure and Writing Guidelines"* (v1.0).
> Author: Adriano Araujo Santos, PhD. Every rule in this skill derives from this file.
> Anything added beyond it lives in `references/extensions/`, `references/document-types/`
> or `references/citation-styles/` and is labeled **[EXTENSION]**.
> When an extension conflicts with this file, this file wins for articles and reports.

## Description

This template provides a structured guideline for the development of scientific articles and technical research reports. Its purpose is to support researchers throughout the writing process by organizing the main sections of a scientific publication and defining the key elements that should be addressed in each section.

The template follows a standard scientific writing structure commonly adopted in areas such as Computer Science, Engineering, Health Technology, and Applied Sciences. It guides authors from the initial presentation of the research problem and motivation through the description of the proposed solution, methodological procedures, experimental evaluation, analysis of results, and final conclusions.

Each section includes recommendations regarding the type of information that should be presented, the expected level of detail, and the relationship between sections. The template emphasizes the importance of clearly defining the research problem, positioning the work in relation to existing literature, describing a rigorous evaluation methodology, distinguishing between results and interpretation, and explicitly presenting scientific contributions and limitations.

This guideline can be used as a reference during the planning, writing, and revision phases of scientific manuscripts and reports, helping authors produce documents that are clear, coherent, reproducible, and aligned with academic publication standards.

## ABSTRACT

The abstract should be concise and self-contained. It should answer the following questions:

- **What is the problem addressed by the study?**
- **Why is this problem relevant and interesting?**
- **What does the proposed solution do?**
- **What are the main findings and results obtained?**

The abstract should briefly present:

- The research context;
- The problem and motivation;
- The proposed approach or solution;
- The evaluation method;
- The main results and conclusions.

### Subject Categories and Descriptors

Include the appropriate categories according to the target conference or journal classification system.

Example:

- **D.3.3 Software and Its Engineering – Programming Languages**
- **Health and Work**
- **Health and Technology**
- Other categories relevant to the research domain.

### General Terms

Use the terms required by the target conference or publication venue.

### Keywords

Select the most representative terms related to the research topic. Keywords should reflect the main concepts, methods, and application domains of the work.

## 1. INTRODUCTION

The introduction should establish the research context and motivate the study. It should include:

### General Statement of the Research Area

Introduce the broader research domain and explain the importance of the topic.

### Description of the Specific Problem

Clearly define the problem addressed by the research. Discuss:

- The difficulty involved;
- The existing challenges;
- The limitations of current approaches.

### Problem Importance and Motivation

Explain why solving this problem matters:

- Who is affected by this problem?
- What are the consequences of leaving it unresolved?
- Why are current solutions insufficient?

Distinguish between:

- **Business problem:** practical motivation, organizational impact, or real-world needs.
- **Technical problem:** the computational, methodological, or scientific challenge that must be solved.

### Existing Approaches and Limitations

Provide a brief overview of traditional or state-of-the-art solutions and explain their limitations.

### Proposed Solution Overview

Present a high-level description of the proposed approach.

### Evaluation Overview

Briefly summarize:

- How the solution was evaluated;
- What positive and negative results were obtained.

Avoid describing the article structure explicitly (e.g., "Section 2 presents…"), since well-defined section titles already communicate the organization of the paper. However, references to specific sections may be used, when necessary, throughout the introduction.

## 2. RELATED WORK

This section should critically analyze previous research related to the proposed work. For each relevant study, address:

### Study Overview

- What is the main purpose of the work?
- Provide a concise synthesis of the research.

### Main Contributions

- Describe the contributions claimed by the authors.
- Clearly state what the original authors identify as their main achievements.

### Relationship to the Proposed Work

Discuss all relevant similarities between the previous study and your research, including:

- Similar objectives;
- Similar methodologies;
- Similar technologies;
- Similar application domains.

### Technical Gaps and Limitations

Identify:

- Technical problems not addressed by previous works;
- Limitations of existing approaches;
- Aspects considered in your proposal that were not considered previously.

This section should clearly position your contribution in relation to existing literature.

### Comparative Analysis Table

Create a comparison table based on:

- Related works;
- Evaluation criteria;
- Technical characteristics;
- Limitations;
- Supported features.

The final row of the table should present your proposed approach.

## 3. METHOD

This section describes the proposed solution and how it was evaluated.

### 3.1 Proposed Solution

Describe the developed solution, including:

- Architecture;
- Main components;
- Algorithms;
- Frameworks;
- Technologies;
- Implementation details.

Explain how the proposed approach addresses the problem identified in the introduction.

### 3.2 Research Methodology

Describe the methodology adopted to evaluate the proposed solution. Although different classifications may be presented, this section should preferably be written as continuous academic text. The research can be classified according to:

- **Research Area:** Theoretical research; Methodological research; Empirical research; Practical research.
- **Research Nature:** Original scientific research; Survey or review research.
- **Research Objectives:** Exploratory research; Descriptive research; Explanatory research.
- **Research Procedures:** Field research; Document-based research.
- **Research Object:** Bibliographic research; Laboratory research; Field research.
- **Research Approach:** Quantitative approach; Qualitative approach; Mixed-method approach.

### 3.3 Models and Frameworks Used

Describe the theoretical or computational models adopted in the research. Examples: Standards; Frameworks; Conceptual models; Evaluation models; Software engineering models.

### 3.4 Experimental Planning

Describe the complete experimental design. The planning should include:

- **Context Selection** — Where the experiment was conducted; the application domain; the participants or datasets involved.
- **Hypothesis Formulation** — Define the research hypotheses. Example: Null hypothesis (H0); Alternative hypothesis (H1).
- **Variable Selection** — Independent variables; Dependent variables; Control variables.
- **Experimental Units Selection** — The subjects, datasets, systems, or environments used in the experiment.
- **Experimental Design** — Experimental groups; Control groups; Procedures; Execution steps.
- **Instrumentation** — Tools and instruments used for data collection. Examples: Software tools; Questionnaires; Sensors; Measurement systems.
- **Validity Assessment (Threats to Validity)** — Discuss possible threats according to:
  - **External Validity:** Can the results be generalized in other contexts?
  - **Internal Validity:** Could factors other than the proposed method influence the results?
  - **Construct Validity:** Are the measurements appropriate representations of the concepts being evaluated?
  - **Conclusion Validity:** Are the statistical analyses and conclusions reliable?

**Important:** Do not present results in this section.

## 4. RESULTS

This section presents experimental outcomes.

Guidelines:

- Present only the results.
- Avoid interpretation or explanation.
- Interpretation belongs to the Discussion section.

Answer:

- What was obtained from the experiments?
- What data was collected?
- What are the measured outcomes?

Recommendations:

- Present summarized and aggregated data rather than raw data.
- Use appropriate visualizations: Tables; Charts; Graphs; Statistical summaries.

Select the most appropriate visualization according to the type of data. A concise results section may follow the principle: "The results are shown in Figure 1."

**Note:** Results and Discussion may be combined into a single section if required by the publication venue. However, separating them often improves clarity.

## 5. DISCUSSION

This section interprets and explains the results. It should:

- **Interpret Results** — Do not simply repeat the results. Explain their meaning.
- **Explain Relationships** — Identify relationships among findings and explain the logical reasoning that leads to conclusions.
- **Evaluate Hypotheses** — For each hypothesis: determine whether it can be rejected or supported; provide statistical evidence.
- **Discuss Findings** — Include: evidence supporting conclusions; unexpected findings; exceptions; missing correlations; limitations.
- **Compare with Previous Studies** — Discuss similarities and differences between your findings and previous publications.
- **Provide a Self-Contained Discussion** — The reader should understand your conclusions without needing to consult other papers. Avoid leaving interpretation for the reader.
- **Evaluate Threats to Validity** — Discuss how validity threats may affect the interpretation of results.

## 6. CONCLUSIONS

This section should summarize the overall contribution of the research. A good conclusion should include:

### Research Summary

Briefly summarize: the problem investigated; the proposed solution; the evaluation performed.

### Main Conclusions

Present the final conclusions derived from the research.

### Contributions

Explicitly state: Scientific contributions; Technical contributions; Practical contributions.

Provide a higher-level evaluation than the Discussion section and explain why the work is significant. Address:

- Were the original objectives achieved?
- Was the research problem solved?
- Was the business problem addressed?

### Limitations and Future Work

Discuss: remaining limitations; open challenges; possible improvements; future research directions. Include: new research questions; new hypotheses; future experiments.

## REFERENCES

List all cited references according to the required citation style of the target conference or journal. Examples: ACM Reference Format; IEEE Reference Style; APA Style; Springer LNCS Style.
