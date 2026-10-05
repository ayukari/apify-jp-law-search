import sys
import types
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.modules.setdefault("apify", types.SimpleNamespace(Actor=None))  # plan() doesn't need the SDK
from src.main import plan  # noqa: E402


class PlanTest(unittest.TestCase):
    def test_article_formats(self):
        _, _, arts, _ = plan({"lawTitle": "消費税法", "articles": ["30", "第57条の4", "第9条"]})
        self.assertEqual(arts, ["30", "57_4", "9"])

    def test_requires_title_or_ids(self):
        with self.assertRaises(ValueError):
            plan({})

    def test_max_laws_clamped(self):
        self.assertEqual(plan({"lawTitle": "x", "maxLaws": 999})[3], 100)


if __name__ == "__main__":
    unittest.main()
