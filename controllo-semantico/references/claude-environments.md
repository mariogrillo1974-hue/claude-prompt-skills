# Ambienti Claude

Applica il protocollo in modo coerente con la superficie realmente in uso.

## Claude.ai e Cowork

- La skill si carica come archivio ZIP dalle impostazioni delle funzionalita.
- L'accesso a rete, connettori, Drive, GitHub, MCP e file dipende dal piano e dalle impostazioni correnti.
- Prima di leggere o scrivere, verifica che il relativo strumento sia disponibile e autorizzato.
- Una risposta testuale non prova una scrittura. Dopo ogni modifica esterna esegui readback e confronta i campi portanti.
- Le skill personalizzate sono personali all'utente: non presumere che siano installate per altri membri del team.

## Claude Code

- Installa la directory in `~/.claude/skills/controllo-semantico/` per uso personale oppure in `.claude/skills/controllo-semantico/` per il singolo progetto.
- Considera il repository corrente e `CLAUDE.md` come contesto separato dalla skill.
- Non fare commit, push, pull request, merge, tag o release senza autorizzazione distinta.
- Non installare pacchetti globali; usa ambienti o dipendenze locali quando una modifica e autorizzata.
- Tratta i comandi shell come operazioni reali: controlla working tree, branch, percorsi, exit code e output.

## Claude API e Managed Agents

- Il bundle deve avere una sola directory di primo livello chiamata `controllo-semantico`, contenente `SKILL.md`.
- Il runtime delle skill non dispone di rete e non consente installazioni di pacchetti a esecuzione avviata.
- Gli script inclusi usano soltanto la libreria standard Python e lavorano su file locali.
- L'upload della skill nel workspace non concede accesso a servizi esterni; gli strumenti vanno configurati separatamente.
- Distingui creazione della skill, creazione di una sua versione e collegamento della skill a un agente.

## Regola comune

Quando una capacita non e osservabile, scrivi `non verificato nell'ambiente corrente`. Non sostituire la prova runtime con una deduzione basata sulla documentazione o su un'altra superficie Claude.
