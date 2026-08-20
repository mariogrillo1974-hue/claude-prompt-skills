#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

TARGETS = {"github", "drive", "wiki", "obsidian", "graphify"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("record")
    args = parser.parse_args()
    data = json.loads(Path(args.record).read_text(encoding="utf-8"))
    errors = []
    for key in ("canonical_id", "version", "status", "authorization_ref", "targets"):
        if key not in data:
            errors.append(f"missing {key}")
    targets = data.get("targets", {})
    unknown = set(targets) - TARGETS
    if unknown:
        errors.append("unknown targets: " + ", ".join(sorted(unknown)))
    included = []
    for name, record in targets.items():
        if not isinstance(record, dict):
            errors.append(f"target {name} must be object")
            continue
        if record.get("included"):
            included.append(name)
            if record.get("readback") is not True:
                errors.append(f"target {name} lacks successful readback")
            if name == "github" and not re.fullmatch(r"[0-9a-fA-F]{40}", str(record.get("commit", ""))):
                errors.append("github commit must be 40 hex chars")
            if name == "drive":
                if not record.get("file_id"):
                    errors.append("drive file_id missing")
                if not re.fullmatch(r"[0-9a-fA-F]{64}", str(record.get("sha256", ""))):
                    errors.append("drive sha256 invalid")
            if name in {"wiki", "obsidian", "graphify"} and not record.get("object_id"):
                errors.append(f"target {name} object_id missing")
    if data.get("status") == "PROMOTED" and (not included or errors):
        errors.append("PROMOTED requires all included targets to pass")
    if data.get("status") == "PARTIAL" and not included:
        errors.append("PARTIAL requires at least one included target")
    result = {"valid": not errors, "errors": errors, "included_targets": included}
    print(json.dumps(result, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
