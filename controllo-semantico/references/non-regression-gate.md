# Gate di Non Regressione (NR)

## Principio

Applicare questo gate a ogni operazione che modifica uno stato esistente: codice,
configurazioni, documenti, dati, workflow, Drive, Wiki, repository, skill o altri
artefatti. Il gate e trasversale ai 29 controlli: non li sostituisce e non diventa
il controllo n. 30.

Regola madre:

> Aggiungere non significa sostituire. Migliorare non significa cancellare. Ogni
> funzionalita, contenuto o comportamento preesistente resta requisito di
> compatibilita finche la sua rimozione o variazione incompatibile non e stata
> esplicitamente autorizzata nello scope corrente.

Una modifica apparentemente corretta non e promuovibile se introduce una
regressione non autorizzata.

## Quando scatta

Eseguire NR prima della chiusura quando l'azione include almeno una di queste
operazioni:

- creare o aggiornare una versione di un artefatto esistente;
- modificare, riscrivere, sostituire, rinominare, spostare o cancellare;
- migrare dati, schema, configurazione o formato;
- fare merge, promozione, pubblicazione, deploy o sincronizzazione;
- aggiornare Drive, Wiki, inventari, manifest o fonti canoniche;
- aggiornare questa skill o una sua dipendenza.

Usare `N/A` solo quando non e avvenuta alcuna mutazione oppure l'output e una
nuova entita indipendente che non sostituisce, sovrascrive o altera nulla di
preesistente. Motivare comunque `N/A`.

## Stato NR

- **VERDE**: baseline osservata, scope autorizzato identificato, prove prima/dopo
  sufficienti, test pertinenti superati e nessuna regressione non autorizzata.
- **GIALLO**: nessuna regressione osservata ma la baseline o i test non coprono
  abbastanza da provarne l'assenza. Per una modifica funzionale, il semaforo
  risposta non puo essere VERDE.
- **ROSSO**: funzionalita, contenuto, comportamento, dato o collegamento
  preesistente e stato perso, degradato o reso incompatibile senza autorizzazione,
  oppure un test di regressione e fallito.
- **N/A**: nessuna mutazione soggetta al gate.

Un NR ROSSO blocca `APPROVED`, `PUBLISHED`, `PROMOTED`, merge, deploy o altra
chiusura equivalente. Un NR GIALLO consente al massimo uno stato condizionato o
bozza quando la non regressione e requisito sostanziale.

## Workflow obbligatorio

### 1. Acquisire la baseline

Prima della prima modifica:

1. identificare oggetto, versione, revisione, commit, ID o hash correnti;
2. leggere lo stato corrente dalla fonte canonica;
3. inventariare funzionalita, contenuti, interfacce, collegamenti e vincoli
   pertinenti allo scope;
4. identificare i test gia esistenti e gli esempi di comportamento noti;
5. distinguere esplicitamente:
   - **DEVE CAMBIARE**;
   - **PUO CAMBIARE**;
   - **NON DEVE CAMBIARE**;
6. registrare le eventuali rimozioni o breaking change autorizzate.

Se la baseline non e leggibile e la modifica puo sovrascrivere o perdere
funzionalita, non procedere alla cieca: NR e almeno GIALLO e puo diventare ROSSO
se la baseline e indispensabile per operare in sicurezza.

### 2. Definire il contratto di compatibilita

Trasformare la baseline in una lista verificabile di invarianti. Esempi:

- endpoint e comandi esistenti ancora disponibili;
- campi, sezioni o allegati non interessati ancora presenti;
- ID e link Drive ancora validi;
- workflow precedenti ancora percorribili;
- output invariati per gli input che non appartengono alla nuova modifica;
- permessi, audit e tracciabilita non ridotti;
- risorse della skill e trigger preesistenti ancora disponibili.

Non usare la sola assenza di errori come prova di compatibilita.

### 3. Modificare con scope minimo

- Toccare solo file, campi, record e risorse necessari.
- Non cancellare o rinominare elementi fuori scope.
- Non interpretare una richiesta di aggiunta come autorizzazione a sostituire.
- Conservare originali, storia e riferimenti quando il dominio lo richiede.
- Se emerge la necessita di una breaking change non prevista, fermare la
  promozione e ottenere autorizzazione esplicita prima di considerarla parte
  dello scope.

### 4. Eseguire il confronto prima/dopo

Confrontare almeno:

1. inventario delle risorse;
2. funzionalita e comportamenti osservabili;
3. dati e metadati pertinenti;
4. interfacce e contratti esterni;
5. autorizzazioni, workflow e collegamenti;
6. output dei test o casi rappresentativi.

Il diff testuale e una prova utile ma non sufficiente: una regressione puo
esistere anche quando nessun file e stato cancellato.

### 5. Eseguire i test di non regressione

La chiusura richiede tre famiglie di prove:

