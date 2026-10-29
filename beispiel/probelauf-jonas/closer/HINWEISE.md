# Hinweise zu den Entwürfen

Nichts davon ist verschickt. Es gibt keine `freigaben.json`, also hat niemand ein Ja gegeben. Jonas ist eine erfundene
Beispielperson.

- `01-cherry-ventures.md`: Erste Mail an die Adresse, die Cherry Ventures auf der Kontaktseite für Investmentanfragen nennt.
  Der Bezug im ersten Absatz stammt von deren Seite ("industry-curious", KI als Thema). Fit laut Liste nur 2: Phase
  und Ticket sind bei Cherry nicht belegt.
- `02-berlin-angel-club.md`: Allgemeine Kontaktadresse des Berlin Angel Club. Eigentlich ist das Bewerbungsformular der
  richtige Weg. Die Mail fragt deshalb nur, ob sich eine Bewerbung in dieser frühen Phase lohnt.
- `01-cherry-ventures-nachfass-1.md`: Erster Nachfasser, frühestens fünf Werktage nach dem Versand der ersten Mail. **Der
  Text setzt voraus, dass Jonas wirklich mit zehn Coaches gesprochen hat.** Ist das nicht passiert, muss der Text vor
  dem Ja geändert werden. Ein zweiter Nachfasser wäre der letzte.
- Für Formular-Investoren (Calm/Storm, Speedinvest, Angels4Health, Companisto) schreibt der Closer keinen Maileintrag,
  sondern den Text fürs Formular. Das ist hier nicht ausgeführt.

Prüfung der drei Entwürfe mit dem Werkzeug:

```bash
py skills/seed-closer/versand.py pruefen beispiel/probelauf-jonas/closer/01-cherry-ventures.md
```
