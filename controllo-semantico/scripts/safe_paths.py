#!/usr/bin/env python3
"""Confinamento dei percorsi della skill sotto /mnt/data."""
from __future__ import annotations

from pathlib import Path

SANDBOX_ROOT = Path("/mnt/data").resolve()


def resolve_local_root(value: str, *, must_exist: bool = True) -> Path:
    """Restituisce una directory locale sicura sotto /mnt/data.

    I componenti esistenti vengono risolti per impedire fughe tramite symlink.
    """
    raw = Path(value).expanduser()
    candidate = raw.resolve(strict=False)
    try:
        candidate.relative_to(SANDBOX_ROOT)
    except ValueError as exc:
        raise ValueError(f"percorso fuori dal sandbox consentito: {candidate}") from exc

    if candidate == SANDBOX_ROOT:
        raise ValueError("specificare una sottocartella di /mnt/data, non la radice del sandbox")
    if must_exist and (not candidate.exists() or not candidate.is_dir()):
        raise ValueError(f"la cartella locale non esiste o non e una directory: {candidate}")
    return candidate
