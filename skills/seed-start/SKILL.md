---
name: seed-start
description: >-
  Der Einstieg in den Seed Skill. Fragt deine Idee in sieben kurzen Fragen ab, legt den
  Ordner seed/ mit der Datei idee.md an, prüft, ob die Idee für Startkapital überhaupt
  reif ist, und schickt dich zum richtigen nächsten Skill. Nutze ihn, wenn der Nutzer
  sagt "ich brauche Startkapital", "ich suche Investoren", "wie komme ich an Geld für
  mein Startup", "Seed Skill starten", "Pre-Seed", "Finanzierungsrunde" oder "wo fange
  ich an" (englisch: "I need funding", "find investors", "raise a seed round", "start
  the seed skill").
argument-hint: "[deine Idee in einem Satz]"
---

# seed-start

Der Startpunkt für alles, was mit Kapital von Investoren zu tun hat. Dieser Skill sammelt
die Fakten über deine Idee an einem Ort, damit die anderen zehn Skills nicht jedes Mal von
vorn fragen.

## Grundregeln (gelten für das ganze Paket)

- Keine Finanz- oder Rechtsberatung. Verträge, Bewertung, Anteile und Steuern
  prüft eine Fachperson, bevor etwas unterschrieben wird.
- Du erfindest nie einen Investor, eine Zahl, einen Preis oder ein Zitat. Jede Angabe
  über Dritte hat eine öffentliche Quelle mit Link. Fehlt sie, schreibst du "nicht belegt".
- Du verschickst nie etwas. Mails entstehen als Entwurf. Verschickt wird nur nach einem
  ausdrücklichen Ja des Nutzers (mehr dazu in `/seed-closer`).
- Du weißt nicht, ob jemand investiert. Du erhöhst nur die Chance, dass die richtigen
  Leute dein Anliegen sauber und schnell lesen.

## Schritt 1: die sieben Fragen

Stell sie nacheinander, eine Nachricht je Frage, und warte auf die Antwort. Frag nichts
doppelt, was schon in `seed/idee.md` steht.

1. **Was baust du?** Ein Satz, so dass es ein Zwölfjähriger versteht.
2. **Für wen?** Eine konkrete Gruppe, kein "für alle".
3. **Welches Problem löst es, und was tun die Leute heute stattdessen?**
4. **Woran verdienst du?** Abo, Einmalpreis, Provision, Lizenz. Mit Preis, auch geschätzt.
5. **Wo stehst du?** Idee, Prototyp, erste Nutzer, erste Einnahmen. Mit Zahlen, falls es sie gibt.
6. **Wie viel Geld brauchst du, wofür, und wie lange soll es reichen?**
7. **Wer bist du?** Ausbildung, Erfahrung, Team, Land und Stadt, Rechtsform (oder noch keine).

Schreib die Antworten in `seed/idee.md`, in diesen Überschriften: Idee, Zielgruppe, Problem,
Erlösmodell, Stand, Kapitalziel, Team und Ort. Gibt es die Datei schon, lies sie, zeig dem
Nutzer eine Zusammenfassung und frag nur nach dem, was fehlt oder veraltet ist.

## Schritt 2: der Reifetest

Geh die Liste ehrlich durch. Ein Nein ist kein Todesurteil, es ist die nächste Aufgabe.

| Frage | Wenn Nein, dann zuerst |
| --- | --- |
| Gibt es mindestens zehn Menschen aus der Zielgruppe, die mit dir gesprochen haben? | Gespräche führen, bevor du Investoren ansprichst |
| Gibt es einen Prototyp, eine Demo oder eine Landingpage? | Etwas Sichtbares bauen, sei es klein |
| Gibt es ein Zeichen echter Nachfrage (Warteliste, Vorverkauf, zahlende Pilotkunden)? | `/seed-markt` und ein günstiger Test |
| Stimmt das Kapitalziel zu den Kosten? | `/seed-zahlen` |
| Bist du bereit, 5 bis 20 Prozent der Firma abzugeben? | Eine Nacht darüber schlafen und `/seed-foerderung` ansehen |

Sag offen, wenn Investoren für die Phase unwahrscheinlich sind. Zeig dann die Alternativen:
Förderung (`/seed-foerderung`), Kunden als Geldgeber (Vorverkauf) und Eigenleistung.

## Schritt 3: der Weg durch das Paket

Empfohlene Reihenfolge, jede Datei landet in `seed/`:

1. `/seed-konkurrenz` findet die Schwachstellen der Konkurrenz (`konkurrenz.md`).
2. `/seed-markt` schätzt die Marktgröße mit nachvollziehbarer Rechnung (`markt.md`).
3. `/seed-zahlen` rechnet Kapitalbedarf, Bewertung und Verwässerung (`finanzplan.md`).
4. `/seed-investoren` sucht passende Business Angels und Fonds (`investoren.md`).
5. `/seed-foerderung` zeigt öffentliche Förderung als Alternative oder Ergänzung (`foerderung.md`).
6. `/seed-plan` schreibt den Businessplan (`plan.md`).
7. `/seed-praesentation` baut das Pitch Deck (`pitch-deck.html`).
8. `/seed-crm` legt die Kontaktliste an (`crm.csv`).
9. `/seed-closer` schreibt jedem Investor eine persönliche Mail als Entwurf (`closer/`).
10. `/seed-gespraech` bereitet dich auf das Gespräch vor (`gespraech.md`).

Frag den Nutzer, ob er alles der Reihe nach will oder bei einem Skill einsteigt. Beides geht.

## Ergebnis

`seed/idee.md`, ein Reifetest in drei Sätzen im Chat und ein konkreter Vorschlag: "Als
Nächstes `/seed-konkurrenz`." Mehr nicht. Lade den Nutzer nicht mit Erklärungen zu.
