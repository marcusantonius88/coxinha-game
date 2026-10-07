# Design

## Context

Ver `proposal.md` (Why). Estado atual relevante:

- Gravidade global `arcade.gravity.y = 300` em `src/main.ts`.
- Força do salto `jumpForce = -400` em `src/scenes/GameScene.ts` (`update()`).
- Impulso da pisada `setVelocityY(-300)` em `handleEnemyContact()`.
- Com a física de projectile de Arcade: `altura = v0²/(2g)` e `tempo total = 2·v0/g` → hoje ~267 px e ~2,67 s no ar.
- Apenas o Coxinha é corpo dinâmico; plataforma e inimigo são estáticos.

## Goals / Non-Goals

**Goals:**

- Alinhar o salto ao preset **Equilibrado** aprovado: ~1,2 s no ar (faixa 1,0–1,4 s) e ~240 px de altura (faixa 220–260 px).
- Manter a mecânica de pisada com a mesma sensação relativa (bounce proporcional ao salto, mesma relação de alturas ~0,56).
- Manter os valores de física explicados junto ao código (comentários) para futuras changes.

**Non-Goals:**

- Salto variável (segurar a tecla para pular mais alto), coyote time, jump buffering.
- Qualquer alteração de velocidade horizontal, corrida, hitbox, controles, colisões, lógica/posição dos inimigos, dano, animações, sons, HUD, coletáveis ou fases.
- Refatorar os parâmetros para um módulo de configuração compartilhado (as constantes permanecem nos atuais pontos de definição).

## Decisions

1. **Aumentar `v0` e gravidade em conjunto** — Reduzir o tempo mantendo a altura exige escalar os dois: com gravidade 300 fixa, manter 240 px implicaria `v0 ≈ -379` e tempo ≈2,5 s (continua lento); aumentar só a gravidade com `v0 = -400` derrubaria a altura para ~60 px. Alternativa descartada: manter `v0 = -400` e só encher gravidade.
2. **Valores: `jumpForce = -800`, gravidade `y = 1330`** — `T = 1600/1330 ≈ 1,20 s`, `h = 640000/2660 ≈ 241 px`, dentro das faixas do spec com folga para integração quadro a quadro. Alternativas consideradas: `g = 1333` (idêntico na prática), `g = 1350`/`v0 = -810` (faixa mais folgada no tempo, menos na altura) — refinar na medição se necessário.
3. **Impulso da pisada: `-600`** — mantém a razão atual 0,75 (`-300/-400`) em relação à força do salto, e com a nova gravidade dá bounce de ~135 px / ~0,9 s — relação de altura bounce/salto ≈0,56 idêntica à de hoje (150/267). Alternativa descartada (aprovada pelo usuário como opção): manter `-300` fixo → bounce de apenas ~26 px, sensação de pisada fraca.
4. **Constantes nos pontos atuais** — `jumpForce` na `update()`, gravidade no config do Phaser, impulso da pisada em `handleEnemyContact()`, cada um com comentário relacionando-os ("razão 0,75 com jumpForce"). Alternativa: arquivo único de constantes de física — postergada (Non-Goal), não altera comportamento observável.
5. **Validação por medição real** — calibrar/confirmar com medição no navegador (tempo do salto pleno e apogeu), reaproveitando a abordagem de automação via CDP usada na change `inimigo-base`.

## Risks / Trade-offs

- [Queda mais rápida aproxima o Coxinha do inimigo por mais px por quadro (~13 px/quadro a 60 fps vs ~7 hoje), reduzindo a margem da detecção de pisada (`prev.y + height <= top + 8`)] → a janela ainda cobre penetrações até ~21 px/quadro; validar a pisada em teste real; só ajustar a tolerância se o teste falhar (mudança de detalhe, não de comportamento).
- [O baseline relatado (~4 s) difere do teórico (~2,67 s)] → medir o comportamento atual antes de alterar qualquer parâmetro; se o valor real divergir da teoria, investigar a causa antes de calibrar os alvos.
- [Gravidade é global no `main.ts` e afeta todo corpo dinâmico futuro] → aceitável e esperado; hoje só o jogador é dinâmico, sem efeito colateral.
- [Precisão de medição em navegador (latência de tecla, 60 fps)] → faixas de aceitação no spec (1,0–1,4 s; 220–260 px) já absorvem a variabilidade; alvos de projeto são ~1,2 s/~240 px.
- [Sensação de "queda pesada" com gravidade 4,4× maior] → se o pulo parecer pesado na validação manual, ajustar dentro das faixas (ex.: `v0 = -840`, `g = 1470` mantém ~240 px com tempo ~1,14 s).

## Migration Plan

Troca de três constantes numéricas; rollback = rever o commit. Build estático, sem migração de dados ou configuração de ambiente.

## Open Questions

(nenhuma — o preset foi aprovado pelo usuário durante o propose; a discrepância do baseline é tratada como risco com tarefa de medição dedicada.)
