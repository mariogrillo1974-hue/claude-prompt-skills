---
name: protocollo_coding
description: >-
  Protocollo prompt vincolante per task di codice ad alto rischio (fix,
  feature, refactor, test) dove l'agent manipola dati sensibili o
  business-critical. Attivalo prima di toccare il codice: governa rigore
  operativo (scope, no path assoluti, verifica binaria, no warning silenziati,
  secret, edge case, validazione input, no modifiche architetturali silenziose)
  e ragionamento (diagnosi prompt, doppio semaforo, Hegel, prova vincolante).
  Universale e indipendente dallo stack.
---

# Protocollo Coding — Regole operative per agent AI su codice

> Protocollo prompt **vincolante** per ogni task di codice/fix/ottimizzazione su
> progetti ad alto rischio, dove l'agent AI manipola dati sensibili o business-critical.
> Universale e indipendente dallo stack: sostituisci gli esempi di comando con quelli
> reali del progetto corrente.
>
> Le sezioni A–F governano *come si tocca il codice* (rigore operativo). Le sezioni G–H
> innestano il **Protocollo di controllo prompt** (5 fasi, 29 controlli) che governa
> *come si ragiona* prima e dopo.

## Regola 0 — Non andare in loop sprecando token

**Prima di agire, sappi cosa stai facendo.** Se non hai un modello chiaro del problema,
del file giusto o della causa di un errore, **fermati**: non tirare a indovinare in
cicli ripetuti.

- **Niente loop ciechi.** Mai ripetere lo stesso tentativo (stessa modifica, stesso
  comando, stessa ricerca) sperando in un esito diverso. Due tentativi falliti sulla
  stessa ipotesi = l'ipotesi è sbagliata: cambia approccio o fermati.
- **Soglia di stop esplicita.** Dopo ~2-3 iterazioni senza progresso reale e misurabile,
  interrompi e **chiedi conferma all'utente** con: cosa hai capito, cosa hai provato, dove
  sei bloccato, quali sono le 2-3 strade possibili. Meglio una domanda mirata che dieci
  tentativi a vuoto.
- **Diagnosi prima dell'azione.** In caso di errore, **non indovinare**: leggi i log/output
  reali, isola la causa, poi agisci sui fatti (anti-allucinazione). Leggere un file di più
  costa meno di un ciclo di fix sbagliati.
- **Economia di contesto.** Non ricaricare/rileggere ciò che già sai, non rilanciare
  build/test identici già verdi, non esplorare a tappeto quando un target è già noto. Ogni
  azione deve ridurre l'incertezza; se non lo fa, non farla.
- **Ambiguità che cambia l'esito → ferma e chiedi** (FASE -1), non procedere a forza.

---

## A. Le 11 regole non negoziabili (rigore operativo)

Valgono per **ogni sub-chat e agent AI** che opera sul repo. Sono non negoziabili.

### 1. Nessun file di lavoro fuori dal repo
Mai creare file di pianificazione, task-list, scratchpad, note o artefatti di lavoro fuori dal working tree. La pianificazione si gestisce in-chat o nella cartella di lavoro dichiarata dal progetto. Script diagnostici una-tantum: solo nelle cartelle script del progetto o inline, mai in `%APPDATA%`, `~/.claude`, `C:\Temp`, ecc.

### 2. Nessun path assoluto nei file persistenti
Vietati `file:///`, `C:/`, `/c/Users/...` in markdown, codice, walkthrough, docs. Solo path **relativi alla root del repo** (es. `src/<modulo>/<file>`).

### 3. Verifica binaria full-repo obbligatoria
La "fatto" è binaria. Si dichiara "0 errori 0 warning" **solo dopo** aver eseguito e incollato l'**ultima riga di output reale** della pipeline di verifica del progetto (lint + type/compile-check + test + build), tutta verde. **Non vale** incollare il command literal preso dalla configurazione — quella è la *definizione* dello script, non l'output. Se stdout è vuoto, va detto esplicitamente ("exit 0, stdout vuoto"). Per le suite di test si incolla la riga di conteggio reale (es. `Tests run: N, Failures: 0, Errors: 0, Skipped: 0` / `N passed`), **mai** una riga separatrice.

