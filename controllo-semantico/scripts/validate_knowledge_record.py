#!/usr/bin/env python3
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ALLOWED_STATUS = {"DRAFT", "VALIDATED", "APPROVED", "PUBLISHED", "PROMOTED", "SUPERSEDED", "REJECTED", "PARTIAL"}
ALLOWED_CLASS = {"public", "internal", "restricted", "secret"}
REQUIRED = {"type", "canonical_id", "project_code", "title", "version", "status", "classification", "source_refs", "source_hashes", "created_at", "updated_at", "owner"}
SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|token|password|passwd|secret)\s*[:=]\s*[^\s{}]+"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"(?i)\.env(?:\.|$)"),
]


def parse_scalar(value):
    value = value.strip()
    if value in {"[]", "{}"}:
        return [] if value == "[]" else {}
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    return value


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    block = text[4:end]
    data = {}
    current = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current:
            data.setdefault(current, []).append(parse_scalar(raw[4:]))
            continue
        if ":" not in raw:
            raise ValueError(f"unsupported frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        current = key
        data[key] = [] if value == "" else parse_scalar(value)
    return data, text[end + 5:]


def validate(path):
    text = path.read_text(encoding="utf-8")
    data, body = parse_frontmatter(text)
    errors = []
    warnings = []
    missing = sorted(REQUIRED - set(data))
    if missing:
        errors.append("missing fields: " + ", ".join(missing))
    cid = str(data.get("canonical_id", ""))
    if cid and not re.fullmatch(r"[A-Z0-9][A-Z0-9._-]{4,127}", cid):
        errors.append("canonical_id must be stable uppercase identifier")
    if data.get("status") not in ALLOWED_STATUS:
        errors.append("invalid status")
    if data.get("classification") not in ALLOWED_CLASS:
        errors.append("invalid classification")
    for key in ("source_refs", "source_hashes"):
        if key in data and not isinstance(data[key], list):
            errors.append(f"{key} must be a YAML list")
    for item in data.get("source_hashes", []):
        if not re.fullmatch(r"sha256:[0-9a-fA-F]{64}", str(item)):
            errors.append(f"invalid source hash: {item}")
    if data.get("classification") != "secret" and not data.get("source_refs"):
        errors.append("source_refs cannot be empty outside secret records")
    scan = text
    for pattern in SECRET_PATTERNS:
        if pattern.search(scan):
            errors.append(f"possible secret pattern: {pattern.pattern}")
    if data.get("classification") == "secret":
        warnings.append("secret record: must not be published or exported")
    digest = hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()
    return {"file": str(path), "valid": not errors, "errors": errors, "warnings": warnings, "canonical_id": cid or None, "sha256": digest, "body_bytes": len(body.encode("utf-8"))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = []
    for value in args.paths:
        path = Path(value)
        if path.is_dir():
            for item in sorted(path.rglob("*.md")):
                results.append(validate(item))
        else:
            results.append(validate(path))
    ok = all(r["valid"] for r in results)
    if args.json:
        print(json.dumps({"valid": ok, "results": results}, indent=2, ensure_ascii=False))
    else:
        for r in results:
            print(("PASS" if r["valid"] else "FAIL"), r["file"])
            for error in r["errors"]:
                print("  ERROR:", error)
            for warning in r["warnings"]:
                print("  WARN:", warning)
        print("OVERALL:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
