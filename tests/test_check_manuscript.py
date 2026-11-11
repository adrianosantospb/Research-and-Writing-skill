"""Tests for skills/research-writing/scripts/check_manuscript.py (run: python3 -m unittest discover tests)."""
import contextlib
import io
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "research-writing" / "scripts"))
import check_manuscript as cm  # noqa: E402

FIX = ROOT / "tests" / "fixtures"
MAIN_RULES = ["R10", "R13", "R19", "R18", "R20", "R24/C2", "R28/C4", "R30", "R32"]


def rules(text, doc_type="article", lang="auto"):
    findings, _ = cm.run_checks(text, doc_type, lang)
    return {(f.rule, f.severity) for f in findings}


def warnings(path, lang="auto"):
    return {rule for rule, sev in rules((FIX / path).read_text(encoding="utf-8"), lang=lang) if sev == "warning"}


class TestBackwardCompatibility(unittest.TestCase):
    """Original v1.0 behavior (English and Portuguese) must be preserved."""

    def test_bad_article_flags_main_rules(self):
        r = warnings("bad_article_en.md")
        for expected in MAIN_RULES:
            self.assertIn(expected, r)

    def test_good_article_has_no_warnings(self):
        self.assertEqual(warnings("good_article_pt.md"), set())

    def test_roadmap_is_info_for_thesis(self):
        text = "# Introdução\nO restante deste trabalho está organizado da seguinte forma.\n"
        self.assertIn(("R10", "info"), rules(text, "thesis"))
        self.assertIn(("R10", "warning"), rules(text, "article"))

    def test_latex_sections_and_tabular(self):
        text = (
            "\\section{Related Work}\n\\begin{tabular}{ll}\nA & yes \\\\\nThis work & yes \\\\\n\\end{tabular}\n"
            "\\section{Method}\nWe planned the study.\n"
        )
        _, summary = cm.run_checks(text, "article")
        self.assertTrue(any("related_work" in s for s in summary["sections_detected"]))
        self.assertNotIn(("R13", "warning"), rules(text))

    def test_two_argument_call_still_works(self):
        findings, summary = cm.run_checks((FIX / "bad_article_en.md").read_text(encoding="utf-8"), "article")
        self.assertTrue(findings)
        self.assertIn("sections_detected", summary)

    def test_old_cli_language_options(self):
        for lang in ("pt", "en", "auto"):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(cm.main([str(FIX / "good_article_pt.md"), "--lang", lang]), 0)


class TestMultilingualStructure(unittest.TestCase):
    def test_spanish_negative_case(self):
        r = warnings("bad_article_es.md")
        for expected in MAIN_RULES:
            self.assertIn(expected, r)

    def test_spanish_positive_case(self):
        self.assertEqual(warnings("good_article_es.md"), set())

    def test_french_negative_case(self):
        r = warnings("bad_article_fr.md")
        for expected in MAIN_RULES:
            self.assertIn(expected, r)

    def test_french_positive_case(self):
        self.assertEqual(warnings("good_article_fr.md"), set())

    def test_spanish_and_french_headings(self):
        for name in ("good_article_es.md", "good_article_fr.md"):
            _, summary = cm.run_checks((FIX / name).read_text(encoding="utf-8"), "article")
            keys = {s.split(" -> ")[1] for s in summary["sections_detected"]}
            self.assertTrue({"abstract", "introduction", "related_work", "method", "results",
                             "discussion", "conclusions", "references"} <= keys, name)

    def test_merged_results_and_discussion_in_spanish(self):
        text = "# Resultados y discusión\nTexto.\n"
        self.assertIn(("R22", "info"), rules(text))


class TestLanguageSelection(unittest.TestCase):
    def test_detection_on_manuscripts(self):
        cases = {"bad_article_en.md": "en", "good_article_pt.md": "pt", "good_article_es.md": "es",
                 "good_article_fr.md": "fr", "bad_article_es.md": "es", "bad_article_fr.md": "fr"}
        for name, lang in cases.items():
            self.assertEqual(cm.detect_language((FIX / name).read_text(encoding="utf-8"))[0], lang, name)

    def test_detection_on_editing_samples(self):
        for lang in ("pt", "es", "fr", "en"):
            text = (FIX / "editing" / lang / "original.md").read_text(encoding="utf-8")
            self.assertEqual(cm.detect_language(text)[0], lang)

    def test_detection_too_short_is_unknown(self):
        self.assertEqual(cm.detect_language("H0 H1 42")[0], "unknown")

    def test_regional_tags(self):
        self.assertEqual(cm.parse_lang("pt-BR"), ("pt", "pt-BR"))
        self.assertEqual(cm.parse_lang("es-419"), ("es", "es-419"))
        self.assertEqual(cm.parse_lang("fr_CA"), ("fr", "fr_CA"))
        self.assertEqual(cm.parse_lang("en-GB"), ("en", "en-GB"))
        self.assertEqual(cm.parse_lang("AUTO"), ("auto", None))
        with self.assertRaises(ValueError):
            cm.parse_lang("de")

    def test_explicit_language_and_region_in_summary(self):
        _, summary = cm.run_checks((FIX / "good_article_es.md").read_text(encoding="utf-8"), "article", "es-MX")
        self.assertEqual(summary["language_used"], "es")
        self.assertEqual(summary["region"], "es-MX")
        self.assertIn("no grammar", summary["scope"])

    def test_cli_rejects_unsupported_language(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            cm.main([str(FIX / "good_article_pt.md"), "--lang", "de"])

    def test_author_check_counts_as_placeholder(self):
        self.assertIn(("I5", "info"), rules("# Introduction\nText [AUTHOR CHECK: which model?] here.\n"))


if __name__ == "__main__":
    unittest.main()