### 4. Nessun silenziamento di warning
Vietato chiudere un warning sopprimendolo (`@SuppressWarnings`, `eslint-disable*`, `@ts-ignore`, `as any`, cast forzati, eccezioni ingoiate, import morti). Se genuinamente necessario → **fermati e chiedi conferma** prima di procedere.

### 5. Nessuna modifica fuori scope
Lo scope = i path elencati nella sezione OUTPUT del prompt corrente. Tutto il resto è **read-only**.

### 6. Source-of-Truth immutabile (eccezione: walkthrough finale)
La documentazione/vault di progetto è Source-of-Truth immutabile. Uniche modifiche permesse: la redazione finale di un walkthrough nel **percorso autorizzato dichiarato nel prompt operativo del repo corrente**. Il walkthrough documenta lavoro svolto, file modificati, test eseguiti, esiti reali, deviazioni dal piano e rischi residui. Eventuali aggiornamenti di stato nella roadmap li applica l'orchestratore in fase di commit, non l'agent esecutore.

### 7. Lingua dei deliverable
- **Deliverable / walkthrough / commenti utente-visibili** → lingua di progetto.
- **Codice e identificatori** (variabili, funzioni, classi, file) → **inglese**.
- **Contenuti cliente-finale** (testi, messaggi, template) → nelle lingue richieste, **revisionati da persona competente** prima della produzione. L'agent **non improvvisa né traduce a vanvera**.

### 8. Sicurezza dei secret (no hardcoding)
Mai chiavi/token/password/secret in codice, file versionati, commit message, test, log. Tutte le credenziali si leggono a runtime dal loader centralizzato del progetto, validato; i file `.env` sono gitignored e gli `.example` contengono **solo** placeholder neutri. I dati personali si cifrano (mai in chiaro). **Mai incollare secret in chat né in output diagnostica.** Valori dummy/di test sono ammessi.

### 9. Integrità dei dati e casi limite
Massima attenzione a calcoli numerici ed **edge case**.
- Valori **monetari** **MAI** perdono centesimi: lavorare in **interi (centesimi)**, mai floating point binario.
- Conteggi al confine (capacità, posti, rate-limit) gestiti esplicitamente: zero, `null`/`undefined`, negativi non previsti, overflow, stringhe/collezioni vuote, date/orari al confine (fusi, turni). Obiettivo: **zero stati incoerenti, zero record fantasma**.

### 10. Validazione input prima della business logic
Nessun input utente né parametro al **confine del sistema** (route, payload webhook, job scheduler, env vars) entra senza **validazione preventiva con schema**, **prima** della business logic e di ogni effetto collaterale (scrittura DB, dispatch messaggi, notifiche). Input nullo/negativo/malformato → **rifiutato con errore esplicito** (es. `400`), mai propagato silenziosamente.

### 11. Nessuna creazione/modifica architetturale silenziosa
Complemento della Regola 5. Anche **dentro** lo scope autorizzato, non creare nuovi file sorgente, nuove **dipendenze**, nuove tabelle/migrazioni, nuovi endpoint, nuovi canali o cambi architetturali senza prima **dichiarare in chat la logica e la motivazione**. Le scelte tecnologiche di fondo restano del committente: vietato introdurre librerie/pattern non concordati "di nascosto" dentro un task di altra natura.

---

## B. Workflow TDD (test-first) — ordine tassativo

Per ogni nuova funzionalità/endpoint/componente:

1. **Pianificazione** — breve dichiarazione di intenti (in chat o nella cartella di lavoro, mai in file esterni — Regola 1).
2. **Test prima** — scrivere **PRIMA** i test (unit + integrazione) coprendo **happy path**, **casi limite**, **errori**. Test **mordenti/anti-masking**: rossi se la logica regredisce o se trapelano dati sensibili, non solo verdi per costruzione.
3. **Implementazione** — codice **minimo** per far passare i test.
4. **Verifica** — singola responsabilità + nessuna violazione delle Regole 0-11.

