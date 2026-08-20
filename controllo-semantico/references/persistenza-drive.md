# Persistenza Google Drive e Wiki condivisa

## Perimetro autorizzato

Questa procedura si applica solo in modalita COMPLETA. Il trigger `controllo semantico` autorizza le operazioni qui elencate: verificare/creare la struttura canonica, caricare la nota Markdown e aggiornare la Wiki pertinente. Non autorizza invii, email, messaggi, condivisioni o modifiche ad altre aree.

## Target canonici

- Controlli: `CLAUDE/OBSIDIAN/00 - Controlli/`
- ID storico da verificare: `15aUcOM2e-CtAJjXuv-gmTGujl0XUfG_8`
- Wiki: `CLAUDE/OBSIDIAN/Wiki/`
- MOC: `_MOC - Wiki.md`

L'ID e un indizio operativo, non una prova eterna. Verificarlo con metadata prima dell'uso.

## A. Risoluzione cartella controlli

1. Chiamare metadata sul folder ID storico.
2. Accettarlo solo se e una cartella accessibile e il nome corrisponde a `00 - Controlli`.
3. Se non valido, cercare cartelle con query brevi e specifiche.
4. Quando serve ricostruire la gerarchia, partire da Drive root e per ogni livello:
   - elencare i figli diretti;
   - riusare l'esatta cartella gia presente;
   - creare la cartella solo se non esiste;
   - rileggere metadata dopo la creazione.
5. Non creare sottocartelle vuote o duplicati omonimi.

## B. Upload della nota

1. Usare la copia locale validata e il relativo SHA-256.
2. Caricare come file raw Markdown, mai come Google Doc.
3. Passare il file locale tramite il parametro file del connettore, lasciando al runtime la conversione in file reference.
4. Impostare come parent l'ID risolto di `00 - Controlli`.
5. Prima dell'upload verificare se un file con lo stesso nome esiste. Se esiste:
   - non sovrascriverlo;
   - generare un nuovo nome con timestamp o suffisso breve;
   - registrare il conflitto evitato.

## C. Readback obbligatorio

Dopo l'upload:

1. leggere metadata del nuovo file;
2. leggere il contenuto del file;
3. verificare nome, parent, MIME type, dimensione e timestamp;
4. confrontare il contenuto con la copia locale o calcolare un nuovo hash se il connettore restituisce bytes/file reference;
5. dichiarare `PERSISTED` solo dopo il readback.

Se l'upload riesce ma il readback fallisce, stato `UPLOAD-UNVERIFIED`, non `PERSISTED`.

## D. Aggiornamento Wiki read-before-write

Aggiornare la Wiki solo se il controllo produce almeno un fatto canonico: definizione, decisione, dato di riferimento, nome/ID, processo vigente o regola stabile.

1. Risolvere la cartella `Wiki` senza duplicati.
2. Cercare e leggere `_MOC - Wiki.md`.
3. Cercare la voce pertinente; caricare solo quella necessaria.
4. Registrare metadata e `modifiedTime` iniziale.
5. Preparare localmente la versione aggiornata preservando contenuto, frontmatter, link e storico.
6. Rileggere metadata immediatamente prima dell'update.
7. Se `modifiedTime` e cambiato, rileggere il file e rifare il merge; non sovrascrivere alla cieca.
8. Aggiornare il file raw `.md` in place oppure crearne uno nuovo se nessuna voce e pertinente.
9. Eseguire readback e registrare ID, timestamp e differenze applicate.
10. Aggiornare il MOC solo se nasce una nuova voce e solo dopo averlo riletto.

## E. Stati operativi

- `LOCAL-CREATED`: nota locale creata.
- `LOCAL-VALIDATED`: validatore e hash completati.
- `DRIVE-FOLDER-VERIFIED`: target verificato.
- `DRIVE-FOLDER-CREATED`: target creato e riletto.
- `UPLOADED`: upload ricevuto dal connettore.
- `PERSISTED`: upload + readback coerente.
- `UPLOAD-UNVERIFIED`: upload senza readback sufficiente.
- `WIKI-NOT-NEEDED`: nessun fatto canonico.
- `WIKI-UPDATED`: update + readback coerente.
- `PARTIAL`: almeno un passaggio richiesto incompleto.
- `FAILED`: passaggio essenziale fallito.

## F. Fallimenti

Per ogni fallimento indicare:

- azione tentata;
- tool e target;
- errore osservato;
- cosa e comunque disponibile localmente;
- prova necessaria per chiudere;
- owner e prossima azione.

Non ripetere la stessa chiamata senza cambiare ipotesi, input o metodo.
