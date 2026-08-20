#!/usr/bin/env python3
"""Genera una nota di controllo semantico da un payload JSON."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

from safe_paths import resolve_local_root

REQUIRED = [
    "object", "category", "mode", "prompt_light", "semantic_light",
    "response_light", "persistence_status", "sections"
]
LIGHTS = {"VERDE", "GIALLO", "GIALLO-FORMA", "GIALLO-SOSTANZA", "ROSSO", "N/A"}

# Titoli canonici delle sezioni: le chiavi snake_case del payload vengono
# normalizzate qui, cosi' la nota passa sempre validate_control_note.py.
CANONICAL_TITLES = {
    "prompt_operativo": "Prompt operativo",
    "prompt operativo": "Prompt operativo",
    "conclusione": "Conclusione",
    "assunzioni": "Assunzioni",
    "termini_portanti": "Termini portanti",
    "claim_decisivi": "Claim decisivi",
    "tesi": "Tesi",
    "antitesi": "Antitesi",
    "sintesi": "Sintesi",
    "prova_del_nove": "Prova del nove",
    "non_regressione": "Non regressione",
    "non regressione": "Non regressione",
    "limiti": "Limiti",
    "fonti": "Fonti",
    "semafori": "Semafori",
    "punti_aperti": "Punti aperti",
    "punti aperti": "Punti aperti",
}


def canonical_title(raw: str) -> str:
    key = str(raw).strip()
    mapped = CANONICAL_TITLES.get(key.lower())
    if mapped:
        return mapped
    text = key.replace("_", " ").replace("-", " ").strip()
    return (text[:1].upper() + text[1:]) if text else "Sezione"


def yaml_scalar(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{text}"'


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return (value[:80] or "oggetto")


def validate(payload: dict) -> None:
    missing = [k for k in REQUIRED if k not in payload]
    if missing:
        raise ValueError("campi mancanti: " + ", ".join(missing))
    for key in ("prompt_light", "semantic_light", "response_light"):
        if payload[key] not in LIGHTS:
            raise ValueError(f"{key} non ammesso: {payload[key]}")
    nr = payload.get("non_regression_light", "N/A")
    if nr not in {"VERDE", "GIALLO", "ROSSO", "N/A"}:
        raise ValueError(f"non_regression_light non ammesso: {nr}")
    if not isinstance(payload["sections"], dict) or not payload["sections"]:
        raise ValueError("sections deve essere un oggetto non vuoto")


def render(payload: dict, now: dt.datetime) -> str:
    sources = payload.get("sources", [])
    open_points = payload.get("open_points", [])
    lines = ["---"]
    fm = {
        "type": "controllo-semantico",
        "data": now.isoformat(timespec="seconds"),
        "oggetto": payload["object"],
        "categoria": payload["category"],
        "modalita": payload["mode"],
        "project_name": payload.get("project_name"),
        "project_code": payload.get("project_code"),
        "semaforo_prompt": payload["prompt_light"],
        "semaforo_semantico": payload["semantic_light"],
        "semaforo_risposta": payload["response_light"],
        "semaforo_non_regressione": payload.get("non_regression_light", "N/A"),
        "stato_persistenza": payload["persistence_status"],
        "owner": payload.get("owner"),
        "scadenza": payload.get("deadline"),
        "fonti": sources,
        "sha256": None,
        "punti_aperti": len(open_points),
    }
    for key, value in fm.items():
        if isinstance(value, list):
            rendered = "[" + ", ".join(yaml_scalar(v) for v in value) + "]"
        else:
            rendered = yaml_scalar(value)
        lines.append(f"{key}: {rendered}")
    lines.extend(["---", "", f"# Controllo semantico — {payload['object']}", ""])
    open_points_body = None
    for title, body in payload["sections"].items():
        norm = canonical_title(title)
        if norm == "Punti aperti":
            # Evitare la sezione duplicata: il corpo confluisce nella
            # sezione "Punti aperti" generata in coda.
            open_points_body = str(body).rstrip()
            continue
        lines.extend([f"## {norm}", "", str(body).rstrip(), ""])
    lines.extend(["## Punti aperti", ""])
    if open_points_body:
        lines.append(open_points_body)
    if open_points:
        for item in open_points:
            if isinstance(item, dict):
                lines.append(
                    f"- Serve: {item.get('proof', 'dato non disponibile')} da "
                    f"{item.get('owner', 'owner non disponibile')} entro "
                    f"{item.get('deadline', 'evento non disponibile')} — "
                    f"effetto: {item.get('impact', 'dato non disponibile')}."
                )
            else:
                lines.append(f"- {item}")
    if not open_points and not open_points_body:
        lines.append("- Nessun punto aperto dichiarato.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="payload JSON")
    parser.add_argument("--root", default="/mnt/data/controlli-semantici")
    args = parser.parse_args()
    try:
        payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
        validate(payload)
        root_path = Path(args.root)
        if not root_path.exists():
            sandbox = Path("/mnt/data").resolve()
            parent_candidate = root_path.parent.resolve(strict=False)
            if parent_candidate == sandbox:
                parent = sandbox
            else:
                parent = resolve_local_root(str(root_path.parent), must_exist=True)
            root_path = parent / root_path.name
            root_path.mkdir(exist_ok=False)
        root = resolve_local_root(str(root_path), must_exist=True)
        now = dt.datetime.now().astimezone()
        stem = f"{now:%Y%m%d-%H%M%S}__{slugify(payload['object'])}__controllo-semantico"
        path = root / f"{stem}.md"
        counter = 1
        while path.exists():
            path = root / f"{stem}-{counter}.md"
            counter += 1
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(render(payload, now))
        print(path)
        return 0
    except Exception as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
