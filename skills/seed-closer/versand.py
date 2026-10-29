#!/usr/bin/env python3
"""Freigabe-Schranke für seed-closer. Nur Standardbibliothek, kein Netzwerk.

Keine Rechtsberatung. Das Werkzeug verschickt nie eine Mail und spricht mit keinem Postfach.
Es macht genau drei Dinge rund um den einen Moment, der zählt, dein Ja:

  pruefen    prüft einen Entwurf (Markdown-Datei mit Kopfzeilen) gegen die Regeln des Pakets:
             genau ein Empfänger, keine Kopie oder Blindkopie, eine öffentliche Quelle für die
             Adresse, keine offenen Platzhalter, höchstens zwei Nachfasser.
  freigabe   erfasst dein ausdrückliches Ja für GENAU diesen Entwurf. Als Ja zählt eine Antwort,
             die mit "ja" oder "yes" (oder "y") beginnt und keine Bedingung und keine Mehrzahl
             enthält. "Ja, aber ...", "ja zu allen", "ok", "passt" zählen nicht.
  status     sagt, ob der Entwurf freigegeben ist. Ändert sich der Text nach dem Ja, gilt das Ja
             nicht mehr (Fingerabdruck), dann braucht der neue Text ein neues Ja.

    python3 versand.py pruefen seed/closer/01-calm-storm.md
    python3 versand.py freigabe seed/closer/01-calm-storm.md --reply "ja"
    python3 versand.py status seed/closer/01-calm-storm.md

Das Ja wird in seed/closer/freigaben.json neben dem Entwurf festgehalten (nur anhängen).

Kopfzeilen eines Entwurfs:

    An: kontakt@beispiel.de
    Quelle: https://beispiel.de/kontakt        (öffentliche Seite, auf der die Adresse steht)
    Betreff: ...
    Nachfass: 0                                (0 = erste Mail, 1 oder 2 = Nachfasser)
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

MAX_NACHFASS = 2
YES_WORDS = ("yes", "y", "ja")
BATCH_WORDS = {"all", "every", "everything", "alle", "allen", "allem", "alles", "beide", "beiden",
               "jede", "jeden", "jedes", "stapel", "rest", "restlichen", "übrigen", "jeder"}
DOUBT_WORDS = {"no", "not", "dont", "don't", "wait", "cancel", "stop", "but", "maybe", "later", "hold",
               "unless", "if", "nein", "nicht", "kein", "keine", "warte", "moment", "abbrechen",
               "stopp", "aber", "vielleicht", "später", "halt", "außer", "wenn", "falls", "doch",
               "erst", "noch", "sonst", "bloß", "nur"}
EMAIL_RE = re.compile(r"[\w.+\-]+@[\w\-]+(?:\.[\w\-]+)+")
URL_RE = re.compile(r"^https?://\S+\.\S+(\s.*)?$")  # Text hinter dem Link ist erlaubt


class VersandError(Exception):
    pass


def parse_yes(reply):
    """True nur bei einem klaren, bedingungslosen Ja für genau diesen Entwurf."""
    text = (reply or "").strip().lower()
    if not text:
        return False
    if "?" in text:
        return False
    words = re.findall(r"[\wäöüß']+", text)
    if not words or words[0] not in YES_WORDS:
        return False
    rest = set(words[1:])
    if rest & BATCH_WORDS or rest & DOUBT_WORDS:
        return False
    return True


def kopf(text):
    """Liest die Kopfzeilen (An, Quelle, Betreff, Nachfass) und gibt Kopf und Rumpf zurück."""
    head, body = {}, []
    in_head = True
    for line in text.splitlines():
        m = re.match(r"^(An|Cc|Bcc|Quelle|Betreff|Nachfass)\s*:\s*(.*)$", line, re.I) if in_head else None
        if m:
            head[m.group(1).lower()] = m.group(2).strip()
        else:
            if in_head and line.strip() == "" and head:
                in_head = False
                continue
            if in_head and head:
                in_head = False
            body.append(line)
    return head, "\n".join(body)


def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pruefen(text):
    """Gibt eine Liste von Fehlern zurück. Leer heißt: der Entwurf ist formal in Ordnung."""
    head, body = kopf(text)
    fehler = []
    an = head.get("an", "")
    adressen = EMAIL_RE.findall(an)
    if len(adressen) != 1 or len(re.split(r"[;,]", an)) != 1:
        fehler.append("Genau ein Empfänger in der Zeile An. Keine Sammelmails.")
    if head.get("cc") or head.get("bcc"):
        fehler.append("Keine Kopie (Cc) und keine Blindkopie (Bcc). Eine persönliche Anfrage geht an eine Person.")
    if not URL_RE.match(head.get("quelle", "")):
        fehler.append("Die Zeile Quelle braucht den Link der öffentlichen Seite, auf der die Adresse steht.")
    if not head.get("betreff"):
        fehler.append("Der Betreff fehlt.")
    try:
        n = int(head.get("nachfass", "0"))
        if n < 0 or n > MAX_NACHFASS:
            fehler.append("Nachfass darf nur 0, 1 oder 2 sein: mehr als zwei Nachfasser gibt es nicht.")
    except ValueError:
        fehler.append("Nachfass braucht eine Zahl (0, 1 oder 2).")
    if re.search(r"\[[^\]]+\]|\{\{|TODO|XXX", body):
        fehler.append("Im Text stehen noch Platzhalter in eckigen Klammern oder TODO.")
    if len(body.split()) < 40:
        fehler.append("Der Text ist zu kurz für eine persönliche Anfrage (unter 40 Wörter).")
    if len(body.split()) > 220:
        fehler.append("Der Text ist zu lang (über 220 Wörter). Investoren lesen kurze Mails.")
    return fehler


def freigaben_pfad(entwurf):
    return os.path.join(os.path.dirname(os.path.abspath(entwurf)), "freigaben.json")


def lade(pfad):
    if not os.path.exists(pfad):
        return []
    with open(pfad, encoding="utf-8") as fh:
        return json.load(fh)


def freigabe(entwurf, reply, now=None):
    with open(entwurf, encoding="utf-8") as fh:
        text = fh.read()
    fehler = pruefen(text)
    if fehler:
        raise VersandError("Entwurf nicht freigabefähig: " + " ".join(fehler))
    if not parse_yes(reply):
        raise VersandError("Das war kein ausdrückliches Ja für diesen Entwurf (Antwort: %r). "
                           "Es zählt nur ein einfaches Ja ohne Bedingung." % reply)
    pfad = freigaben_pfad(entwurf)
    eintraege = lade(pfad)
    eintraege.append({
        "entwurf": os.path.basename(entwurf), "fingerabdruck": fingerprint(text), "antwort": reply,
        "zeit": (now or datetime.datetime.now()).replace(microsecond=0).isoformat(),
    })
    with open(pfad, "w", encoding="utf-8") as fh:
        json.dump(eintraege, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return eintraege[-1]


def ist_freigegeben(entwurf):
    with open(entwurf, encoding="utf-8") as fh:
        text = fh.read()
    fp = fingerprint(text)
    name = os.path.basename(entwurf)
    return any(e["entwurf"] == name and e["fingerabdruck"] == fp for e in lade(freigaben_pfad(entwurf)))


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="Freigabe-Schranke für Investorenmails")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("pruefen", "freigabe", "status"):
        s = sub.add_parser(name)
        s.add_argument("entwurf")
        if name == "freigabe":
            s.add_argument("--reply", required=True)
    a = p.parse_args(argv)
    try:
        if a.cmd == "pruefen":
            with open(a.entwurf, encoding="utf-8") as fh:
                fehler = pruefen(fh.read())
            if fehler:
                print("Nicht bereit:")
                for f in fehler:
                    print("- " + f)
                return 1
            print("Formal in Ordnung. Verschickt ist nichts. Es fehlt dein Ja.")
            return 0
        if a.cmd == "freigabe":
            e = freigabe(a.entwurf, a.reply)
            print("Dein Ja ist erfasst (%s). Erst jetzt darf genau dieser Entwurf raus." % e["zeit"])
            return 0
        if ist_freigegeben(a.entwurf):
            print("Freigegeben (Text unverändert seit deinem Ja).")
            return 0
        print("Nicht freigegeben. Es fehlt ein Ja für den aktuellen Text.")
        return 1
    except (VersandError, OSError, ValueError) as e:
        print("Nicht erfasst: %s" % e, file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
