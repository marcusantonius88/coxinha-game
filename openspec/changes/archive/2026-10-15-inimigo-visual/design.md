# Design

## Context

Ver `proposal.md` (seção Why) para a motivação. O estado atual que limita a abordagem:

- `src/scenes/GameScene.ts`: o inimigo é `this.add.rectangle(600, 535, 40, 40, 0x2e8b57)` — retângulo **visível**, corpo estático Arcade 40×40 (topo em y=515; base em y=555 = linha do chão). O colisor com callback `handleEnemyContact()` aplica a regra de pisada (contato pelo topo + `prev.y` acima, tolerância 8) e, na derrota, faz `enemyDefeated=true` → `enemyCollider.active=false` → `enemy.destroy()` → `setVelocityY(-690)`.
- O Coxinha já segue o padrão **corpo físico invisível + `Sprite` visual** sincronizado, com animações registradas em `createAnimations()` e chaves centralizadas — o inimigo adotará o mesmo padrão, em escala menor.
- Renderização: `src/main.ts` já configura `render: { pixelArt: true, roundPixels: true }` (filtro NEAREST + posições inteiras) — preservada sem alteração.
- Assets prontos em `assets/enemies/slime/` (medidos): 4 spritesheets RGBA de **256×48 = 4 quadros de 64×48**, alfa binário; linha de base dos pés: `idle`/`walk` no quadro y=39 (8 px de padding transparente inferior), `defeat` em [41, 41, 41, 35]; conteúdo centrado em x≈32. README recomenda: IDLE em loop, DEFEAT uma vez após a pisada, corpo físico separado do visual.
- Física congelada por esta change: gravidade `1840`, salto `-920`, pisada `-690`, hitbox do Coxinha 30×30, corpo do inimigo 40×40 estático, colisões e limites.
- Stack: Phaser 3.90 + TS 5.4 + Vite 5; build `tsc && vite build`; sem framework de testes (verificação por harness de navegador, como nas changes anteriores).

## Goals / Non-Goals

**Goals:**

- Inimigo exibido com a arte aprovada do slime (sem gerar/modificar PNGs), `IDLE` em loop enquanto ativo.
- `DEFEAT` reproduzida uma única vez após pisada válida, com remoção consistente (visual + corpo) ao concluí-la e derrotas duplicadas impedidas.
- Corpo físico 40×40 intocado e invisível; zero alteração em física, controles, animações do Coxinha e config de render.
- Escala inteira (pixel-perfect preservado), pés do slime alinhados à base do corpo físico.

**Non-Goals:**

- Movimentação autônoma, perseguição, ataques, pontuação, sons, múltiplos inimigos.
- Carregar/animações de `WALK`/`HIT` do slime (assets ficam no projeto sem uso nesta change).
- Alterar tamanho/posição da hitbox do inimigo, a régua de stomp ou o impulso `-690`.
- Qualquer mudança nos sprites ou animações do Coxinha.

## Decisions

