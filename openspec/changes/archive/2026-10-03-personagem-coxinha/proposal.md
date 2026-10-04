# Proposal

## Why

O personagem temporário utilizado na primeira versão do jogo não representa a identidade do Coxinha. É necessário substituí-lo por uma representação visual inicial do protagonista, mantendo inalteradas as mecânicas de movimentação já implementadas.

Esta change introduz a primeira identidade visual do personagem, mas não tem como objetivo implementar animações ou novas mecânicas de gameplay.

## What Changes

- Substituir o personagem geométrico temporário pela pose estática `IDLE` do asset `assets/coxinha/coxinha-idle.png` (imagem única, pixel art 16-bit, Bulldog Francês, protagonista do jogo).
- Manter `assets/coxinha/coxinha-sprite-sheet.png` no projeto como asset futuro para animações (`WALK`, `RUN`, `JUMP`, `FALL`, `LAND`, `HIT`); não utilizar `load.spritesheet()` para o personagem nesta change.

Não fazem parte desta change:

- animações ativas (`WALK`, `RUN`, `JUMP`, `FALL`, `LAND`, `HIT`);
- ataques;
- inimigos;
- coletáveis;
- sons;
- HUD;
- novas mecânicas de gameplay.

Nota: `assets/coxinha/coxinha-idle.png` é o asset visual utilizado nesta change; `assets/coxinha/coxinha-sprite-sheet.png` permanece no projeto como referência futura para animações.

## Capabilities

### New Capabilities

- `personagem-coxinha`: Integrar a pose estática `IDLE` do asset `assets/coxinha/coxinha-idle.png` à cena `jogo-inicial`, preservando física ARCADE, hitbox, controles, velocidades, gravidade, colisões e limites; manter `assets/coxinha/coxinha-sprite-sheet.png` como asset futuro para animações

### Modified Capabilities

- `jogo-inicial`: O personagem temporário utilizado na cena inicial passa a utilizar a representação visual do Coxinha, sem alteração dos requisitos de comportamento e movimentação.

## Impact

- Inclusão e versionamento do asset visual do Coxinha no projeto.
- Alteração de `src/scenes/GameScene.ts` para utilizar o novo asset.
- Possíveis ajustes na estrutura de carregamento de assets.
- Nenhuma alteração nas dependências do projeto.
- Nenhuma alteração na lógica de movimentação, física ou controles existentes.