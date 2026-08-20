# Wiki locale di progetto

## Scopo

La Wiki e una memoria locale facoltativa. Crearla o controllarla soltanto quando l'utente lo chiede esplicitamente e indica una cartella esistente sotto `/mnt/data`.

`CONTEXT.md` e una vista derivata: non sostituisce fonti, test, approvazioni o verbali.

## Tipi di documento

| Tipo | Percorso locale | Scopo |
|---|---|---|
| Context pack | `_wiki/CONTEXT.md` | ingresso operativo locale |
| Decisione | `_wiki/decisioni/D-*.md` | decisioni con stato, data e fonte |
| Fatto | `_wiki/fatti/*.md` | valori e definizioni |
| Processo | `_wiki/processo/*.md` | procedure e controlli |
| Ricerca | `_wiki/ricerche/*.md` | tesi, antitesi, evidenza e sintesi |

Ogni file fuori `Archivio/` riporta `project_name`, `project_code`, `tags`, `tipo`, `stato` e `aggiornato`.

## Ciclo locale

1. Verificare che la root sia sotto `/mnt/data`.
2. Leggere soltanto `_wiki/` e `wiki.config.json` nella root indicata.
3. Creare la Wiki solo se `_wiki/` non esiste.
4. Non sovrascrivere file esistenti.
5. Aggiornare `CONTEXT.md` per ultimo quando l'utente richiede una modifica manuale della Wiki.
6. Eseguire `scripts/lint_wiki.py`.
7. Registrare esito e violazioni residue.

## Bootstrap

```bash
python scripts/wiki_init.py --root /mnt/data/NOME_CARTELLA --project-name "NOME" --project-code CODICE
python scripts/lint_wiki.py --vault /mnt/data/NOME_CARTELLA
```

## Linter

Il linter controlla frontmatter, identita progetto, collegamenti interni, identificativi, dimensioni, decisioni, freschezza di `CONTEXT.md`, indice e integrita minima delle evidenze. Controlla coerenza, non verita. Zero violazioni consente al massimo `VALIDATED`.
