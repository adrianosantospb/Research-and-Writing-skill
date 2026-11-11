#!/usr/bin/env python3
"""Heuristic structure checks for scientific manuscripts (research-writing skill).

Reads a Markdown, LaTeX or plain-text manuscript in English, Portuguese, Spanish or
French, splits it into sections and reports signals related to the guideline rules
(core-rules.md). The output is a list of STRUCTURAL HINTS to be verified by a
human/agent, not a verdict. It does NOT check grammar, spelling or style: linguistic
proofreading is done by the skill's editing mode (references/writing/).

Usage:
    python3 check_manuscript.py FILE [--type article|report|thesis]
                                     [--lang auto|en|pt|es|fr|<regional tag, e.g. pt-BR, es-MX, fr-CA, en-GB>]
                                     [--json]

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
    "abstract": ["abstract", "resumo", "summary", "resumen", "resume"],
    "introduction": ["introduction", "introducao", "introduccion"],
    "background": ["background", "fundamentacao teorica", "referencial teorico", "theoretical foundation",
                   "marco teorico", "fundamentos teoricos", "cadre theorique", "fondements theoriques"],
    "related_work": ["related work", "trabalhos relacionados", "estado da arte", "related works", "literature review",
                     "revisao da literatura", "trabajos relacionados", "estado del arte", "revision de la literatura",
                     "travaux connexes", "travaux relies", "etat de l'art", "revue de la litterature"],
    "method": ["method", "methodology", "metodologia", "metodo", "materials and methods", "materiais e metodos",
               "proposed solution", "proposta", "experimental design", "evaluation design",
               "metodos", "materiales y metodos", "propuesta", "solucion propuesta",
               "methode", "methodologie", "methodes", "materiel et methodes", "approche proposee", "solution proposee"],
    "results": ["results", "resultados", "resultats"],
    "discussion": ["discussion", "discussao", "discusion"],
    "conclusions": ["conclusion", "conclusions", "conclusao", "conclusoes", "consideracoes finais", "final remarks",
                    "concluding remarks", "conclusiones", "consideraciones finales"],
    "references": ["references", "referencias", "bibliography", "bibliografia", "bibliographie"],
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
    if "result" in t and "discus" in t:  # en/pt/es/fr "results and discussion"
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


LANGS = ("en", "pt", "es", "fr")

# Patterns are written on accent-free lowercase text (see norm()).
P = {
    "roadmap": {
        "en": [r"\b(section|chapter)\s+\d+\s+(presents|describes|discusses)",
               r"(the )?(rest|remainder) of (this|the) (paper|article|work|report|thesis) (is|are) (organized|structured)",
               r"(this|the) (paper|article|work|report) is (organized|structured) as follows"],
        "pt": [r"\b(secao|capitulo)\s+\d+\s+(apresenta|descreve|discute|traz)",
               r"(o )?restante deste (trabalho|artigo|documento|relatorio)",
               r"(este|o presente) (trabalho|artigo|documento) (esta|encontra-se) (organizado|estruturado)",
               r"organizacao do (trabalho|texto|documento)"],
        "es": [r"\b(seccion|capitulo)\s+\d+\s+(presenta|describe|discute|aborda)",
               r"(el )?resto (de este|del) (trabajo|articulo|documento|informe)",
               r"(este|el presente) (trabajo|articulo|documento) (esta|se) (organizado|estructurado|organiza|estructura)",
               r"organizacion del (trabajo|documento|texto)"],
        "fr": [r"\b(la )?(section|chapitre)\s+\d+\s+(presente|decrit|discute|aborde)",
               r"(le )?reste de (cet|ce) (article|document|travail|rapport|memoire)",
               r"(cet|ce) (article|document|travail|rapport) est (organise|structure)",
               r"organisation du (document|memoire|travail)"],
    },
    "result_in_method": {
        "en": [r"\b(achiev\w*|obtain\w*|reach\w*|outperform\w*)\b[^.]{0,80}\d+([.,]\d+)?\s?%",
               r"\b(results|the experiment)\s+(show\w*|indicat\w*|demonstrat\w*)"],
        "pt": [r"\b(alcan\w*|obtev\w*|atingi\w*|superou)\b[^.]{0,80}\d+([.,]\d+)?\s?%",
               r"\b(os resultados|o experimento)\s+(mostr\w*|indic\w*|demonstr\w*)"],
        "es": [r"\b(alcanz\w*|obtuv\w*|logr\w*|super[oa]\w*)\b[^.]{0,80}\d+([.,]\d+)?\s?%",
               r"\b(los resultados|el experimento)\s+(muestr\w*|indic\w*|demuestr\w*)"],
        "fr": [r"\b(atteint|obtenu\w*|surpass\w*)\b[^.]{0,80}\d+([.,]\d+)?\s?%",
               r"\b(les resultats|l'experience|l'experimentation)\s+(montr\w*|indiqu\w*|demontr\w*)"],
        "*": [r"\bp\s?[<=]\s?0?[.,]\d+"],
    },
    "interpretation": {
        "en": [r"\bthis (shows|indicates|suggests|demonstrates|means|implies)\b",
               r"\b(which|that) (means|suggests|indicates|implies)\b",
               r"\b(because|due to|this is explained|surprisingly|as expected|interestingly)\b"],
        "pt": [r"\b(isto|isso|o que) (mostra|indica|sugere|demonstra|significa|implica)\b",
               r"\b(devido a|porque|explica-se|surpreendentemente|como esperado|curiosamente)\b"],
        "es": [r"\b(esto|lo que|ello) (muestra|indica|sugiere|demuestra|significa|implica)\b",
               r"\b(debido a|porque|se explica|sorprendentemente|como era de esperar|curiosamente)\b"],
        "fr": [r"\b(cela|ceci|ce qui) (montre|indique|suggere|demontre|signifie|implique)\b",
               r"\b(en raison de|parce que|s'explique|etonnamment|comme prevu|curieusement)\b"],
    },
    "proposal_row": {
        "en": [r"this work", r"our (approach|proposal|method|work)", r"proposed", r"\bproposal\b"],
        "pt": [r"este trabalho", r"nossa (abordagem|proposta)", r"\bproposta\b", r"presente trabalho"],
        "es": [r"este trabajo", r"nuestr[ao] (enfoque|propuesta|metodo)", r"\bpropuesta\b", r"presente trabajo"],
        "fr": [r"ce travail", r"notre (approche|proposition|methode)", r"approche proposee", r"\bproposition\b"],
    },
    "future": {
        "en": [r"future work", r"future research"],
        "pt": [r"trabalhos? futuros?", r"pesquisas? futuras?"],
        "es": [r"trabajos? futuros?", r"investigaciones? futuras?", r"lineas? futuras?"],
        "fr": [r"travaux futurs", r"recherches? futures?", r"\bperspectives\b"],
    },
    "business": {
        "en": [r"business problem", r"business", r"organizational"],
        "pt": [r"problema de negocio", r"negocio", r"organizacional"],
        "es": [r"problema de negocio", r"negocio", r"organizacional"],
        "fr": [r"probleme metier", r"\bmetier\b", r"organisationnel\w*", r"\bentreprises?\b"],
    },
    "technical": {
        "en": [r"technical problem", r"technical challenge"],
        "pt": [r"problema tecnico", r"desafio tecnico"],
        "es": [r"problema tecnico", r"desafio tecnico", r"reto tecnico"],
        "fr": [r"probleme technique", r"defi technique"],
    },
    "threats_heading": {
        "en": [r"threats? to validity"],
        "pt": [r"ameacas? a validade"],
        "es": [r"amenazas? a la validez"],
        "fr": [r"menaces? (a|pour) la validite"],
    },
    "method_labels": {
        "en": ["theoretical", "empirical", "exploratory", "descriptive", "explanatory", "quantitative", "qualitative"],
        "pt": ["teorica", "empirica", "exploratoria", "descritiva", "explicativa", "quantitativa", "qualitativa"],
        "es": ["teorica", "empirica", "exploratoria", "descriptiva", "explicativa", "cuantitativa", "cualitativa"],
        "fr": ["theorique", "empirique", "exploratoire", "descriptive", "explicative", "quantitative", "qualitative"],
    },
}
P_KEYED = {
    "threats": {
        "external": {"en": [r"external validity"], "pt": [r"validade externa"], "es": [r"validez externa"], "fr": [r"validite externe"]},
        "internal": {"en": [r"internal validity"], "pt": [r"validade interna"], "es": [r"validez interna"], "fr": [r"validite interne"]},
        "construct": {"en": [r"construct validity"], "pt": [r"validade de constru(c)?to"], "es": [r"validez de constructo"], "fr": [r"validite de construit"]},
        "conclusion": {"en": [r"conclusion validity", r"statistical conclusion validity"], "pt": [r"validade de conclusao"],
                       "es": [r"validez de (la )?conclusion"], "fr": [r"validite de (la )?conclusion"]},
    },
    "contrib": {
        "scientific": {"en": [r"scientific contribution"], "pt": [r"contribuic\w*[^.]{0,40}cientific"],
                       "es": [r"contribuc\w*[^.]{0,40}cientific"], "fr": [r"contribution\w*[^.]{0,40}scientifi"]},
        "technical": {"en": [r"technical contribution"], "pt": [r"contribuic\w*[^.]{0,40}tecnic"],
                      "es": [r"contribuc\w*[^.]{0,40}tecnic"], "fr": [r"contribution\w*[^.]{0,40}techni"]},
        "practical": {"en": [r"practical contribution"], "pt": [r"contribuic\w*[^.]{0,40}pratic"],
                      "es": [r"contribuc\w*[^.]{0,40}practic"], "fr": [r"contribution\w*[^.]{0,40}prati"]},
    },
}


def pats(name: str, langs) -> list[str]:
    d = P[name]
    out = list(d.get("*", []))
    for lang in langs:
        out += d.get(lang, [])
    return out


def keyed(name: str, langs) -> dict[str, list[str]]:
    return {k: [p for lang in langs for p in v.get(lang, [])] for k, v in P_KEYED[name].items()}


# --------------------------------------------------------------------------- language
# Distinctive function words (accent-free). Ambiguous words shared by several languages are omitted.
STOPWORDS = {
    "en": {"the", "and", "of", "is", "are", "this", "that", "with", "we", "which", "was", "were", "be", "by",
           "from", "these", "it", "an", "for", "to", "on", "has", "have", "our", "their"},
    "pt": {"nao", "uma", "um", "do", "da", "dos", "das", "os", "com", "sao", "foram", "pelo", "pela", "tambem",
           "isso", "ao", "aos", "em", "na", "e", "mais", "foi", "seu", "sua", "pelos", "pelas"},
    "es": {"el", "los", "las", "del", "una", "con", "y", "es", "son", "fue", "fueron", "tambien", "esto", "al",
           "lo", "muy", "su", "sus", "estos", "hay", "pero"},
    "fr": {"le", "les", "des", "du", "et", "est", "sont", "dans", "qui", "avec", "sur", "ce", "cette", "nous",
           "pas", "ete", "au", "aux", "une", "il", "ces", "leur", "par"},
}
REGION_TAG = re.compile(r"^(en|pt|es|fr)([-_][A-Za-z0-9]{2,3})?$")


def parse_lang(value: str) -> tuple[str, str | None]:
    """'pt-BR' -> ('pt', 'pt-BR'); 'auto' -> ('auto', None). Raises ValueError if unsupported."""
    v = value.strip()
    if v.lower() == "auto":
        return "auto", None
    m = REGION_TAG.match(v)
    if not m:
        raise ValueError(f"unsupported language '{value}' (use auto, en, pt, es, fr or a regional tag such as pt-BR)")
    base = m.group(1).lower()
    return base, (v if m.group(2) else None)


def detect_language(text: str) -> tuple[str, float]:
    """Return (language, confidence) using distinctive function words; ('unknown', 0.0) if too little text."""
    body = re.sub(r"\\[a-zA-Z]+(\[[^\]]*\])?(\{[^}]*\})?", " ", text)   # LaTeX commands
    body = re.sub(r"https?://\S+", " ", body)
    words = re.findall(r"[a-z]+(?:'[a-z]+)?", norm(body))
    scores = {lang: sum(1 for w in words if w in sw) for lang, sw in STOPWORDS.items()}
    total = sum(scores.values())
    if total < 5:
        return "unknown", 0.0
    best = max(scores, key=scores.get)
    return best, round(scores[best] / total, 2)


PLACEHOLDER = re.compile(r"\[(CITATION NEEDED|DATA PENDING|STATISTICAL EVIDENCE PENDING|MISSING FIELD|CATEGORY PENDING|AUTHOR CHECK)[^\]]*\]")
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


def run_checks(raw: str, doc_type: str, lang: str = "auto") -> tuple[list[Finding], dict]:
    """lang: 'auto' or a code/regional tag (en, pt, es, fr, pt-BR, ...). English patterns are always
    added because abstracts/keywords are often in English; 'unknown' detection uses all languages."""
    base, region = parse_lang(lang)
    detected, confidence = detect_language(raw)
    used = base if base != "auto" else detected
    langs = LANGS if used == "unknown" else tuple(dict.fromkeys((used, "en")))
    ROADMAP, RESULT_IN_METHOD, INTERPRETATION = pats("roadmap", langs), pats("result_in_method", langs), pats("interpretation", langs)
    PROPOSAL_ROW, FUTURE, BUSINESS, TECHNICAL = pats("proposal_row", langs), pats("future", langs), pats("business", langs), pats("technical", langs)
    THREATS, CONTRIB = keyed("threats", langs), keyed("contrib", langs)
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
        labels = "|".join(sorted({w for lg in langs for w in P["method_labels"][lg]}))
        bullets = len(re.findall(rf"^\s*[-*•]\s+({labels})", nm, flags=re.M))
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
        if len(missing) == 4 and not any(re.search(p, nd) for p in pats("threats_heading", langs)):
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
        "scope": "structural heuristics only; no grammar, spelling or style checking",
        "language_requested": lang,
        "language_detected": detected,
        "detection_confidence": confidence,
        "language_used": used if used != "unknown" else "all",
        "region": region,
        "sections_detected": [f"{s.title} -> {s.key}" for s in sections if s.key],
        "hypotheses_in_method": sorted("H" + h for h in hyps_method),
        "hypotheses_in_discussion": sorted("H" + h for h in hyps_disc),
        "warnings": sum(1 for x in f if x.severity == "warning"),
        "infos": sum(1 for x in f if x.severity == "info"),
    }
    return f, summary


def to_markdown(findings: list[Finding], summary: dict, path: str) -> str:
    out = [f"# Automatic checks — {path}", "",
           "_Structural heuristic hints only: verify each one before reporting it as an issue. "
           "This script does not check grammar, spelling or style (use the editing mode for linguistic proofreading)._", ""]
    lang_line = f"**Language:** detected `{summary['language_detected']}` (confidence {summary['detection_confidence']}); patterns used: `{summary['language_used']}`" + ("" if summary['language_used'] in ("en", "all") else " + `en`")
    if summary.get("region"):
        lang_line += f"; regional preference `{summary['region']}`"
    out.append(lang_line)
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
    ap.add_argument("--lang", default="auto",
                    help="auto (default), en, pt, es, fr, or a regional tag such as pt-BR, es-ES, es-MX, fr-CA, en-GB")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)
    try:
        parse_lang(args.lang)
    except ValueError as exc:
        ap.error(str(exc))

    if args.file.lower().endswith((".docx", ".pdf", ".odt")):
        print("Convert the file to text/Markdown first (e.g., pandoc file.docx -o file.md; pdftotext file.pdf).", file=sys.stderr)
        return 2
    try:
        with open(args.file, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
    except OSError as exc:
        print(f"Cannot read {args.file}: {exc}", file=sys.stderr)
        return 2

    findings, summary = run_checks(raw, "thesis" if args.type == "thesis" else "article", args.lang)
    if args.json:
        print(json.dumps({"summary": summary, "findings": [asdict(x) for x in findings]}, ensure_ascii=False, indent=2))
    else:
        print(to_markdown(findings, summary, args.file))
    return 0


if __name__ == "__main__":
    sys.exit(main())
