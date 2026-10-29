import json
import unittest

from _load import load, example

fp = load("seed-zahlen", "finanzplan")


def spec():
    with open(example("seed-zahlen", "example.json"), encoding="utf-8") as fh:
        return json.load(fh)


class Bewertung(unittest.TestCase):
    def test_pre_and_post_from_share(self):
        v = fp.valuation(150000, anteil=0.15)
        self.assertAlmostEqual(v["post_money"], 1000000, places=2)
        self.assertAlmostEqual(v["pre_money"], 850000, places=2)

    def test_share_from_pre_money(self):
        v = fp.valuation(150000, pre_money=850000)
        self.assertAlmostEqual(v["investor_share"], 0.15, places=6)
        self.assertAlmostEqual(v["post_money"], 1000000, places=2)

    def test_exactly_one_of_share_or_pre_money(self):
        with self.assertRaises(fp.ZahlenError):
            fp.valuation(150000)
        with self.assertRaises(fp.ZahlenError):
            fp.valuation(150000, anteil=0.1, pre_money=1000000)

    def test_share_out_of_range_is_refused(self):
        for bad in (0, 1, 1.5, -0.1):
            with self.assertRaises(fp.ZahlenError):
                fp.valuation(150000, anteil=bad)


class Verwaesserung(unittest.TestCase):
    def test_dilution_keeps_sum_at_one(self):
        h = fp.dilute({"A": 0.6, "B": 0.4}, 0.2, "X")
        self.assertAlmostEqual(sum(h.values()), 1.0, places=9)
        self.assertAlmostEqual(h["A"], 0.48, places=9)
        self.assertAlmostEqual(h["X"], 0.2, places=9)

    def test_example_cap_table(self):
        steps = fp.cap_table(spec())
        self.assertEqual([s[0] for s in steps], ["Nach dem Seed", "Nach Seed 2"])
        seed = steps[0][1]
        self.assertAlmostEqual(seed["Jonas"], 0.95 * 0.85, places=6)
        self.assertAlmostEqual(seed["Optionspool"], 0.05 * 0.85, places=6)
        self.assertAlmostEqual(seed["Seed-Investoren"], 0.15, places=6)
        after2 = steps[1][1]
        self.assertAlmostEqual(after2["Jonas"], 0.95 * 0.85 * 0.8, places=6)
        self.assertAlmostEqual(sum(after2.values()), 1.0, places=9)

    def test_founder_shares_must_sum_to_100_percent(self):
        s = spec()
        s["gruender"] = [{"name": "A", "anteil": 0.5}, {"name": "B", "anteil": 0.3}]
        with self.assertRaises(fp.ZahlenError):
            fp.cap_table(s)


class Kapitalbedarf(unittest.TestCase):
    def test_example_numbers(self):
        a = fp.analyse(spec())
        self.assertEqual(a["startup"], 7000)
        self.assertEqual(a["burn"], 12000)
        self.assertEqual(round(a["need_cash"]), 103600)
        self.assertEqual(round(a["buffer"]), 36000)
        self.assertEqual(round(a["need_total"]), 139600)
        self.assertIsNone(a["runway"])
        self.assertEqual(a["flags"], [])

    def test_goal_too_small_is_flagged(self):
        s = spec()
        s["kapital_ziel"] = 90000
        a = fp.analyse(s)
        self.assertTrue(any("reicht nicht" in f for f in a["flags"]))
        self.assertIsNotNone(a["runway"])
        self.assertLess(a["runway"], 12)

    def test_big_share_is_flagged_but_not_forbidden(self):
        s = spec()
        s["abgabe_anteil"] = 0.4
        a = fp.analyse(s)
        self.assertTrue(any("40 Prozent" in f and "Faustregel" in f for f in a["flags"]))

    def test_bad_input_is_refused_not_guessed(self):
        s = spec()
        s["einnahmen_monatlich"] = [0] * 11
        with self.assertRaises(fp.ZahlenError):
            fp.analyse(s)
        s = spec()
        del s["kapital_ziel"]
        with self.assertRaises(fp.ZahlenError):
            fp.analyse(s)
        s = spec()
        s["ausgaben_monatlich"][0]["cost"] = "viel"
        with self.assertRaises(fp.ZahlenError):
            fp.analyse(s)

    def test_report_mentions_the_key_numbers(self):
        s = spec()
        text = fp.report(s, fp.analyse(s))
        for needle in ("139.600 €", "850.000 €", "1.000.000 €", "15,0 %", "80,8 %", "Keine Finanz- oder Rechtsberatung"):
            self.assertIn(needle, text)


if __name__ == "__main__":
    unittest.main()
