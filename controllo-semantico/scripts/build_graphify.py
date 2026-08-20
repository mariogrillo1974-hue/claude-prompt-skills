#!/usr/bin/env python3
import argparse
import csv
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EXCLUDED_STATUS = {"SUPERSEDED", "REJECTED"}
EXCLUDED_DIRS = {".git", ".obsidian", "secrets", "98_SEGRETI_NON_INDICIZZARE"}
RELATIONS = {"RELATES_TO", "DEPENDS_ON", "SUPERSEDES", "IMPLEMENTS", "VALIDATES", "DERIVED_FROM", "DOCUMENTS"}


def parse_value(value):
    value = value.strip()
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_note(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated frontmatter")
    data = {}
    current = None
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current:
            data.setdefault(current, []).append(parse_value(raw[4:]))
            continue
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        current = key.strip()
        data[current] = [] if not value.strip() else parse_value(value)
    normalized = text.replace("\r\n", "\n")
    data["_hash"] = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    data["_path"] = str(path)
    return data


def edge_id(source, relation, target):
    return hashlib.sha256(f"{source}|{relation}|{target}".encode()).hexdigest()[:24]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir")
    parser.add_argument("output_dir")
    args = parser.parse_args()
    source = Path(args.source_dir)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    records = {}
    excluded = []
    conflicts = []
    for path in sorted(source.rglob("*.md")):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            excluded.append({"file": str(path), "reason": "excluded path"})
            continue
        try:
            data = parse_note(path)
        except Exception as exc:
            excluded.append({"file": str(path), "reason": str(exc)})
            continue
        cid = str(data.get("canonical_id", ""))
        if not cid:
            excluded.append({"file": str(path), "reason": "missing canonical_id"})
            continue
        if data.get("classification") == "secret" or data.get("status") in EXCLUDED_STATUS:
            excluded.append({"file": str(path), "reason": "classification/status excluded"})
            continue
        if not data.get("source_refs") or not data.get("source_hashes"):
            excluded.append({"file": str(path), "reason": "missing provenance"})
            continue
        if cid in records and records[cid]["_hash"] != data["_hash"]:
            conflicts.append({"canonical_id": cid, "files": [records[cid]["_path"], data["_path"]]})
            continue
        records[cid] = data
    if conflicts:
        print(json.dumps({"error": "canonical_id conflicts", "conflicts": conflicts}, indent=2))
        return 2
    nodes_path = out / "nodes.csv"
    edges_path = out / "edges.csv"
    with nodes_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["node_id", "label", "node_type", "project_code", "version", "status", "classification", "source_refs", "source_hashes", "content_hash", "updated_at"])
        writer.writeheader()
        for cid, data in sorted(records.items()):
            writer.writerow({
                "node_id": cid,
                "label": data.get("title", cid),
                "node_type": data.get("type", "knowledge-record"),
                "project_code": data.get("project_code", ""),
                "version": data.get("version", ""),
                "status": data.get("status", ""),
                "classification": data.get("classification", ""),
                "source_refs": json.dumps(data.get("source_refs", []), ensure_ascii=False, separators=(",", ":")),
                "source_hashes": json.dumps(data.get("source_hashes", []), ensure_ascii=False, separators=(",", ":")),
                "content_hash": data["_hash"],
                "updated_at": data.get("updated_at", ""),
            })
    edge_rows = []
    for cid, data in sorted(records.items()):
        for target in data.get("related_ids", []):
            if target in records:
                edge_rows.append((cid, "RELATES_TO", target, data.get("source_refs", [""])[0], "high"))
        for raw in data.get("relations", []):
            match = re.fullmatch(r"([A-Z_]+):(.+)", str(raw))
            if not match:
                continue
            relation, target = match.groups()
            if relation in RELATIONS and target in records:
                edge_rows.append((cid, relation, target, data.get("source_refs", [""])[0], "high"))
    with edges_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["edge_id", "source_id", "relation", "target_id", "source_ref", "confidence"])
        writer.writeheader()
        for source_id, relation, target_id, source_ref, confidence in sorted(set(edge_rows)):
            writer.writerow({"edge_id": edge_id(source_id, relation, target_id), "source_id": source_id, "relation": relation, "target_id": target_id, "source_ref": source_ref, "confidence": confidence})
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_dir": str(source.resolve()),
        "node_count": len(records),
        "edge_count": len(edge_rows),
        "included_files": sorted(data["_path"] for data in records.values()),
        "excluded": excluded,
        "conflicts": conflicts,
        "outputs": {"nodes.csv": digest(nodes_path), "edges.csv": digest(edges_path)},
    }
    (out / "graph_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "nodes": len(records), "edges": len(edge_rows), "output_dir": str(out)}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
