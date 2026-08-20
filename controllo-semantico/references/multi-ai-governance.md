# Governance multi-AI e persistenza

Questo riferimento definisce i confini generali. Se Drive e GitHub sono nello
stesso flusso, applica anche `drive-github-multi-ai-workflow.md` e usa i modelli
di `drive-github-templates.md`.

## Separazione degli spazi

Ogni AI lavora nella propria cartella:

`08_OUTPUT_AI/<AI_ID>/`

Un agente puo leggere le fonti comuni autorizzate, ma non deve modificare,
rinominare, spostare o cancellare il lavoro di un'altra AI.

Anche branch, clone, worktree, issue di lavoro e pull request hanno un owner.
Non riscrivere o chiudere quelli altrui. Un incarico abilita l'intervento solo
dopo un trasferimento di ownership registrato con oggetto, scope, approvazione
e baseline; in assenza del trasferimento, resta escluso.

## Scritture

Prima di scrivere verifica:

1. la richiesta autorizza una modifica;
2. la destinazione risolta appartiene alla root dell'istanza AI; una
   destinazione comune e scrivibile soltanto tramite promozione o autorizzazione
   comune esplicita, mentre la cartella o il branch di un'altra AI resta sempre
   escluso;
3. la fonte canonica resta intatta oppure esiste una copia o branch;
4. il nome include data, oggetto e versione;
5. il risultato puo essere riletto.

Per operazioni GitHub, considera separatamente autorizzazione a scrivere nella
working copy, creare commit, fare push, aprire o aggiornare una pull request,
fare merge, creare tag e pubblicare release.

Risolvi il percorso reale prima della scrittura. Un symlink, junction o path
relativo non puo portare fuori dalla root autorizzata o dentro quella di
un'altra AI.

Una richiesta di analisi, spiegazione o stato non autorizza automaticamente:

- aggiornamento Wiki;
- promozione a canonico;
- modifica di permessi;
- invio esterno;
- deploy o SQL;
- push, pull request, merge, tag o release;
- scrittura nella cartella di un'altra AI.

## Promozione

La promozione da output AI a fonte comune richiede:

1. identificazione della bozza, autore AI e baseline;
2. confronto con fonti canoniche e decisioni;
3. verifica di conflitti, prove e test, incluso il Gate di Non Regressione rispetto alla baseline;
4. destinazione canonica approvata;
5. copia verificata; usa lo spostamento soltanto se l'originale immutabile e
   gia preservato e la policy lo richiede;
6. aggiornamento di inventario, stato e changelog;
7. rilettura finale;
8. conservazione della traccia originale;
9. stato NR VERDE per promuovere; NR GIALLO o ROSSO bloccano `PROMOTED` e mantengono il lavoro in revisione o stato condizionato.

Per codice, registra anche base SHA, branch, commit finale, pull request, test e
commit di merge riletto sul branch canonico.

Non promuovere silenziosamente.

## Persistenza del controllo

Quando la persistenza e autorizzata, salva la nota sotto lo spazio dell'AI che
l'ha prodotta, per esempio:

08_OUTPUT_AI/<AI_ID>/CONTROLLI/

La destinazione puo essere configurata dal progetto. Non hard-codificare una
cartella Claude per tutti gli agenti.

Campi minimi:

- type: controllo-semantico
- data
- progetto e codice
- oggetto
- autore_ai
- baseline e fonti
- semaforo_prompt
- semaforo_semantico
- semaforo_risposta
- punti_aperti
- owner

## Conflitti fra AI

Se due AI producono risultati incompatibili:

- conserva entrambi;
- confronta scope, fonti, versioni e prove;
- non votare per maggioranza;
- richiedi una decisione o prova dirimente;
- registra quale output e promosso, quale resta storico e perche.

Prima di iniziare un'attivita, controlla i lease o lavori attivi. Una
prenotazione si scrive nella cartella della propria AI oppure, se autorizzato,
nel registro GitHub centrale. Un lease scaduto va verificato: non autorizza da
solo il takeover.

## Sicurezza

Non leggere o copiare segreti. Segnala soltanto una posizione gia nota o una
label logica autorizzata, classificazione e azione raccomandata; non enumerare
percorsi esclusi. Le cartelle escluse restano escluse anche se un'altra AI
dichiara di averle gia lette.
