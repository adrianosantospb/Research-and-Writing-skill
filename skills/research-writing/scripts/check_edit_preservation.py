#!/usr/bin/env python3
"""Check that an edited text preserves the protected content of the original (research-writing skill).

Compares ORIGINAL and EDITED versions of a text (Markdown, LaTeX or plain text, any language)
and reports changes in content that editing must never alter (core-rules E1-E3, E8):
numbers and statistics, citation markers, equations, inline/fenced code, URLs and DOIs.
It also reports the word-count change and [AUTHOR CHECK] flags.

This is a preservation check, not a grammar or meaning check: it cannot tell whether the
meaning of a sentence changed. Review the edited text as well.

Usage:
    python3 check_edit_preservation.py ORIGINAL EDITED [--level 1|2|3] [--json]

Exit code: 0 = nothing protected changed, 1 = protected content changed, 2 = usage/IO error.
Standard library only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter

PROTECTED = [
    ("code", re.compile(r"```.*?```", re.S)),
    ("code", re.compile(r"`[^`\n]+`")),
    ("equation", re.compile(r"\$\$.*?\$\$", re.S)),
    ("equation", re.compile(r"\\begin\{(equation|align|eqnarray|math|displaymath)\*?\}.*?\\end\{\1\*?\}", re.S)),
    ("equation", re.compile(r"\\\[.*?\\\]", re.S)),
    ("equation", re.compile(r"\\\(.*?\\\)", re.S)),
    ("equation", re.compile(r"(?<![\\$])\$[^$\n]+\$")),
    ("url", re.compile(r"https?://[^\s)>\]]+")),
    ("url", re.compile(r"\b10\.\d{4,9}/[^\s)>\]]+")),
    ("citation", re.compile(r"\\(?:cite|citep|citet|parencite|textcite|autocite|footcite)\*?(?:\[[^\]]*\])*\{[^}]+\}")),
    ("citation", re.compile(r"\[\^[^\]]+\]")),                                   # Markdown footnotes
    ("citation", re.compile(r"\[\d+(?:\s*[,;–-]\s*\d+)*\]")),                      # [1], [2, 5], [3-7]
    ("citation", re.compile(r"\((?:[^()]*?[A-ZÀ-Ý][^()]*?),?\s(?:\d{4}[a-z]?|s\.\s?d\.|n\.d\.)(?:[^()]*)\)")),  # (Silva, 2023, p. 4)
    ("citation", re.compile(r"\b[A-ZÀ-Ý][\w'’-]+(?:\s(?:et al\.|and|e|y|et|&)\s?[A-ZÀ-Ý]?[\w'’-]*)?\s\(\d{4}[a-z]?\)")),  # Silva (2023)
]
# thousands groups only with non-breaking spaces (a plain space would merge "Table 2 100 ...")
NUMBER = re.compile(r"(?<![\w.,])[-−+]?\d+(?:[.,\u00a0\u202f]\d{3})*(?:[.,]\d+)?(?:[\s\u00a0\u202f]?%)?(?![\w])")
AUTHOR_CHECK = re.compile(r"\[AUTHOR CHECK[^\]]*\]")
LEVEL_LIMITS = {1: 0.10, 2: 0.25, 3: 0.50}   # informative thresholds for relative word-count change


def extract(text: str) -> tuple[dict[str, Counter], str]:
    """Return protected spans by kind and the text with those spans blanked out."""
    found: dict[str, Counter] = {k: Counter() for k in ("code", "equation", "url", "citation")}
    rest = text
    for kind, rx in PROTECTED:
        def repl(m: re.Match, kind=kind) -> str:
            found[kind][" ".join(m.group(0).split())] += 1
            return " " * len(m.group(0))
        rest = rx.sub(repl, rest)
    return found, rest


def numbers(text: str) -> Counter:
    return Counter(re.sub(r"[\s\u00a0\u202f]", "", m.group(0)).replace("−", "-") for m in NUMBER.finditer(text))


def canon(num: str) -> str:
    return re.sub(r"[.,\s%]", "", num) + ("%" if "%" in num else "")


def compare(original: str, edited: str, level: int | None = None) -> dict:
    o_prot, o_rest = extract(original)
    e_prot, e_rest = extract(edited)
    findings = []
    for kind in ("citation", "equation", "code", "url"):
        missing = o_prot[kind] - e_prot[kind]
        added = e_prot[kind] - o_prot[kind]
        for item, n in missing.items():
            findings.append({"severity": "changed", "kind": kind, "change": "missing or altered", "item": item, "count": n})
        for item, n in added.items():
            findings.append({"severity": "changed", "kind": kind, "change": "added or altered", "item": item, "count": n})

    o_num, e_num = numbers(o_rest), numbers(e_rest)
    missing, added = o_num - e_num, e_num - o_num
    # pair format-only changes (0,05 -> 0.05; 10 000 -> 10000) so they are reported separately
    added_by_canon: dict[str, list[str]] = {}
    for item, n in added.items():
        added_by_canon.setdefault(canon(item), []).extend([item] * n)
    for item, n in missing.items():
        for _ in range(n):
            pool = added_by_canon.get(canon(item))
            if pool:
                new = pool.pop()
                findings.append({"severity": "format", "kind": "number", "change": f"format changed to {new}", "item": item, "count": 1})
            else:
                findings.append({"severity": "changed", "kind": "number", "change": "missing or altered", "item": item, "count": 1})
    for pool in added_by_canon.values():
        for item in pool:
            findings.append({"severity": "changed", "kind": "number", "change": "added", "item": item, "count": 1})

    o_words, e_words = len(original.split()), len(edited.split())
    ratio = (e_words - o_words) / o_words if o_words else 0.0
    info = {
        "words_original": o_words,
        "words_edited": e_words,
        "relative_change": round(ratio, 3),
        "author_checks": AUTHOR_CHECK.findall(edited),
        "protected_counts_original": {k: sum(v.values()) for k, v in o_prot.items()} | {"number": sum(o_num.values())},
    }
    if level in LEVEL_LIMITS and abs(ratio) > LEVEL_LIMITS[level]:
        findings.append({"severity": "info", "kind": "length", "item": f"{ratio:+.0%}",
                         "change": f"word count changed more than expected for level {level} (±{LEVEL_LIMITS[level]:.0%})", "count": 1})
    status = "changed" if any(f["severity"] == "changed" for f in findings) else "preserved"
    return {"status": status, "findings": findings, "info": info,
            "scope": "protected-content preservation only; does not check grammar or meaning"}


def to_markdown(result: dict) -> str:
    out = ["# Edit preservation check", "",
           "_Checks numbers, citations, equations, code and URLs only — not grammar or meaning._", ""]
    i = result["info"]
    out.append(f"**Status:** {result['status'].upper()}  ·  words {i['words_original']} → {i['words_edited']} ({i['relative_change']:+.1%})")
    out.append("**Protected items in original:** " + ", ".join(f"{k} {v}" for k, v in i["protected_counts_original"].items()))
    if i["author_checks"]:
        out.append(f"**[AUTHOR CHECK] flags:** {len(i['author_checks'])}")
    out.append("")
    if not result["findings"]:
        out.append("All protected content preserved.")
    icons = {"changed": "❌", "format": "⚠️", "info": "ℹ️"}
    for f in result["findings"]:
        out.append(f"- {icons[f['severity']]} **{f['kind']}** {f['change']}: `{f['item']}`" + (f" ×{f['count']}" if f["count"] > 1 else ""))
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("original")
    ap.add_argument("edited")
    ap.add_argument("--level", type=int, choices=[1, 2, 3], help="editing level, for the length-change hint")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        with open(args.original, encoding="utf-8", errors="replace") as fh:
            original = fh.read()
        with open(args.edited, encoding="utf-8", errors="replace") as fh:
            edited = fh.read()
    except OSError as exc:
        print(f"Cannot read input: {exc}", file=sys.stderr)
        return 2
    result = compare(original, edited, args.level)
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else to_markdown(result))
    return 1 if result["status"] == "changed" else 0


if __name__ == "__main__":
    sys.exit(main())
