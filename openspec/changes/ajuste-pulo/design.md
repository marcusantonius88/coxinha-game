# Design

## Context

Ver `proposal.md` (Why). Estado atual relevante:

- Estado original (antes desta change): gravidade `300`, `jumpForce = -400`, pisada `setVelocityY(-300)` → ~267 px e ~2,67 s no ar (medido 263 px / 2,665 s).
- Estado da 1ª iteração (já aplicada no working tree): `jumpForce = -800`, `arcade.gravity.y = 1330`, pisada `-600` → medido salto **1,189 s / 233 px** (teórico 1,20 s / 241 px) e bounce **130 px** (teórico 135 px; relação 0,56). No teste manual a permanência no ar ainda pareceu um pouco lenta.
- Fórmulas de projectile do Arcade: `altura = v0²/(2g)` e `tempo total = 2·v0/g`; invertidas para calibração: `g = 8·h/T²` e `v0 = 4·h/T`.
- Apenas o Coxinha é corpo dinâmico; plataforma e inimigo são estáticos.

## Goals / Non-Goals

**Goals:**

- Refinar o salto para ~1,0 s no ar (faixa 0,9–1,1 s) e ~225 px de altura (faixa 220–230 px): mais responsivo, sem torná-lo excessivamente baixo ou brusco.
- Manter a mecânica de pisada com a mesma sensação relativa (bounce proporcional ao salto, relação de alturas ~0,56; bounce ~130 px teórico / ~125 px medido).
- Manter os valores de física explicados junto ao código (comentários) para futuras changes.

**Non-Goals:**

- Salto variável (segurar a tecla para pular mais alto), coyote time, jump buffering.
- Qualquer alteração de velocidade horizontal, corrida, hitbox, controles, colisões, lógica/posição dos inimigos, dano, animações, sons, HUD, coletáveis ou fases.
- Refatorar os parâmetros para um módulo de configuração compartilhado (as constantes permanecem nos atuais pontos de definição).

## Decisions

1. **Recalcular `v0` e gravidade em conjunto a partir dos novos alvos** — Fixar T = 1,0 s e h = 230 px (topo da faixa 220–230 px; folga para o déficit sistemático de ~4–8 px da amostragem do apogeu observado na medição) e aplicar `g = 8h/T²`, `v0 = 4h/T`. Com `g = 1330` fixa, T = 1,0 s exigiria `v0 = 665` → h ≈ 166 px (fora da faixa); reduzir só `v0` derruba a altura. Alternativa descartada: manter os valores da 1ª iteração (`-800`/`1330` → 1,2 s), rejeitada no teste manual como ainda lenta.
2. **Valores: `jumpForce = -920`, gravidade `y = 1840`** — `T = 2·920/1840 = 1,000 s`, `h = 920²/3680 = 230 px` teórico → medido esperado ~222–227 px, dentro de 220–230 px. Alternativas consideradas e descartadas: `900`/`1800` (h teórico 225 px — o medido correria risco de furar o piso de 220 px pelo déficit de amostragem); `v0 = -928`, `g = 1856` (h teórico 232 px — reserva maior, números menos redondos; usar só se a medição ficar marginamente abaixo).
3. **Impulso da pisada: `-690`** — mantém a razão histórica 0,75 (`-300/-400`) em relação à força do salto (`0,75 × 920 = 690`). Com a nova gravidade dá bounce de ~129 px teórico / ~125 px medido e voo de ~0,75 s, mantendo a relação de alturas bounce/salto = 0,75² = 0,5625 ≈ 0,56 — bounce pequeno e controlado. Alternativas descartadas: manter `-600` (razão 0,65 → bounce ~98 px, sensação de pisada mais fraca que a histórica); `-300` fixo (bounce ~25 px, pisada quase sem retorno).
4. **Constantes nos pontos atuais** — `jumpForce` na `update()`, gravidade no config do Phaser, impulso da pisada em `handleEnemyContact()`, cada um com comentário relacionando-os ("razão 0,75 com jumpForce") atualizado para os novos valores. Alternativa: arquivo único de constantes de física — postergada (Non-Goal), não altera comportamento observável.
5. **Validação por medição real** — calibrar/confirmar com medição no navegador (tempo do salto pleno e apogeu), reaproveitando a abordagem de automação via CDP usada nas medições desta change (3 réplicas com mediana e correção de lacunas).

## Risks / Trade-offs

- [Queda mais rápida aproxima o Coxinha do inimigo por mais px por quadro (~15 px/quadro na queda livre com v final ≈ 920 px/s a 60 fps, vs ~13 na 1ª iteração e ~7 no original), reduzindo a margem da detecção de pisada (`prev.y + height <= top + 8`)] → a janela ainda cobre penetrações até ~23 px/quadro; validar a pisada em teste real; só ajustar a tolerância se o teste falhar (mudança de detalhe, não de comportamento).
- [O baseline relatado (~4 s) difere do teórico (~2,67 s)] → resolvido na 1ª iteração: medido 2,665 s / 263 px (ver tasks 1.1/1.2); manter a medição real como fonte de verdade na validação do refino.
- [Gravidade é global no `main.ts` e afeta todo corpo dinâmico futuro] → aceitável e esperado; hoje só o jogador é dinâmico, sem efeito colateral.
- [Precisão de medição em navegador (latência de tecla, cadência de captura)] → faixas de aceitação no spec (0,9–1,1 s; 220–230 px) absorvem a variabilidade observada: a medição com 3 réplicas, mediana e correção de lacunas divergiu ~−0,01 s e ~−8 px do teórico na 1ª iteração; alvos de projeto são ~1,0 s / ~225 px.
- [Sensação de "queda pesada" com gravidade ~6× maior que a original] → se o pulo parecer brusco na validação manual, reajustar mantendo T = 1,0 s dentro das faixas (com T fixa, `v0 = 4h` e `g = 8h`; ex.: h = 220 px → `v0 = -880`, `g = 1760`).

## Migration Plan

Ajuste de três constantes numéricas (da 1ª iteração para os valores refinados); rollback = reverter o commit. Build estático, sem migração de dados ou configuração de ambiente.

## Open Questions

(nenhuma — os alvos refinados (~1,0 s / 220–230 px) foram definidos pelo usuário após o teste manual da 1ª iteração; os valores numéricos derivaram das equações de projectile e ficam sujeitos à confirmação por medição na validação do refino.)
