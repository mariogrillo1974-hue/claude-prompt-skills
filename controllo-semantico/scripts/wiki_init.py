#!/usr/bin/env python3
"""Crea una nuova Wiki locale senza sovrascrivere file esistenti."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

from safe_paths import resolve_local_root

SUBDIRS = ["decisioni", "fatti", "processo", "ricerche", "Archivio"]
CODE_RE = re.compile(r"[A-Z0-9][A-Z0-9._-]{2,127}")


def frontmatter(project_name: str, project_code: str, tipo: str, stato: str, oggi: str, extra: str = "") -> str:
    return (
        "---\n"
        f'project_name: "{project_name}"\n'
        f"project_code: {project_code}\n"
        f"tags: [{tipo}, llm-wiki]\n"
        f"tipo: {tipo}\n"
        f"stato: {stato}\n"
        f"aggiornato: {oggi}\n"
        f"{extra}"
        "---\n\n"
    )


def build_files(project_name: str, project_code: str, oggi: str) -> dict[str, str]:
    state = frontmatter(project_name, project_code, "stato-corrente", "vincolante", oggi) + f"""# 00 — Stato corrente — {project_name}

> Dashboard locale del progetto. Aggiornarla solo su richiesta esplicita.

## Identita

**Nome progetto:** {project_name}  
**Codice progetto:** `{project_code}`

## Obiettivo e perimetro

Da compilare con dati forniti dall'utente.

## Stato per area

| Area | Stato | Prova | Prossima azione |
|---|---|---|---|
| Wiki | inizializzata | bootstrap {oggi} | registrare fatti e decisioni |
| Progetto | da compilare | dato non disponibile | consolidare lo stato reale |

## Punti aperti

- Definire owner, scadenze ed evidenze mancanti.
"""

    index = frontmatter(project_name, project_code, "indice-decisioni", "vincolante", oggi) + """# 00 — Indice delle decisioni

> Ogni `D-*.md` appare esattamente una volta nella sezione coerente con il suo stato.

## Aperte

| id | titolo | data | link |
|---|---|---|---|

## Decise

| id | titolo | data | link |
|---|---|---|---|

## Accantonate

| id | titolo | data | link |
|---|---|---|---|

## Superate

| id | titolo | data | link |
|---|---|---|---|
"""

    extra = "derivato-da: [_wiki/00 - Stato corrente.md, _wiki/decisioni/00 - Indice.md]\n"
    context = frontmatter(project_name, project_code, "context-pack", "vincolante", oggi, extra) + f"""# CONTEXT — {project_name}

> Vista derivata locale. Non sostituisce le fonti primarie.

## 1. Identita del progetto

**Nome:** {project_name}  
**Codice:** `{project_code}`

## 2. Stato corrente

La Wiki e inizializzata. Il contenuto operativo deve essere consolidato.

## 3. Decisioni chiave

Nessuna decisione registrata.

## 4. Fatti canonici

Nessun fatto registrato.

## 5. Roadmap

1. Consolidare stato, fatti e decisioni.
2. Aggiornare questa vista per ultima.
3. Eseguire il linter locale.

## 6. Punti aperti

- Stato operativo non ancora compilato.
"""
    return {
        "00 - Stato corrente.md": state,
        "decisioni/00 - Indice.md": index,
        "CONTEXT.md": context,
    }


def validate_identity(project_name: str, project_code: str) -> None:
    if not project_name.strip():
        raise ValueError("project_name non puo essere vuoto")
    if "\n" in project_name or "\r" in project_name or '"' in project_name:
        raise ValueError("project_name contiene caratteri non ammessi")
    if not CODE_RE.fullmatch(project_code):
        raise ValueError("project_code deve usare lettere maiuscole, numeri, punto, trattino o underscore")


def main() -> int:
    parser = argparse.ArgumentParser(description="Crea una nuova Wiki locale nel sandbox")
    parser.add_argument("--root", required=True, help="cartella esistente sotto /mnt/data")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--project-code", required=True)
    args = parser.parse_args()

    try:
        root = resolve_local_root(args.root, must_exist=True)
        project_name = args.project_name.strip()
        project_code = args.project_code.strip()
        validate_identity(project_name, project_code)
    except ValueError as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2

    wiki = root / "_wiki"
    config = root / "wiki.config.json"
    if wiki.exists() or config.exists():
        print("ERRORE: _wiki o wiki.config.json esiste gia; nessun file modificato.", file=sys.stderr)
        return 2

    today = dt.date.today().isoformat()
    files = build_files(project_name, project_code, today)
    created_paths: list[Path] = []
    try:
        wiki.mkdir()
        created_paths.append(wiki)
        for subdir in SUBDIRS:
            directory = wiki / subdir
            directory.mkdir()
            created_paths.append(directory)
            if subdir != "decisioni":
                keep = directory / ".gitkeep"
                keep.write_text("", encoding="utf-8", errors="strict")
                created_paths.append(keep)

        for relative, content in files.items():
            path = wiki / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(content)
            created_paths.append(path)

        payload = {
            "project_name": project_name,
            "project_code": project_code,
            "max_kb": 40,
            "context_max_kb": 80,
            "context_max_words": 12000,
            "canonical_values": {},
            "evidence_integrity": False,
        }
        with config.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        created_paths.append(config)
    except Exception as exc:
        for path in reversed(created_paths):
            try:
                if path.is_file():
                    path.unlink()
                elif path.is_dir():
                    path.rmdir()
            except OSError:
                pass
        print(f"ERRORE: creazione annullata: {exc}", file=sys.stderr)
        return 1

    print(f"Wiki locale creata: {root}")
    for relative in sorted(str(path.relative_to(root)) for path in created_paths if path.is_file()):
        print("  creato", relative)
    print(f"Eseguire: python scripts/lint_wiki.py --vault {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
