---
name: seed-zahlen
description: >-
  Der Finanzchef für die Runde. Rechnet mit einem Python-Werkzeug den Kapitalbedarf für
  das erste Jahr (Startkosten, laufende Kosten, Einnahmen, Reserve), die Reichweite des
  Geldes, die Bewertung vor und nach der Runde (Pre-Money, Post-Money), den Anteil der
  Investoren und die Verwässerung über spätere Runden. Jede Zahl lässt sich auf eine
  Eingabe zurückführen. Nutze ihn, wenn der Nutzer sagt "wie viel Geld brauche ich",
  "Kapitalbedarf", "Bewertung", "wie viel Anteil gebe ich ab", "Verwässerung",
  "Finanzplan", "wie lange reicht das Geld" oder "Cap Table" (englisch: "how much should
  I raise", "valuation", "dilution", "runway").
argument-hint: "[Pfad zu seed/zahlen.json]"
---

# seed-zahlen

Die Frage hinter jedem Investorengespräch: "Wie viel brauchst du, wofür, und was bekomme
ich dafür?" Dieser Skill beantwortet sie mit Rechnung statt Bauchgefühl.

Werkzeug in diesem Ordner:

```bash
python3 "${CLAUDE_SKILL_DIR}/finanzplan.py" seed/zahlen.json --out seed/finanzplan.md
```

Unter Windows nimm gleich `py` statt `python3`, dort fehlt `python3` meistens. Das Werkzeug braucht nur die
Standardbibliothek.

## Grundregeln

- Keine Finanz- oder Rechtsberatung. Bewertung, Anteile, Wandeldarlehen und Verträge
  prüft eine Fachperson, bevor etwas unterschrieben wird.
- Das Werkzeug rechnet nur mit deinen Eingaben. Eine Schätzung bleibt eine Schätzung und
  wird im Bericht auch so genannt. Stell nie eine Schätzung als Tatsache dar.
- Die "übliche Spanne" für abgegebene Anteile (10 bis 25 Prozent in einer ersten Runde)
  ist eine Faustregel aus dem Markt, kein Gesetz. Sag das, wenn du sie nennst.

## Schritt 1: Eingaben sammeln

Schreib `seed/zahlen.json` (Aufbau: `example.json` in diesem Ordner, ein Fitness-KI-Gründer
mit 150.000 € Ziel). Felder:

| Feld | Was hineingehört |
| --- | --- |
| `kapital_ziel` | die Summe, die du einsammeln willst |
| `startup` | einmalige Ausgaben vor dem Start (Gründung, Marke, erste Ausstattung) |
| `ausgaben_monatlich` | alles, was jeden Monat anfällt (Entwicklung, Hosting, Marketing, Gehälter) |
| `einnahmen_monatlich` | 12 Zahlen: erwartete Einnahmen je Monat, vorsichtig |
| `puffer_monate` | wie viele Monate Ausgaben als Reserve bleiben sollen (Standard 3) |
| `abgabe_anteil` | Anteil, den du abgibst (zum Beispiel 0.15) **oder** `pre_money`: die Bewertung vor der Runde |
| `gruender` | Namen und Anteile vor der Runde, Summe 1.0 |
| `optionspool` | Anteil für künftige Mitarbeiter, vor der Runde gebildet |
| `folgerunden` | optional: spätere Runden mit Betrag und Pre-Money zum Durchrechnen |

Woher die Zahlen kommen, in dieser Reihenfolge: eigene Angebote, Rechnungen und Verträge;
öffentliche Preise (Preisliste des Dienstleisters, mit Link in `seed/zahlen-quellen.md`);
deine Schätzung, als Schätzung beschriftet. Frag nach allem, was nur der Nutzer weiß.

## Schritt 2: rechnen

Starte das Werkzeug. Es gibt aus:
- den Kapitalbedarf: tiefster Kontostand im ersten Jahr plus Reserve,
- die Reichweite: wie viele Monate das Ziel-Kapital trägt,
- Pre-Money, Post-Money und den Anteil der Investoren,
- eine Tabelle, wem nach dem Seed und nach jeder Folgerunde was gehört,
- den Kontostand Monat für Monat (ohne das neue Kapital),
- Warnungen, wenn das Ziel zu klein ist, das Geld weniger als 12 Monate hält oder mehr als
  25 Prozent abgegeben werden.

Lies die Warnungen vor und erkläre sie in normalen Worten. Fehlermeldungen des Werkzeugs
("die Anteile der Gründer müssen zusammen 100 Prozent ergeben") gibst du dem Nutzer weiter
und rätst nie selbst Werte dazu.

## Schritt 3: die Fragen, die Investoren stellen

Beantworte mit den Zahlen:
1. Wie viel Geld und warum genau diese Summe? (Kapitalbedarf plus Reserve.)
2. Was erreichst du damit in 12 bis 18 Monaten? Drei Meilensteine mit Zahlen.
3. Welche Bewertung und warum? Gib die Rechnung und sag, dass die Bewertung am Ende
   Verhandlung ist. Ein hoher Wunsch ohne Beleg schreckt ab.
4. Was bleibt dir nach der zweiten Runde? (Die Tabelle zeigt es.)
5. Wann bist du ohne neues Geld am Ende, und was passiert dann?

## Schritt 4: Was-wäre-wenn

Rechne mindestens drei Varianten durch und zeig sie nebeneinander: Einnahmen 30 Prozent
niedriger, Kosten 20 Prozent höher, Runde 3 Monate später. Ändere dafür die Datei und starte
das Werkzeug erneut. Sag ehrlich, wann das Ziel nicht mehr reicht.

## Ergebnis

`seed/zahlen.json`, `seed/finanzplan.md` und ein Absatz im Chat: "Du brauchst X, gibst Y
Prozent ab, das Geld hält Z Monate." Als Nächstes: `/seed-investoren`.
