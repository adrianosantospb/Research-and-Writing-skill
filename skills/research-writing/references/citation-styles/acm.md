# ACM Reference Format

Used by ACM conferences and journals (computing). Always use the official `acmart` template.

## In-text
- Default numeric for most proceedings: [1], [2, 5]; some ACM journals use author-year (natbib `\citet`, `\citep`). The `acmart` class decides — follow the template option (`sigconf`, `acmsmall`, …).

## Reference list — format examples (fictitious)
- Journal: Ana Silva and John Smith. 2024. Title of the Article. *ACM Trans. Softw. Eng. Methodol.* 33, 4, Article 98 (May 2024), 30 pages. https://doi.org/10.1145/xxxxxxx
- Proceedings: Ana Silva, John Smith, and Lee Wong. 2024. Title of the Paper. In *Proceedings of the 46th International Conference on Software Engineering (ICSE '24)*. ACM, New York, NY, USA, 1–12. https://doi.org/10.1145/xxxxxxx
- Book: Ana Silva. 2023. *Title of the Book*. Publisher, City.
- Online: Ana Silva. 2024. Title of the Page. Retrieved November 10, 2026 from URL
- Full first names, year after authors, DOI as URL.

## Metadata
- ACM CCS concepts (2012 CCS) and keywords are required: generate the CCS block via the ACM CCS tool; never invent codes (`[CATEGORY PENDING: ACM CCS]`).
- Note: the guideline's example "D.3.3 Programming Languages" belongs to the older 1998 ACM CCS; most current ACM venues require the 2012 CCS.

## Tools
LaTeX: `\documentclass[sigconf]{acmart}` + `\bibliographystyle{ACM-Reference-Format}`. Zotero/Mendeley: CSL "Association for Computing Machinery".
