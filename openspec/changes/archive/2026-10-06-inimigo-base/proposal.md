# Proposal

## Why

O jogo ainda não possui nenhum inimigo, então a primeira interação de combate entre Coxinha e um adversário nunca foi validada. Esta change introduz o primeiro inimigo na cena inicial e estabelece a mecânica básica de derrota por pisada, criando a base sobre a qual futuras mecânicas de inimigos (IA, movimentação, vida/dano, animações) poderão ser construídas.

## What Changes

- Adicionar o primeiro inimigo à cena inicial (`GameScene`), posicionado sobre a plataforma, com hitbox própria e permanecendo parado.
- Implementar a derrota do inimigo quando Coxinha cai sobre a sua parte superior durante um salto (pisada).
- Aplicar um pequeno impulso para cima em Coxinha logo após a pisada.
- Garantir que colisões laterais ou por baixo NÃO derrotem o inimigo.
- Preservar as mecânicas existentes de movimentação, corrida, salto, física, colisões, hitbox e limites da área de jogo.

Não fazem parte desta change:

- IA ou movimentação do inimigo;
- sistema de vida/dano do Coxinha;
- animações;
- sons;
- HUD;
- coletáveis;
- novas fases.

## Capabilities

### New Capabilities

- `inimigo-base`: Primeiro inimigo da cena inicial, com hitbox própria e comportamento parado, derrotado por pisada quando Coxinha cai sobre a sua parte superior durante um salto, com pequeno impulso para cima após a pisada; colisões laterais ou por baixo não o derrotam.

### Modified Capabilities

Nenhuma. Os requisitos das capacidades existentes (`jogo-inicial`, `personagem-coxinha`) permanecem válidos sem alteração; a nova interação é um comportamento aditivo coberto pela nova capacidade `inimigo-base`.

## Impact

- Alteração de `src/scenes/GameScene.ts` para criar o inimigo, registrar a colisão e implementar a detecção de pisada e o impulso.
- Nenhum novo asset de imagem (não existe asset de inimigo no projeto; a representação visual inicial será uma forma geométrica temporária, seguindo o padrão já utilizado pelo projeto).
- Nenhuma alteração em dependências (`package.json`), `tsconfig.json` ou `vite.config.ts`.
- Nenhuma alteração nos controles, velocidades de movimento/corrida, força do salto, gravidade, hitbox do jogador, colisão com a plataforma ou limites horizontais.