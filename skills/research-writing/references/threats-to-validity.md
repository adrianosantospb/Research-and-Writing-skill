# Threats to validity

Rules R18 (plan in Method) and R28 (revisit in Discussion). Four types from the guideline:

| Type | Guiding question (guideline) | Typical threats | Typical mitigations |
|---|---|---|---|
| **External** | Can the results be generalized to other contexts? | Single dataset/domain; convenience sample; students instead of practitioners; lab vs. real setting | Multiple datasets/sites; describe context precisely; replication package |
| **Internal** | Could factors other than the proposed method influence the results? | Confounding variables; selection bias; learning/fatigue effects; data leakage; tuning the proposal more than baselines | Randomization; control groups; counterbalancing; same tuning budget for all methods; leakage checks |
| **Construct** | Are the measurements appropriate representations of the concepts evaluated? | Metric that does not capture the concept; non-validated questionnaire; mono-method bias | Multiple metrics; validated instruments; operational definitions |
| **Conclusion** | Are the statistical analyses and conclusions reliable? | Low statistical power; violated test assumptions; multiple comparisons; random seeds | Power analysis; assumption checks; corrections (Bonferroni/Holm); repeated runs, CIs and effect sizes |

## How to write
- Method: for each type, list the threats you anticipated and how the design mitigates them.
- Discussion: for each threat, state whether it materialized and how it limits the interpretation.
- Be honest; reviewers distrust "no threats were identified".

[EXTENSION] Qualitative studies often use trustworthiness criteria (credibility, transferability, dependability, confirmability); see `extensions/qualitative-and-mixed-methods.md`. Keep the four types when the venue expects them.
