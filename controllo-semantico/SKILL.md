---
name: controllo-semantico
description: >-
  Protocollo operativo per validare prompt, significati, fonti, prove, risposte
  e decisioni con 29 controlli, tesi-antitesi-sintesi, falsificazione e
  guardrail quantitativi. Usare per "controllo semantico", "applica il
  protocollo", "valida", "stress-test", "red team", "trova i buchi" o
  GO/NO-GO su documenti, bandi, norme, software, contratti o decisioni. Il
  trigger "controllo semantico" attiva analisi, nota Markdown, Drive e Wiki
  read-before-write; "solo analisi" e "locale" disattivano scritture remote.
  Usare anche per governance multi-AI Drive/GitHub e per ogni modifica, merge,
  migrazione o promozione che richiede il Gate di Non Regressione.
---

# Protocollo semantico operativo

Versione: **v2.2-non-regression** (19/08/2026)  
Base consolidata: v2.1-unione + Gate di Non Regressione trasversale. I 29 controlli restano invariati; ogni mutazione deve ora dimostrare che le capacita preesistenti non sono state eliminate o degradate fuori dallo scope esplicitamente autorizzato.

Applicare il protocollo prima della conclusione. Il rigore resta massimo; si puo comprimere l'esposizione, non il controllo.

## 1. Modalita operative

Determinare la modalita dalle parole dell'utente, senza chiedere conferma quando la scelta e univoca.

- **COMPLETA** — trigger esatto `controllo semantico`, `applica il protocollo` o richiesta equivalente senza limitazioni. Eseguire analisi, creare la nota `.md`, archiviarla su Drive e aggiornare la Wiki quando emerge un fatto canonico.
- **SOLO-ANALISI** — l'utente dice `solo analisi`, `non salvare`, `senza Drive` o equivalente. Nessuna scrittura locale o remota.
- **LOCALE** — l'utente dice `locale`, `salva localmente` o indica una root sotto `/mnt/data`. Creare e validare artefatti locali, senza Drive.
- **DOSSIER** — l'utente chiede red-team, contro-dossier, due diligence, GO/NO-GO o l'oggetto e ad alto rischio. Applicare anche il motore dialettico profondo; la persistenza segue COMPLETA/LOCALE/SOLO-ANALISI.

Una richiesta di `controllo semantico` e autorizzazione esplicita al workflow COMPLETA descritto nella frontmatter. Non estendere questa autorizzazione ad altri servizi, destinatari o operazioni.

## 2. Regole non negoziabili

1. Considerare tutti i 29 controlli; usare N/A con motivazione quando non pertinenti.
2. Validare nell'ordine: prompt, semantica, risposta.
3. Produrre tre semafori: prompt, semantico, risposta; aggiungere lo stato di Non Regressione per ogni attivita e lo stato di persistenza nelle modalita con scrittura.
4. Non inventare fatti, fonti, numeri, versioni, identificativi, risultati di tool o azioni esterne.
5. Circoscrivere ogni VERDE a oggetto, versione, ambiente, data e prova.
6. Etichettare i claim decisivi: FATTO, INFERENZA, RISCHIO, RACCOMANDAZIONE, ASSUNZIONE.
7. Distinguere statico da runtime, creato da validato, validato da approvato, caricato da riletto.
8. Costruire l'antitesi dallo steelman e usare evidenze contrarie reali.
9. Scegliere un vincitore per asse o indicare la prova esatta mancante.
10. Un rischio e chiuso solo da prova vincolante: fonte vigente, firma, misura, test riproducibile, contratto, build, readback o audit.
11. Ogni fallimento di lettura, scrittura, upload, update o readback e visibile; mai procedere come se fosse riuscito.
12. Non usare numeri puntuali inventati. Leggere `references/quantitative-guardrails.md` prima di Kelly, Fermi, E14 o minimax quantitativo.
13. Non modificare file di terzi senza leggere la versione corrente e preservarne il contenuto pertinente.
14. Non creare duplicati Drive: verificare cartella e nome prima di creare o caricare.
15. Non usare Google Docs per la persistenza: salvare Markdown grezzo `.md`.
16. Non includere segreti, token, cookie, chiavi o dati personali non necessari negli artefatti.
17. Se nome o codice progetto non sono disponibili, usare YAML `null` e registrarli come punto aperto; non inventarli.
18. Gli stati `APPROVED`, `PUBLISHED` e `PROMOTED` richiedono prova diretta osservata.
19. Un linter verde dimostra coerenza formale, non verita sostanziale.
20. Una nota locale non prova la persistenza Drive; un upload non prova il contenuto finche non e eseguito il readback.
21. Ogni mutazione deve applicare `references/non-regression-gate.md`: acquisire la baseline prima di scrivere, preservare tutto cio che non e esplicitamente autorizzato a cambiare, confrontare prima/dopo ed eseguire test NUOVO, PREESISTENTE e INTEGRITA. Un test nuovo verde non compensa una regressione precedente.
22. Non interpretare mai una richiesta di aggiunta, miglioramento o correzione come autorizzazione implicita a eliminare funzionalita, contenuti, dati, workflow o compatibilita esistenti.