- **NUOVO**: la nuova capacita o correzione funziona;
- **PREESISTENTE**: i comportamenti della baseline continuano a funzionare;
- **INTEGRITA**: non sono scomparsi contenuti, dati, risorse, link o garanzie
  non autorizzati.

Usare test gia esistenti quando disponibili. Se mancano, costruire smoke test o
casi rappresentativi dalla baseline osservata e dichiararne la copertura.

### 6. Classificare ogni differenza

Per ogni differenza materiale indicare una classe:

- `INTENDED`: richiesta o autorizzata esplicitamente;
- `COMPATIBLE`: cambiamento interno senza perdita osservabile;
- `ADDITION`: nuova capacita che non sostituisce il preesistente;
- `REGRESSION`: perdita o degradazione non autorizzata;
- `UNKNOWN`: effetto non provato.

`REGRESSION` produce NR ROSSO. `UNKNOWN` su un comportamento critico impedisce
NR VERDE.

### 7. Gate prima della promozione

Prima di dichiarare successo o promuovere:

- rileggere la versione finale effettivamente salvata o distribuita;
- verificare che i test si riferiscano a quella stessa versione;
- registrare baseline, versione finale, test, differenze autorizzate e stato NR;
- non confondere build verde con non regressione: servono prove riferite alla
  baseline.

## Regole per dominio

### Software e codice

Verificare almeno, quando pertinenti:

- test esistenti + nuovi test;
- build e lint;
- API, CLI, eventi e payload esistenti;
- migrazioni e compatibilita dati;
- permessi e sicurezza;
- configurazioni e feature flag;
- comportamento su casi precedentemente funzionanti;
- dipendenze e versioni;
- diff di file e risorse per intercettare rimozioni inattese.

Il successo del nuovo test non compensa il fallimento di un vecchio test.

### Documenti e artefatti testuali

Verificare almeno:

- sezioni, clausole, tabelle, note e allegati preesistenti;
- riferimenti incrociati, numerazione, fonti e metadati;
- contenuti fuori scope invariati semanticamente;
- formattazione o struttura quando hanno valore operativo.

Una riscrittura piu breve che omette un requisito e una regressione se
l'omissione non era autorizzata.

### Drive, Wiki e conoscenza

Applicare read-before-write e readback. Verificare:

- file/record precedenti ancora presenti salvo rimozione autorizzata;
- ID, link, cartelle e relazioni ancora validi;
- contenuto canonico pertinente preservato;
- nessuna duplicazione o sostituzione silenziosa;
- inventari, MOC e riferimenti aggiornati senza perdita di voci non coinvolte.

### Workflow e configurazioni

Eseguire almeno un percorso preesistente rappresentativo oltre al nuovo
percorso. Verificare ruoli, permessi, stati, transizioni, notifiche, retry,
audit e fallback pertinenti.

### Aggiornamento della skill `controllo-semantico`

Ogni nuova versione della skill deve essere verificata contro la versione
precedente prima del packaging. Preservare salvo autorizzazione esplicita:

- trigger e modalita `COMPLETA`, `SOLO-ANALISI`, `LOCALE`, `DOSSIER`;
- tutti i 29 controlli e S1-S5;
- tesi/antitesi/sintesi, falsificazione e guardrail quantitativi;
- semafori, note Markdown, builder, validatore e hash;
- persistenza Drive, readback e Wiki;
- governance multi-AI e workflow Drive/GitHub;
- template, script, riferimenti e metadata dell'agente;
- protezioni su segreti, duplicati, versioni e fonti canoniche.

Usare `scripts/non_regression_guard.py` per il confronto strutturale della
cartella quando una baseline locale e disponibile. Il suo PASS prova soltanto
l'assenza delle regressioni strutturali che controlla; non sostituisce i test
funzionali o semantici.

## Breaking change autorizzata

Una rimozione o incompatibilita puo essere classificata `INTENDED` solo se:

1. e descritta esplicitamente nella richiesta o in una decisione approvata;
2. sono identificati gli elementi che possono essere rimossi o resi
   incompatibili;
3. tutto cio che resta fuori da tale elenco continua a essere protetto dal gate;
4. impatto e, quando necessario, migrazione o rollback sono documentati.

Non inferire mai una breaking change dal solo fatto che semplificherebbe il
lavoro.

## Evidenze minime da registrare

Per una mutazione riportare almeno:

- baseline osservata;
- versione finale osservata;
- scope autorizzato;
- invarianti di compatibilita;
- test NUOVO / PREESISTENTE / INTEGRITA;
- differenze `INTENDED`, `COMPATIBLE`, `ADDITION`, `REGRESSION`, `UNKNOWN`;
- stato NR con motivazione;
- prova mancante per il livello superiore, se non VERDE.

Per output strutturati usare `assets/templates/12_non_regressione.md`.
