import json
import os
import re
import unittest

from _load import ROOT, SKILLS_DIR

SKILLS = ["seed-start", "seed-konkurrenz", "seed-markt", "seed-investoren", "seed-plan", "seed-praesentation",
          "seed-zahlen", "seed-foerderung", "seed-closer", "seed-gespraech", "seed-crm"]
EN_DASH = chr(0x2013)
EM = chr(0x2014)  # im Code gebaut, damit diese Datei ihre eigene Prüfung nicht auslöst


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return (m.group(1) if m else ""), text


def text_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", ".pytest_cache")]
        for f in files:
            if f.endswith((".md", ".py", ".json", ".txt", ".csv", ".html")) or f in ("LICENSE", ".gitignore"):
                yield os.path.join(base, f)


class Repo(unittest.TestCase):
    def test_exactly_eleven_skill_folders(self):
        found = sorted(d for d in os.listdir(SKILLS_DIR) if os.path.isfile(os.path.join(SKILLS_DIR, d, "SKILL.md")))
        self.assertEqual(len(found), 11)
        self.assertEqual(found, sorted(SKILLS))
        self.assertEqual(len(os.listdir(SKILLS_DIR)), 11)

    def test_frontmatter_is_valid_and_name_matches_folder(self):
        for s in SKILLS:
            fm, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertTrue(fm, s)
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"(?m)^description: >-$", s)
            self.assertGreater(len(fm), 300, "%s description is too thin" % s)
            self.assertGreater(len(text.splitlines()), 60, s)

    def test_yaml_colon_trap(self):
        # Die description steht als gefalteter Block (>-), dort ist ": " erlaubt. Alle einzeiligen
        # Felder mit ": " im Wert müssen in Anführungszeichen stehen.
        for s in SKILLS:
            fm, _ = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for line in fm.splitlines():
                if line.startswith(" "):
                    continue
                key, _, value = line.partition(":")
                value = value.strip()
                if value and value not in (">-", ">", "|") and ": " in value:
                    self.assertTrue(value.startswith('"') and value.endswith('"'), "%s: %s" % (s, line))

    def test_every_skill_says_no_advice(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            self.assertIn("Keine Finanz- oder Rechtsberatung", " ".join(text.split()), s)

    def test_tools_named_in_skills_exist(self):
        for s in SKILLS:
            _, text = frontmatter(os.path.join(SKILLS_DIR, s, "SKILL.md"))
            for tool in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w.\-/]+\.(?:py|md|json))", text):
                self.assertTrue(os.path.exists(os.path.join(SKILLS_DIR, s, tool)), "%s: %s" % (s, tool))

    def test_plugin_manifests(self):
        with open(os.path.join(ROOT, ".claude-plugin", "plugin.json"), encoding="utf-8") as fh:
            plugin = json.load(fh)
        self.assertEqual(plugin["name"], "seed-skill")
        self.assertEqual(plugin["license"], "MIT")
        with open(os.path.join(ROOT, ".claude-plugin", "marketplace.json"), encoding="utf-8") as fh:
            market = json.load(fh)
        self.assertEqual(market["plugins"][0]["name"], "seed-skill")
        self.assertEqual(market["plugins"][0]["source"], "./")

    def test_readme_and_closer_carry_the_legal_sentence(self):
        for rel in ("README.md", os.path.join("skills", "seed-closer", "SKILL.md")):
            with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
                text = " ".join(fh.read().split())
            self.assertIn("Unaufgeforderte Werbemails können in Deutschland und Österreich rechtliche Grenzen haben", text, rel)
            self.assertIn("Massenmails", text, rel)

    def test_readme_lists_all_skills_and_install(self):
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        self.assertTrue(readme.startswith("# Der Seed Skill"))
        self.assertIn("install skill", readme)
        for s in SKILLS:
            self.assertIn("`skills/%s`" % s, readme)

    def test_examples_parse(self):
        with open(os.path.join(SKILLS_DIR, "seed-zahlen", "example.json"), encoding="utf-8") as fh:
            json.load(fh)

    def test_no_dashes(self):
        for path in text_files():
            with open(path, encoding="utf-8") as fh:
                text = fh.read()
            self.assertNotIn(EM, text, os.path.relpath(path, ROOT))
            self.assertNotIn(EN_DASH, text, os.path.relpath(path, ROOT))
            self.assertNotRegex(text, r"(?<=\s)--(?=\s)", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    unittest.main()
