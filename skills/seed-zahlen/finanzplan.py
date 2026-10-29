#!/usr/bin/env python3
"""Finanzplan, Kapitalbedarf, Bewertung und Verwässerung für seed-zahlen. Nur Standardbibliothek, kein Netzwerk.

Keine Finanz- oder Rechtsberatung. Das Werkzeug rechnet nur mit den Zahlen, die du eingibst.

    python3 finanzplan.py seed/zahlen.json
    python3 finanzplan.py seed/zahlen.json --out seed/finanzplan.md
    python3 finanzplan.py seed/zahlen.json --json

Die Eingabe (siehe example.json in diesem Ordner):

    unternehmen         Name, für den Bericht
    kapital_ziel        so viel Geld willst du einsammeln (Euro)
    startup             [{label, cost}]  einmalige Ausgaben zum Start
    ausgaben_monatlich  [{label, cost}]  laufende Kosten pro Monat
    einnahmen_monatlich 12 Zahlen: Einnahmen je Monat des ersten Jahres (optional, Standard 0)
    puffer_monate       so viele Monate Ausgaben sollen als Reserve übrig bleiben (Standard 3)
    abgabe_anteil       Anteil, den du für das Kapital abgibst, zum Beispiel 0.15
    pre_money           alternativ: Bewertung vor der Runde. Genau eines von beiden angeben
    gruender            [{name, anteil}]  Anteile vor der Runde, Summe 1.0
    optionspool         Anteil für künftige Mitarbeiter, wird vor der Runde aus allen Anteilen gebildet (Standard 0)
    folgerunden         [{name, betrag, pre_money}]  spätere Runden zum Durchrechnen (optional)
"""

import argparse
import json
import math
import sys


class ZahlenError(Exception):
    pass


