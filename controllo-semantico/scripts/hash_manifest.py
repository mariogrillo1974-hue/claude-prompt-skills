#!/usr/bin/env python3
"""Calcola SHA-256 e crea un manifest JSON locale senza sovrascrivere."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    args = parser.parse_args()
    try:
        path = Path(args.path).resolve()
        path.relative_to(Path("/mnt/data").resolve())
        if not path.is_file():
            raise ValueError("file non trovato")
        digest = sha256(path)
        manifest = path.with_suffix(path.suffix + ".manifest.json")
        counter = 1
        while manifest.exists():
            manifest = path.with_suffix(path.suffix + f".manifest-{counter}.json")
            counter += 1
        payload = {
            "file": path.name,
            "path": str(path),
            "size": path.stat().st_size,
            "sha256": digest,
            "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "state": "LOCAL-VALIDATED"
        }
        with manifest.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        print(digest)
        print(manifest)
        return 0
    except Exception as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
