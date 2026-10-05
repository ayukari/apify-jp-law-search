import io
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from egov import EgovClient, normalize_article, summarize_law  # noqa: E402

FIX = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class EgovTest(unittest.TestCase):
    def test_summarize_law_from_real_search(self):
        data = load("laws_shohizei.json")
        rec = summarize_law(data["laws"][0])
        self.assertEqual(rec["lawId"], "363AC0000000108")
        self.assertEqual(rec["lawTitle"], "消費税法")
        self.assertEqual(rec["lawNum"], "昭和六十三年法律第百八号")
        self.assertTrue(rec["url"].endswith("363AC0000000108"))

    def test_normalize_real_article_30(self):
        rec = normalize_article(load("law_data_shohizei_art30.json"))
        self.assertEqual(rec["articleNum"], "30")
        self.assertEqual(rec["articleTitle"], "第三十条")
        self.assertEqual(rec["articleCaption"], "（仕入れに係る消費税額の控除）")
        self.assertGreaterEqual(len(rec["paragraphs"]), 2)
        self.assertTrue(rec["paragraphs"][0]["text"].startswith("事業者"))
        self.assertTrue(any(line.strip().startswith("一") for line in rec["paragraphs"][0]["items"]))
        self.assertIn("イ", rec["text"])  # Subitem1 rendered
        self.assertTrue(rec["text"].startswith("第三十条（仕入れに係る消費税額の控除）"))

    def test_client_builds_urls_and_parses(self):
        seen = []

        def opener(req, timeout):
            seen.append(req.full_url)
            return FakeResponse(json.dumps({"ok": 1}).encode())

        c = EgovClient(opener=opener, min_interval=0)
        self.assertEqual(c.search_laws(title="消費税法", limit=2), {"ok": 1})
        c.get_article("363AC0000000108", 30)
        self.assertIn("law_title=%E6%B6%88%E8%B2%BB%E7%A8%8E%E6%B3%95", seen[0])
        self.assertIn("/law_data/363AC0000000108?", seen[1])
        self.assertIn("elm=MainProvision-Article_30", seen[1])


if __name__ == "__main__":
    unittest.main()
