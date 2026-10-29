---
name: seed-konkurrenz
description: >-
  Der Schwachstellen-Finder. Sucht direkte und indirekte Konkurrenten aus öffentlichen
  Quellen, liest ihre Preise, Bewertungen und Beschwerden und zeigt, wo sie angreifbar
  sind und wo deine Idee sich absetzen kann. Jede Angabe hat einen Link, nichts wird
  erfunden. Nutze ihn, wenn der Nutzer sagt "wer ist meine Konkurrenz", "Schwachstellen
  der Konkurrenz", "was machen die anderen falsch", "Wettbewerbsanalyse", "warum sollte
  jemand zu mir kommen" oder "Konkurrenzanalyse für Investoren" (englisch: "competitor
  analysis", "find competitor weaknesses").
argument-hint: "[Pfad zu seed/idee.md oder die Idee in einem Satz]"
---

# seed-konkurrenz

Jeder Investor fragt: "Und was ist mit X?" Wer die Antwort schon hat, wirkt vorbereitet.
Dieser Skill findet die Konkurrenz und vor allem die Stelle, an der sie wehtut.

## Grundregeln

- Keine Finanz- oder Rechtsberatung.
- Nur öffentliche Quellen: Webseiten der Anbieter, Preisseiten, App-Store-Seiten,
  Bewertungsportale, Presse, Foren. Jede Angabe bekommt einen Link und das Abrufdatum.
- Was du nicht findest, schreibst du als "nicht gefunden". Keine erfundenen Preise,
  Nutzerzahlen, Bewertungen oder Zitate. Schätzungen kennzeichnest du als Schätzung.
- Kein Scraping gegen die Bedingungen einer Seite.
- Zitiere Kundenbeschwerden nur in eigenen Worten zusammengefasst, mit Link zur Quelle.

## Schritt 1: lies die Idee

Lies `seed/idee.md`. Fehlt sie, starte `/seed-start`. Notiere in einem Satz, welches
Problem für wen gelöst wird. Davon hängt ab, wer alles Konkurrenz ist.

## Schritt 2: drei Ringe

Suche in dieser Reihenfolge und halte jeden Ring getrennt:

1. **Direkte Konkurrenz:** löst dasselbe Problem für dieselbe Gruppe.
2. **Indirekte Konkurrenz:** löst es anders (eine Tabelle, ein Mensch, ein Buch, eine andere App-Art).
3. **Nichtstun:** was Menschen heute tun, wenn sie weder dich noch irgendwen nutzen.

Nutze die Websuche für Anbieter, App-Stores, Vergleichsseiten und Bewertungen. Such mit
Stichworten der Zielgruppe in ihrer Sprache und, wenn die Idee international ist, auch
auf Englisch. Ziel sind sechs bis zwölf Wettbewerber, ehrlich gewichtet: Lieber acht
belegte als zwanzig geratene.

## Schritt 3: pro Wettbewerber ein Steckbrief

Für jeden: Name und Link, Land, was sie anbieten, für wen, Preis (mit Link zur
Preisseite), Gründungsjahr oder Alter, falls öffentlich, bekannte Finanzierung (nur mit
Quelle, zum Beispiel eine Pressemeldung), wie sie sich positionieren (ein Satz in ihren
eigenen Worten von der Startseite) und die **Schwachstelle**.

Schwachstellen findest du hier:
- Bewertungen mit ein bis drei Sternen: was wiederholt sich?
- Preisseite: was kostet extra, was fehlt im günstigen Tarif?
- Funktionen, die Kunden in Foren und Rezensionen vermissen.
- Zielgruppe, die sie ignorieren (Sprache, Land, Branche, Anfänger oder Profis).
- Technik oder Daten, die sich nicht leicht kopieren lassen, und was ihnen fehlt.

Schreib nur auf, was sich mindestens zweimal unabhängig zeigt. Eine einzelne Beschwerde
ist ein Hinweis, kein Muster.

## Schritt 4: die Schwachstellen-Karte

Eine Tabelle: Wettbewerber in den Zeilen, in den Spalten die Kriterien, die der Zielgruppe
wichtig sind (zum Beispiel Preis, Persönlichkeit, Sprache, Aufwand, Ergebnis). Feld
mit Ja, Teils oder Nein, jedes mit Beleg-Nummer. Darunter:

- **Wo alle gleich sind:** das ist Standard, damit gewinnst du nichts.
- **Wo alle schwach sind:** hier liegt deine Chance.
- **Deine Antwort:** in zwei Sätzen, was du dort besser machst, und woran Investoren
  das glauben können (ein Beleg, kein Versprechen).
- **Die drei härtesten Investorenfragen zur Konkurrenz** mit je einer ehrlichen Antwort.
  Ist die ehrliche Antwort schwach, sag das und schlag vor, was vorher zu klären ist.

## Ergebnis

`seed/konkurrenz.md` mit Steckbriefen, Karte, Schwachstellen und Quellenliste (Nummer,
Link, Abrufdatum). Dazu `seed/konkurrenz.csv` mit einer Zeile je Wettbewerber, damit
`/seed-praesentation` die Folie "Wettbewerb" daraus baut. Als Nächstes: `/seed-markt`.
