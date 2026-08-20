# Obsidian schema

## Frontmatter obbligatorio

```yaml
---
type: knowledge-record
canonical_id: PRJ-AREA-TIPO-NNN
project_code: PRJ-TAMIOT-AUTOMAZIONE
title: Titolo leggibile
version: 1.0.0
status: DRAFT
classification: internal
source_refs:
  - drive:FILE_ID
source_hashes:
  - sha256:HEX
created_at: 2026-08-03T12:00:00+02:00
updated_at: 2026-08-03T12:00:00+02:00
owner: Claude
aliases: []
tags: []
related_ids: []
---
```

## Regole

- `canonical_id` e immutabile e univoco nel vault.
- `version` usa SemVer quando possibile.
- `status` usa gli stati ammessi dalla skill.
- `classification`: `public`, `internal`, `restricted` o `secret`.
- `secret` non puo essere pubblicato, esportato o inviato a Graphify.
- `source_refs` usa prefissi espliciti: `drive:`, `github:`, `wiki:`, `obsidian:`, `graphify:`.
- `source_hashes` usa `sha256:`.
- `related_ids` contiene ID canonici, non titoli liberi.
- Il corpo contiene fatti, inferenze, rischi, decisioni, prove e punti aperti.
- Non modificare `.obsidian` senza autorizzazione separata.

## Struttura consigliata

```text
00 - Controlli/
10 - Progetti/
20 - Decisioni/
30 - Specifiche/
40 - Handoff/
50 - Fonti/
90 - Conflitti/
99 - Archivio/
```

## Wikilink

Usa `[[canonical_id|Titolo]]` quando l'ID e noto. Non creare link a entita presunte.

## Conflitti

Crea una nota in `90 - Conflitti/` con:

- ID coinvolti;
- versioni e hash;
- fonti;
- owner;
- decisione necessaria;
- stato `DRAFT` o `PARTIAL`.
