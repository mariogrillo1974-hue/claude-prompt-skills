# Graphify schema

## Principio

Graphify e una vista derivata. Il grafo deve poter essere eliminato e rigenerato dalle fonti validate.

## Nodi CSV

Campi minimi:

- `node_id`: uguale al `canonical_id`.
- `label`: titolo leggibile.
- `node_type`: valore di `type`.
- `project_code`.
- `version`.
- `status`.
- `classification`.
- `source_refs`: JSON compatto.
- `source_hashes`: JSON compatto.
- `content_hash`: SHA-256 del contenuto normalizzato.
- `updated_at`.

## Archi CSV

Campi minimi:

- `edge_id`: SHA-256 abbreviato di sorgente, relazione e destinazione.
- `source_id`.
- `relation`: `RELATES_TO`, `DEPENDS_ON`, `SUPERSEDES`, `IMPLEMENTS`, `VALIDATES`, `DERIVED_FROM`, `DOCUMENTS`.
- `target_id`.
- `source_ref`.
- `confidence`: `high`, `medium`, `low`.

## Deduplicazione

1. Deduplica per `canonical_id`.
2. Stesso ID e stesso hash: una sola istanza.
3. Stesso ID e hash diverso: errore bloccante, salvo versione superiore esplicitamente selezionata.
4. Titolo uguale con ID diverso: non fondere.
5. Alias non diventano nodi autonomi salvo identita propria.

## Esclusioni

Escludi:

- `classification: secret`;
- `status: SUPERSEDED` o `REJECTED`;
- file in percorsi con `98_SEGRETI`, `.obsidian`, `.git`, `secrets`;
- file con pattern di credenziali;
- record privi di `canonical_id` o provenienza.

## Manifest

`graph_manifest.json` include:

- versione schema;
- timestamp;
- radice analizzata;
- file inclusi ed esclusi;
- nodi e archi generati;
- hash di `nodes.csv` e `edges.csv`;
- errori e conflitti.
