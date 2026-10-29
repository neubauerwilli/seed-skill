# Der Seed Skill

Elf Claude-Skills auf Deutsch, die dir helfen, Startkapital von Investoren zu holen. Kostenlos, MIT, keine
Anmeldung, kein API-Schlüssel, nichts zu verbinden.

`skills/seed-start` `skills/seed-konkurrenz` `skills/seed-markt` `skills/seed-investoren` `skills/seed-plan`
`skills/seed-praesentation` `skills/seed-zahlen` `skills/seed-foerderung` `skills/seed-closer`
`skills/seed-gespraech` `skills/seed-crm`

Einer findet die Schwachstellen deiner Konkurrenz. Einer sucht die Investoren, die zu deiner Idee passen, jeden
mit öffentlicher Quelle. Einer schreibt den Businessplan und das Pitch Deck. Und der Closer schreibt jedem Investor
eine persönliche Mail, hält die Gespräche am Laufen und fasst nach, bis ein Termin steht.

Der Closer verschickt nie von selbst. Jede Mail ist ein Entwurf, und raus geht sie erst, wenn du für genau diese
Mail ausdrücklich Ja sagst.

Dieses Paket ist eine eigene deutsche Umsetzung der Idee aus einem Reel von opusjake (27.10.2026). Es enthält
keinen Code aus einem anderen Repo.

## Einrichten

Füge den Link zu diesem Repo in Claude ein und sag `install skill`:

```
https://github.com/neubauerwilli/seed-skill

install skill
```

Oder als Plugin in Claude Code:

```
/plugin marketplace add neubauerwilli/seed-skill
/plugin install seed-skill@seed-skill
```

Als Plugin bekommen die Skills einen Namensraum, sie heißen dann `/seed-skill:seed-start` und so weiter. Wenn du
einfach `/seed-start` willst, kopiere die Ordner:

```bash
git clone https://github.com/neubauerwilli/seed-skill.git
cp -r seed-skill/skills/seed-* ~/.claude/skills/
```

Nur für ein Projekt statt global: dieselben Ordner nach `.claude/skills/` in deinem Projekt kopieren. Gar kein
Claude Code? Füge eine einzelne `SKILL.md` oben in einen Chat ein, dann läuft sie als Modus. Die Python-Werkzeuge
fallen dann weg, die Methode funktioniert trotzdem.

Die Werkzeuge brauchen Python 3.8 oder neuer. Nichts per pip installieren. Unter Windows heißt der Aufruf oft
`py` statt `python3`.

## Los geht es

Sag `/seed-start` und beschreib deine Idee. Der Skill fragt sieben Dinge ab, legt den Ordner `seed/` an und sagt dir,
was als Nächstes dran ist. Alle Ergebnisse landen als Dateien in `seed/`.

## Die elf

| Befehl | Rolle | Was er macht |
| --- | --- | --- |
| `/seed-start` | Einstieg | Fragt deine Idee in sieben Fragen ab, prüft, ob sie für Investoren reif ist, und leitet dich weiter. |
| `/seed-konkurrenz` | Schwachstellen-Finder | Sucht direkte und indirekte Konkurrenz, liest Preise und Beschwerden und zeigt, wo sie angreifbar ist. Jede Angabe mit Link. |
| `/seed-markt` | Marktgröße | Rechnet TAM, SAM und SOM von unten nach oben, mit Quellen oder gekennzeichneten Annahmen und drei Szenarien. |
| `/seed-investoren` | Investoren-Scout | Findet Business Angels, Netzwerke und Fonds, die zu deiner Phase und Branche passen. Mit Begründung und Quelle, nie erfunden. |
| `/seed-plan` | Businessplaner | Schreibt den Plan (kurz oder voll) aus den vorhandenen Dateien, trennt Fakten von Annahmen. |
| `/seed-praesentation` | Pitch-Deck-Bauer | Zwölf Folien mit Sprechtext, als Gliederung oder als HTML-Datei zum Blättern und Drucken. |
| `/seed-zahlen` | Finanzchef | Kapitalbedarf, Reichweite, Bewertung, Anteil der Investoren und Verwässerung, gerechnet mit einem Python-Werkzeug. |
| `/seed-foerderung` | Förder-Scout | Öffentliche Förderung als Alternative oder Ergänzung (zum Beispiel KfW, EXIST, aws, FFG), nur mit Quelle. |
| `/seed-closer` | Closer | Schreibt persönliche Mails als Entwurf, verlangt ein Ja je Mail, fasst höchstens zweimal nach. |
| `/seed-gespraech` | Gesprächstrainer | Bereitet das Gespräch vor, nennt die harten Fragen und übt sie mit dir. |
| `/seed-crm` | Kontaktliste | Hält Status, letzten Kontakt und Nachfass-Datum je Investor in einer CSV fest und sagt, wer fällig ist. |

