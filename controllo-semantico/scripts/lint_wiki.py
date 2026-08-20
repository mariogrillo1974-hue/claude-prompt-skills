#!/usr/bin/env python3
"""Linter della wiki di progetto integrato nel controllo semantico.

Controlla coerenza strutturale, identità progetto e freschezza. Non dimostra la
verità sostanziale dei contenuti.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from collections import Counter
from pathlib import Path

from frontmatter_utils import split_frontmatter
from safe_paths import resolve_local_root

REQUIRED_FM = {"project_name", "project_code", "tags", "tipo", "stato", "aggiornato"}
REF_KEYS = {"dipende-da", "blocca", "sostituisce", "superata-da"}
EMOJI_STATE = {"🔴", "🟡", "🟠", "✅", "⛔", "🟢", "❌"}
SECTION_STATES = {
    "Aperte": {"proposta", "aperta"},
    "Decise": {"decisa"},
    "Accantonate": {"accantonata"},
    "Superate": {"superata"},
}


def as_list(value) -> list:
    if value in (None, ""):
        return []
    return value if isinstance(value, list) else [value]


class WikiLinter:
    def __init__(self, vault: Path, config: dict):
        self.vault = vault
        self.wiki = vault / "_wiki"
        self.config = config
        self.violations: list[dict] = []
        self.files = sorted(self.wiki.rglob("*.md")) if self.wiki.exists() else []
        self.expected_name = str(config.get("project_name", "")).strip()
        self.expected_code = str(config.get("project_code", "")).strip()
        self.max_kb = int(config.get("max_kb", 40))
        self.context_max_kb = int(config.get("context_max_kb", 80))
        self.context_max_words = int(config.get("context_max_words", 12000))

    def add(self, rule: int, path: Path, line: int, message: str, code: str | None = None):
        self.violations.append({
            "rule": rule,
            "code": code or f"LINT{rule:02d}",
            "file": str(path.relative_to(self.vault)) if path.is_absolute() else str(path),
            "line": line,
            "message": message,
        })

    def parse(self, path: Path):
        text = path.read_text(encoding="utf-8", errors="replace")
        try:
            data, body = split_frontmatter(text)
            return data, body, text
        except Exception as exc:
            self.add(1, path, 1, str(exc))
            return None, text, text

    def outside_archive(self, path: Path) -> bool:
        return "Archivio" not in path.parts

    def rule1_frontmatter_identity(self):
        for path in self.files:
            if not self.outside_archive(path):
                continue
            data, _, _ = self.parse(path)
            if data is None:
                continue
            missing = sorted(REQUIRED_FM - set(data))
            if missing:
                self.add(1, path, 1, "frontmatter missing: " + ", ".join(missing))
            if self.expected_name and data.get("project_name") != self.expected_name:
                self.add(1, path, 1, f"project_name mismatch: {data.get('project_name')!r}")
            if self.expected_code and data.get("project_code") != self.expected_code:
                self.add(1, path, 1, f"project_code mismatch: {data.get('project_code')!r}")

    def rule2_no_strikethrough_emoji(self):
        for path in self.files:
            if not self.outside_archive(path) or "processo" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for index, line in enumerate(text.splitlines(), 1):
                if "~~" in line:
                    self.add(2, path, index, "testo barrato non ammesso")
                for emoji in EMOJI_STATE:
                    if emoji in line:
                        self.add(2, path, index, f"emoji di stato non ammessa: {emoji}")

    def rule3_wikilinks(self):
        stems = {path.stem for path in self.files}
        pattern = re.compile(r"\[\[([^\]|#]+?)(?:\|[^\]]*)?\]\]")
        for path in self.files:
            if not self.outside_archive(path):
                continue
            for index, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                for match in pattern.finditer(line):
                    target = match.group(1).strip().split("/")[-1]
                    if target not in stems:
                        self.add(3, path, index, f"wikilink morto: {target}")

    def known_ids(self) -> set[str]:
        known = set()
        for folder in ("decisioni", "fatti"):
            for path in (self.wiki / folder).glob("*.md") if (self.wiki / folder).exists() else []:
                data, _, _ = self.parse(path)
                if data and data.get("id"):
                    known.add(str(data["id"]))
        return known

    def rule4_ids(self):
        known = self.known_ids()
        decision_dir = self.wiki / "decisioni"
        if not decision_dir.exists():
            return
        for path in decision_dir.glob("D-*.md"):
            data, _, _ = self.parse(path)
            if not data:
                continue
            for key in REF_KEYS:
                for ref in as_list(data.get(key)):
                    value = str(ref)
                    if not value or value in known or value.startswith("~") or value.startswith("ext:"):
                        continue
                    self.add(4, path, 1, f"id inesistente in {key}: {value}")

    def rule5_size(self):
        for path in self.files:
            if not self.outside_archive(path):
                continue
            size_kb = path.stat().st_size / 1024
            if path.name == "CONTEXT.md":
                if size_kb > self.context_max_kb:
                    self.add(5, path, 1, f"CONTEXT.md {size_kb:.1f} KB > {self.context_max_kb}")
                words = len(path.read_text(encoding="utf-8", errors="replace").split())
                if words > self.context_max_words:
                    self.add(5, path, 1, f"CONTEXT.md {words} parole > {self.context_max_words}")
            elif size_kb > self.max_kb:
                self.add(5, path, 1, f"file {size_kb:.1f} KB > {self.max_kb}")

    def rule6_decided_complete(self):
        decision_dir = self.wiki / "decisioni"
        if not decision_dir.exists():
            return
        for path in decision_dir.glob("D-*.md"):
            data, _, _ = self.parse(path)
            if not data or data.get("stato") != "decisa":
                continue
            if not data.get("data-decisione"):
                self.add(6, path, 1, "decisione decisa senza data-decisione")
            if not as_list(data.get("ricerche")) and not data.get("fonte"):
                self.add(6, path, 1, "decisione decisa senza fonte o ricerche")

    def rule7_context_freshness(self):
        context = self.wiki / "CONTEXT.md"
        if not context.exists():
            self.add(7, context, 1, "CONTEXT.md mancante")
            return
        data, _, _ = self.parse(context)
        if not data:
            return
        sources = as_list(data.get("derivato-da"))
        if not sources:
            self.add(7, context, 1, "derivato-da mancante")
            return
        for source in sources:
            source_path = self.vault / str(source)
            if not source_path.exists():
                self.add(7, context, 1, f"fonte derivata inesistente: {source}")
            elif source_path.stat().st_mtime > context.stat().st_mtime:
                self.add(7, context, 1, f"CONTEXT.md più vecchio di {source}")

    def rule8_index(self):
        decision_dir = self.wiki / "decisioni"
        index_path = decision_dir / "00 - Indice.md"
        if not index_path.exists():
            return
        sections: dict[str, list[str]] = {}
        current = None
        for line in index_path.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("## "):
                current = line[3:].strip()
                sections.setdefault(current, [])
            elif current and line.startswith("|"):
                cells = [cell.strip() for cell in line.split("|")]
                if len(cells) > 1:
                    match = re.match(r"^(D-[\w-]+)", cells[1].strip(" *_"))
                    if match:
                        sections[current].append(match.group(1))
        all_entries = [entry for entries in sections.values() for entry in entries]
        for path in decision_dir.glob("D-*.md"):
            count = all_entries.count(path.stem)
            if count != 1:
                self.add(8, path, 1, f"decisione presente {count} volte nell'indice")
        for section, entries in sections.items():
            for entry in entries:
                path = decision_dir / f"{entry}.md"
                if not path.exists():
                    self.add(8, index_path, 1, f"indice punta a file inesistente: {entry}")
                    continue
                data, _, _ = self.parse(path)
                if data and data.get("stato") not in SECTION_STATES.get(section, set()):
                    self.add(8, path, 1, f"stato {data.get('stato')} incoerente con sezione {section}")

    def rule9_canonical_values(self):
        values = self.config.get("canonical_values", {})
        for path in self.files:
            if not self.outside_archive(path) or "fatti" in path.parts or "processo" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for canonical, spec in values.items():
                for alias in spec.get("forbidden_aliases", []):
                    if alias in text:
                        self.add(9, path, 1, f"valore non canonico {alias}; usare {canonical}")

    def rule10_evidence_integrity(self):
        if not self.config.get("evidence_integrity"):
            return
        outcome = re.compile(r"\b(PASS|FAIL|OK|SUCCESS|VERDE|ROSSO|SUPERATO|FALLITO|nessun errore|zero violazioni)\b", re.I)
        measure = re.compile(r"\b\d+(?:/\d+)?\b|sha256:[0-9a-f]{64}|\b[0-9a-f]{7,40}\b", re.I)
        for path in (self.wiki / "decisioni").glob("D-*.md") if (self.wiki / "decisioni").exists() else []:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            in_evidence = False
            for index, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("## Evidenza"):
                    in_evidence = True
                    continue
                if in_evidence and stripped.startswith("## "):
                    in_evidence = False
                if in_evidence and re.match(r"^\d+\.", stripped):
                    if not outcome.search(stripped) and not measure.search(stripped):
                        self.add(10, path, index, "evidenza numerata senza misura o esito")

    def run(self):
        if not self.wiki.exists():
            self.add(1, self.wiki, 1, "directory _wiki mancante")
            return self.violations
        self.rule1_frontmatter_identity()
        self.rule2_no_strikethrough_emoji()
        self.rule3_wikilinks()
        self.rule4_ids()
        self.rule5_size()
        self.rule6_decided_complete()
        self.rule7_context_freshness()
        self.rule8_index()
        self.rule9_canonical_values()
        self.rule10_evidence_integrity()
        return self.violations


def load_config(vault: Path) -> dict:
    path = vault / "wiki.config.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint wiki metodo Karpathy")
    parser.add_argument("--vault", required=True, help="cartella esistente sotto /mnt/data")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--summary", action="store_true")
    args = parser.parse_args()

    try:
        vault = resolve_local_root(args.vault, must_exist=True)
    except ValueError as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2
    linter = WikiLinter(vault, load_config(vault))
    violations = linter.run()
    if args.json:
        print(json.dumps({
            "valid": not violations,
            "total": len(violations),
            "by_rule": dict(Counter(item["rule"] for item in violations)),
            "violations": violations,
            "note": "lint verde dimostra coerenza strutturale, non verità sostanziale",
        }, indent=2, ensure_ascii=False))
    elif args.summary:
        counts = Counter(item["rule"] for item in violations)
        for rule in range(1, 11):
            print(f"Regola {rule}: {counts.get(rule, 0)}")
        print("TOTALE:", len(violations))
    elif violations:
        print(f"FAIL: {len(violations)} violazioni")
        for item in violations:
            print(f"  {item['file']}:{item['line']} {item['code']} {item['message']}")
    else:
        print("OK: 0 violazioni. Wiki coerente; verità sostanziale non attestata.")
    return 0 if not violations else 1


if __name__ == "__main__":
    sys.exit(main())
