import json
import os
import tempfile
import unittest

from _load import load

v = load("seed-closer", "versand")

TEXT = ("Guten Tag Frau Muster,\n\nich habe gesehen, dass Ihr Fonds in digitale Gesundheit investiert, und baue eine App, "
        "die Trainingspläne für Kunden von Online-Coaches mit KI erstellt. Zwölf Coaches nutzen den Prototyp seit sechs "
        "Wochen, vier davon zahlen schon. Ich suche 150.000 Euro für ein Jahr Entwicklung und Vertrieb. Hätten Sie in den "
        "nächsten zwei Wochen 20 Minuten für ein Gespräch? Ich schicke Ihnen gern vorab das Pitch Deck.\n\nViele Grüße\nJonas\n")
KOPF = ("An: kontakt@beispiel.de\nQuelle: https://beispiel.de/kontakt\nBetreff: Trainingspläne per KI für Coaches\n"
        "Nachfass: 0\n\n")


class JaErkennung(unittest.TestCase):
    def test_plain_yes_counts(self):
        for r in ("ja", "Ja.", "JA", "yes", "y", "ja, bitte senden", "Ja, diese Mail", "ja schick sie"):
            self.assertTrue(v.parse_yes(r), r)

    def test_yes_but_does_not_count(self):
        for r in ("ja, aber ändere den Betreff", "ja aber", "Ja, aber nur wenn er antwortet", "yes but later",
                  "ja, später", "ja wenn es passt", "ja außer die zweite", "ja, warte noch kurz", "ja vielleicht",
                  "ja, nur an Frau Muster"):
            self.assertFalse(v.parse_yes(r), r)

    def test_batch_and_vague_do_not_count(self):
        for r in ("ja zu allen", "ja, alle", "ja beide", "yes to all", "ok", "okay", "passt", "mach", "sure",
                  "klingt gut", "ja?", "", "   ", "nein", "nicht ja", "mach mal"):
            self.assertFalse(v.parse_yes(r), r)

    def test_none_does_not_count(self):
        self.assertFalse(v.parse_yes(None))


class Pruefen(unittest.TestCase):
    def test_good_draft_passes(self):
        self.assertEqual(v.pruefen(KOPF + TEXT), [])

    def test_two_recipients_fail(self):
        t = (KOPF + TEXT).replace("An: kontakt@beispiel.de", "An: a@beispiel.de, b@beispiel.de")
        self.assertTrue(any("ein Empfänger" in f for f in v.pruefen(t)))

    def test_cc_and_bcc_fail(self):
        for header in ("Cc: x@beispiel.de\n", "Bcc: x@beispiel.de\n"):
            t = KOPF.replace("Nachfass: 0\n", header + "Nachfass: 0\n") + TEXT
            self.assertTrue(any("Kopie" in f for f in v.pruefen(t)), header)

    def test_missing_source_fails(self):
        t = (KOPF + TEXT).replace("Quelle: https://beispiel.de/kontakt\n", "")
        self.assertTrue(any("Quelle" in f for f in v.pruefen(t)))

    def test_placeholder_fails(self):
        t = KOPF + TEXT.replace("Frau Muster", "[Name]")
        self.assertTrue(any("Platzhalter" in f for f in v.pruefen(t)))

    def test_third_followup_fails(self):
        t = (KOPF + TEXT).replace("Nachfass: 0", "Nachfass: 3")
        self.assertTrue(any("zwei Nachfasser" in f for f in v.pruefen(t)))
        for n in ("1", "2"):
            self.assertEqual(v.pruefen((KOPF + TEXT).replace("Nachfass: 0", "Nachfass: " + n)), [])

    def test_too_short_fails(self):
        self.assertTrue(any("zu kurz" in f for f in v.pruefen(KOPF + "Hallo, bitte Geld.\n")))


class Freigabe(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "01-test.md")
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write(KOPF + TEXT)

    def tearDown(self):
        self.tmp.cleanup()

    def test_not_approved_without_yes(self):
        self.assertFalse(v.ist_freigegeben(self.path))

    def test_wrong_reply_is_not_recorded(self):
        with self.assertRaises(v.VersandError):
            v.freigabe(self.path, "ja, aber kürzer")
        self.assertFalse(os.path.exists(v.freigaben_pfad(self.path)))
        self.assertFalse(v.ist_freigegeben(self.path))

    def test_yes_is_recorded_for_exactly_this_text(self):
        e = v.freigabe(self.path, "ja")
        self.assertEqual(e["antwort"], "ja")
        self.assertTrue(v.ist_freigegeben(self.path))
        with open(v.freigaben_pfad(self.path), encoding="utf-8") as fh:
            self.assertEqual(len(json.load(fh)), 1)

    def test_changed_text_needs_a_new_yes(self):
        v.freigabe(self.path, "yes")
        with open(self.path, "a", encoding="utf-8") as fh:
            fh.write("\nPS: Noch ein Satz.\n")
        self.assertFalse(v.ist_freigegeben(self.path))

    def test_broken_draft_cannot_be_approved(self):
        with open(self.path, "w", encoding="utf-8") as fh:
            fh.write(KOPF.replace("kontakt@beispiel.de", "a@b.de, c@d.de") + TEXT)
        with self.assertRaises(v.VersandError):
            v.freigabe(self.path, "ja")

    def test_cli_exit_codes(self):
        self.assertEqual(v.main(["pruefen", self.path]), 0)
        self.assertEqual(v.main(["status", self.path]), 1)
        self.assertEqual(v.main(["freigabe", self.path, "--reply", "ja zu allen"]), 2)
        self.assertEqual(v.main(["freigabe", self.path, "--reply", "ja"]), 0)
        self.assertEqual(v.main(["status", self.path]), 0)


if __name__ == "__main__":
    unittest.main()