---

## C. Definition of Done (rubrica binaria)

Una task è **"fatta"** SOLO quando **tutte** le caselle sono verdi (applicazione della Regola 3):

- [ ] La validazione dell'input avviene **prima** della business logic (Regola 10).
- [ ] **Tutti** i test (unit + integrazione) verdi, con l'**ULTIMA RIGA REALE** di output incollata (Regola 3).
- [ ] **Nessun secret né dato personale** esposto in log, risposte, analytics, audit, notifiche (Regola 8).
- [ ] Le **eccezioni** sono gestite senza crashare: in assenza di dato certo → **handoff a operatore umano** (HITL), **mai** valori inventati su categorie critiche.
- [ ] **Nessun warning silenziato** (Regola 4) e **nessuna modifica fuori scope** (Regola 5).

In caso di errore durante lo sviluppo: **non indovinare** (anti-allucinazione, Regola 0). Fermarsi, analizzare i **log reali**, proporre correzione basata sui fatti.

---

## D. Source of Truth (principio anti-improvvisazione)

Il sistema **non inventa mai** dati ad alto rischio. In assenza di dato certo e tracciabile a una fonte → **handoff a operatore umano (HITL)**, mai valore inventato.

Categorie tipicamente ad **alto rischio**, da **non improvvisare mai**: dati sanitari/di sicurezza, valori monetari e prezzi, scadenze e termini di legge, disponibilità e stato delle risorse, dati personali. Per queste la fonte autorevole = contenuti confermati e tracciabili. Ciò che non è confermato è **da verificare**, non da inventare.

---

## E. Template prompt per task di codice (riutilizzabile)

```
## SCOPE (path autorizzati alla modifica — tutto il resto è read-only)
- src/<modulo>/*
- tests/<modulo>/*

## DIAGNOSI PROMPT (FASE -1)
- Obiettivo, dati/file di riferimento, vincoli, rischio, output atteso presenti?
- Se manca un elemento bloccante → fermati e chiedi. Altrimenti dichiara le assunzioni.
- Semaforo AL PROMPT: verde / giallo (procedo con assunzioni) / rosso (chiedo chiarimenti).

## OBIETTIVO
<descrizione concreta del risultato atteso>

## VINCOLI NON-NEGOZIABILI
0. Non andare in loop: se non sai cosa stai facendo, fermati e chiedi (Regola 0).
1. Solo file nello scope (Regola 5).
2. Nessun path assoluto nei file (Regola 2).
3. Input validato con schema prima della business logic (Regola 10).
4. Nessun silenziamento di warning (Regola 4).
5. Valori monetari in interi/centesimi (Regola 9).
6. In assenza di dato certo → handoff umano, mai valore inventato (Source of Truth).
7. Fonti = codice reale, test, schema, doc nella versione in uso. Leggi prima di assumere.

## WORKFLOW
1. Dichiara in chat la tua pianificazione.
2. Scrivi prima i test (happy path + edge case + errori).
3. Implementa il codice minimo.
4. Esegui la pipeline di verifica del progetto (lint + compile/type + test + build).
5. Incolla l'ULTIMA RIGA REALE di output di ciascun comando.
6. Redigi a fine lavoro un walkthrough, solo nel percorso autorizzato, con sintesi
   operativa, file modificati, RED/GREEN, verifiche reali e rischi residui.

## OUTPUT ATTESO
- Differenziale delle modifiche.
- Ultima riga di output reale dei comandi di verifica.
- Path relativo del walkthrough finale.
- Semaforo finale DELLA RISPOSTA (verde / giallo-forma / giallo-sostanza / rosso) + registro punti aperti.
- Dichiarazione esplicita di aver rispettato le regole (o segnalazione di dove ha dovuto deviare).
```

---

## F. Perché questo protocollo funziona (lezioni estraibili)

