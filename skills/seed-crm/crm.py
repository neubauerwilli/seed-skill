#!/usr/bin/env python3
"""Kontaktliste für Investorenanfragen (seed-crm). Nur Standardbibliothek, kein Netzwerk.

Das Werkzeug verschickt nie etwas. Es führt eine CSV (Semikolon, UTF-8) mit Status und
Nachfass-Datum und setzt die Regeln des Pakets durch:

  * höchstens zwei Nachfasser je Investor,
  * zwischen zwei Nachrichten mindestens fünf Werktage (Montag bis Freitag; Feiertage
    rechnet das Werkzeug nicht mit, zähl sie selbst dazu),
  * nach dem zweiten Nachfasser und fünf weiteren Werktagen ohne Antwort: "kein_interesse".

    python3 crm.py init seed/crm.csv
    python3 crm.py add seed/crm.csv --name "Calm/Storm" --typ Fonds --quelle https://calmstorm.vc/pitch
    python3 crm.py entwurf seed/crm.csv --id 1
    python3 crm.py versendet seed/crm.csv --id 1 --datum 2026-11-02
    python3 crm.py nachfass seed/crm.csv --id 1 --datum 2026-11-09
    python3 crm.py antwort seed/crm.csv --id 1 --datum 2026-11-10
    python3 crm.py termin seed/crm.csv --id 1 --datum 2026-11-20
    python3 crm.py faellig seed/crm.csv --heute 2026-11-12
    python3 crm.py abschliessen seed/crm.csv --heute 2026-11-30
    python3 crm.py liste seed/crm.csv
"""

import argparse
import csv
import datetime
import os
import sys

FELDER = ["id", "name", "typ", "kontakt", "quelle", "status", "erste_nachricht", "letzter_kontakt",
          "nachfass_anzahl", "naechster_nachfass", "notiz"]
STATI = ("offen", "entwurf", "versendet", "antwort", "termin", "absage", "kein_interesse")
MAX_NACHFASS = 2
ABSTAND_WERKTAGE = 5


class CrmError(Exception):
    pass


def parse_date(text, label="Datum"):
    try:
        return datetime.date.fromisoformat(str(text))
    except ValueError:
        raise CrmError("%s muss JJJJ-MM-TT sein, nicht %r" % (label, text))


def add_workdays(start, days):
    """Addiert Werktage (Montag bis Freitag). Feiertage zählt das Werkzeug nicht."""
    d, left = start, days
    while left > 0:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5:
            left -= 1
    return d


def read(path):
    if not os.path.exists(path):
        raise CrmError("Datei fehlt: %s (erst `init` ausführen)" % path)
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter=";"))
    for r in rows:
        for f in FELDER:
            r.setdefault(f, "")
    return rows


def write(path, rows):
    d = os.path.dirname(path)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FELDER, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def find(rows, id_):
    for r in rows:
        if str(r["id"]) == str(id_):
            return r
    raise CrmError("keinen Eintrag mit id %s gefunden" % id_)


def add(rows, name, typ="", kontakt="", quelle="", notiz=""):
    if not name.strip():
        raise CrmError("name fehlt")
    if not quelle.strip():
        raise CrmError("quelle fehlt: ohne öffentliche Quelle kommt kein Investor in die Liste")
    nxt = max([int(r["id"]) for r in rows] + [0]) + 1
    row = {"id": str(nxt), "name": name.strip(), "typ": typ, "kontakt": kontakt, "quelle": quelle,
           "status": "offen", "erste_nachricht": "", "letzter_kontakt": "", "nachfass_anzahl": "0",
           "naechster_nachfass": "", "notiz": notiz}
    rows.append(row)
    return row


def set_entwurf(row):
    if row["status"] != "offen":
        raise CrmError("Entwurf nur für Einträge mit Status offen (aktuell: %s)" % row["status"])
    row["status"] = "entwurf"


def set_versendet(row, datum):
    """Erste Nachricht ist raus. Nur nach dem ausdrücklichen Ja des Nutzers und dem echten Versand aufrufen."""
    if row["status"] != "entwurf":
        raise CrmError("versendet nur nach einem Entwurf (aktuell: %s)" % row["status"])
    d = parse_date(datum)
    row["status"] = "versendet"
    row["erste_nachricht"] = d.isoformat()
    row["letzter_kontakt"] = d.isoformat()
    row["nachfass_anzahl"] = "0"
    row["naechster_nachfass"] = add_workdays(d, ABSTAND_WERKTAGE).isoformat()


def set_nachfass(row, datum):
    if row["status"] != "versendet":
        raise CrmError("Nachfassen nur bei Status versendet (aktuell: %s)" % row["status"])
    n = int(row["nachfass_anzahl"] or 0)
    if n >= MAX_NACHFASS:
        raise CrmError("schon %d Nachfasser: mehr gibt es nicht. Der Status wird nach dem Warten kein_interesse" % n)
    d = parse_date(datum)
    frueh = parse_date(row["naechster_nachfass"], "naechster_nachfass")
    if d < frueh:
        raise CrmError("zu früh: frühestens am %s (fünf Werktage Abstand)" % frueh.isoformat())
    row["nachfass_anzahl"] = str(n + 1)
    row["letzter_kontakt"] = d.isoformat()
    row["naechster_nachfass"] = add_workdays(d, ABSTAND_WERKTAGE).isoformat()


