# Claude Prompt Skills

Due skill **universali** (dominio-agnostiche) per Claude Code, per ottenere risposte
verificabili e codice affidabile su task ad alto rischio.

| Skill | Cosa fa |
|---|---|
| [`protocollo-prompt`](protocollo-prompt/SKILL.md) | Protocollo di controllo per **prompt e risposte affidabili**: 5 fasi, 29 controlli (diagnosi prompt, doppio semaforo, fonti, ragionamento Hegel, prova vincolante, output). Per bandi, norme, atti, valutazioni, decisioni operative, codice. |
| [`protocollo_coding`](protocollo_coding/SKILL.md) | Protocollo prompt **vincolante per task di codice** ad alto rischio: rigore operativo (scope, no path assoluti, verifica binaria, no warning silenziati, secret, edge case, validazione input) + ragionamento. Include la **Regola 0**: non andare in loop sprecando token — se non sai cosa stai facendo, fermati e chiedi. |

## Installazione

Le skill di Claude Code vivono in `~/.claude/skills/<nome-skill>/SKILL.md`
(una cartella per skill, file chiamato esattamente `SKILL.md`).

### A — clona e copia (Windows / PowerShell)
```powershell
git clone https://github.com/mariogrillo1974-hue/claude-prompt-skills.git
cd claude-prompt-skills
New-Item -ItemType Directory -Force "$HOME\.claude\skills\protocollo-prompt" | Out-Null
New-Item -ItemType Directory -Force "$HOME\.claude\skills\protocollo_coding" | Out-Null
Copy-Item ".\protocollo-prompt\SKILL.md" "$HOME\.claude\skills\protocollo-prompt\SKILL.md" -Force
Copy-Item ".\protocollo_coding\SKILL.md" "$HOME\.claude\skills\protocollo_coding\SKILL.md" -Force
```

### B — clona e copia (macOS / Linux)
```bash
git clone https://github.com/mariogrillo1974-hue/claude-prompt-skills.git
cd claude-prompt-skills
mkdir -p ~/.claude/skills/protocollo-prompt ~/.claude/skills/protocollo_coding
cp protocollo-prompt/SKILL.md ~/.claude/skills/protocollo-prompt/SKILL.md
cp protocollo_coding/SKILL.md ~/.claude/skills/protocollo_coding/SKILL.md
```

## Verifica

Riavvia Claude Code e digita `/`: devono comparire `/protocollo-prompt` e
`/protocollo_coding`. Si attivano da sole quando il task rientra nella loro
descrizione, oppure le richiami a mano col nome.
