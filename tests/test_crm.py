import datetime
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout, redirect_stderr

from _load import load

crm = load("seed-crm", "crm")
D = datetime.date


def neue_zeile(rows=None):
    rows = [] if rows is None else rows
    return crm.add(rows, "Beispiel Fonds", "Fonds", "Formular", "https://beispiel.de/pitch"), rows


class Werktage(unittest.TestCase):
    def test_five_workdays_skip_weekends(self):
        self.assertEqual(crm.add_workdays(D(2026, 11, 2), 5), D(2026, 11, 9))  # Montag + 5 Werktage
        self.assertEqual(crm.add_workdays(D(2026, 11, 6), 5), D(2026, 11, 13))  # Freitag + 5 Werktage

    def test_weekend_start(self):
        self.assertEqual(crm.add_workdays(D(2026, 11, 7), 1), D(2026, 11, 9))  # Samstag + 1 = Montag


class Nachfass(unittest.TestCase):
    def versendet(self):
        row, rows = neue_zeile()
        crm.set_entwurf(row)
        crm.set_versendet(row, "2026-11-02")
        return row, rows

    def test_add_requires_a_source(self):
        with self.assertRaises(crm.CrmError):
            crm.add([], "Ohne Quelle", quelle="")

    def test_send_sets_next_followup_five_workdays_later(self):
        row, _ = self.versendet()
        self.assertEqual(row["status"], "versendet")
        self.assertEqual(row["naechster_nachfass"], "2026-11-09")
        self.assertEqual(row["nachfass_anzahl"], "0")

    def test_cannot_send_without_draft(self):
        row, _ = neue_zeile()
        with self.assertRaises(crm.CrmError):
            crm.set_versendet(row, "2026-11-02")

    def test_followup_too_early_is_refused(self):
        row, _ = self.versendet()
        with self.assertRaises(crm.CrmError):
            crm.set_nachfass(row, "2026-11-06")
        self.assertEqual(row["nachfass_anzahl"], "0")

    def test_two_followups_then_no_third(self):
        row, _ = self.versendet()
        crm.set_nachfass(row, "2026-11-09")
        self.assertEqual(row["nachfass_anzahl"], "1")
        self.assertEqual(row["naechster_nachfass"], "2026-11-16")
        crm.set_nachfass(row, "2026-11-16")
        self.assertEqual(row["nachfass_anzahl"], "2")
        with self.assertRaises(crm.CrmError):
            crm.set_nachfass(row, "2026-11-23")

    def test_due_list_and_closing_after_second_followup(self):
        row, rows = self.versendet()
        self.assertEqual(crm.faellig(rows, D(2026, 11, 6)), [])
        self.assertEqual(crm.aktion(row, D(2026, 11, 9)), "nachfassen")
        crm.set_nachfass(row, "2026-11-09")
        crm.set_nachfass(row, "2026-11-16")
        self.assertIsNone(crm.aktion(row, D(2026, 11, 20)))
        self.assertEqual(crm.aktion(row, D(2026, 11, 23)), "abschliessen")
        geschlossen = crm.abschliessen(rows, D(2026, 11, 23))
        self.assertEqual(len(geschlossen), 1)
        self.assertEqual(row["status"], "kein_interesse")
        self.assertEqual(row["naechster_nachfass"], "")
        self.assertEqual(crm.faellig(rows, D(2026, 12, 31)), [])

    def test_answer_stops_followups(self):
        row, rows = self.versendet()
        crm.set_antwort(row, "2026-11-04")
        self.assertEqual(row["status"], "antwort")
        self.assertEqual(crm.faellig(rows, D(2026, 12, 31)), [])
        with self.assertRaises(crm.CrmError):
            crm.set_nachfass(row, "2026-11-09")
        crm.set_termin(row, "2026-11-20")
        self.assertEqual(row["status"], "termin")

    def test_bad_date_is_refused(self):
        row, _ = neue_zeile()
        crm.set_entwurf(row)
        with self.assertRaises(crm.CrmError):
            crm.set_versendet(row, "2. November")


class Datei(unittest.TestCase):
    def test_roundtrip_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "seed", "crm.csv")
            out, err = io.StringIO(), io.StringIO()
            with redirect_stdout(out), redirect_stderr(err):
                self.assertEqual(crm.main(["init", path]), 0)
                self.assertEqual(crm.main(["add", path, "--name", "Ä Fonds", "--quelle", "https://a.de"]), 0)
                self.assertEqual(crm.main(["entwurf", path, "--id", "1"]), 0)
                self.assertEqual(crm.main(["versendet", path, "--id", "1", "--datum", "2026-11-02"]), 0)
                self.assertEqual(crm.main(["faellig", path, "--heute", "2026-11-09"]), 0)
                self.assertEqual(crm.main(["nachfass", path, "--id", "1", "--datum", "2026-11-04"]), 2)
                self.assertEqual(crm.main(["init", path]), 2)
            rows = crm.read(path)
            self.assertEqual(rows[0]["name"], "Ä Fonds")
            self.assertEqual(rows[0]["status"], "versendet")
            self.assertIn("nachfassen", out.getvalue())


if __name__ == "__main__":
    unittest.main()
