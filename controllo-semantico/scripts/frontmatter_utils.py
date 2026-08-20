#!/usr/bin/env python3
"""Parser frontmatter YAML minimale condiviso dagli script della skill.

Supporta scalari, booleani, interi, liste block-style e flow-style.
Non pretende di essere un parser YAML completo: rifiuta strutture ambigue invece
che interpretarle in modo silenziosamente errato.
"""
from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Any


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value == "[]":
        return []
    if value == "{}":
        return {}
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        reader = csv.reader(io.StringIO(inner), skipinitialspace=True)
        row = next(reader)
        return [parse_scalar(item) for item in row]
    lower = value.lower()
    if lower in {"true", "false"}:
        return lower == "true"
    if value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
        try:
            return int(value)
        except ValueError:
            pass
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        raise ValueError("missing YAML frontmatter")
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise ValueError("unterminated YAML frontmatter")
    block = normalized[4:end]
    body = normalized[end + 5 :]
    data: dict[str, Any] = {}
    current: str | None = None
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - "):
            if not current:
                raise ValueError(f"orphan list item: {raw}")
            if not isinstance(data.get(current), list):
                raise ValueError(f"field {current} mixes scalar and list values")
            data[current].append(parse_scalar(raw[4:]))
            continue
        if raw.startswith("-"):
            raise ValueError(f"unsupported top-level list item: {raw}")
        if ":" not in raw:
            raise ValueError(f"unsupported frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        key = key.strip()
        if not key:
            raise ValueError(f"empty frontmatter key: {raw}")
        current = key
        value = value.strip()
        data[key] = [] if value == "" else parse_scalar(value)
    return data, body


def read_frontmatter(path: Path) -> tuple[dict[str, Any], str, str]:
    text = path.read_text(encoding="utf-8")
    data, body = split_frontmatter(text)
    return data, body, text.replace("\r\n", "\n")
