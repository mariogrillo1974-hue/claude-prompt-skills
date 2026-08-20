# Prove, claim e semafori

## Principio

Il colore appartiene a un claim o a una decisione delimitata, non a un file in
astratto. Una prova vale soltanto per oggetto, versione, ambiente, data e scope
che dimostra.

## Registro claim-prova

Per i claim decisivi usa:

| ID | Claim | Stato epistemico | Prova | Scope | Data/versione | Limite | Colore |
|---|---|---|---|---|---|---|---|
| C-01 | ... | FATTO/INFERENZA/... | E-01 | ... | ... | ... | ... |

Ogni prova deve essere identificabile:

| Tipo | Esempi | Dimostra | Non dimostra automaticamente |
|---|---|---|---|
| Fonte ufficiale vigente | norma, bando, atto | testo e vigenza nel suo ambito | applicazione al caso senza interpretazione |
| Approvazione autentica | firma, verbale, decision record | decisione o consenso | correttezza tecnica dell'oggetto approvato |
| Misura o benchmark | dataset, rilievo, confronto | valore osservato nel campione | generalizzazione fuori campione |
| Esecuzione riproducibile | test, esperimento, build, query | esito nell'ambiente dichiarato | produzione o altri ambienti |
| Contratto applicabile | clausola firmata, penale | obbligo ed enforcement dichiarati | adempimento futuro |
| Readback o audit | rilettura, hash, log, ricevuta | persistenza o consegna osservata | effetto a valle non verificato |

Una dichiarazione di un'altra AI e una fonte secondaria finche non rimanda a
prove verificabili.

## Scope del VERDE

Un VERDE deve dichiarare almeno:

- oggetto;
- versione o identificatore;
- ambiente o contesto;
- data di osservazione o vigenza;
- prova diretta;
- esclusioni.

Esempio corretto: VERDE statico per applicabilita del diff allo snapshot X.
Esempio scorretto: VERDE, la patch funziona.

## Aggregazione

- Un pilastro critico ROSSO impedisce il VERDE della decisione che ne dipende.
- Un GIALLO-FORMA non diventa ROSSO se la sostanza e provata ma manca una
  consegna o approvazione formale.
- Un GIALLO-SOSTANZA non diventa VERDE grazie a forma, firma o integrita del
  pacchetto.
- Un claim indipendente puo restare VERDE anche se una consegna accessoria
  fallisce; dichiara la separazione.

## Gerarchia delle fonti

Non usare una gerarchia universale. Determina:

1. giurisdizione o dominio;
2. autorita emittente;
3. forza vincolante;
4. vigenza;
5. specificita rispetto al caso;
6. versione;
7. conflitti e regole di prevalenza.

Per software, il comportamento reale richiede coerenza fra sorgente, dipendenze,
configurazione, database e prove sullo stesso ambiente.

## Fallimenti

Se una lettura o verifica richiesta fallisce:

- nomina esattamente l'operazione fallita;
- non usare il dato atteso;
- crea un punto aperto;
- degrada soltanto i claim che dipendono da quel dato;
- non ripetere la stessa azione senza cambiare ipotesi o metodo.


## Gate di Non Regressione

Per ogni mutazione applicare `non-regression-gate.md` e registrare uno stato
separato dai tre semafori principali:

- `NR VERDE`: baseline e versione finale osservate, test NUOVO/PREESISTENTE/INTEGRITA sufficienti, nessuna regressione non autorizzata;
- `NR GIALLO`: nessuna regressione osservata ma copertura insufficiente per provarne l'assenza;
- `NR ROSSO`: regressione osservata, rimozione non autorizzata o test di regressione fallito;
- `NR N/A`: nessuna mutazione soggetta al gate, con motivazione.

Un NR ROSSO blocca la promozione e impedisce un VERDE globale. Un NR GIALLO su una modifica funzionale sostanziale limita il semaforo risposta al massimo a GIALLO-SOSTANZA. Una rimozione esplicitamente autorizzata non e regressione se e circoscritta e tutte le capacita fuori scope risultano preservate.

Il confronto strutturale, un diff o una build verde sono prove parziali: non dimostrano da soli la non regressione funzionale.

## Persistenza richiesta

Quando la modalita COMPLETA include Drive:

- persistenza riuscita e riletto: non altera un semaforo sostanziale gia corretto;
- analisi valida ma persistenza fallita: almeno GIALLO-FORMA;
- persistenza e criterio essenziale dichiarato dall'utente: fallimento = ROSSO del deliverable;
- upload non riletto: `UPLOAD-UNVERIFIED`, mai VERDE di persistenza.
