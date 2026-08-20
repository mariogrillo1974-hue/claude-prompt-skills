# Workflow Drive/GitHub per progetti multi-AI

## Scopo

Usa questo riferimento quando piu AI lavorano sullo stesso progetto e Drive e
GitHub partecipano alla catena di lavoro. L'obiettivo e evitare tre errori:

- due AI modificano lo stesso artefatto senza saperlo;
- una copia sincronizzata viene scambiata per fonte canonica;
- una bozza diventa verita di progetto senza approvazione e prova.

## Matrice di autorita

Assegna una sola fonte canonica a ogni tipo di informazione.

| Oggetto | Fonte canonica predefinita | Copia secondaria |
|---|---|---|
| obiettivi, vincoli, fonti, decisioni, approvazioni | Drive progetto | riferimenti in issue o PR |
| codice e cronologia tecnica | repository GitHub | snapshot Drive identificato da commit |
| stato di una modifica software | branch, commit e pull request | handoff Drive dell'AI |
| analisi e bozze di una AI | `08_OUTPUT_AI/<AI>` | link nella PR, se autorizzato |
| release software | tag/release GitHub | verbale e manifest Drive |

Questa matrice e una regola predefinita. Se il progetto dichiara una matrice
diversa, usa quella. Non mantenere due
copie entrambe dichiarate canoniche: crea split-brain e rende indimostrabile lo
stato corrente.

## Struttura Drive consigliata

Mantieni la struttura esistente del progetto. Quando e autorizzata la cartella
GitHub in Drive, usa:

```text
Drive/
|-- 00_PROGETTO/
|   |-- README_PROGETTO
|   |-- AGENTS
|   |-- STATO_PROGETTO
|   |-- FONTI_CANONICHE
|   `-- INVENTARIO
|-- 07_HANDOFF/
|-- 08_OUTPUT_AI/
|   |-- <AI_ID_A>/
|   |-- <AI_ID_B>/
|   `-- <AI_ID_N>/
`-- GITHUB/
    `-- <CODICE_PROGETTO>/
        |-- MANIFEST_REPOSITORY.md
        |-- STATO_GITHUB.md
        |-- RELEASE_E_SNAPSHOT/
        `-- HANDOFF_INDEX.md
