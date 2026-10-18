# Proposal

## Why

O inimigo da cena inicial ainda é representado pelo retângulo verde temporário (40×40), enquanto o restante do jogo já usa arte pixel art aprovada (Coxinha animado com 6 estados). Os sprites do slime estão prontos e revisados em `assets/enemies/slime/` (IDLE/WALK/HIT/DEFEAT, quadros 64×48 RGBA), e a mecânica de derrota por pisada já existe e foi aprovada — integrar o visual do slime com animação de derrota dá feedback imediato da pisada sem tocar na física ou nos controles aprovados.

## What Changes

- Substituir a representação visual do inimigo (retângulo verde visível) pelos sprites aprovados do slime: o corpo físico permanece um retângulo estático 40×40 **invisível**, independente do sprite visual (mesma separação física↔visual já usada no Coxinha).
- Exibir o slime com a animação `IDLE` em loop enquanto o inimigo estiver ativo.
- Ao receber uma pisada válida, reproduzir a animação `DEFEAT` **uma única vez** e, ao concluí-la, remover o visual e o corpo do inimigo de forma consistente; a interação física cessa imediatamente no momento da pisada e derrotas duplicadas permanecem impedidas pela guarda existente.
- Preservar integralmente: mecânica de derrota por pisada (topo + aproximação de cima), impulso `-690`, colisões laterais/por baixo, hitbox do Coxinha, gravidade, força do salto, velocidades, controles, limites, animações existentes do Coxinha e a renderização pixel-perfect já configurada (`pixelArt`/`roundPixels`).
- Nenhuma arte nova: apenas os PNGs existentes em `assets/enemies/slime/` são utilizados; `slime_walk_spritesheet.png` e `slime_hit_spritesheet.png` permanecem no projeto sem uso nesta change.
- Fora de escopo (não implementar nesta change): movimentação autônoma ou perseguição, ataques, sistema de pontuação, sons, múltiplos inimigos, animação `HIT`/`WALK` do slime e qualquer alteração nos sprites ou animações do Coxinha.

## Capabilities

### New Capabilities

(nenhuma)

### Modified Capabilities

- `inimigo-base`: requisito "Inimigo presente na cena inicial" ganha um novo requisito de representação visual animada do slime (sprite independente do corpo físico, `IDLE` em loop, escala inteira pixel-perfect); o requisito "Derrota por pisada" é modificado para prever a reprodução única de `DEFEAT` antes da remoção do inimigo, com interação física cessando imediatamente e sem derrotas duplicadas. Os requisitos "Impulso para cima após a pisada" e "Preservação das mecânicas existentes" permanecem sem alteração.

## Impact

- Código: `src/scenes/GameScene.ts` — `preload()` carrega as spritesheets de `IDLE` e `DEFEAT` (URLs resolvidas pelo Vite); criação das animações do inimigo; `enemy` passa a ser invisível e ganha um `enemyVisual` (`Sprite`) ancorado no pé do corpo físico; `handleEnemyContact()` troca `enemy.destroy()` imediato por `play('slime-defeat')` + remoção na `animationcomplete`, mantendo flags/colisor como hoje.
- Assets: nenhum PNG criado ou alterado; uso exclusivo de `assets/enemies/slime/slime_idle_spritesheet.png` e `assets/enemies/slime/slime_defeat_spritesheet.png` (células 64×48, RGBA).
- Sem mudanças de física, hitbox, controles, configuração de renderização ou de build (`tsc && vite build` permanece igual).
- Verificação posterior na aplicação: `npm run build` (exit 0) + harness de navegador (pisada ⇒ `DEFEAT` ⇒ remoção; colisão lateral não derrota; sem erros de console) + regressão das animações do Coxinha.
