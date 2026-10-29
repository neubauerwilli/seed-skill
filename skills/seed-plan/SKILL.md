---
name: seed-plan
description: >-
  Der Businessplaner. Schreibt aus allem, was das Paket bisher erarbeitet hat, einen
  Businessplan in deutscher Sprache, der auch für Banken, Förderstellen und Business
  Angels taugt: Zusammenfassung, Problem, Lösung, Markt, Wettbewerb, Geschäftsmodell,
  Vertrieb, Team, Meilensteine, Finanzplan und Kapitalbedarf. Erfindet nichts, trennt
  Fakten von Annahmen. Nutze ihn, wenn der Nutzer sagt "schreib meinen Businessplan",
  "Businessplan für Investoren", "Kurzfassung", "One-Pager", "Plan für die Bank",
  "Executive Summary" oder "Förderantrag vorbereiten" (englisch: "write my business
  plan", "executive summary").
argument-hint: "[kurz | voll]"
---

# seed-plan

Ein Businessplan ist kein Pflichtdokument, sondern ein Denkwerkzeug. Wer ihn schreibt,
merkt, wo die Idee noch nicht trägt. Dieser Skill baut ihn aus den Teilen, die schon
vorliegen, und sagt dir, was fehlt.

## Grundregeln

- Keine Finanz- oder Rechtsberatung. Zahlen und Verträge prüft eine Fachperson.
- Der Plan sagt nur, was in den anderen Dateien belegt ist. Neue Behauptungen ohne Beleg
  kommen nicht hinein.
- Annahmen stehen im Plan als Annahmen, mit einem Satz, wie sie geprüft werden.
- Deine Stimme, nicht Beraterdeutsch: kurze Sätze, konkrete Zahlen, keine Floskeln wie
  "innovative Lösung" oder "disruptiv".

## Schritt 1: Vorarbeit prüfen

Lies, was vorhanden ist: `seed/idee.md`, `konkurrenz.md`, `markt.md`, `finanzplan.md`,
`investoren.md`, `foerderung.md`. Fehlt etwas Wichtiges, sag es und biete an, den passenden
Skill zuerst zu starten. Schreib den Plan trotzdem, mit einer Lücke, die laut sichtbar ist
("Markt: noch nicht gerechnet, siehe `/seed-markt`").

Frag, welche Fassung gebraucht wird:
- **kurz:** zwei Seiten, für das erste Gespräch und als Anhang zur Mail.
- **voll:** zehn bis fünfzehn Seiten, für Banken, Förderstellen und die Prüfung durch Investoren.

## Schritt 2: der Aufbau

Jedes Kapitel in dieser Reihenfolge, in der Kurzfassung je ein Absatz:

1. **Zusammenfassung:** was, für wen, warum jetzt, wie viel Geld, wofür. Zuletzt schreiben.
2. **Problem:** wer leidet woran, mit einer Zahl oder einem Beleg aus Gesprächen.
3. **Lösung:** was du baust, in drei Sätzen, und was der Kunde danach anders tun kann.
4. **Produkt und Stand:** was es heute gibt, was als Nächstes kommt, was es kostet zu bauen.
5. **Markt:** die Kette aus `seed/markt.md`, mit TAM, SAM, SOM.
6. **Wettbewerb:** die Karte aus `seed/konkurrenz.md` und deine Antwort darauf.
7. **Geschäftsmodell:** wer zahlt, wie viel, wie oft. Eine Beispielrechnung für einen Kunden.
8. **Vertrieb und Marketing:** die zwei bis drei Kanäle, die du bedienst, mit Kosten je Kunde als Annahme.
9. **Team:** wer macht was, was fehlt, wen holst du dir (Beirat, Freelancer, Mentoren).
10. **Meilensteine:** drei bis fünf messbare Ziele für die nächsten 12 Monate mit Datum.
11. **Finanzplan:** Kapitalbedarf, Verwendung in Prozent, Einnahmen und Ausgaben, Reichweite
    des Geldes (aus `seed/finanzplan.md`).
12. **Risiken:** die fünf größten, jedes mit einer Gegenmaßnahme.
13. **Rechtliches in einem Absatz:** Rechtsform, Marken, Datenschutz, geplante Verträge. Nur
    benennen, nicht bewerten. Verweis auf eine Fachperson.

## Schritt 3: die Verwendung des Geldes

Eine Tabelle, die in Prozent und Euro zeigt, wohin die Summe geht (Entwicklung, Vertrieb,
Gehälter, Reserve). Die Summen müssen mit `seed/finanzplan.md` übereinstimmen. Stimmt etwas
nicht, korrigiere im Plan, nicht im Finanzplan, und sag es dem Nutzer.

## Schritt 4: Gegenlesen

Lies den fertigen Plan, als wärst du der skeptischste Investor, der ihn je bekommen hat.
Schreib die fünf Stellen auf, an denen du aufhören würdest zu lesen oder Fragen hättest,
und die Antworten darauf, soweit die Dateien sie hergeben. Fehlende Antworten wandern in
den Abschnitt "Offene Punkte" am Ende des Plans und in die Vorbereitung von `/seed-gespraech`.

Prüfe auch den Ton: Jeder Satz mit "revolutionär", "einzigartig", "führend" ohne Beleg wird
gestrichen oder belegt.

## Ergebnis

`seed/plan.md` (und auf Wunsch `plan-kurz.md`). Dazu eine Liste "Was ich angenommen habe" mit
allen Annahmen auf einer Seite. Als Nächstes: `/seed-praesentation`.
