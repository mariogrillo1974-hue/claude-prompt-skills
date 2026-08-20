# Metodo dei 29 controlli

## Principio

Applicare tutti i controlli. Usare `N/A` solo con una motivazione che dimostri la non pertinenza.

## FASE -1 — Diagnosi del prompt

### 1 — Entita necessarie
Verificare soggetto, oggetto, obiettivo, destinatario, dati, vincoli, fonti, vigenza, alternative, formato e criterio di successo. Classificare ogni mancanza: bloccante, assumibile o opzionale.

### 2 — Classe della richiesta
Classificare: normativa, fiscale, amministrativa, tecnica, software, strategica, economica, comunicativa, ricerca o decisione operativa.

### 3 — Chiarimenti
Chiedere solo cio che puo cambiare materialmente conclusione o azione. Massimo 3-5 domande ordinate per impatto.

### 4 — Prompt operativo e angolo cieco
Ricostruire: devo valutare `[oggetto]` per `[finalita]`, usando `[dati]`, con `[vincoli]`, producendo `[output]`, distinguendo fatti, inferenze, rischi, raccomandazioni e assunzioni. Aggiungere un pre-mortem breve.

### 5 — Semaforo prompt
- VERDE: entita sufficienti.
- GIALLO: dati mancanti assumibili e dichiarati.
- ROSSO: manca un elemento che puo cambiare conclusione o azione.

## FASE -0.5 — Coerenza dei significati

- S1: un termine, un senso.
- S2: definizioni esplicite dei termini portanti.
- S3: nomi canonici, versioni e unita coerenti.
- S4: disambiguazione prima delle conclusioni.
- S5: tipo, unita, contesto e periodo per ogni dato portante.

Semaforo semantico:
- VERDE: termini decisivi univoci.
- GIALLO: ambiguita non decisiva dichiarata.
- ROSSO: ambiguita che cambia conclusione o azione.

## FASE 0 — Perimetro

### 6 — Quesito reale
Formulare cosa e incluso e cosa resta escluso.

### 7 — Dati e provenienza
Separare fornito, dichiarato, osservato, calcolato ed esterno; marcare verificato, inferito o non verificato.

### 8 — Ruolo, destinatario e uso
Identificare chi parla, chi usa l'output e per quale atto.

### 9 — Giudice, alternative e paletti
Identificare chi puo contestare, includere il non fare nulla e registrare i vincoli non negoziabili.

## FASE 1 — Fonti

### 10 — Regime probatorio
Scegliere prove adeguate al dominio. Per il dettaglio leggere `evidence-and-semaphores.md`.

### 11 — Autorita adeguata
Per norme usare fonti ufficiali; per software usare sorgente, commit/versione, build, test, log e readback dello stesso ambiente.

### 12 — Vigenza e versione
Verificare data, release, norma, bando, snapshot e versione applicabili.

### 13 — Gerarchia e conflitti
Dichiarare gerarchia, conflitti e fonti subordinate.

### 14 — Citazioni e identificazione
Collegare ogni claim decisivo a titolo o ID, data, versione, ambiente e ruolo probatorio.

### 15 — Dati mancanti
Scrivere `dato non disponibile`; non colmare con memoria o versioni storiche non autorizzate.

## FASE 2 — Ragionamento e dialettica

### 16 — Tesi, antitesi e sintesi
Costruire la tesi migliore, attaccarla con fatti contrari e sintetizzare per asse. Applicare minimax solo secondo i guardrail.

### 17 — Falsificazione e assurdo
Indicare quale osservazione renderebbe falsa la conclusione. L'assurdo non produce un VERDE da solo.

### 18 — Dimostrato e sperato
Separare capacita attuale, obiettivo futuro, promessa e assunzione.

### 19 — Stato epistemico e grado
Etichettare FATTO, INFERENZA, RISCHIO, RACCOMANDAZIONE, ASSUNZIONE e assegnare grado alto, medio o basso.

### 20 — Base-rate e allocazione
Usare base-rate o Kelly solo con dati calibrati e coerenti. Altrimenti N/A.

### 21 — Prova che chiude il rischio
Identificare fonte vigente, approvazione, misura, esecuzione, contratto, build, test, readback o audit necessario.

## FASE 3 — Verifica e uscita

### 22 — Prova del nove
Controllare numeri, date, unita, dipendenze e coerenza cross-documento. E14 puo solo degradare, mai promuovere.

### 23 — Plausibilita
Usare Fermi come intervallo trasparente, non come valore puntuale inventato.

### 24 — Completezza
Riconciliare risultato, formato, fonti, criterio di successo e viste derivate richieste.

### 25 — Contestazione esterna
Simulare tecnico, revisore, ente, utente, investitore o controparte.

### 26 — Pre-mortem finale
Trasformare i tre failure mode principali in controlli o limiti.

### 27 — Verifica professionale
Segnalare quando serve il titolare della decisione o un professionista abilitato.

### 28 — Registro punti aperti
Per ogni punto indicare prova necessaria, owner, scadenza/evento, impatto e prossima azione.

### 29 — Semaforo risposta
- VERDE: usabile nello scope dichiarato con prova diretta, corrente e sufficiente.
- GIALLO-FORMA: sostanza pronta; manca approvazione, firma, consegna o persistenza richiesta.
- GIALLO-SOSTANZA: manca una prova che puo cambiare il GO.
- ROSSO: contraddizione, fonte non vigente, pilastro privo di prova o deliverable essenziale fallito.

Spiegare perche il colore scelto e corretto e perche non lo sono almeno il livello superiore e quello inferiore.