## 3. Profili di esposizione

- **COMPATTO**: prompt ricostruito, assunzioni decisive, conclusione, punti aperti, tre semafori.
- **STANDARD**: aggiungere mappa prove, tesi/antitesi, limiti e prossime azioni.
- **DOSSIER**: aggiungere motore profondo, pre-mortem, minimax, registro completo, gate e contestazione esterna.

Usare STANDARD come default. Usare COMPATTO solo per richieste semplici; DOSSIER nei casi ad alto rischio.

## 4. Metodo obbligatorio

Leggere `references/metodo-29-controlli.md`. Applicare in sequenza:

1. FASE -1: diagnosi e ricostruzione del prompt.
2. FASE -0.5: coerenza dei significati S1-S5.
3. FASE 0: perimetro, dati, ruolo, giudice e alternative.
4. FASE 1: fonti, autorita, vigenza, gerarchia, citazioni e dati mancanti.
5. FASE 2: tesi, antitesi, sintesi, falsificazione, dimostrato/sperato, base-rate e prova vincolante.
6. FASE 3: prova del nove, plausibilita, completezza, contestazione, pre-mortem, verifica professionale, punti aperti e semaforo risposta.

Se l'attivita modifica uno stato esistente, eseguire inoltre il **Gate di Non Regressione** descritto in `references/non-regression-gate.md` prima della chiusura o promozione. Il gate e trasversale e non modifica il conteggio dei 29 controlli.

Per alto rischio leggere anche `references/motore-dialettico.md` e usare i template `assets/templates/00_...` fino a `12_...` solo per le parti pertinenti.

## 5. Produzione della nota Markdown

Nelle modalita COMPLETA o LOCALE:

1. Preparare una nota con `assets/templates/09_nota_obsidian.md`.
2. Includere almeno: data/ora, oggetto, categoria, modalita, project_name, project_code, semaforo_prompt, semaforo_semantico, semaforo_risposta, semaforo_non_regressione, stato_persistenza, owner, scadenza, fonti, hash e punti_aperti. Per attivita senza mutazioni usare `N/A` con motivo; per mutazioni usare VERDE/GIALLO/ROSSO secondo il gate NR.
3. Salvare prima una copia locale nuova sotto `/mnt/data/controlli-semantici/`; non sovrascrivere. Nome: `YYYYMMDD-HHMMSS__slug-oggetto__controllo-semantico.md`.
4. Eseguire `scripts/validate_control_note.py` e `scripts/hash_manifest.py`.
5. Consegnare sempre il file `.md` nella chat, anche quando Drive riesce.

Usare `scripts/build_control_note.py` quando i dati sono strutturabili in JSON. Non dichiarare VALIDATED se il validatore fallisce.

Titoli di sezione obbligatori nella nota: `## Prompt operativo` e `## Punti aperti` (il validatore li richiede con questa esatta grafia). Il builder normalizza automaticamente le chiavi snake_case del payload (`prompt_operativo` -> `Prompt operativo`); una eventuale sezione `punti_aperti` nel payload confluisce nella sezione finale `Punti aperti` senza duplicati.

## 6. Persistenza Google Drive

In modalita COMPLETA leggere ed eseguire `references/persistenza-drive.md`.

Target canonico:

- percorso: `CLAUDE/OBSIDIAN/00 - Controlli/`
- folder ID storico da verificare: `15aUcOM2e-CtAJjXuv-gmTGujl0XUfG_8`
- Wiki: `CLAUDE/OBSIDIAN/Wiki/`
- MOC: `Wiki/_MOC - Wiki.md`

Sequenza minima:

1. verificare metadata e accesso al target ID;
2. se il target non e valido, cercare o ricostruire la catena `CLAUDE` -> `OBSIDIAN` -> `00 - Controlli` senza duplicati;
3. caricare il `.md` grezzo;
4. rileggere metadata e contenuto del file caricato;
5. confrontare hash locale e contenuto riletto quando tecnicamente disponibile;
6. aggiornare la Wiki solo se emerge un fatto canonico, sempre read-before-write;
7. riportare ID, link, nome, timestamp e readback osservati.

Se Drive o il connettore non sono disponibili, non simulare il successo: mantenere il file locale, indicare `PERSISTENZA: ROSSO`, creare il punto aperto e degradare il semaforo risposta secondo `references/evidence-and-semaphores.md`.

## 7. Wiki condivisa e Wiki locale

- **Wiki Drive**: seguire `references/persistenza-drive.md`; consultare il MOC, leggere la voce corrente, aggiornare solo il fatto canonico necessario, rileggere dopo l'update.
- **Wiki locale**: leggere `references/wiki-skill.md` solo quando l'utente chiede una Wiki locale o la modalita LOCALE lo richiede.

Aggiornare `CONTEXT.md` per ultimo. Non confondere una vista derivata con la fonte primaria.

