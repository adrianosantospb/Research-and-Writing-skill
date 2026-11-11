"""Tests for skills/research-writing/scripts/check_manuscript.py (run: python3 -m unittest discover tests)."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "research-writing" / "scripts"))
import check_manuscript as cm  # noqa: E402

FIX = ROOT / "tests" / "fixtures"


def rules(text, doc_type="article"):
    findings, _ = cm.run_checks(text, doc_type)
    return {(f.rule, f.severity) for f in findings}


class TestChecker(unittest.TestCase):
    def test_bad_article_flags_main_rules(self):
        r = {rule for rule, sev in rules((FIX / "bad_article_en.md").read_text()) if sev == "warning"}
        for expected in ["R10", "R13", "R19", "R18", "R20", "R24/C2", "R28/C4", "R30", "R32"]:
            self.assertIn(expected, r)

    def test_good_article_has_no_warnings(self):
        r = [rule for rule, sev in rules((FIX / "good_article_pt.md").read_text()) if sev == "warning"]
        self.assertEqual(r, [])

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


if __name__ == "__main__":
    unittest.main()
