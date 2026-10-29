---
name: seed-closer
description: >-
  Der Closer. Schreibt jedem Investor eine persönliche Mail als Entwurf, führt die
  Gespräche weiter und fasst nach, bis ein Termin steht. Verschickt nie von selbst:
  Entwürfe landen in einer Datei oder im Entwurfsfach des Postfachs, und erst ein
  ausdrückliches Ja des Nutzers für genau diese Mail lässt sie raus ("ja, aber" zählt
  nicht). Nachfassen höchstens zweimal, mindestens fünf Werktage Abstand, danach Status
  "kein Interesse". Nutze ihn, wenn der Nutzer sagt "schreib den Investoren", "Mail an
  Investoren", "Anschreiben", "nachfassen", "Terminanfrage", "der Investor hat
  geantwortet" oder "Closer starten" (englisch: "write to investors", "follow up").
argument-hint: "[Investor-ID aus seed/crm.csv | nachfassen]"
---

# seed-closer

Der Skill, der Ergebnisse bringt: eine kurze, persönliche Mail an eine Person, die dein
Anliegen in 30 Sekunden versteht, und ein sauberes Nachfassen, bis es einen Termin gibt
oder ein Nein. Kein Spam, keine Massenmail, kein Druck.

Werkzeuge in diesem Ordner:

```bash
python3 "${CLAUDE_SKILL_DIR}/versand.py" pruefen seed/closer/01-name.md
python3 "${CLAUDE_SKILL_DIR}/versand.py" freigabe seed/closer/01-name.md --reply "<Antwort des Nutzers, Wort für Wort>"
python3 "${CLAUDE_SKILL_DIR}/versand.py" status seed/closer/01-name.md
```

## Grundregeln

- Keine Finanz- oder Rechtsberatung.
- **Unaufgeforderte Werbemails können in Deutschland und Österreich rechtliche Grenzen
  haben.** Deshalb nur persönliche, einzelne Anfragen an Kontaktadressen, die der Investor
  selbst öffentlich nennt, mit Link zur Quelle. Keine Massenmails, keine gekauften oder
  geratenen Adressen, keine Kopien an mehrere Investoren. Gibt es ein Bewerbungsformular
  (Pitch-Seite), ist das der bessere Weg als eine Mail. Bei Zweifeln prüft eine Fachperson.
- **Nichts wird verschickt, ohne dass der Nutzer ausdrücklich Ja sagt.** Du schreibst nur
  Entwürfe: als Datei in `seed/closer/` oder, wenn ein Postfach-Werkzeug angebunden ist, im
  Entwurfsfach. Nie senden, nie planen, nie automatisch.
- Du erfindest nichts über den Investor. Persönlicher Bezug kommt nur aus öffentlichen
  Quellen (Portfolio, Beitrag, Seite), mit Link in der Quelle-Zeile oder im Entwurfsnotiz.

## Schritt 1: die Vorbereitung

Lies `seed/idee.md`, `plan.md` (oder `plan-kurz.md`), `finanzplan.md`, `investoren.md` und
`crm.csv`. Wähle mit dem Nutzer die Investoren aus, an die zuerst geschrieben wird: drei bis
fünf auf einmal, nicht fünfzig. Für jeden suchst du auf der Investorenseite die zwei Dinge,
die ihn mit der Idee verbinden (Portfolio, Branche, Region, öffentlich geäußerte Interessen).

## Schritt 2: der Entwurf

Eine Datei je Investor, `seed/closer/NN-name.md`, mit diesen Kopfzeilen und dem Text:

```
An: <genau eine öffentliche Adresse>
Quelle: <Link der Seite, auf der die Adresse steht>
Betreff: <konkret, unter 60 Zeichen>
Nachfass: 0

<Text>
```

Aufbau des Textes, 90 bis 160 Wörter:
1. **Warum du:** ein Satz, der zeigt, dass du seine Arbeit kennst (aus öffentlicher Quelle).
2. **Was ich baue:** ein Satz, ohne Fachwörter.
3. **Beweis:** eine Zahl oder Tatsache (Nutzer, Pilotkunden, Warteliste, Umsatz). Gibt es
   noch keine, schreib den ehrlichen Stand und den nächsten Test.
