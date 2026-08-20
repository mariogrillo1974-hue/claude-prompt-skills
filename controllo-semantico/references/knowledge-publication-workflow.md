# Knowledge publication workflow

## Indice
1. Scopo
2. Modello a cinque sistemi
3. Stati
4. Pipeline
5. Conflitti
6. Sicurezza
7. Readback
8. Rollback

## 1. Scopo

Coordinare GitHub, Drive, Wiki, Obsidian e Graphify senza confondere fonte canonica e viste derivate.

## 2. Modello a cinque sistemi

- GitHub: codice, commit, branch, pull request, tag e release.
- Drive: decisioni, approvazioni, fonti, inventario, manifest, handoff e snapshot.
- Wiki: conoscenza pubblicata, revisionata e leggibile.
- Obsidian: note Markdown portabili, operative e collegate.
- Graphify: grafo derivato per esplorazione e ricerca relazionale.

Ogni record usa un `canonical_id` stabile. Un nome file, titolo pagina o label del grafo non sostituisce l'identita.

## 3. Stati

`DRAFT -> VALIDATED -> APPROVED -> PUBLISHED -> PROMOTED`

Stati laterali: `PARTIAL`, `SUPERSEDED`, `REJECTED`.

Non saltare `APPROVED` per target comuni o pubblici. `PROMOTED` richiede readback di tutti i target inclusi nello scope.

## 4. Pipeline

1. Risolvi la matrice canonica del progetto.
2. Leggi fonti, inventario, stato e lavori attivi.
3. Acquisisci lease sullo scope.
4. Crea o aggiorna il record nello spazio AI.
5. Calcola hash dei contenuti normalizzati.
6. Valida con `validate_knowledge_record.py`.
7. Richiedi autorizzazione per la pubblicazione.
8. Pubblica target per target.
9. Rileggi ogni target e confronta identita, versione, hash e stato.
10. Crea un promotion record e valida con `validate_promotion_record.py`.
11. Aggiorna inventario e handoff.
12. Promuovi o registra `PARTIAL`.

## 5. Conflitti

- Stesso `canonical_id`, versioni diverse: non sovrascrivere; identifica la fonte autorevole.
- Titoli uguali, ID diversi: mantieni separati finche una prova non dimostra equivalenza.
- Due AI sullo stesso scope: sospendi la scrittura comune e risolvi lease/owner.
- Hash diversi dopo readback: stato `PARTIAL`, apri recovery.
- Fonte modificata dopo pubblicazione: marca la vista come da revisionare; non riscrivere automaticamente.

## 6. Sicurezza

Escludi sempre:

- cartelle o file dichiarati segreti;
- `.env`, cookie, token, chiavi, password, credenziali e chiavi private;
- dati personali non necessari;
- duplicati non classificati;
- contenuti `SUPERSEDED` o `REJECTED`;
- sorgenti con segreti incorporati non sanificati.

## 7. Readback

Il readback deve verificare almeno:

- target e ID effettivi;
- versione;
- `canonical_id`;
- hash o campi portanti;
- timestamp e revisione;
- autorizzazione applicata;
- assenza di contenuti esclusi.

Una risposta del tool senza rilettura non prova la persistenza completa.

## 8. Rollback

Ogni pubblicazione registra:

- oggetto precedente o revisione precedente;
- comando o azione di ripristino;
- owner;
- condizione di attivazione;
- prova del rollback in ambiente controllato quando rilevante.