```

`Drive/GITHUB/<CODICE_PROGETTO>` e una cabina di controllo. Non e, per
impostazione predefinita, una working copy Git condivisa. I client di
sincronizzazione possono osservare file interni di `.git` in momenti diversi,
duplicare conflitti o propagare lock transitori. Per lavoro multi-AI usa copie
locali separate fuori dalla cartella sincronizzata. `HANDOFF_INDEX.md` e una
vista comune read-only per le AI: soltanto il coordinatore o una promozione
autorizzata puo aggiornarla. Ogni AI salva l'handoff reale in
`08_OUTPUT_AI/<AI_ID>/HANDOFF/`.

Se l'utente impone un repository attivo dentro Drive, dichiara il rischio,
richiedi un solo writer alla volta e non promettere isolamento multi-AI.

## Identita e stati

Usa identificatori stabili:

- progetto: codice immutabile, indipendente dal nome leggibile;
- lavoro: UUID/ULID o ID issue collision-resistant;
- artefatto: UUID/ULID o ID assegnato dal registro;
- istanza: `agent_instance_id`, distinto da `owner_ai`;
- branch: `ai/<agent-instance-id>/<work-id>-<slug>`;
- commit di base: SHA completo osservato;
- versione Drive: ID/revisione o hash del file letto.

Usa timestamp ISO-8601 in UTC. Nei lease registra anche revisione o epoch per
riconoscere aggiornamenti concorrenti.

Stati ammessi per gli artefatti:

`DRAFT -> IN_REVIEW -> APPROVED -> PROMOTED -> ARCHIVED`

`REJECTED` e uno stato terminale conservato, non una cancellazione. Non saltare
da DRAFT a PROMOTED senza gate esplicito.

## Preflight di sessione

Prima di modificare qualsiasi cosa:

1. identifica root e codice progetto;
2. leggi README, AGENTS, stato, fonti canoniche e inventario;
3. leggi decisioni e handoff pertinenti piu recenti;
4. escludi cartelle segreti e percorsi vietati;
5. identifica repository, remote, branch principale e commit canonico;
6. verifica che la working copy appartenga all'AI corrente;
   risolvi symlink e junction e verifica containment nella root autorizzata;
7. confronta il commit locale con il commit di base atteso;
8. scandisci le dichiarazioni di lavoro attive delle altre AI;
9. registra scope logico, risorse, path normalizzati, case e glob previsti e
   prove di completamento;
10. scegli quali scritture sono autorizzate: locale, Drive comune, push, PR,
    merge, tag o release sono permessi distinti;
11. se e prevista una mutazione, acquisisci la baseline di non regressione e il
    contratto di compatibilita secondo `non-regression-gate.md` prima della
    prima modifica.

Se identita progetto, baseline o scope sono ambigui e l'errore potrebbe
sovrascrivere lavoro, il semaforo prompt e ROSSO.

## Prenotazione senza collisioni

Una cartella comune Markdown non e un lock atomico. Usa uno dei due modelli:

### Modello A - GitHub autorizzato

Usa una issue o un record equivalente come registro centrale. Inserisci work
ID, owner AI, agent instance, scope logico, path normalizzati, base SHA, branch,
stato, heartbeat, revisione e scadenza. Prima di partire cerca sovrapposizioni
aperte.

### Modello B - solo Drive o nessuna scrittura esterna

Ogni AI crea la dichiarazione soltanto nella propria cartella:

`08_OUTPUT_AI/<AI>/LAVORI_ATTIVI/<WORK_ID>.md`

Le altre AI leggono tutte le dichiarazioni, ma non le modificano. Un eventuale
registro comune e una vista derivata aggiornata soltanto dal coordinatore
autorizzato.

Una prenotazione e un lease cooperativo, non una prova di proprieta. Se due
lease si sovrappongono:

- sospendi le modifiche nello scope comune;
- proponi una divisione per file o componente verificabile;
- altrimenti richiedi una decisione del coordinatore;
- conserva entrambe le dichiarazioni.

### Attivazione in due fasi

La sequenza `scansione -> creazione` non e atomica: due AI potrebbero non
vedersi e partire insieme. Riduci questa finestra cosi:

1. crea il lease in stato `PLANNED` con ID, scope, file e base SHA;
2. rileggi il proprio lease, inclusa revisione osservata, per verificarne la
   persistenza;
3. ripeti la scansione di tutti i lease e del registro GitHub autorizzato;
   confronta anche risorse logiche e path dopo normalizzazione di separatori,
   case, glob, symlink e junction;
4. se emerge una sovrapposizione, passa a `BLOCKED_CONFLICT` e non scrivere
   nello scope comune;
5. se non emerge conflitto, passa ad `ACTIVE` e rileggi lo stato;
6. immediatamente prima della prima modifica, esegui un ultimo controllo dello
   scope concorrente.

Questo protocollo riduce ma non elimina la race. Se il progetto richiede
esclusione forte, usa un coordinatore o un sistema di lock atomico esterno
autorizzato; non descrivere un file Drive come mutex affidabile.

Se Drive non offre una vista centrale fresca o un readback di revisione, il
lease e soltanto advisory: non consentire lavori paralleli su scope
sovrapposti.

Mantieni un heartbeat periodico con revisione e scadenza. Per aggiungere file,
glob o risorse logiche fuori dallo scope ACTIVE, non iniziare a modificarli:
riporta il lease a `PLANNED`, aggiorna scope e revisione, esegui readback e
nuova scansione, quindi torna ad `ACTIVE` soltanto senza conflitti.

Un lease scaduto non autorizza automaticamente il takeover. Controlla ultimo
heartbeat, branch, commit, PR e handoff. Marca `STALE_DA_VERIFICARE` e assegna
il takeover solo con evidenza o approvazione.

## Isolamento Git per AI

Ogni istanza AI usa di default una clone e un branch propri. Una clone separa
index, config, reflog e operazioni repo-wide. Un worktree condivide `.git` e non
equivale a isolamento: usalo soltanto se un owner coordinatore controlla il
repository comune e vieta fetch/prune/config/gc/rebase/reset o altre operazioni
che possono toccare il lavoro altrui. Prima di scrivere registra `git status`,
repository ID/URL, remote effettivo, branch e base SHA. Non modificare, forzare,
cancellare o riscrivere il branch di un'altra AI.

Regole predefinite:

- niente commit direttamente sul branch principale;
- niente force-push su branch condivisi;
- niente credenziali o segreti nel repository, output o log;
- commit piccoli e riferiti al work ID;
- test registrati con comando, ambiente ed esito;
- file non correlati lasciati intatti;
- conflitti risolti confrontando intenti e prove, non scegliendo l'ultima copia.

Creare un branch locale e scrivere nella propria working copy non autorizza il
push. Push, apertura PR, commenti, merge, tag e release sono operazioni esterne
distinte e richiedono l'autorita prevista dalla sessione e dal progetto.

Registra i permessi come matrice: local write, commit, Drive common, push, PR,
commenti, merge, tag e release. Per ogni voce conserva `granted_by`, evidenza,
scope e scadenza. Un'approvazione PR non concede implicitamente autorita di
merge.

## Handoff

Per un'attivita articolata crea un handoff in
`08_OUTPUT_AI/<AI_ID>/HANDOFF/`. Includi:

- progetto, work ID, autore AI e data;
- obiettivo, incluso ed escluso;
- baseline Drive e SHA Git iniziale;
- branch e commit finali;
- file modificati e motivazione;
- fonti, comandi di test, risultati e limiti;
- decisioni prese e alternative scartate;
- operazioni esterne eseguite o non autorizzate;
- punti aperti, owner e prossimo passo;
- hash degli artefatti consegnati.

Un handoff non e una promozione. E una descrizione verificabile del lavoro.

## Gate di promozione

La promozione del codice avviene tramite pull request o gate equivalente:

1. identifica bozza, autore, work ID, base SHA e branch;
2. verifica che il branch non includa modifiche estranee;
3. confronta con fonti, specifiche e decisioni Drive correnti;
4. esegui build, test e controlli richiesti nello stesso ambiente dichiarato;
   includi test di non regressione sulla baseline (NUOVO, PREESISTENTE,
   INTEGRITA) secondo `non-regression-gate.md`;
5. risolvi conflitti e review senza cancellare la traccia delle alternative;
6. verifica `NON REGRESSIONE`: solo VERDE consente `PROMOTED`; ROSSO blocca
   la promozione e GIALLO mantiene il lavoro in revisione o stato condizionato;
7. ottieni l'approvazione richiesta;
8. registra repository ID/URL, PR head SHA, metodo di merge atteso e check
   riferiti allo SHA realmente testato; esegui il merge soltanto se autorizzato;
9. rileggi su GitHub metodo osservato, commit risultante, presenza del commit
   risultante sul branch principale, equivalenza della modifica sorgente,
   check e stato PR; gestisci correttamente merge, squash o rebase senza
   pretendere che l'head SHA originale appaia su main;
10. aggiorna manifest, stato e inventario Drive soltanto se autorizzato;
11. rileggi file ID, revisione e hash Drive e conserva l'output AI originale.

Lo stato iniziale della promozione e `PENDING`. Diventa `PROMOTED` soltanto
quando expected e observed coincidono in tutti i sistemi nello scope. Se un
merge GitHub riesce ma il readback Drive fallisce, o viceversa, registra
`PARTIAL`, non ripetere alla cieca l'operazione gia riuscita e apri un piano di
riconciliazione.

Un merge verificato puo rendere VERDE la persistenza del codice, ma non prova
da solo il funzionamento in produzione. Un aggiornamento Drive verificato non
prova da solo che il commit sia sul branch principale.

## Conflitti fra output

Quando due AI propongono soluzioni incompatibili:

1. conserva entrambi gli output e i rispettivi branch;
2. allinea scope, baseline, versioni e ambiente;
3. costruisci il registro claim-prova per ciascuna soluzione;
4. esegui test discriminanti o richiedi la decisione mancante;
5. registra la soluzione promossa e il motivo;
6. archivia, non cancellare, la soluzione non scelta.

Non usare maggioranza, anzianita del file o timestamp piu recente come prova di
correttezza.

## Errori, duplicati e recupero

Se una lettura, scrittura, sincronizzazione o operazione GitHub fallisce:

- registra operazione, target osservato, errore e stato parziale;
- non dichiarare creato, inviato, unito o aggiornato cio che non e stato
  riletto;
- non sovrascrivere un duplicato finche contenuto, autore, baseline e hash non
  sono confrontati;
- proponi una recovery reversibile;
- aggiorna il semaforo soltanto per i claim dipendenti.

Se Drive e GitHub divergono, applica prima la matrice canonica approvata del
progetto. In assenza di una regola diversa, GitHub prevale per codice e commit e
Drive per decisioni e fonti di progetto. Segnala comunque la divergenza e
blocca una promozione che richiede entrambi allineati.

## Segreti e attraversamento del perimetro

- non leggere, enumerare o indicizzare percorsi esclusi;
- non riportare valori segreti in prompt, output, log, commit, PR o handoff;
- redigi i dati sensibili gia presenti negli output prima di conservarli;
- usa uno scanner redatto sul codice autorizzato per controllare il diff staged
  senza stamparne il valore e senza aprire cartelle escluse;
- risolvi symlink e junction prima di leggere o scrivere;
- blocca ogni percorso risolto fuori dalla root autorizzata.

Se un segreto risulta gia staged, interrompi commit e push, segnala il file e
il tipo di rischio con granularita minima e chiedi una procedura di bonifica.

## Criterio di chiusura

Chiudi il lavoro soltanto quando:

- lo scope prenotato e riconciliato con i file realmente modificati;
- l'output e nella cartella, clone e branch dell'istanza AI corretti;
- test e readback sono registrati;
- il Gate di Non Regressione e VERDE oppure, se GIALLO, la chiusura e esplicitamente condizionata e non promossa come pienamente compatibile;
- il lease e chiuso o l'handoff spiega perche resta aperto;
- le operazioni non autorizzate sono esplicitamente indicate come non eseguite;
- nessun segreto, lavoro altrui o fonte canonica non autorizzata e stato
  modificato.
