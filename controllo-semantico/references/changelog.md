# Changelog

## v2.2-non-regression — 2026-08-19

- Introdotto il Gate di Non Regressione trasversale senza modificare il conteggio dei 29 controlli.
- Obbligatorie baseline pre-modifica, contratto di compatibilita, confronto prima/dopo e prove NUOVO/PREESISTENTE/INTEGRITA per ogni mutazione.
- Rimozioni e breaking change sono ammesse solo se esplicitamente autorizzate e circoscritte; tutto il resto della baseline resta protetto.
- Aggiunti `references/non-regression-gate.md`, `assets/templates/12_non_regressione.md` e `scripts/non_regression_guard.py`.
- Integrato NR nei gate Drive/GitHub, nella governance multi-AI, nei modelli di output e nelle note di controllo.
- Builder aggiornato con `semaforo_non_regressione` mantenendo compatibilita con payload precedenti; validatore compatibile con note legacy prive del nuovo campo.
- Ricostruito il bundle assets nel pacchetto e verificata la presenza di tutti i template storici prima del packaging.

## v2.1-unione — 2026-08-12

- Consolidata la base v2.0.1-operativa con governance progetti multi-AI, workflow Drive/GitHub, knowledge publication e Graphify.
- Ratificata la struttura progetto numerata, gli handoff in `07_HANDOFF` e gli output AI in `08_OUTPUT_AI/<AI>/`.

## v2.0.1-operativa — 2026-08-05

- Rinominata la skill in `controllo-semantico` per sostituire la versione precedente ed evitare due skill concorrenti sugli stessi trigger.
- Allineati builder e validatore: `build_control_note.py` normalizza le chiavi snake_case nei titoli canonici (`prompt_operativo` -> `Prompt operativo`).
- Eliminata la duplicazione della sezione `Punti aperti` quando il payload la contiene tra le sections.
- Documentati nella SKILL.md i titoli di sezione esatti richiesti dal validatore.

## v2.0-operativa — 2026-08-05

- Ripristinata la modalita completa con persistenza Google Drive.
- Definito il trigger `controllo semantico` come autorizzazione esplicita al workflow completo.
- Reintrodotti `CLAUDE/OBSIDIAN/00 - Controlli/`, Wiki condivisa e read-before-write.
- Aggiunti verifica cartella, anti-duplicazione, upload raw Markdown, readback e controllo concorrenza.
- Conservati i guardrail v2.0-safe su fonti, prove, semafori, stati e limiti quantitativi.
- Aggiunte modalita SOLO-ANALISI e LOCALE.
- Aggiunti generatori, validatore e manifest SHA-256 locali.
- Ripristinati i 12 template del motore dialettico come schemi operativi.

## v1.5 — 2026-07-10

- 29 controlli, FASE -0.5 S1-S5, metodo Hegel, minimax, Kelly, Fermi, E14, E15, E20.
- Persistenza Obsidian e Wiki condivisa.

## v2.0-safe locale — 2026-08-04

- Rafforzati i guardrail ma rimossa l'operativita Drive.
- Questa regressione e corretta dalla v2.0-operativa.