| Problema ricorrente | Regola che lo previene |
|---|---|
| Agent che cicla a vuoto bruciando token | Regola 0 (no loop, soglia di stop, chiedi) |
| Agent che crea file ovunque → lavoro non riproducibile | Regola 1 (file solo nel repo) |
| Path assoluti che rompono il porting | Regola 2 (solo path relativi) |
| "Fatto!" senza aver verificato | Regola 3 (verifica binaria + ultima riga reale) |
| Warning nascosti sotto tappeto | Regola 4 (no silenziamento) |
| Agent che riscrive mezzo repo | Regola 5 (scope esplicito) |
| Traduzioni non revisionate in produzione | Regola 7 (revisione umana) |
| Secret nel codice | Regola 8 (loader centralizzato + cifratura) |
| Stati incoerenti / centesimi persi | Regola 9 (interi + edge case) |
| Input malformato che propaga | Regola 10 (schema prima della logica) |
| Dipendenze/architettura introdotte di nascosto | Regola 11 (dichiara prima) |
| Allucinazione su dati critici | Source of Truth (HITL, non improvvisare) |

---

## G. Protocollo di controllo prompt (29 controlli in 5 fasi)

> Governa *come si ragiona* prima e dopo il codice. **Rigore sempre massimo: si comprime l'esposizione, mai il controllo. Prima si valida il prompt, poi la risposta.**

### Principi non negoziabili (oltre alle 11 regole)
- **Due semafori distinti.** Il semaforo del *prompt* (qualità della domanda) e quello della *risposta* (solidità del lavoro consegnato) sono oggetti diversi. Non confonderli.
- **I paletti vincono sempre.** Un vincolo morale/strategico fissato a priori non si bilancia coi rischi e non è soggetto al verdetto. Se la soluzione richiede di violarlo → fermati e segnala.
- **Non inventare mai.** L'assenza di prova/dato è informazione utile da dichiarare (`dato non disponibile`), non un buco da coprire con frasi eleganti.

### FASE -1 — Diagnosi del prompt
Verifica che il task contenga: **obiettivo · scope/path · dati e file di riferimento · vincoli · livello di rischio · output atteso (incl. comandi di verifica)**. Manca un elemento *non decisivo* → procedi dichiarando l'assunzione. Manca un elemento *bloccante* → **fermati e chiedi** max 3–5 domande ordinate (bloccanti · utili · opzionali). Chiudi con un **semaforo AL PROMPT**: 🟢 sufficiente · 🟡 procedo con assunzioni dichiarate · 🔴 chiedo chiarimenti.

### FASE 0 — A monte
Riformula in una riga *cosa è chiesto davvero e cosa è escluso dallo scope*. Identifica **ruolo, destinatario e uso finale** dell'output e il **giudice esterno** (reviewer, CI, te-stesso-fra-sei-mesi, audit di sicurezza). Mappa i dati: file forniti · comportamento dichiarato dall'utente · contratti/API esterni · valori calcolati — segnalando subito le mancanze che condizionano la soluzione.

### FASE 1 — Fonti (per il codice: contratti, non opinioni)
Base decisiva = **codice reale della repo, test esistenti, schema DB/entità, contratti API e documentazione ufficiale delle librerie nella versione in uso**. Mai assumere firme di metodi, nomi di colonne o comportamenti: **leggi il file prima**. Verifica **vigenza** (versione corrente della dipendenza, API non deprecata). Quando due fonti divergono (doc vs codice), **prevale il codice reale** e si dichiara la divergenza.

