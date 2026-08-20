# Guardrail quantitativi

## Regola generale

Una formula non migliora una decisione se gli input non sono documentati,
calibrati e coerenti con il modello. In quel caso usa intervalli, scenari o
non calcolabile.

## E13 — stime di Fermi

Usa Fermi per delimitare un ordine di grandezza, non per creare una precisione
inesistente.

1. Definisci variabile, unita, periodo e popolazione.
2. Costruisci limite inferiore e superiore con assunzioni visibili.
3. Verifica che i limiti siano fisicamente e semanticamente comparabili.
4. Restituisci l'intervallo e le assunzioni.

La media geometrica e ammessa solo se:

- entrambi i limiti sono strettamente positivi;
- la scala e moltiplicativa o logaritmica;
- serve un valore centrale per uno scenario, non come dato osservato.

Se un limite e zero, negativo, monetariamente asimmetrico o su scala additiva,
non usare la radice del prodotto. Mantieni l'intervallo o usa scenari basso,
centrale e alto con metodo dichiarato.

## Kelly

Usa Kelly soltanto per dimensionare un'esposizione ripetibile con:

- probabilita p calibrata su base-rate pertinente;
- payoff b definito sullo stesso orizzonte;
- perdita massima identificata;
- possibilita reale di frazionare l'esposizione.

Se questi requisiti mancano, Kelly e N/A. Non sostituire p con una media
geometrica di limiti arbitrari. Un risultato negativo blocca quella esposizione
speculativa, non automaticamente l'intero progetto.

## E14 — coerenza globale

Mappa le dipendenze fra claim. Non calcolare il prodotto delle probabilita se:

- le probabilita non sono empiricamente calibrate;
- i nodi condividono fonti, dati o cause;
- la dipendenza non e modellata.

In questi casi applica il principio qualitativo dell'anello debole e indica il
pilastro limitante. Qualsiasi soglia, incluso 0,70, e solo una policy esplicita
del decisore; non e una costante universale.

## Minimax regret

Usa minimax quantitativo soltanto se alternative, stati e utilita sono
confrontabili. Altrimenti:

1. elenca alternative e stati;
2. ordina i rimpianti come basso, medio, alto;
3. mostra quale assunzione cambierebbe l'ordine;
4. non inventare una matrice numerica.

## E20 — interazione strategica

Non chiamare ogni rapporto un dilemma del prigioniero. E20 richiede:

- almeno due attori con scelte autonome;
- payoff o incentivi identificabili;
- possibilita reale di cooperazione e defezione;
- conseguenza materiale sulla decisione.

Se manca uno di questi elementi, usa una normale analisi degli incentivi.

## Output quantitativo minimo

Ogni numero stimato deve mostrare:

- fonte o metodo;
- unita e periodo;
- intervallo;
- dipendenze;
- sensibilita della conclusione;
- etichetta STIMA-FERMI o ASSUNZIONE quando pertinente.
