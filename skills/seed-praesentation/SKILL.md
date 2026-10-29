---
name: seed-praesentation
description: >-
  Der Pitch-Deck-Bauer. Macht aus Idee, Markt, Wettbewerb, Plan und Finanzplan ein
  Pitch Deck für Investoren: zwölf Folien mit je einer Aussage, wahlweise als Gliederung
  mit Sprechtext oder als fertige HTML-Präsentation in einer Datei, die sich im Browser
  öffnen und als PDF drucken lässt. Nutze ihn, wenn der Nutzer sagt "bau mein Pitch
  Deck", "Präsentation für Investoren", "Folien", "Pitch", "Investor Deck", "Slides für
  die Runde" oder "Deck überarbeiten" (englisch: "pitch deck", "investor presentation").
argument-hint: "[gliederung | html]"
---

# seed-praesentation

Ein Deck ist kein Bericht. Es ist die Folie, die ein Investor in zwei Minuten durchblättert,
bevor er entscheidet, ob er mit dir spricht. Zwölf Folien, eine Aussage je Folie.

## Grundregeln

- Keine Finanz- oder Rechtsberatung.
- Jede Zahl im Deck steht auch in `seed/finanzplan.md`, `seed/markt.md` oder
  `seed/konkurrenz.md` mit Quelle. Ein Deck erfindet nichts.
- Eine Folie, ein Gedanke. Höchstens 30 Wörter Text auf der Folie, der Rest gehört in den
  Sprechtext.
- Keine fremden Firmenlogos ohne Erlaubnis. Namen genügen. Keine erfundenen Kundenzitate.

## Schritt 1: Material und Form

Lies `seed/idee.md`, `markt.md`, `konkurrenz.md`, `finanzplan.md`, `plan.md`. Frag:
Gliederung mit Sprechtext (schnell, zum Weiterbauen in Keynote, PowerPoint oder Canva) oder
fertige HTML-Datei `seed/pitch-deck.html` (eine Datei, keine Abhängigkeiten, Pfeiltasten zum
Blättern, Druckansicht)?

## Schritt 2: die zwölf Folien

1. **Titel:** Name, ein Satz, was ihr tut, Kontakt.
2. **Problem:** wer, was kostet es, ein Beleg aus Gesprächen oder Daten.
3. **Lösung:** was du baust, ein Bild oder ein Ablauf in drei Schritten.
4. **Warum jetzt:** was sich geändert hat (Technik, Verhalten, Regel).
5. **Produkt:** Screenshot oder Skizze. Nur das, was es gibt, als "gibt es" markiert, den Rest als "kommt".
6. **Markt:** TAM, SAM, SOM aus `markt.md`, als Rechnung, nicht als Kreis mit Milliarden.
7. **Geschäftsmodell:** Preis, Marge, Beispielkunde.
8. **Traktion:** alles, was bewiesen ist (Nutzer, Warteliste, Pilotkunden, Umsatz). Ist es noch
   nichts, zeig den Test und die Zahl, die ihr in 30 Tagen erreicht haben wollt.
9. **Wettbewerb:** die Schwachstellen-Karte, zwei Achsen oder eine kleine Tabelle.
10. **Team:** Gesichter, je ein Satz, warum ihr das könnt.
11. **Zahlen:** Umsatz und Ausgaben für drei Jahre, ein Diagramm, die wichtigste Annahme darunter.
12. **Die Bitte:** Betrag, Anteil, Verwendung in drei Posten, Meilensteine, die das Geld erreicht.

Dazu ein Anhang für Fragen: Cap Table nach der Runde, Details zur Konkurrenz, Risiken.

## Schritt 3: Sprechtext

Zu jeder Folie ein Sprechtext von 20 bis 40 Sekunden, in der Sprache des Gründers. Der Text
beginnt nie mit "Auf dieser Folie sehen Sie". Er beantwortet die Frage, die der Investor
bei der Folie stellen würde. Am Ende jeder Folie in Klammern: die härteste Nachfrage und
eine Antwort.

## Schritt 4: bauen

**Gliederung:** `seed/pitch-deck.md` mit Folie, Titel (als Aussage, nicht als Thema!), Text,
Bildidee, Sprechtext. Titel wie "Trainer verlieren 6 Stunden pro Woche mit Plänen", nicht
"Problem".

**HTML:** `seed/pitch-deck.html`, eine einzige Datei: Folien als `<section>`, Blättern mit
den Pfeiltasten, 16:9, große Schrift, ruhige Farben mit einer Akzentfarbe, Druckstil
(`@media print`, eine Folie pro Seite). Keine Skripte von Fremdseiten, keine externen
Schriften. Diagramme als einfaches Inline-SVG aus den echten Zahlen.

## Schritt 5: der Mülltest

Geh jede Folie durch und frag: Was passiert, wenn ich sie streiche? Merkt es keiner, raus.
Dann zähle: mehr als zwölf Folien im Hauptteil? Kürzen. Folie mit mehr als einer Aussage?
Teilen oder streichen.

## Ergebnis

`seed/pitch-deck.md` oder `seed/pitch-deck.html`, dazu eine Liste "Fehlt noch" (zum Beispiel
Screenshot, Teamfoto, Traktion). Erkläre dem Nutzer, wie er die HTML-Datei als PDF druckt
(Browser, Drucken, Als PDF speichern). Als Nächstes: `/seed-gespraech`.
