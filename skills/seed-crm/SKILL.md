---
name: seed-crm
description: >-
  Die Kontaktliste. Führt alle Investoren als CSV-Datei mit Status, letztem Kontakt und
  Nachfass-Datum und sagt dir jeden Tag, bei wem etwas fällig ist. Setzt die Regeln des
  Pakets durch: höchstens zwei Nachfasser, mindestens fünf Werktage Abstand, danach
  Status "kein Interesse". Verschickt selbst nichts. Nutze ihn, wenn der Nutzer sagt
  "wer ist fällig", "Investorenliste führen", "Status der Anfragen", "wem muss ich
  nachfassen", "Kontaktliste", "CRM" oder "wie weit bin ich mit den Investoren"
  (englisch: "investor tracker", "who do I follow up with").
argument-hint: "[liste | faellig | add | ...]"
---

# seed-crm

Wer zwanzig Investoren anschreibt, verliert den Überblick, wenn er ihn nicht festhält.
Dieser Skill ist die einfachste Lösung: eine CSV-Datei, die du in Excel öffnen kannst, und
ein kleines Werkzeug, das die Fristen rechnet.

Werkzeug in diesem Ordner:

```bash
python3 "${CLAUDE_SKILL_DIR}/crm.py" faellig seed/crm.csv
```

Unter Windows heißt der Aufruf oft `py` statt `python3`. Nur Standardbibliothek, kein
Netzwerk, das Werkzeug verschickt nie etwas.

## Grundregeln

- Keine Finanz- oder Rechtsberatung.
- Ohne öffentliche Quelle kommt kein Investor in die Liste. Das Werkzeug lehnt `add` ohne
  `--quelle` ab.
- Personenbezogene Daten sparsam: Name und die Kontaktadresse, die der Investor selbst
  öffentlich nennt. Keine privaten Notizen über Menschen. Die Datei bleibt auf dem Rechner
  des Nutzers.
- Das Werkzeug zählt Werktage von Montag bis Freitag. Feiertage kennt es nicht: Zähl sie
  selbst dazu, und verschiebe das Nachfass-Datum entsprechend im Zweifel nach hinten.

## Die Status

| Status | Bedeutung | Weiter mit |
| --- | --- | --- |
| `offen` | Investor ist in der Liste, noch nichts geschrieben | `entwurf` |
| `entwurf` | Mail liegt als Entwurf vor, wartet auf das Ja des Nutzers | `versendet` |
| `versendet` | die Mail ist raus (Datum steht), Nachfass-Datum gesetzt | `antwort`, Nachfassen, `termin` |
| `antwort` | der Investor hat geantwortet | `termin` oder `absage` |
| `termin` | ein Gespräch ist vereinbart | `/seed-gespraech` |
| `absage` | der Investor hat Nein gesagt | nichts, mit Grund in der Notiz |
| `kein_interesse` | keine Antwort nach zwei Nachfassern und fünf weiteren Werktagen | nichts |

## Die Befehle

```bash
python3 crm.py init seed/crm.csv
python3 crm.py add seed/crm.csv --name "Name" --typ Fonds --kontakt "Formular" --quelle https://...
python3 crm.py entwurf seed/crm.csv --id 3
python3 crm.py versendet seed/crm.csv --id 3 --datum 2026-11-02
python3 crm.py faellig seed/crm.csv --heute 2026-11-09
python3 crm.py nachfass seed/crm.csv --id 3 --datum 2026-11-09
python3 crm.py antwort seed/crm.csv --id 3 --datum 2026-11-10
python3 crm.py termin seed/crm.csv --id 3 --datum 2026-11-20
python3 crm.py abschliessen seed/crm.csv --heute 2026-11-30
python3 crm.py liste seed/crm.csv
```

`versendet` trägst du erst ein, wenn die Mail wirklich raus ist (nach dem Ja des Nutzers in
`/seed-closer` und dem echten Versand). `nachfass` zählt einen Nachfasser und setzt das
nächste Datum fünf Werktage später. Vor dem Datum lehnt das Werkzeug es ab, ebenso einen
dritten Nachfasser.

## Schritt 1: Liste anlegen

Gibt es `seed/investoren.csv` oder `seed/investoren.md`, übernimm die Einträge mit Fit ab 3
per `add`, jeweils mit Quelle. Frag den Nutzer, wen er zuerst anschreiben will, und setze
nur diese Einträge auf `entwurf`, sobald `/seed-closer` den Entwurf hat.

## Schritt 2: die tägliche Frage

Wenn der Nutzer fragt, was fällig ist, oder `/seed-crm` ohne Zusatz ruft:
1. `crm.py faellig` mit dem heutigen Datum.
2. Pro Treffer ein Satz: wer, wie oft schon nachgefasst, ob "nachfassen" oder "abschließen"
   fällig ist.
3. Für jedes "nachfassen": biete an, den Entwurf über `/seed-closer` zu schreiben. Er geht
   nur mit Ja raus.
4. Für jedes "abschließen": frag kurz nach und starte `crm.py abschliessen`.

## Schritt 3: der Wochenblick

Einmal pro Woche eine Zusammenfassung aus `crm.py liste`: wie viele offen, versendet,
Antworten, Termine, Absagen, kein Interesse. Dazu zwei Sätze: Wo stockt es, und was ist die
nächste Handlung? Ehrlich bleiben: Kalte Anfragen bleiben oft unbeantwortet, das ist normal und
kein Urteil über die Idee.

## Ergebnis

`seed/crm.csv` (Semikolon, UTF-8, öffnet in Excel) und der Überblick im Chat. Als Nächstes:
`/seed-closer` für alles, was auf ein Ja oder ein Nachfassen wartet.
