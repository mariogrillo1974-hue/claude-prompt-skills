# Claude Prompt Skills

Skill **universali** (dominio-agnostiche) per Claude Code, per ottenere risposte
verificabili e codice affidabile su task ad alto rischio.

| Skill | Cosa fa |
|---|---|
| [`controllo-semantico`](controllo-semantico/SKILL.md) | **Skill operativa corrente (v2.2).** 29 controlli, FASE semantica S1–S5, tesi/antitesi/sintesi, persistenza Drive/Wiki e Gate di Non Regressione. Trigger: *controllo semantico*, *applica il protocollo*, red-team, GO/NO-GO. |
| [`protocollo-prompt`](protocollo-prompt/SKILL.md) | Protocollo compatto per **prompt e risposte affidabili**: 5 fasi, 29 controlli. Per bandi, norme, atti, valutazioni, decisioni operative, codice. |
| [`protocollo_coding`](protocollo_coding/SKILL.md) | Protocollo prompt **vincolante per task di codice** ad alto rischio: rigore operativo (scope, no path assoluti, verifica binaria, no warning silenziati, secret, edge case, validazione input) + ragionamento. Include la **Regola 0**: non andare in loop sprecando token — se non sai cosa stai facendo, fermati e chiedi. |

`controllo-semantico` è la versione operativa completa del protocollo (template, script, Drive/Wiki, non regressione). `protocollo-prompt` resta il checklist compatto a un solo file.

## Installazione

Le skill di Claude Code vivono in `~/.claude/skills/<nome-skill>/SKILL.md`
(una cartella per skill, file chiamato esattamente `SKILL.md`).

`controllo-semantico` va copiata **intera** (template, script, references). Le altre due sono un solo `SKILL.md`.

### A — clona e copia (Windows / PowerShell)
```powershell
git clone https://github.com/mariogrillo1974-hue/claude-prompt-skills.git
cd claude-prompt-skills
Copy-Item -Recurse -Force ".\controllo-semantico" "$HOME\.claude\skills\controllo-semantico"
New-Item -ItemType Directory -Force "$HOME\.claude\skills\protocollo-prompt" | Out-Null
New-Item -ItemType Directory -Force "$HOME\.claude\skills\protocollo_coding" | Out-Null
Copy-Item ".\protocollo-prompt\SKILL.md" "$HOME\.claude\skills\protocollo-prompt\SKILL.md" -Force
Copy-Item ".\protocollo_coding\SKILL.md" "$HOME\.claude\skills\protocollo_coding\SKILL.md" -Force
```

### B — clona e copia (macOS / Linux)
```bash
git clone https://github.com/mariogrillo1974-hue/claude-prompt-skills.git
cd claude-prompt-skills
cp -R controllo-semantico ~/.claude/skills/controllo-semantico
mkdir -p ~/.claude/skills/protocollo-prompt ~/.claude/skills/protocollo_coding
cp protocollo-prompt/SKILL.md ~/.claude/skills/protocollo-prompt/SKILL.md
cp protocollo_coding/SKILL.md ~/.claude/skills/protocollo_coding/SKILL.md
```

## Verifica

Riavvia Claude Code e digita `/`: devono comparire `/controllo-semantico`,
`/protocollo-prompt` e `/protocollo_coding`. Si attivano da sole quando il task
rientra nella loro descrizione, oppure le richiami a mano col nome.

Trigger di `controllo-semantico`: *controllo semantico* (workflow completo),
*solo analisi* / *locale* per disattivare le scritture remote.
