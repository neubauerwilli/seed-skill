---
name: seed-investoren
description: >-
  Der Investoren-Scout. Sucht zu deiner Idee die passenden Business Angels, Angel-Netzwerke
  und Frühphasenfonds im DACH-Raum und darüber hinaus, mit Begründung, warum sie passen,
  und einer öffentlichen Quelle für jede Angabe. Erfindet keinen Investor, keine
  Ticketgröße und keine Kontaktadresse. Nutze ihn, wenn der Nutzer sagt "welche
  Investoren passen zu mir", "finde Business Angels", "wer investiert in meine Branche",
  "Investorenliste", "Fonds für mein Startup", "an wen wende ich mich" oder "Investoren
  recherchieren" (englisch: "find investors", "angel investors for my startup").
argument-hint: "[Pfad zu seed/idee.md]"
---

# seed-investoren

Ein Investor, der nicht zu deiner Idee passt, kostet dich Wochen und bringt ein höfliches
Nein. Dieser Skill sucht nach Fit, nicht nach Menge, und belegt jede Zeile.

## Grundregeln

- Keine Finanz- oder Rechtsberatung.
- **Nichts erfinden.** Jeder Investor, jede Ticketgröße, jede Branche und jede
  Kontaktadresse hat einen öffentlichen Link. Was du nicht belegen kannst, schreibst du als
  "nicht belegt" in die Zelle oder lässt den Investor weg. Lieber zehn belegte als dreißig
  geratene.
- Eine Aggregator-Seite (Datenbanken, Ranglisten) ist ein Hinweis, kein Beleg. Öffne die
  eigene Seite des Investors und prüfe dort Phase, Branche und Kontaktweg. Gibt es nur die
  Aggregator-Angabe, markiere sie als "nur Dritt-Quelle".
- Kontaktadressen nur, wenn der Investor sie selbst öffentlich nennt (Kontaktseite,
  Pitch-Seite). Rate nie Adressen und rate nie Vornamen-Muster. Hat ein Investor ein
  Bewerbungsformular, nutze das und schreib "Formular" statt einer Adresse.
- Prüfe, ob Konditionen noch aktuell sind (Datum der Seite, Fonds-Laufzeit, aktueller
  Fokus). Ein Fonds, der laut Seite nicht mehr investiert, fliegt raus.

## Schritt 1: das Suchprofil

Lies `seed/idee.md`, `seed/markt.md` und `seed/finanzplan.md`, falls sie existieren. Halte
fest:
- Branche und Geschäftsmodell (zum Beispiel B2C-Abo, Gesundheit, KI).
- Phase (Idee, Prototyp, erste Kunden, erste Einnahmen).
- Gesuchtes Kapital und gewünschter Anteil.
- Land und Stadt des Teams, Sprache, ob Gründerin oder Gründer (einige Fonds haben Programme für Frauen, nur mit Quelle erwähnen).

Das Profil aus drei Zeilen kommt an den Anfang von `seed/investoren.md`.

## Schritt 2: suchen

Such mit der Websuche in vier Töpfen und notiere pro Fund den Link:

1. **Business-Angel-Netzwerke und Clubs** (Dachverband, regionale Netzwerke, Branchenclubs).
2. **Frühphasenfonds** (Pre-Seed und Seed), regional oder mit Branchenfokus.
3. **Öffentlich getragene Fonds** (Beteiligungsgesellschaften der Länder, Bundesfonds).
4. **Crowdinvesting und Plattformen**, wenn viele kleine Geldgeber zur Idee passen.

Für jeden Kandidaten öffnest du die eigene Seite und liest: Phasen, Branchen, Region, wie
man sich bewirbt, ob eine Ticketgröße genannt wird, Beispiele aus dem Portfolio.

## Schritt 3: bewerten

Je Investor ein Fit-Wert von 0 bis 5, aus vier getrennt genannten Punkten:
- **Phase:** investiert er in deiner Phase?
- **Branche:** nennt er deine Branche oder verwandte Beispiele im Portfolio?
- **Ticket:** passt dein Kapitalziel zu seiner genannten Größe? (Ist sie nicht genannt: "offen".)
- **Region und Weg:** investiert er in dein Land, und gibt es einen öffentlichen Bewerbungsweg?

Ein Investor, dessen genannte Mindestsumme klar über deinem Ziel liegt, bekommt ehrlich
"derzeit nicht passend, später prüfen". Das gehört in die Liste: Es zeigt dem Nutzer, wer
für die zweite Runde interessant wird.

## Schritt 4: die Liste

`seed/investoren.md`, eine Tabelle: Name, Typ, Sitz, Fit (0 bis 5), Begründung in einem
Satz, Ticket laut Quelle, Bewerbungsweg (Formular oder öffentliche Adresse), Link zur
Quelle, Abrufdatum, Vermerke (nur Dritt-Quelle, Name geändert, Fonds evtl. geschlossen).
Sortiere nach Fit. Darunter in zwei Absätzen: wo die Lücken sind und was der Nutzer selbst
noch prüfen muss (aktuelle Konditionen, ob der Fonds noch aktiv ist).

Ergänze `seed/investoren.csv` (Spalten wie in `/seed-crm`) und importiere die Top-Treffer
mit Fit ab 3 in die Kontaktliste, jeweils mit Quelle.

## Ergebnis

Die Liste, die CSV und ein Satz im Chat, wie viele Investoren belegt sind und wie viele
nur über eine Dritt-Quelle. Sag es, wenn die Zahl klein ist. Als Nächstes:
`/seed-foerderung`, dann `/seed-closer`.
