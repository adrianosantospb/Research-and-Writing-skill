# [EXTENSION] ABNT (Brazil)

## Standards to check (confirm the editions adopted by the institution)
- **NBR 6023** — references. 3rd edition published in **May 2025** (NBR 6023:2025); many institutions still adopt **NBR 6023:2018** (with errata). Ask which one.
- **NBR 10520:2023** — citations in documents (replaced the 2002 edition).
- **NBR 14724** — academic works (TCC, dissertation, thesis) presentation; updated edition released in Dec 2024 (some manuals cite it as 2024, others as 2025).
- NBR 6028:2021 (abstracts), NBR 6024 (section numbering), NBR 6027 (table of contents), NBR 6022 (articles in periodicals), NBR 10719 (technical reports).
- Institutional manuals (library guides) may adapt the norms — they take precedence for the student.

## In-text citations (NBR 10520:2023)
- Author-date system (most common) or numeric system — never mixed.
- **Since 2023, author names inside parentheses are no longer in uppercase**:
  - Parenthetical: (Silva, 2023) · (Silva; Souza, 2023) · (Silva *et al.*, 2023)
  - Narrative: Silva (2023) states that…
  - Direct quotation: page is mandatory — (Silva, 2023, p. 45).
  - Direct quotations > 3 lines: separate block, 4 cm indent, smaller font, no quotation marks.
  - Multiple works same author/year: (Silva, 2023a, 2023b).
  - Institutional author: (Associação Brasileira de Normas Técnicas, 2023) or acronym if defined.
  - Citation of citation: (Silva, 2010 *apud* Souza, 2023) — use sparingly.

## Reference list (NBR 6023) — format examples (fictitious placeholders)
- Book: SOBRENOME, Nome. **Título do livro**: subtítulo. 2. ed. Cidade: Editora, 2024.
- Chapter: SOBRENOME, Nome. Título do capítulo. *In*: SOBRENOME, Nome (org.). **Título do livro**. Cidade: Editora, 2024. p. 10-25.
- Journal article: SOBRENOME, Nome; SOBRENOME, Nome. Título do artigo. **Nome do Periódico**, Cidade, v. 12, n. 3, p. 45-60, 2024. DOI: 10.xxxx/xxxxx.
- Conference paper: SOBRENOME, Nome. Título do trabalho. *In*: NOME DO EVENTO, 10., 2024, Cidade. **Anais** [...]. Cidade: Editora, 2024. p. 1-10. DOI: ….
- Thesis/dissertation: SOBRENOME, Nome. **Título**. 2024. Tese (Doutorado em Ciência da Computação) – Instituto, Universidade, Cidade, 2024.
- Website: SOBRENOME, Nome (or INSTITUIÇÃO). **Título da página**. Cidade, 2024. Disponível em: URL. Acesso em: 10 nov. 2026.
- Software/dataset: AUTOR. **Nome do software/dataset**. Versão 1.2. [*S. l.*]: Editora/Repositório, 2024. Disponível em: URL.
- Up to 3 authors: list all; 4 or more: may list all or first author + *et al.* (be consistent).
- Title element in **bold** (or another consistent highlight); list in alphabetical order (author-date system); left-aligned, single spacing, blank line between entries.

## Tools
- LaTeX: **abnTeX2** (`abntex2` class + `abntex2cite`) or **biblatex-abnt** (`\usepackage[style=abnt]{biblatex}`). Check whether the package version implements NBR 10520:2023 (mixed-case names).
- Zotero/Mendeley: CSL "Associação Brasileira de Normas Técnicas" (choose the variant matching the institution).
