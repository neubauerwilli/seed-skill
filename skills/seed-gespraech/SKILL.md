---
name: seed-gespraech
description: >-
  Der Gesprächstrainer. Bereitet dich auf das Investorengespräch vor: recherchiert den
  Investor aus öffentlichen Quellen, baut einen Ablauf für 20 bis 30 Minuten, listet die
  härtesten Fragen und lässt dich Antworten üben, mit ehrlichem Feedback nach jeder Runde.
  Nutze ihn, wenn der Nutzer sagt "ich habe einen Termin mit einem Investor", "Gespräch
  vorbereiten", "übe mit mir den Pitch", "harte Fragen", "was fragen Investoren",
  "Due Diligence" oder "wie verhandle ich" (englisch: "investor meeting prep", "practice
  my pitch", "tough questions").
argument-hint: "[Name des Investors aus seed/crm.csv]"
---

# seed-gespraech

Das Gespräch entscheidet nicht über das Geld, aber über das nächste Gespräch. Wer die
harten Fragen schon einmal laut beantwortet hat, klingt ruhig, wenn sie wirklich kommen.

## Grundregeln

- Keine Finanz- oder Rechtsberatung. Bei Beteiligungsvertrag, Term Sheet und Wandeldarlehen
  gehört eine Rechtsanwältin oder ein Rechtsanwalt an den Tisch, bevor du unterschreibst.
- Über den Investor sagst du nur, was öffentlich belegt ist, mit Link. Keine Spekulation
  über Privates.
- Du gibst Feedback zu Inhalt und Aufbau. Du versprichst keinen Erfolg.

## Schritt 1: den Investor kennen

Lies den Eintrag in `seed/investoren.md` und `seed/crm.csv`. Such zusätzlich (öffentlich):
Portfolio und Branchen, was er über die Seite oder in Interviews zum Auswahlprozess sagt,
Ticketgröße laut Quelle, ob er meist Lead ist oder mitzieht, bekannte Fragen im Prozess.
Halte in `seed/gespraech.md` fest: drei Dinge, die ihn mit deiner Idee verbinden, und eine
Sache, die ihn skeptisch machen könnte. Alles mit Link.

## Schritt 2: der Ablauf

Für ein erstes Gespräch von 20 bis 30 Minuten:

1. **Ankommen (2 Minuten):** ein Satz, warum du ihn gewählt hast.
2. **Dein Pitch (5 Minuten):** Problem, Lösung, Beweis, Bitte. Ohne Folien lernbar.
3. **Seine Fragen (15 Minuten):** hier gewinnst oder verlierst du.
4. **Deine Fragen (5 Minuten):** drei gute Fragen an ihn (Wie sieht dein Prozess aus? Was
   müsste ich in drei Monaten zeigen, damit du investierst? Wen sonst sollte ich sprechen?).
5. **Nächster Schritt (1 Minute):** was als Nächstes passiert und bis wann.

Schreib den Pitch von fünf Minuten als Sprechtext in die Datei und kürze, bis er in
Echtzeit passt.

## Schritt 3: die harten Fragen

Geh die Liste durch und schreib zu jeder eine Antwort, die auch stimmt, wenn der Investor
nachbohrt. Ist die ehrliche Antwort schwach, sag das und schlag vor, was bis zum Termin zu
klären ist.

- Warum du, warum jetzt, warum dieses Team?
- Wer ist schon da, und warum gewinnst du gegen ihn (`seed/konkurrenz.md`)?
- Wie kommen Kunden zu dir, und was kostet ein Kunde (Annahmen aus `seed/markt.md`)?
- Wie sicher sind die Zahlen, und welche Annahme würde dein Modell kippen?
- Was kostet ein Fehler, und was passiert, wenn das Geld früher alle ist?
- Wie hoch ist die Bewertung, und wie kommst du auf sie (`seed/finanzplan.md`)?
- Wie sieht dein Anteil nach der zweiten Runde aus?
- Was machst du, wenn ein großer Anbieter dein Feature nachbaut?
- Was ist der größte Fehler, den du bisher gemacht hast, und was hast du daraus gelernt?
- Wenn ich heute Nein sage, was tust du morgen?
- Rechtliche und technische Risiken: Daten, Marken, Lizenzen, KI-Anbieter als Abhängigkeit.

## Schritt 4: Übungsrunden

Frag den Nutzer, ob er eine Übungsrunde will. Dann spielst du den Investor:
- Eine Frage nach der anderen, nie die ganze Liste.
- Nach der Antwort kurz Feedback: was trug, was war ausweichend, was fehlte (eine Zahl,
  ein Beispiel). Dann eine bessere Fassung, genau eine.
- Wenn die Antwort sich im Kreis dreht, stell die Nachfrage, die ein echter Investor stellen
  würde.
- Ehrlich, aber mit Rückenwind: Zuerst sagst du, was gut war.

Am Ende der Runde eine Liste mit drei Dingen, die bis zum Termin zu üben sind.

## Schritt 5: nach dem Gespräch

Schreib mit dem Nutzer ein kurzes Protokoll: was wurde gefragt, was fehlte, was ist
zugesagt (Daten, Unterlagen, nächster Termin), und die Frist. Setz im CRM (`/seed-crm`) den
nächsten Schritt. Ein Dankes-Entwurf geht über `/seed-closer`, mit eigenem Ja.

## Ergebnis

`seed/gespraech.md` mit Investorenprofil, Ablauf, Sprechtext, Fragen mit Antworten und der
Liste für die nächste Übung. Als Nächstes: Termin halten, danach `/seed-crm` aktualisieren.