## 8. Uscita minima

Usare `references/output-templates.md`. La risposta deve includere:

- prompt operativo e perimetro;
- assunzioni e termini portanti;
- claim decisivi etichettati;
- tesi, antitesi e sintesi;
- prova del nove e limiti;
- punti aperti con prova, owner, scadenza/evento e impatto;
- semafori prompt, semantico e risposta;
- stato Non Regressione (VERDE/GIALLO/ROSSO/N/A) e, per le mutazioni, baseline e prove prima/dopo;
- nelle modalita con persistenza: file locale, validazione, hash, stato Drive, readback e stato Wiki.

## 9. Script inclusi

- `scripts/build_control_note.py`: genera una nota nuova da JSON sotto `/mnt/data`.
- `scripts/validate_control_note.py`: valida frontmatter e sezioni obbligatorie.
- `scripts/hash_manifest.py`: produce SHA-256 e manifest locale.
- `scripts/non_regression_guard.py`: crea una baseline strutturale e segnala rimozioni inattese; usarlo come supporto al gate NR, mai come sostituto dei test funzionali.
- `scripts/wiki_init.py`: inizializza una Wiki locale senza sovrascrivere.
- `scripts/lint_wiki.py`: controlla la Wiki locale.
- `scripts/frontmatter_utils.py` e `scripts/safe_paths.py`: supporto locale.

Gli script non effettuano chiamate di rete. Le operazioni Drive si eseguono esclusivamente tramite il connettore disponibile nella sessione.

## 10. Chiusura differenziale

Per ogni semaforo spiegare:

- perche il colore scelto e corretto;
- quale prova manca per il livello superiore;
- perche il livello inferiore sarebbe eccessivamente severo.

Se la persistenza era parte del criterio di successo e non e riuscita, non chiudere con un VERDE globale.

Se una mutazione ha `NON REGRESSIONE: ROSSO`, non chiudere con VERDE e non promuovere. Se ha `NON REGRESSIONE: GIALLO` per copertura insufficiente su funzionalita sostanziali, il semaforo risposta e al massimo GIALLO-SOSTANZA. Una breaking change puo essere compatibile con NR VERDE solo quando la rimozione e esplicitamente autorizzata e tutto il resto della baseline e provato come preservato.

## 11. Governance progetti multi-AI su Drive (da v1.7, target di Mario)

Per il lavoro sui PROGETTI leggere ed eseguire `references/drive-github-multi-ai-workflow.md`,
`references/multi-ai-governance.md` e `references/claude-environments.md`
(template in `references/drive-github-templates.md`; pubblicazione conoscenza in
`references/knowledge-publication-workflow.md`).

Target canonico dei progetti (deciso da Mario, 12/08/2026):

- cartella madre: `01 - PROGETTI GESTITI CON INTELLIGENZA ARTIFICIALE`
  — folder ID `16Ty6PiHhoUEcNIkVqEJLMamGqQdtpiRb`;
- ogni progetto e una sottocartella della madre con la struttura numerata
  (modello: progetto "1 - Automazione Tamiot con WA e chat AI",
  ID `1wvfuMhlv8Lb2PCDJbl_78xRPkiTAbbxQ`):
  `00_PROGETTO` (README, AGENTS, STATO_PROGETTO, FONTI_CANONICHE, INVENTARIO),
  `01_FONTI_ATTIVE`, `02_ANALISI`, `03_SPECIFICHE`, `04_SORGENTI`,
  `05_TEST_E_COLLAUDI`, `06_DECISIONI`, `07_HANDOFF`, `08_OUTPUT_AI/<AI>/`,
  `09_WIKI`, `98_SEGRETI_NON_INDICIZZARE`, `99_ARCHIVIO_DA_VERIFICARE`;
- gli HANDOFF di progetto vanno in `07_HANDOFF` (ratificato da Mario 12/08);
- ogni AI scrive SOLO in `08_OUTPUT_AI/<propria-AI>/` salvo autorizzazione
  comune esplicita (ratificato da Mario 12/08); Claude Code usa
  `08_OUTPUT_AI/CLAUDE-CODE/`;
- `98_SEGRETI_NON_INDICIZZARE` e sempre esclusa da letture di massa, indici,
  note e artefatti;
- matrice di autorita: Drive governa obiettivi, decisioni, manifest e handoff;
  GitHub governa il codice; Wiki/Obsidian/Graphify sono viste derivate;
- stati artefatti: DRAFT -> IN_REVIEW -> APPROVED -> PROMOTED -> ARCHIVED
  (REJECTED terminale conservato); mai saltare i gate;
- prima di modificare un progetto eseguire il preflight di sessione degli 11
  passi definito in `drive-github-multi-ai-workflow.md`.

Le NOTE DI CONTROLLO restano in `CLAUDE/OBSIDIAN/00 - Controlli/` (sezione 6):
i due flussi non si mescolano — la nota cita il progetto, il progetto archivia
i propri artefatti nella sua struttura numerata.
