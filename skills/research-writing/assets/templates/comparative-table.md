# Comparative analysis table template

**Table X** – Comparison between related works and the proposed approach.

| Work | [Criterion 1] | [Criterion 2] | [Criterion 3] | [Technical characteristic] | [Evaluation] | Main limitation |
|---|---|---|---|---|---|---|
| Author A et al. [ref] | ✓ | ✗ | ◐ | [e.g., CNN] | [e.g., 1 dataset, accuracy] | [ ] |
| Author B et al. [ref] | ✗ | ✓ | ✗ | | | |
| Author C et al. [ref] | ◐ | ✓ | ✓ | | | |
| **This work (proposal)** | **✓** | **✓** | **✓** | **[ ]** | **[ ]** | **[honest limitation]** |

Legend: ✓ supported/addressed · ◐ partially · ✗ not addressed · — not reported.
Source: [the author(s)].

Rules:
- Last row is always the proposal (R13) and must match the Method (C6).
- Criteria come from the gaps identified in the cards; explain each criterion in the text.
- Do not hide criteria the proposal does not meet.

LaTeX hint: use `booktabs`; markers `\checkmark` (amssymb), `$\times$`, `$\circ$`; highlight the last row with `\rowcolor` (xcolor `table` option) or bold.
