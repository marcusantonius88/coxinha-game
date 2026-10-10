# Tasks

## 1. Produção e aprovação da arte (dependência aberta)

- [ ] 1.1 Obter a primeira versão da arte das 22 frames por **geração assistida com IA** (caminho preferencial), fora do código do jogo, como PNGs individuais **48×32 RGBA** com fundo transparente e sem textos, cenários ou elementos decorativos — verificação: arquivos existem e abrem como PNG RGBA 48×32. **Bloqueante: enquanto os arquivos de arte não existirem e não forem aprovados na 1.2, esta task, a 1.2 e todas as tarefas de integração (2.x–4.x) permanecem desmarcadas.**
- [ ] 1.2 Revisão visual e aprovação da arte antes de qualquer integração (identidade: pelagem caramelo, focinho escuro, peito creme, orelhas eretas, corpo compacto; dimensões, proporções e alinhamento dos pés consistentes nos 22 quadros; ausência de textos, cenários ou decoração; comparação lado a lado com o tamanho atual exibido no jogo — dimensões 48×32 e caixa 96×64 preservadas, sujeitas à conferência com a arte atual) — verificação: aprovação explícita registrada; se a geração por IA produzir frames inconsistentes (proporções, paleta, alinhamento, estilo), fazer ajustes ou produção complementar em ferramenta de pixel art até passar na revisão (gerador procedural somente como último recurso); nunca integrar arte reprovada nem usar `coxinha-sprite-sheet.png`/`coxinha-idle.png` como fonte.
- [ ] 1.3 Converter a arte aprovada em sprite sheet técnico com `scripts/build-coxinha-sheet.mjs` (cópia pixel a pixel por célula — sem escala, interpolação ou alteração de paleta — com validação que falha alto: frame diferente de 48×32 RGBA, canto com alpha ≠ 0, linha de base variando >1 px entre frames, centro horizontal desviando >1 px) → `assets/coxinha/coxinha-frames.png` — verificação: `node scripts/build-coxinha-sheet.mjs` exit 0 e `file` reporta PNG RGBA 1056×32 (22 frames: IDLE 0–3, WALK 4–9, RUN 10–15, JUMP 16–17, FALL 18–19, LAND 20–21).

## 2. Carregamento e animações no GameScene

- [ ] 2.1 Trocar o `preload()` de `load.image('coxinha-idle', ...)` para `load.spritesheet('coxinha-frames', ...)` com `frameWidth: 48`/`frameHeight: 32`, removendo o carregamento do asset estático sem apagar os arquivos antigos — verificação: `grep` em `src/scenes/GameScene.ts` não encontra mais `coxinha-idle`, `npm run build` exit 0 e o jogo carrega sem erro de asset no console.
- [ ] 2.2 Implementar `createAnimations()` registrando `IDLE` (4 f @6, loop), `WALK` (6 f @10, loop), `RUN` (6 f @14, loop), `JUMP` (2 f @8, loop), `FALL` (2 f @8, loop) e `LAND` (2 f @12, uma vez) a partir dos índices de frame definidos no design — verificação: `npm run build` exit 0 e as 6 animações respondem `this.anims.exists(chave) === true` na cena carregada.
- [ ] 2.3 Substituir `playerVisual` de `Image` por `Sprite` mantendo a sincronização com o corpo físico (`setPosition(body.center.x, body.bottom)`), com `setOrigin(0.5, 1)` e escala inteira ×2 (caixa exibida 96×64 px, idêntica à do Coxinha atual) — verificação: `npm run build` exit 0 e no navegador o Coxinha aparece no mesmo tamanho de caixa do atual, com os pés ancorados no corpo físico durante andar/correr/pular, sem erros de console.

## 3. Seleção automática de estado

- [ ] 3.1 Implementar em `update()` o estado-alvo derivado da física (ar: `v.y < 0` → `JUMP`, `v.y > 0` → `FALL`, `v.y == 0` mantém anterior; terra: `|v.x|` com `Shift` → `RUN`/`WALK`, parado → `LAND`/`IDLE`) somente escrevendo no visual — verificação: `npm run build` exit 0 e teste manual rápido no navegador: os 6 estados aparecem nos cenários correspondentes.
- [ ] 3.2 Implementar a guarda anti-restart (`currentAnim` só chama `anims.play()` quando o estado muda) e o flip horizontal apenas quando `|v.x| > 0` — verificação: no navegador, parado 3 s o `IDLE` não reinicia (frame corrente continua), segurar a mesma tecla não reinvoca `play` repetidamente, e andar para a esquerda espelha o sprite.
- [ ] 3.3 Implementar a aterrissagem (flag `wasAirborne` na transição ar→chão, `LAND` uma vez via `animationcomplete`, com prioridade de `WALK`/`RUN` sobre `LAND`) — verificação: no navegador, pular exibe `JUMP`→`FALL`→`LAND`→`IDLE` e começar a andar no instante do pouso mostra `WALK`/`RUN` imediatamente.

## 4. Verificação integrada

- [ ] 4.1 Rodar `npm run build` após todos os ajustes — verificação: exit code 0 (`tsc` sem erros + bundle Vite gerado).
- [ ] 4.2 Conferir no navegador todos os cenários da spec de animação (IDLE/WALK/RUN/JUMP/FALL/LAND, mesmo-estado-não-reiniciado, sprite sheet de apresentação não usada, visual seguindo o corpo, tamanho/aparência correspondentes à arte aprovada) — verificação: checklist executado com o jogo rodando (`npm run preview`) e resultado registrado; nenhum erro de console.
- [ ] 4.3 Executar a regressão de preservação (hitbox 30×30, controles, limites, derrota por pisada, sem erros de console) com o harness de navegador existente — verificação: harness reporta 23/23 checks passed.
- [ ] 4.4 Validar os artefatos da change — verificação: `openspec validate animacoes-coxinha --strict` retorna exit 0 e `openspec status --change animacoes-coxinha` mostra 4/4 artefatos completos com todas as tasks marcadas.
