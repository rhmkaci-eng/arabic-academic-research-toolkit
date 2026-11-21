import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from arabic_academic_humanizer import analyze_prose, quick_purify_rules


class TestArabicAcademicHumanizer(unittest.TestCase):
    def test_analyze_prose_schema(self):
        report = analyze_prose("البحث العلمي يقتضي تحرير محل النزاع وضبط الحدود.")
        for key in ("total_words", "findings_count", "authenticity_score", "cliche_density", "findings"):
            self.assertIn(key, report)
        self.assertIsInstance(report["findings"], list)
        self.assertGreater(report["total_words"], 0)

    def test_detects_cliches_polemics_and_loanwords(self):
        raw = (
            "مما لا شك فيه أن نقد المنهج التجريبي "
            "في الرؤية التيليولوجية يساهم في تحرير المسألة."
        )
        report = analyze_prose(raw)
        self.assertGreaterEqual(report["findings_count"], 3)
        joined = " ".join(f["matched"] for f in report["findings"])
        self.assertIn("مما لا شك فيه", joined)
        self.assertIn("نقد", joined)
        self.assertIn("التيليولوجية", joined)

    def test_quick_purify_improves_score_and_replaces_terms(self):
        raw = "مما لا شك فيه أن نقد المنهج التجريبي يلعب دوراً محورياً في التيليولوجية."
        purified = quick_purify_rules(raw)
        self.assertNotIn("مما لا شك فيه", purified)
        self.assertIn("تحليل", purified)
        self.assertNotIn("نقد", purified)

        raw_score = analyze_prose(raw)["authenticity_score"]
        purified_score = analyze_prose(purified)["authenticity_score"]
        self.assertGreater(purified_score, raw_score)

    def test_clean_scholarly_prose_scores_high(self):
        clean = (
            "الأصل في هذا الباب تحريرُ محل النزاع بين الدليل العقلي والنقل، "
            "فحصاً للجهة الغائية ومناطات الاستدلال قدر الطاقة دون إطناب."
        )
        report = analyze_prose(clean)
        self.assertEqual(report["findings_count"], 0)
        self.assertGreaterEqual(report["authenticity_score"], 90)


if __name__ == "__main__":
    unittest.main()