1. **Padrão corpo↔visual idêntico ao do Coxinha**: `enemy` (Rectangle) permanece o único ator físico, ganha `setVisible(false)`; novo `enemyVisual` (`Phaser.GameObjects.Sprite`, sem corpo) posicionado uma única vez em `create()` em `(enemy.x, enemy.bottom)` com origem `(0.5, 40/48)`. Como o inimigo é estático (spec proíbe movimento autônomo), não há sincronização por frame — alternativa (sync em `update()`) descartada por desnecessária; reavaliar apenas se um futuro change tornar o inimigo móvel.
2. **Ancoragem pelos pés medida nos PNGs**: quadro 64×48 com baseline no y=39 → origem `40/48` coloca a borda inferior do pixel dos pés exatamente em `body.bottom` (555), mesma técnica do `31/32` do Coxinha. Nos quadros de `DEFEAT` a base varia [41..35]: no máximo 1 px de sobreposição cosmética com o chão e 6 px de "levantamento" no último quadro (efeito de dissolução) — aceito num one-shot de ~0,3 s; origem por quadro foi descartada (sem suporte barato no Phaser, benefício cosmético irrisório).
3. **Escala inteira ×1 (caixa 64×48)**: os quadros já são pixel art nativo ampliado ×2 (32×24→64×48); exibir em escala 1 preserva o pixel-perfect com o filtro NEAREST existente. Alternativa descartada: escalar para casar os 40 px do corpo (escala fracionária 0,625 → quebra pixel-perfect e reduz demais a presença). A caixa visual (64×48) maior que a hitbox (40×40) repete o padrão aprovado do Coxinha (96×64 sobre 30×30): colisão usa só o corpo, visual é apresentação.
4. **Animações do inimigo registradas em `createEnemyAnimations()`**, com guarda `anims.exists()` (mesma convenção do jogador): `slime-idle` = 4 quadros @ **6 FPS**, loop (mesmo ritmo do `idle` do Coxinha); `slime-defeat` = 4 quadros @ **12 FPS**, `repeat: 0` (mesma convenção do `land` — one-shot de ~333 ms). O README não define FPS: valores são polimento ajustável sem mudar specs/design/tasks. Chaves de textura `slime-idle-sheet`/`slime-defeat-sheet`, loader `frameWidth: 64`/`frameHeight: 48`.
5. **Fluxo de derrota com um único ponto de remoção**: em `handleEnemyContact()`, após a confirmação da pisada (código de detecção intacto): `enemyDefeated = true` → `enemyCollider.active = false` (interação física cessa imediatamente, como hoje) → `enemyVisual.play('slime-defeat')` em vez do `destroy()` imediato → listener `animationcomplete` (chave `slime-defeat`) destrói **visual e corpo** juntos; impulso `-690` aplicado na mesma ordem de hoje. Guarda `enemyDefeated` + colisor inativo + destruição ao fim impedem derrotas duplicadas. Alternativa descartada: destruir o corpo imediatamente e manter só o visual — funciona, mas cria dois pontos de remoção e derruba a semântica do guard `!this.enemy.active` usado hoje.
6. **Escopo de carregamento mínimo**: só `idle` e `defeat` são carregadas (nada de `walk`/`hit` sem uso); imports resolvidos pelo Vite como no Coxinha; nenhum sistema existente é tocado além do bloco do inimigo em `preload`/`create` e do fluxo de derrota em `handleEnemyContact`.

## Risks / Trade-offs

- [Visual 64×48 sobre corpo 40×40: o jogador pisar "por cima" da caixa visual] → medida: topo opaco do slime ≈ linhas 8–10 do quadro (tela ~523–525) vs linha de contato 515 — o Coxinha pousa com folga sobre a cabeça visível, sem clipping; confirmar no harness/inspeção visual.
- [A animação `DEFEAT` não disparar (animação não registrada)] → listener anexado em `create()` antes de qualquer stomp possível; harness verifica remoção do inimigo e ausência de erros de console.
- [Baseline variável dos quadros de derrota causando "pulo" do slime] → ≤1 px de diferença por quadro num one-shot; aceito e documentado (Decisão 2).
- [Colisão durante a animação de derrota reprocessar a derrota] → colisor desativado no mesmo frame da pisada + flag `enemyDefeated`; o cenário "Derrota não se repete" cobre o resto.
- [Ritmo de FPS incomodar] → ajustar `frameRate` é mudança local em uma constante, sem impacto em specs, abordagem ou tasks.

## Migration Plan

1. Carregar sheets + `createEnemyAnimations()` + criar `enemyVisual` (corpo permanece intocável e invisível) em `create()`.
2. Trocar o fluxo de derrota em `handleEnemyContact()` (a detecção da pisada permanece igual; só o "o que fazer na derrota" muda).
3. `npm run build` (exit 0) → harness de navegador: pisada ⇒ `DEFEAT` ⇒ remoção; colisão lateral/baixo sem derrota; `IDLE` em loop; sem erros de console; regressão do Coxinha (6 estados + física) → `openspec validate --strict`.
4. Rollback: `git revert` puro — mudança aditiva; nenhum PNG alterado; o retângulo verde volta sem dados persistentes.

## Open Questions

- Ritmo fino do `IDLE`/`DEFEAT` do slime (6/12 FPS) pode ser polido durante a revisão visual sem alterar specs, abordagem ou tasks.
- Integração futura de `WALK`/`HIT` (e possível inimigo móvel) fica para changes seguintes; nenhum outro ponto em aberto.