## So arbeitet der Closer

Der Closer kann viel, deshalb hat er feste Grenzen:

- **Nur Entwürfe.** Mails entstehen als Datei in `seed/closer/` oder im Entwurfsfach deines Postfachs.
- **Ein Ja je Mail.** Das Werkzeug `versand.py` zählt nur ein einfaches "ja" (oder "yes"). "Ja, aber ...", "ja
  zu allen", "ok" und "passt" zählen nicht. Ändert sich der Text nach dem Ja, braucht er ein neues.
- **Ein Empfänger.** Keine Kopie, keine Blindkopie, keine Sammelmails, und die Adresse muss der Investor selbst
  öffentlich nennen (Quelle im Entwurf).
- **Höchstens zwei Nachfasser.** Zwischen zwei Nachrichten mindestens fünf Werktage. Meldet sich danach niemand,
  steht der Investor auf "kein Interesse", und es kommt keine weitere Mail.

Unaufgeforderte Werbemails können in Deutschland und Österreich rechtliche Grenzen haben. Deshalb schreibt der
Closer nur persönliche, einzelne Anfragen an öffentlich genannte Kontaktadressen von Investoren und keine
Massenmails. Gibt es ein Bewerbungsformular, nutz lieber das.

## Kleingedrucktes

**Keine Finanz- oder Rechtsberatung.** Bewertung, Anteile, Verträge, Förderbedingungen und Steuern prüft eine
Fachperson, bevor du etwas unterschreibst oder einreichst. Das steht in jedem Skill, und es gilt.

**Niemand kann dir Geld garantieren.** Die Skills erhöhen die Chance, dass die richtigen Leute dein Anliegen sauber
lesen. Ob jemand investiert, entscheiden die Investoren.

**Recherche nutzt öffentliche Quellen, mit Links.** Keine erfundenen Investoren, Ticketgrößen, Preise, Bewertungen
oder Zitate. Angaben aus Datenbanken und Ranglisten sind Hinweise und gehören auf der Seite des Investors
nachgeprüft. Konditionen ändern sich: Prüf das Datum der Quelle.

**Zahlen sind nur so gut wie die Eingaben.** Der Finanzplan rechnet mit dem, was du einträgst. Schätzungen bleiben
Schätzungen.

**Personenbezogene Daten sparsam.** Die Kontaktliste bleibt auf deinem Rechner. Nimm nur Namen und öffentliche
Kontaktwege auf.

**Idee aus einem Reel.** Belegt ist nur, was das Reel von opusjake (27.10.2026) zeigt: elf Skills, kostenlos,
einer für Konkurrenz-Schwachstellen, einer für passende Investoren, einer für Businessplan und Pitch und ein Closer,
der persönliche Mails schreibt und nachfasst. Alles Weitere ist eigene Arbeit.

## Dateien

```
skills/seed-start/           SKILL.md
skills/seed-konkurrenz/      SKILL.md
skills/seed-markt/           SKILL.md
skills/seed-investoren/      SKILL.md
skills/seed-plan/            SKILL.md
skills/seed-praesentation/   SKILL.md
skills/seed-zahlen/          SKILL.md, finanzplan.py, example.json
skills/seed-foerderung/      SKILL.md
skills/seed-closer/          SKILL.md, versand.py
skills/seed-gespraech/       SKILL.md
skills/seed-crm/             SKILL.md, crm.py
beispiel/probelauf-jonas/    ein kompletter Durchlauf mit einer Beispiel-Idee
tests/                       pytest-Tests
```

## Tests

```bash
py -m pytest tests
```

## Lizenz

MIT, siehe `LICENSE`.
