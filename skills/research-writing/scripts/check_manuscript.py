#!/usr/bin/env python3
"""Heuristic structure checks for scientific manuscripts (research-writing skill).

Reads a Markdown, LaTeX or plain-text manuscript (English or Portuguese), splits it
into sections and reports signals related to the guideline rules (core-rules.md).
The output is a list of HINTS to be verified by a human/agent, not a verdict.

Usage:
    python3 check_manuscript.py FILE [--type article|report|thesis] [--lang en|pt|auto] [--json]

Standard library only. Convert .docx/.pdf to text before running.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from dataclasses import dataclass, field, asdict


def norm(text: str) -> str:
    """Lowercase and strip accents for robust matching."""
    text = unicodedata.normalize("NFKD", text)
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


# --------------------------------------------------------------------------- sections
SECTION_KEYS = {
    "abstract": ["abstract", "resumo", "summary"],
    "introduction": ["introduction", "introducao"],
    "background": ["background", "fundamentacao teorica", "referencial teorico", "theoretical foundation"],
    "related_work": ["related work", "trabalhos relacionados", "estado da arte", "related works", "literature review", "revisao da literatura"],
    "method": ["method", "methodology", "metodologia", "metodo", "materials and methods", "materiais e metodos", "proposed solution", "proposta", "experimental design", "evaluation design"],
    "results": ["results", "resultados"],
    "discussion": ["discussion", "discussao"],
    "conclusions": ["conclusion", "conclusions", "conclusao", "conclusoes", "consideracoes finais", "final remarks", "concluding remarks"],
    "references": ["references", "referencias", "bibliography", "bibliografia"],
}
REQUIRED = ["abstract", "introduction", "related_work", "method", "results", "discussion", "conclusions", "references"]

HEADING_PATTERNS = [
    re.compile(r"^\s{0,3}(#{1,3})\s+(.+?)\s*#*\s*$"),                       # Markdown
    re.compile(r"^\s*\\(chapter|section|subsection)\*?\{(.+?)\}"),          # LaTeX
    re.compile(r"^\s*((?:\d+\.)*\d+\.?)\s+([A-ZÀ-Ý][^\n]{2,80})$"),        # "1 INTRODUCTION" / "3.2 Método"
    re.compile(r"^\s*([A-ZÀ-Ý][A-ZÀ-Ý \-]{3,60})\s*$"),                    # "ABSTRACT" all caps line
]


@dataclass
class Section:
    key: str | None
    title: str
    level: int
    start_line: int
    text: str = ""


def classify(title: str) -> str | None:
    t = norm(re.sub(r"^[\d.\s]+", "", title)).strip(" :.")
    # results-and-discussion merged
    if ("result" in t and "discuss" in t) or ("resultado" in t and "discuss" in t):
        return "results_discussion"
    for key, names in SECTION_KEYS.items():
        for name in names:
            if t == name or t.startswith(name + " ") or t.startswith(name + ":"):
                return key
    return None


def split_sections(lines: list[str]) -> list[Section]:
    sections: list[Section] = [Section(None, "(front matter)", 0, 1)]
    for i, line in enumerate(lines, start=1):
        is_heading = False
        for idx, pat in enumerate(HEADING_PATTERNS):
            m = pat.match(line)
            if not m:
                continue
            if idx == 0:
                level, title = len(m.group(1)), m.group(2)
            elif idx == 1:
                level = {"chapter": 1, "section": 1, "subsection": 2}[m.group(1)]
                title = m.group(2)
            elif idx == 2:
                level, title = m.group(1).rstrip(".").count(".") + 1, m.group(2)
            else:
                level, title = 1, m.group(1)
            key = classify(title)
            # subsections stay inside their parent unless they are themselves a known section
            if level > 1 and key in (None, "method"):
                break
            if idx >= 2 and key is None:
                break  # numbered/all-caps line that is not a known section: treat as text
            sections.append(Section(key, title.strip(), level, i))
            is_heading = True
            break
        if not is_heading:
            sections[-1].text += line + "\n"
    return sections


def merged(sections: list[Section]) -> dict[str, tuple[str, int]]:
    """Return {key: (text, first_line)} concatenating top-level sections with the same key."""
    out: dict[str, tuple[str, int]] = {}
    current = None
    for s in sections:
        if s.key:
            current = s.key
        if current is None:
            continue
        keys = ["results", "discussion"] if current == "results_discussion" else [current]
        for k in keys:
            text, line = out.get(k, ("", s.start_line))
            out[k] = (text + s.text, line)
    return out


# --------------------------------------------------------------------------- findings
@dataclass
class Finding:
    rule: str
    severity: str  # warning | info
    section: str
    message: str
    evidence: list[str] = field(default_factory=list)


def find_sentences(text: str, patterns: list[str], limit: int = 5) -> list[str]:
    sentences = re.split(r"(?<=[.!?])\s+|\n{2,}", text)
    hits = []
    for s in sentences:
        ns = norm(s)
        if any(re.search(p, ns) for p in patterns):
            snippet = " ".join(s.split())
            hits.append(snippet[:160] + ("…" if len(snippet) > 160 else ""))
            if len(hits) >= limit:
                break
    return hits


ROADMAP = [
    r"\b(section|secao|capitulo|chapter)\s+\d+\s+(presents|describes|discusses|apresenta|descreve|discute|traz)",
    r"(the )?(rest|remainder) of (this|the) (paper|article|work|report|thesis) (is|are) (organized|structured)",
    r"(this|the) (paper|article|work|report) is (organized|structured) as follows",
    r"(o )?restante deste (trabalho|artigo|documento|relatorio)",
    r"(este|o presente) (trabalho|artigo|documento) (esta|encontra-se) (organizado|estruturado)",
    r"organizacao do (trabalho|texto|documento)",
]
RESULT_IN_METHOD = [
    r"\b(achiev\w*|obtain\w*|reach\w*|outperform\w*|alcan\w*|obtev\w*|atingi\w*|superou)\b[^.]{0,80}\d+([.,]\d+)?\s?%",
    r"\b(results|the experiment|os resultados|o experimento)\s+(show\w*|indicat\w*|demonstrat\w*|mostr\w*|indic\w*|demonstr\w*)",
    r"\bp\s?[<=]\s?0?[.,]\d+",
]
INTERPRETATION = [
    r"\bthis (shows|indicates|suggests|demonstrates|means|implies)\b",
    r"\b(which|that) (means|suggests|indicates|implies)\b",
    r"\b(because|due to|this is explained|surprisingly|as expected|interestingly)\b",
    r"\b(isto|isso|o que) (mostra|indica|sugere|demonstra|significa|implica)\b",
    r"\b(devido a|porque|explica-se|surpreendentemente|como esperado|curiosamente)\b",
]
PROPOSAL_ROW = [r"this work", r"our (approach|proposal|method|work)", r"proposed", r"\bproposal\b", r"este trabalho", r"nossa (abordagem|proposta)", r"\bproposta\b", r"presente trabalho"]
THREATS = {
    "external": [r"external validity", r"validade externa"],
    "internal": [r"internal validity", r"validade interna"],
    "construct": [r"construct validity", r"validade de construto", r"validade de constructo"],
    "conclusion": [r"conclusion validity", r"validade de conclusao", r"statistical conclusion validity"],
}
CONTRIB = {
    "scientific": [r"scientific contribution", r"contribuic\w* cientific", r"contribuic\w*[^.]{0,40}cientific"],
    "technical": [r"technical contribution", r"contribuic\w* tecnic", r"contribuic\w*[^.]{0,40}tecnic"],
    "practical": [r"practical contribution", r"contribuic\w* pratic", r"contribuic\w*[^.]{0,40}pratic"],
}
FUTURE = [r"future work", r"future research", r"trabalhos? futuros?", r"pesquisas? futuras?"]
BUSINESS = [r"business problem", r"problema de negocio", r"business", r"negocio", r"organizational", r"organizacional"]
TECHNICAL = [r"technical problem", r"problema tecnico", r"technical challenge", r"desafio tecnico"]
PLACEHOLDER = re.compile(r"\[(CITATION NEEDED|DATA PENDING|STATISTICAL EVIDENCE PENDING|MISSING FIELD|CATEGORY PENDING)[^\]]*\]")
HYP = re.compile(r"\bH\s?([0-9]+[a-z]?)\b|\bH_\{?([0-9]+[a-z]?)\}?")


def table_last_row(text: str) -> str | None:
    """Return the last data row of the last Markdown table or LaTeX tabular in text."""
    md_rows = [l for l in text.splitlines() if l.strip().startswith("|") and not re.match(r"^\s*\|[\s:\-|]+\|\s*$", l)]
    tex = re.findall(r"\\begin\{tabular\*?\}(.*?)\\end\{tabular\*?\}", text, flags=re.S)
    if tex:
        rows = [r.strip() for r in re.split(r"\\\\", tex[-1]) if "&" in r]
        if rows:
            return rows[-1]
    if md_rows:
        return md_rows[-1]
    return None


def has_table(text: str) -> bool:
    return bool(re.search(r"^\s*\|.+\|\s*$", text, flags=re.M)) or "\\begin{tabular" in text


def run_checks(raw: str, doc_type: str) -> tuple[list[Finding], dict]:
    lines = raw.splitlines()
    sections = split_sections(lines)
    secs = merged(sections)
    f: list[Finding] = []
    found_keys = [s.key for s in sections if s.key]

    # Structure
    for key in REQUIRED:
        if key not in secs:
            sev = "info" if key == "discussion" and "results_discussion" in found_keys else "warning"
            if key == "related_work" and doc_type == "article" and "background" in secs:
                sev = "warning"
            f.append(Finding("STRUCT", sev, key, f"Section '{key}' not detected (check heading names)."))
    if "results_discussion" in found_keys:
        f.append(Finding("R22", "info", "results", "Results and Discussion merged — acceptable only if the venue requires it."))

    intro = secs.get("introduction", ("", 0))[0]
    if intro:
        hits = find_sentences(intro, ROADMAP)
        if hits:
            if doc_type == "thesis":
                f.append(Finding("R10", "info", "introduction", "Roadmap/organization paragraph found — allowed in theses/dissertations only if the writer decided to include it.", hits))
            else:
                f.append(Finding("R10", "warning", "introduction", "Roadmap paragraph describing the document structure (avoid in articles/reports).", hits))
        n = norm(intro)
        if not any(re.search(p, n) for p in BUSINESS):
            f.append(Finding("R06", "warning", "introduction", "No explicit business/practical problem detected."))
        if not any(re.search(p, n) for p in TECHNICAL):
            f.append(Finding("R06", "info", "introduction", "No explicit 'technical problem' wording detected — verify the technical problem is clearly stated."))

    rw = secs.get("related_work", ("", 0))[0]
    if rw:
        if not has_table(rw):
            f.append(Finding("R13", "warning", "related_work", "No comparative table detected in Related Work."))
        else:
            last = table_last_row(rw)
            if last and not any(re.search(p, norm(last)) for p in PROPOSAL_ROW):
                f.append(Finding("R13", "warning", "related_work", "Last row of the comparative table does not seem to be the proposal.", [last[:160]]))

    method = secs.get("method", ("", 0))[0]
    if method:
        hits = find_sentences(method, RESULT_IN_METHOD)
        if hits:
            f.append(Finding("R19", "warning", "method", "Possible results reported in the Method section.", hits))
        nm = norm(method)
        missing = [k for k, pats in THREATS.items() if not any(re.search(p, nm) for p in pats)]
        if missing:
            f.append(Finding("R18", "warning", "method", f"Threats to validity not found for: {', '.join(missing)}."))
        bullets = len(re.findall(r"^\s*[-*•]\s+(theoretical|empirical|exploratory|descriptive|explanatory|quantitative|qualitative|teorica|empirica|exploratoria|descritiva|explicativa|quantitativa|qualitativa)", nm, flags=re.M))
        if bullets >= 2:
            f.append(Finding("R15", "info", "method", "Methodology classification appears as a bullet list — the guideline prefers continuous prose."))

    results = secs.get("results", ("", 0))[0]
    if results and "results_discussion" not in found_keys:
        hits = find_sentences(results, INTERPRETATION)
        if hits:
            f.append(Finding("R20", "warning", "results", "Possible interpretation in the Results section (move to Discussion).", hits))

    disc = secs.get("discussion", ("", 0))[0]
    hyps_method = {(a or b).lower() for a, b in HYP.findall(method)} if method else set()
    hyps_disc = {(a or b).lower() for a, b in HYP.findall(disc)} if disc else set()
    if method and not hyps_method:
        f.append(Finding("R17", "info", "method", "No hypotheses (H0/H1…) detected in the Method — required for experimental/explanatory studies."))
    alt = sorted(h for h in hyps_method if h not in ("0",))
    not_eval = [h for h in alt if h not in hyps_disc]
    if disc and not_eval:
        f.append(Finding("R24/C2", "warning", "discussion", f"Hypotheses from the Method not mentioned in the Discussion: {', '.join('H' + h for h in not_eval)}."))
    if disc:
        nd = norm(disc)
        missing = [k for k, pats in THREATS.items() if not any(re.search(p, nd) for p in pats)]
        if len(missing) == 4 and not re.search(r"threats? to validity|ameacas? a validade", nd):
            f.append(Finding("R28/C4", "warning", "discussion", "Threats to validity are not revisited in the Discussion."))

    concl = secs.get("conclusions", ("", 0))[0]
    if concl:
        nc = norm(concl)
        missing = [k for k, pats in CONTRIB.items() if not any(re.search(p, nc) for p in pats)]
        if missing:
            f.append(Finding("R30", "warning", "conclusions", f"Contribution types not explicitly stated: {', '.join(missing)}."))
        if not any(re.search(p, nc) for p in FUTURE):
            f.append(Finding("R32", "warning", "conclusions", "No future work detected."))
        if not any(re.search(p, nc) for p in BUSINESS):
            f.append(Finding("R31", "info", "conclusions", "Conclusions do not seem to say whether the business problem was addressed."))

    placeholders = PLACEHOLDER.findall(raw)
    if placeholders:
        f.append(Finding("I5", "info", "all", f"{len(re.findall(PLACEHOLDER, raw))} pending placeholder(s) in the text."))

    summary = {
        "sections_detected": [f"{s.title} -> {s.key}" for s in sections if s.key],
        "hypotheses_in_method": sorted("H" + h for h in hyps_method),
        "hypotheses_in_discussion": sorted("H" + h for h in hyps_disc),
        "warnings": sum(1 for x in f if x.severity == "warning"),
        "infos": sum(1 for x in f if x.severity == "info"),
    }
    return f, summary


def to_markdown(findings: list[Finding], summary: dict, path: str) -> str:
    out = [f"# Automatic checks — {path}", "", "_Heuristic hints: verify each one before reporting it as an issue._", ""]
    out.append("**Sections detected:** " + ("; ".join(summary["sections_detected"]) or "none"))
    out.append(f"**Hypotheses** — Method: {', '.join(summary['hypotheses_in_method']) or 'none'} · Discussion: {', '.join(summary['hypotheses_in_discussion']) or 'none'}")
    out.append(f"**Totals:** {summary['warnings']} warning(s), {summary['infos']} info(s)")
    out.append("")
    if not findings:
        out.append("No signals found.")
    for x in findings:
        icon = "⚠️" if x.severity == "warning" else "ℹ️"
        out.append(f"- {icon} **{x.rule}** [{x.section}] {x.message}")
        for e in x.evidence:
            out.append(f"    - “{e}”")
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("--type", choices=["article", "report", "thesis"], default="article",
                    help="thesis also covers dissertation, TCC and proposal")
    ap.add_argument("--lang", choices=["en", "pt", "auto"], default="auto", help="kept for clarity; patterns cover both languages")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    if args.file.lower().endswith((".docx", ".pdf", ".odt")):
        print("Convert the file to text/Markdown first (e.g., pandoc file.docx -o file.md; pdftotext file.pdf).", file=sys.stderr)
        return 2
    try:
        with open(args.file, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
    except OSError as exc:
        print(f"Cannot read {args.file}: {exc}", file=sys.stderr)
        return 2

    findings, summary = run_checks(raw, "thesis" if args.type == "thesis" else "article")
    if args.json:
        print(json.dumps({"summary": summary, "findings": [asdict(x) for x in findings]}, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(findings, summary, args.file))
    return 0


if __name__ == "__main__":
    sys.exit(main())