### FASE 2 — Ragionamento
- **Tassonomia epistemica** su ogni affermazione portante: `📌 FATTO` (verificato nel codice/output) · `🔎 INFERENZA` · `⚠️ RISCHIO` · `📋 RACCOMANDAZIONE` · `❓ ASSUNZIONE`. Mai spacciare un'inferenza per fatto.
- **Hegel potenziato**: Tesi (la soluzione) → Antitesi (prima *steelman*, poi prova a romperla: edge case non coperti, race condition, regressione, fuga di dati cross-tenant) → Sintesi (un vincitore per asse, nomina l'errore del perdente, azione concreta). Se l'antitesi non attacca davvero, rilanciala più aggressiva.
- **Dimostrazione per assurdo** sui nodi decisivi: assumi che il test passi *per costruzione* e non perché la logica è corretta — cerca il dato che lo smentirebbe (test mordente/anti-masking).
- **Distingui dimostrato da sperato** e usa il **base-rate**: "in cambi simili, cosa rompe di solito?".
- **Prova vincolante, non promessa**: una conclusione è 🟢 solo se chiusa da **output reale di test/build verde, misura, o contratto verificato** — mai da "dovrebbe funzionare".

### FASE 3 — Output
- **Prova del 9 + plausibilità**: numeri, conteggi test, delta di copertura, dipendenze. Ogni conclusione discende dai dati reali? Ordine di grandezza sensato?
- **Completezza**: rileggi il quesito riformulato e spunta voce per voce — nessuna parte dimenticata, nessun punto aperto senza owner.
- **Retrospettiva + pre-mortem**: immagina il diff contestato dal reviewer; "se fra un mese scopro che era sbagliato, i 3 motivi più probabili?" → trasformali in avvisi/limiti/punti aperti.
- **Serve un abilitato?** Segnala quando serve revisione umana prima di un'azione irreversibile (migrazione DB distruttiva, cambio di sicurezza, release).
- **Registro punti aperti**: ogni punto non chiuso = riga `cosa manca · quale prova serve · chi · entro quando · effetto sul semaforo`.
- **Semaforo finale DELLA RISPOSTA**: 🟢 usabile (provato da output reale) · 🟡-forma (soluzione pronta, manca solo l'apposizione della prova: il run finale) · 🟡-sostanza (plausibile ma oggi è obiettivo futuro) · 🔴 non dimostrato/contraddittorio/bloccante.

### Matrice fonte e prova (adattata al codice)
| Tipo | Forza | Attenzione |
|---|---|---|
| Codice reale della repo | Alta | È la base decisiva: leggilo, non assumerlo. |
| Test esistente verde (output reale) | Alta | Chiude rischi di fatto, non di intenzione. |
| Schema DB / entità / migrazione | Alta | Verifica nomi colonna e vincoli effettivi. |
| Doc ufficiale libreria (versione in uso) | Medio-alta | Verifica la **versione**; può divergere dal codice. |
| Issue/blog/forum | Bassa | Mai base decisiva; solo spunto da verificare in repo. |
| "Dovrebbe funzionare" / promessa | Nulla | Mai 🟢. Serve il run reale. |

---

## H. Blocco pronto da incollare (attivazione protocollo forte)

```text
Applica il Protocollo Coding in modalità forte. Rigore massimo: comprimi
l'esposizione, mai il controllo. Prima valida il prompt, poi la risposta.
Regola 0: non andare in loop sprecando token — se non sai cosa stai facendo,
fermati e chiedi. I paletti non negoziabili vincono sempre.

FASE -1 — Diagnosi prompt: obiettivo, scope/path, dati, vincoli, rischio, output
atteso. Ambiguità che cambia la conclusione → max 3-5 domande. Semaforo AL PROMPT.
FASE 0 — Riformula quesito e perimetro escluso. Ruolo, destinatario, giudice esterno.
FASE 1 — Fonti = codice reale, test, schema, doc nella versione in uso. Leggi prima
di assumere. Verifica vigenza. Non inventare: se manca un dato, dichiaralo.
FASE 2 — Etichetta FATTO/INFERENZA/RISCHIO/RACCOMANDAZIONE/ASSUNZIONE. Hegel con
steelman. Assurdo sui nodi decisivi. Dimostrato vs sperato. Base-rate. Prova
vincolante = output reale; senza prova, mai verde.
FASE 3 — Prova del 9 e plausibilità su numeri/conteggi test. Completezza.
Retrospettiva e pre-mortem. Registro punti aperti. Semaforo forte DELLA RISPOSTA:
verde / giallo-forma / giallo-sostanza / rosso.
```