def set_antwort(row, datum):
    if row["status"] != "versendet":
        raise CrmError("Antwort nur bei Status versendet (aktuell: %s)" % row["status"])
    row["status"] = "antwort"
    row["letzter_kontakt"] = parse_date(datum).isoformat()
    row["naechster_nachfass"] = ""


def set_termin(row, datum):
    if row["status"] not in ("antwort", "versendet"):
        raise CrmError("Termin nur bei Status antwort oder versendet (aktuell: %s)" % row["status"])
    row["status"] = "termin"
    row["letzter_kontakt"] = parse_date(datum).isoformat()
    row["naechster_nachfass"] = ""


def set_absage(row):
    row["status"] = "absage"
    row["naechster_nachfass"] = ""


def aktion(row, heute):
    """Was ist heute bei diesem Eintrag fällig? 'nachfassen', 'abschliessen' oder None."""
    if row["status"] != "versendet" or not row["naechster_nachfass"]:
        return None
    if heute < parse_date(row["naechster_nachfass"], "naechster_nachfass"):
        return None
    return "nachfassen" if int(row["nachfass_anzahl"] or 0) < MAX_NACHFASS else "abschliessen"


def faellig(rows, heute):
    return [(r, aktion(r, heute)) for r in rows if aktion(r, heute)]


def abschliessen(rows, heute):
    """Setzt alle Einträge, deren zweiter Nachfasser unbeantwortet blieb, auf kein_interesse."""
    geschlossen = []
    for r, a in faellig(rows, heute):
        if a == "abschliessen":
            r["status"] = "kein_interesse"
            r["naechster_nachfass"] = ""
            geschlossen.append(r)
    return geschlossen


def zusammenfassung(rows):
    zaehler = {s: 0 for s in STATI}
    for r in rows:
        zaehler[r["status"]] = zaehler.get(r["status"], 0) + 1
    return zaehler


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Investoren-Kontaktliste")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("init", "liste", "faellig", "abschliessen", "add", "entwurf", "versendet", "nachfass",
                 "antwort", "termin", "absage"):
        s = sub.add_parser(name)
        s.add_argument("csv")
        if name in ("entwurf", "versendet", "nachfass", "antwort", "termin", "absage"):
            s.add_argument("--id", required=True)
        if name in ("versendet", "nachfass", "antwort", "termin"):
            s.add_argument("--datum", default=datetime.date.today().isoformat())
        if name in ("faellig", "abschliessen"):
            s.add_argument("--heute", default=datetime.date.today().isoformat())
        if name == "add":
            s.add_argument("--name", required=True)
            s.add_argument("--typ", default="")
            s.add_argument("--kontakt", default="")
            s.add_argument("--quelle", default="")
            s.add_argument("--notiz", default="")
    a = p.parse_args(argv)
    try:
        if a.cmd == "init":
            if os.path.exists(a.csv):
                raise CrmError("%s gibt es schon, nichts überschrieben" % a.csv)
            write(a.csv, [])
            print("Angelegt: %s" % a.csv)
            return 0
        rows = read(a.csv)
        if a.cmd == "liste":
            for r in rows:
                print("%s | %s | %s | %s | Nachfass %s | nächster %s" % (
                    r["id"], r["name"], r["status"], r["typ"], r["nachfass_anzahl"], r["naechster_nachfass"] or "-"))
            print(", ".join("%s %d" % (k, v) for k, v in zusammenfassung(rows).items() if v))
            return 0
        if a.cmd == "faellig":
            todo = faellig(rows, parse_date(a.heute))
            for r, akt in todo:
                print("%s | %s | %s (Nachfass %s von %d)" % (r["id"], r["name"], akt, r["nachfass_anzahl"], MAX_NACHFASS))
            if not todo:
                print("Heute ist nichts fällig.")
            return 0
        if a.cmd == "abschliessen":
            zu = abschliessen(rows, parse_date(a.heute))
            write(a.csv, rows)
            print("Auf kein_interesse gesetzt: %s" % (", ".join(r["name"] for r in zu) or "niemand"))
            return 0
        if a.cmd == "add":
            r = add(rows, a.name, a.typ, a.kontakt, a.quelle, a.notiz)
            write(a.csv, rows)
            print("Hinzugefügt: %s (id %s)" % (r["name"], r["id"]))
            return 0
        r = find(rows, a.id)
        if a.cmd == "entwurf":
            set_entwurf(r)
        elif a.cmd == "versendet":
            set_versendet(r, a.datum)
        elif a.cmd == "nachfass":
            set_nachfass(r, a.datum)
        elif a.cmd == "antwort":
            set_antwort(r, a.datum)
        elif a.cmd == "termin":
            set_termin(r, a.datum)
        elif a.cmd == "absage":
            set_absage(r)
        write(a.csv, rows)
        print("%s: Status %s, Nachfasser %s, nächster %s" % (r["name"], r["status"], r["nachfass_anzahl"],
                                                            r["naechster_nachfass"] or "-"))
        return 0
    except CrmError as e:
        print("Fehler: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
