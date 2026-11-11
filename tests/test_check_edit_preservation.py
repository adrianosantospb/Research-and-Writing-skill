"""Tests for skills/research-writing/scripts/check_edit_preservation.py.

Each language folder in tests/fixtures/editing/ holds:
  original.md   — text with real language errors (input of an editing request)
  edited_ok.md  — a correct Level 2 edit: errors fixed, protected content preserved (positive case)
  edited_bad.md — an unacceptable edit: numbers/citations/equations altered (negative case)
"""
import contextlib
import io
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "research-writing" / "scripts"))
import check_edit_preservation as cep  # noqa: E402

EDIT = ROOT / "tests" / "fixtures" / "editing"
LANGS = ("pt", "es", "fr", "en")


def load(lang, name):
    return (EDIT / lang / f"{name}.md").read_text(encoding="utf-8")


def changed_kinds(result):
    return {f["kind"] for f in result["findings"] if f["severity"] == "changed"}


class TestFixtures(unittest.TestCase):
    def test_correct_edits_preserve_protected_content(self):
        for lang in LANGS:
            with self.subTest(lang=lang):
                result = cep.compare(load(lang, "original"), load(lang, "edited_ok"), level=2)
                self.assertEqual(result["status"], "preserved", result["findings"])

    def test_bad_edits_are_detected(self):
        expected = {"pt": {"citation", "number", "equation"}, "es": {"citation", "number"},
                    "fr": {"citation", "number"}, "en": {"citation", "number"}}
        for lang in LANGS:
            with self.subTest(lang=lang):
                result = cep.compare(load(lang, "original"), load(lang, "edited_bad"))
                self.assertEqual(result["status"], "changed")
                self.assertTrue(expected[lang] <= changed_kinds(result), changed_kinds(result))

    def test_edited_ok_actually_differs_from_original(self):
        # guards against a trivially "preserved" fixture
        for lang in LANGS:
            self.assertNotEqual(load(lang, "original"), load(lang, "edited_ok"))


class TestRules(unittest.TestCase):
    def test_identical_text_is_preserved(self):
        text = "Accuracy was 0.91 [2] (Silva, 2020), see https://example.org and $x^2$."
        self.assertEqual(cep.compare(text, text)["status"], "preserved")

    def test_number_format_change_is_reported_separately(self):
        result = cep.compare("A mean of 0,05 was found.", "A mean of 0.05 was found.")
        self.assertEqual(result["status"], "preserved")
        self.assertEqual([f["severity"] for f in result["findings"]], ["format"])

    def test_citation_years_are_not_counted_as_numbers(self):
        result = cep.compare("As shown (Silva, 2020).", "As (Silva, 2020) shows.")
        self.assertEqual(result["status"], "preserved")

    def test_latex_cite_and_equation(self):
        o = "We follow \\cite{silva2020} with $\\alpha=0.1$."
        self.assertEqual(changed_kinds(cep.compare(o, "We follow prior work with $\\alpha=0.1$.")), {"citation"})
        self.assertEqual(changed_kinds(cep.compare(o, "We follow \\cite{silva2020} with $\\alpha=0.2$.")), {"equation"})

    def test_url_and_doi(self):
        o = "Data at https://doi.org/10.5281/zenodo.123."
        self.assertIn("url", changed_kinds(cep.compare(o, "Data at https://doi.org/10.5281/zenodo.124.")))

    def test_level_length_hint(self):
        o = "one two three four five six seven eight nine ten"
        e = o + " eleven twelve"
        kinds = {f["kind"] for f in cep.compare(o, e, level=1)["findings"]}
        self.assertIn("length", kinds)
        self.assertEqual(cep.compare(o, e, level=1)["status"], "preserved")

    def test_author_check_flags_are_reported(self):
        result = cep.compare("It works.", "It works [AUTHOR CHECK: which model?].")
        self.assertEqual(len(result["info"]["author_checks"]), 1)

    def test_cli_exit_codes(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            ok = cep.main([str(EDIT / "en" / "original.md"), str(EDIT / "en" / "edited_ok.md")])
            bad = cep.main([str(EDIT / "en" / "original.md"), str(EDIT / "en" / "edited_bad.md"), "--json"])
        self.assertEqual((ok, bad), (0, 1))


if __name__ == "__main__":
    unittest.main()
