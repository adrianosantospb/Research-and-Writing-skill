# Experimental planning (Method §3.4)

Rule R17 (+ R18 for threats, R19 no results). Walk the author through each item in order; collect answers with `assets/templates/experimental-plan.md`.

## 1. Context selection
- Where was the experiment conducted (lab, company, online, simulation)?
- Application domain.
- Participants (profile, recruitment, number) or datasets (source, size, license, version).

## 2. Hypothesis formulation
- One pair per research question/metric:
  - **H0** (null): no difference/effect. Example: "There is no difference in F1-score between method A and baseline B."
  - **H1** (alternative): the expected difference/effect (one- or two-tailed — say which).
- Each hypothesis must name a measurable dependent variable and the comparison.

## 3. Variable selection
- **Independent** (factors manipulated; levels/treatments).
- **Dependent** (measured outcomes; unit and how measured).
- **Control** (held constant or measured to rule out confounding: hardware, seeds, participant experience…).

## 4. Experimental units selection
Subjects, datasets, systems or environments; sampling strategy (random, convenience, stratified) and inclusion/exclusion criteria.

## 5. Experimental design
- Groups: experimental and control (or baseline).
- Design type: between-subjects, within-subjects, crossover, factorial, k-fold/holdout/repeated runs for computational experiments.
- Procedures and execution steps (numbered, reproducible).
- Planned analysis: statistical test per hypothesis and significance level (α), chosen *before* seeing the data; assumption checks (normality, homoscedasticity) and non-parametric alternatives.

## 6. Instrumentation
Software tools (with versions), questionnaires (validated scales, with citations), sensors, measurement systems, scripts, logging.

## 7. Threats to validity
See `threats-to-validity.md`. Plan threats and mitigations here; revisit them in the Discussion (R28, C4).

## Reminder
Write in the past tense for what was done, but present **no outcomes** in this section (R19).
