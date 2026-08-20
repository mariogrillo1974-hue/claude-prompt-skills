#!/usr/bin/env python3
"""Valida una nota Markdown del protocollo semantico."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_KEYS = {
    "type", "data", "oggetto", "categoria", "modalita", "project_name",
    "project_code", "semaforo_prompt", "semaforo_semantico",
    "semaforo_risposta", "stato_persistenza", "owner", "scadenza",
    "fonti", "sha256", "punti_aperti"
}
REQUIRED_SECTIONS = {
    "Prompt operativo", "Punti aperti"
}


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("frontmatter iniziale mancante")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("chiusura frontmatter mancante")
    data = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"riga frontmatter non valida: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    path = Path(args.path).resolve()
    try:
        path.relative_to(Path("/mnt/data").resolve())
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        missing = sorted(REQUIRED_KEYS - set(fm))
        if missing:
            raise ValueError("chiavi mancanti: " + ", ".join(missing))
        if fm.get("type", "").strip('"') != "controllo-semantico":
            raise ValueError("type non corretto")
        nr = fm.get("semaforo_non_regressione")
        if nr is not None and nr.strip('"') not in {"VERDE", "GIALLO", "ROSSO", "N/A"}:
            raise ValueError("semaforo_non_regressione non ammesso")
        headings = set(re.findall(r"^##\s+(.+?)\s*$", text, flags=re.M))
        for required in REQUIRED_SECTIONS:
            if not any(h.startswith(required) for h in headings):
                raise ValueError(f"sezione obbligatoria mancante: {required}")
        if not re.search(r"^#\s+Controllo semantico", text, flags=re.M):
            raise ValueError("titolo principale mancante")
        print("VALIDATED", path)
        return 0
    except Exception as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