def _num(value, label, minimum=0.0, maximum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ZahlenError("%s braucht eine Zahl" % label)
    if not math.isfinite(value) or value < minimum or (maximum is not None and value > maximum):
        raise ZahlenError("%s liegt außerhalb des erlaubten Bereichs" % label)
    return float(value)


def _items(spec, key, required):
    items = spec.get(key)
    if items is None:
        if required:
            raise ZahlenError("%s fehlt" % key)
        return []
    if not isinstance(items, list):
        raise ZahlenError("%s muss eine Liste sein" % key)
    out = []
    for i, it in enumerate(items):
        if not isinstance(it, dict) or "cost" not in it:
            raise ZahlenError("%s[%d] braucht label und cost" % (key, i))
        out.append((str(it.get("label", key)), _num(it["cost"], "%s[%d].cost" % (key, i))))
    return out


# ---------------------------------------------------------------- Bewertung

def valuation(raise_amount, anteil=None, pre_money=None):
    """Aus Betrag plus Anteil oder Betrag plus Pre-Money die ganze Bewertung ableiten."""
    raise_amount = _num(raise_amount, "kapital", minimum=0.01)
    if (anteil is None) == (pre_money is None):
        raise ZahlenError("genau eines von abgabe_anteil und pre_money angeben")
    if anteil is not None:
        anteil = _num(anteil, "abgabe_anteil", minimum=0.0001, maximum=0.9999)
        post = raise_amount / anteil
        pre = post - raise_amount
    else:
        pre = _num(pre_money, "pre_money", minimum=0.01)
        post = pre + raise_amount
        anteil = raise_amount / post
    return {"raise": raise_amount, "pre_money": pre, "post_money": post, "investor_share": anteil}


def dilute(holders, investor_share, investor_name):
    """Alle bisherigen Anteile schrumpfen um den neuen Anteil. Summe bleibt 1.0."""
    out = {name: share * (1.0 - investor_share) for name, share in holders.items()}
    out[investor_name] = out.get(investor_name, 0.0) + investor_share
    return out


def cap_table(spec):
    """Anteile nach dem Seed und nach jeder Folgerunde."""
    founders = spec.get("gruender") or []
    if not founders:
        raise ZahlenError("gruender fehlt")
    holders = {}
    for i, f in enumerate(founders):
        holders[str(f.get("name", "Gründer %d" % (i + 1)))] = _num(f.get("anteil"), "gruender[%d].anteil" % i)
    if abs(sum(holders.values()) - 1.0) > 1e-6:
        raise ZahlenError("die Anteile der Gründer müssen zusammen 100 Prozent ergeben")
    pool = _num(spec.get("optionspool", 0), "optionspool", maximum=0.5)
    if pool:
        holders = {k: v * (1.0 - pool) for k, v in holders.items()}
        holders["Optionspool"] = pool
    v = valuation(spec["kapital_ziel"], spec.get("abgabe_anteil"), spec.get("pre_money"))
    holders = dilute(holders, v["investor_share"], "Seed-Investoren")
    steps = [("Nach dem Seed", dict(holders), v)]
    for i, r in enumerate(spec.get("folgerunden") or []):
        name = str(r.get("name", "Runde %d" % (i + 2)))
        rv = valuation(r.get("betrag"), None, r.get("pre_money"))
        holders = dilute(holders, rv["investor_share"], name + "-Investoren")
        steps.append(("Nach " + name, dict(holders), rv))
    return steps


# ---------------------------------------------------------------- Cash

def analyse(spec):
    startup = _items(spec, "startup", False)
    monthly = _items(spec, "ausgaben_monatlich", True)
    income = spec.get("einnahmen_monatlich") or [0] * 12
    if not isinstance(income, list) or len(income) != 12:
        raise ZahlenError("einnahmen_monatlich braucht genau 12 Zahlen")
    income = [_num(x, "einnahmen_monatlich[%d]" % i) for i, x in enumerate(income)]
    goal = _num(spec.get("kapital_ziel"), "kapital_ziel", minimum=0.01)
    buffer_months = _num(spec.get("puffer_monate", 3), "puffer_monate", maximum=24)

    startup_total = sum(c for _, c in startup)
    burn = sum(c for _, c in monthly)
    balance, cash = -startup_total, []
    for m in range(12):
        balance += income[m] - burn
        cash.append(balance)
    lowest = min([-startup_total] + cash)
    need_cash = -lowest if lowest < 0 else 0.0
    buffer = buffer_months * burn
    need_total = need_cash + buffer

    # Reichweite: wie viele Monate hält das Kapital, wenn es am Start eingezahlt wird?
    runway, bal = None, goal - startup_total
    if bal < 0:
        runway = 0
    else:
        for m in range(12):
            bal += income[m] - burn
            if bal < 0:
                runway = m
                break
    flags = []
    if goal < need_total:
        flags.append("Das Ziel von %s reicht nicht: Der Plan braucht %s (davon %s Reserve)."
                     % (eur(goal), eur(need_total), eur(buffer)))
    if runway is not None and runway < 12:
        flags.append("Das Geld hält nur %d Monate. Investoren wollen meist 12 bis 18 Monate sehen (Faustregel, kein Gesetz)." % runway)
    v = valuation(goal, spec.get("abgabe_anteil"), spec.get("pre_money"))
    if v["investor_share"] > 0.25:
        flags.append("Du gibst %d Prozent ab. Bei einer ersten Runde sind 10 bis 25 Prozent eine übliche Faustregel; "
                     "prüfe das mit einer Fachperson." % round(v["investor_share"] * 100))
    steps = cap_table(spec)
    return {
        "goal": goal, "startup": startup_total, "burn": burn, "cash": cash, "need_cash": need_cash,
        "buffer": buffer, "need_total": need_total, "runway": runway, "valuation": v, "cap": steps,
        "flags": flags,
    }


# ---------------------------------------------------------------- Ausgabe

def eur(x):
    return ("{:,.0f}".format(x)).replace(",", ".") + " €"


def pct(x):
    return ("%.1f" % (x * 100)).replace(".", ",") + " %"


def report(spec, a):
    name = spec.get("unternehmen", "Dein Unternehmen")
    v = a["valuation"]
    lines = ["# Finanzplan: %s" % name, "",
             "Keine Finanz- oder Rechtsberatung. Alle Zahlen stammen aus deinen Eingaben.", "",
             "## Kapitalbedarf", "",
             "- Einmalige Startkosten: **%s**" % eur(a["startup"]),
             "- Laufende Kosten: **%s pro Monat**" % eur(a["burn"]),
             "- Tiefster Kontostand im ersten Jahr: **%s**" % eur(-a["need_cash"]),
             "- Reserve (%s Monate): **%s**" % (str(int(spec.get("puffer_monate", 3))), eur(a["buffer"])),
             "- **Kapitalbedarf gesamt: %s**" % eur(a["need_total"]),
             "- Dein Ziel: **%s**" % eur(a["goal"])]
    if a["runway"] is None:
        lines.append("- Reichweite: das Geld hält mindestens 12 Monate")
    else:
        lines.append("- Reichweite: das Geld hält **%d Monate**" % a["runway"])
    lines += ["", "## Bewertung", "",
              "- Pre-Money: **%s**" % eur(v["pre_money"]),
              "- Post-Money: **%s**" % eur(v["post_money"]),
              "- Investoren erhalten: **%s**" % pct(v["investor_share"]), "",
              "## Wem gehört was", "", "| Stand | " + " | ".join(sorted(a["cap"][-1][1])) + " |",
              "| --- |" + " --- |" * len(a["cap"][-1][1])]
    names = sorted(a["cap"][-1][1])
    for label, holders, _ in a["cap"]:
        lines.append("| %s | " % label + " | ".join(pct(holders.get(n, 0.0)) for n in names) + " |")
    lines += ["", "## Kontostand Monat für Monat (ohne das neue Kapital)", "", "| Monat | Kontostand |", "| --- | --- |"]
    for i, c in enumerate(a["cash"], 1):
        lines.append("| %d | %s |" % (i, eur(c)))
    if a["flags"]:
        lines += ["", "## Warnungen", ""] + ["- " + f for f in a["flags"]]
    lines += ["", "Prüfe Bewertung, Anteile und Verträge vor einer Zusage mit Steuer- und Rechtsberatung.", ""]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("zahlen")
    p.add_argument("--out")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    try:
        with open(args.zahlen, encoding="utf-8") as fh:
            spec = json.load(fh)
        a = analyse(spec)
    except (OSError, ValueError, ZahlenError) as e:
        print("Fehler: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        a = dict(a)
        a["cap"] = [(l, h) for l, h, _ in a["cap"]]
        print(json.dumps(a, indent=2, ensure_ascii=False))
        return 0
    text = report(spec, a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("Geschrieben: %s" % args.out)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