4. **Was ich suche:** Betrag, Anteil, was das Geld erreicht. Eine Zeile.
5. **Die Bitte:** ein Gespräch von 20 Minuten, mit zwei Terminvorschlägen oder einem Link.
6. Ein Anhang-Hinweis: Pitch Deck oder Kurzplan als Link, nicht als Pflicht.

Ohne Floskeln wie "Sehr geehrte Damen und Herren, ich habe eine revolutionäre Idee". Keine
Massenanrede, keine Platzhalter in eckigen Klammern, keine Übertreibungen. Lies den Entwurf
laut und streich alles, was nach Vorlage klingt.

Dann `versand.py pruefen`. Meldet das Werkzeug Fehler (mehrere Empfänger, Cc, fehlende
Quelle, Platzhalter, zu kurz oder zu lang), behebst du sie, bevor du dem Nutzer den Text
zeigst. Im CRM setzt du den Status auf `entwurf` (`/seed-crm`).

## Schritt 3: das Ja

Zeig dem Nutzer den fertigen Entwurf mit Empfänger und Quelle und stell genau eine Frage:
"Soll diese Mail an <Name> raus? Dann antworte nur mit ja." Eine Frage je Mail. Biete nie
"ja für alle" an.

Gib die Antwort **Wort für Wort** an `versand.py freigabe --reply "..."` weiter. Das
Werkzeug zählt nur ein einfaches Ja, das mit "ja", "yes" oder "y" beginnt und nichts
anhängt. "Ja, aber ändere den Betreff", "ja zu allen", "ok", "passt", "ja?" oder "ja, später"
zählen **nicht**. Übersetze eine Antwort nie selbst in ein Ja. Bei "Nicht erfasst" frag
einmal neu oder überarbeite den Text. Ändert sich der Text nach dem Ja, gilt das Ja nicht
mehr, dann braucht der neue Text ein neues Ja.

Erst nach "Dein Ja ist erfasst" darf der Nutzer die Mail abschicken (oder das Postfach-
Werkzeug, wenn er das ausdrücklich so will). Setz im CRM `versendet` mit dem Versanddatum,
erst wenn das Absenden bestätigt ist.

## Schritt 4: nachfassen, bis ein Termin steht

Frag `crm.py faellig`. Es nennt, wo ein Nachfassen fällig ist.

- **Erster Nachfasser** (Nachfass: 1) frühestens fünf Werktage nach dem Versand: kurz,
  freundlich, ein neuer Anlass (ein neuer Meilenstein, eine Zahl) statt "nur nachfragen, ob
  Sie meine Mail gesehen haben".
- **Zweiter Nachfasser** (Nachfass: 2) frühestens fünf Werktage danach: noch kürzer, mit
  einer einfachen Ausstiegsoption ("Falls es nicht passt, sag es gern, dann störe ich nicht
  weiter").
- **Mehr gibt es nicht.** Meldet sich nach dem zweiten Nachfasser und weiteren fünf
  Werktagen niemand, setzt `crm.py abschliessen` den Status auf `kein_interesse`. Kein
  dritter Versuch, keine neue Mail unter anderem Betreff.

Jeder Nachfasser ist ein eigener Entwurf mit eigenem Ja.

## Schritt 5: wenn eine Antwort kommt

- **Ja, gern ein Gespräch:** Terminvorschläge im Entwurf, Antwort als eigener Entwurf mit Ja.
  Im CRM `antwort`, dann `termin`. Weiter mit `/seed-gespraech`.
- **Rückfragen:** Antwort aus den Dateien belegen, nichts dazuerfinden. Fehlt etwas, sag
  dem Nutzer, was er klären muss.
- **Nein:** ein Dank im Entwurf, Status `absage`, nach dem Grund fragen (höflich, einmal).
  Den Grund notierst du im CRM, nicht zum Diskutieren.

## Ergebnis

Entwürfe in `seed/closer/`, aktualisierte `seed/crm.csv` und im Chat: wer wartet auf ein Ja,
wer ist zum Nachfassen fällig, wer hat geantwortet. Keine Mail ist raus, solange kein Ja
erfasst ist.
