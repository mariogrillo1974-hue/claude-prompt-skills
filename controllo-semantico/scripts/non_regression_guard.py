#!/usr/bin/env python3
"""Snapshot e confronto strutturale per il Gate di Non Regressione.

Il PASS dimostra solo che non risultano rimossi path della baseline non
esplicitamente autorizzati. Non sostituisce test funzionali o semantici.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

DEFAULT_EXCLUDES = {".git", "__pycache__", ".DS_Store"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def inventory(root: Path, excludes: set[str]) -> dict[str, dict[str, object]]:
    root = root.resolve()
    out: dict[str, dict[str, object]] = {}
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in excludes)
        current_path = Path(current)
        for name in sorted(files):
            if name in excludes:
                continue
            path = current_path / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                out[rel] = {"type": "symlink", "target": os.readlink(path)}
            elif path.is_file():
                out[rel] = {
                    "type": "file",
                    "size": path.stat().st_size,
                    "sha256": sha256(path),
                }
    return out


def write_snapshot(root: Path, output: Path, excludes: set[str]) -> int:
    if not root.is_dir():
        raise ValueError(f"root non valida: {root}")
    payload = {
        "schema": "non-regression-structural-v1",
        "root_name": root.name,
        "files": inventory(root, excludes),
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"NR-SNAPSHOT {len(payload['files'])} files -> {output}")
    return 0


def normalize_allow(values: list[str]) -> set[str]:
    return {Path(v).as_posix().lstrip("./") for v in values}


def compare(snapshot: Path, root: Path, allow_remove: set[str], excludes: set[str]) -> int:
    data = json.loads(snapshot.read_text(encoding="utf-8"))
    if data.get("schema") != "non-regression-structural-v1":
        raise ValueError("schema snapshot non supportato")
    before = data.get("files")
    if not isinstance(before, dict):
        raise ValueError("snapshot privo di inventario files")
    after = inventory(root, excludes)

    before_paths = set(before)
    after_paths = set(after)
    removed = sorted(before_paths - after_paths)
    added = sorted(after_paths - before_paths)
    changed = sorted(p for p in before_paths & after_paths if before[p] != after[p])
    unexpected_removed = [p for p in removed if p not in allow_remove]
    authorized_removed = [p for p in removed if p in allow_remove]

    report = {
        "removed_unexpected": unexpected_removed,
        "removed_authorized": authorized_removed,
        "added": added,
        "changed": changed,
        "baseline_count": len(before_paths),
        "candidate_count": len(after_paths),
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    if unexpected_removed:
        print("NR-STRUCTURAL-FAIL: rimossi path baseline non autorizzati", file=sys.stderr)
        return 2
    print("NR-STRUCTURAL-PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--exclude", action="append", default=[])
    sub = parser.add_subparsers(dest="command", required=True)

    snap = sub.add_parser("snapshot")
    snap.add_argument("root")
    snap.add_argument("--output", required=True)

    comp = sub.add_parser("compare")
    comp.add_argument("snapshot")
    comp.add_argument("root")
    comp.add_argument("--allow-remove", action="append", default=[])

    args = parser.parse_args()
    excludes = DEFAULT_EXCLUDES | set(args.exclude)
    try:
        if args.command == "snapshot":
            return write_snapshot(Path(args.root), Path(args.output), excludes)
        return compare(
            Path(args.snapshot),
            Path(args.root),
            normalize_allow(args.allow_remove),
            excludes,
        )
    except Exception as exc:
        print(f"ERRORE: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
