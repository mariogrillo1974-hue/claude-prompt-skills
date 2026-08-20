# Template operativi Drive/GitHub

Usa i campi applicabili. Non inventare ID, URL, SHA, approvazioni o risultati
di test. Scrivi `non disponibile`, `non autorizzato` o `da assegnare`.

## Manifest repository

```yaml
type: repository-manifest
project_id:
project_name:
drive_project_item_id:
drive_project_relative_path:
github_repository:
github_repository_id:
default_branch:
canonical_code: github
canonical_project_memory: drive
drive_github_control_path:
active_repo_in_synced_drive: false
last_verified_default_sha:
verified_at:
verified_by:
branch_policy:
promotion_policy:
secret_paths_excluded:
```

## Dichiarazione lavoro

```yaml
type: ai-work-lease
work_id:
project_id:
owner_ai:
agent_instance_id:
session_id:
workspace_id:
lease_epoch:
lease_revision:
status: PLANNED
objective:
scope_in:
scope_out:
logical_resources:
paths_expected:
paths_normalized:
drive_baseline:
git_base_sha:
branch:
started_at_utc:
last_heartbeat_utc:
expires_at_utc:
conflicts_checked_at:
conflicts_found:
lease_readback_at:
activation_rescan_at:
activated_at:
authorization_matrix:
  local_write: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  commit: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  drive_common: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  push: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  pull_request: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  comments: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  merge: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  tag: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
  release: {authorized: false, granted_by: null, evidence: null, scope: null, expires_at_utc: null}
completion_evidence:
```

Stati lease: `PLANNED`, `ACTIVE`, `BLOCKED_CONFLICT`, `STALE_DA_VERIFICARE`,
`HANDED_OFF`, `CLOSED`.

## Intestazione artefatto AI

```yaml
type:
artifact_id:
project_id:
work_id:
author_ai:
agent_instance_id:
created_at:
status: DRAFT
baseline_drive:
baseline_git_sha:
branch:
commit_sha:
pull_request:
sources:
payload_hash_sha256_sidecar:
verification_state:
```

Calcola l'hash sul payload o su un file sidecar; non includere nello stesso
payload il campo che dovrebbe contenere il suo hash.

## Handoff

```markdown
# Handoff - <WORK_ID> - <oggetto>

## Identita

- Progetto:
- Autore AI:
- Istanza AI:
- Sessione/workspace:
- Data:
- Stato:
- Baseline Drive:
- SHA iniziale:
- Branch:
- SHA finale:
- Pull request:

## Obiettivo e perimetro

- Obiettivo:
- Incluso:
- Escluso:

## Modifiche

| File/artefatto | Azione | Motivo | Hash o commit |
|---|---|---|---|

## Verifiche

| Comando/lettura | Ambiente | Esito | Evidenza |
|---|---|---|---|

## Operazioni esterne

| Operazione | Autorizzata | Eseguita | Readback |
|---|---|---|---|

## Decisioni e limiti

- Decisioni:
- Alternative non scelte:
- Limiti:

## Punti aperti

| Punto | Prova necessaria | Owner | Scadenza/evento | Impatto |
|---|---|---|---|---|

## Prossimo passo

- Azione:
- Owner:
- Precondizione:
```

## Record di promozione

```yaml
type: promotion-record
promotion_status: PENDING
project_id:
work_id:
artifact_id:
source_ai_path:
source_branch:
source_commit:
pull_request:
github_repository_id:
expected_pr_head_sha:
observed_pr_head_sha:
expected_merge_method:
approved_by:
approval_evidence:
checks_on_tested_sha:
observed_merge_method:
observed_merged_commit:
default_branch_contains_observed_merged_commit:
source_change_equivalence:
github_readback_at:
drive_destination:
drive_file_id:
expected_drive_revision_or_hash:
observed_drive_revision_or_hash:
drive_readback_at:
original_preserved_at:
limits:
```

Valori finali di `promotion_status`: `PROMOTED`, `PARTIAL`, `REJECTED`. Non compilare
`PROMOTED` prima dei readback richiesti dallo scope.

## Registro di fallimento

```yaml
type: operation-failure
project_id:
work_id:
operation:
target:
attempted_at:
observed_error:
partial_state:
claims_affected:
recovery_proposal:
owner:
status: OPEN
```

## Chiusura lease

```yaml
type: ai-work-lease-close
work_id:
owner_ai:
agent_instance_id:
session_id:
workspace_id:
lease_epoch:
lease_revision:
closed_at:
final_status:
files_touched:
final_commit:
handoff_path:
open_points:
readback_complete:
lease_close_readback_at:
```
