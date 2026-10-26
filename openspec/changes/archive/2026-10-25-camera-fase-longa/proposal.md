# Proposal

## Why

A cena atual é uma seção de plataforma de **800×600 px que cabe inteira na tela**: o chão (`rectangle(400, 560, 800, 10)`) cobre `x ∈ [0, 800]`, as plataformas aprovadas ocupam `x = 40..760` e o slime fica em `x = 580..620`. O jogador anda da borda esquerda à direita sem nunca sair do enquadramento — não há sensação de mundo, apenas de uma tela.

A spec vigente `cenario-plataformas` explicita essa limitação: *"A seção SHALL caber integralmente na área de jogo visível, sem exigir rolagem de câmera"* e *"SHALL NOT implementar câmera com rolagem nesta change"*. Esta change **substitui** essas restrições por um mundo horizontalmente extenso com câmera que acompanha o Coxinha, mantendo toda a jogabilidade de plataforma já aprovada.

## What Changes

- **Mundo maior que a viewport**: a fase passa a ter `WORLD_WIDTH = 2400 px` (3× a largura visível de 800 px), com o chão redimensionado para cobrir `x ∈ [0, 2400]`.
- **Câmera horizontal**: a câmera principal segue o corpo do Coxinha no eixo X, com rolagem suave e **fixa verticalmente** (sem zoom, sem rotação, sem jitter vertical).
- **Limites do mundo**: a câmera para nos extremos do mundo, sem áreas vazias além das bordas; o corpo do jogador mantém `collideWorldBounds` relativo ao mundo (não mais à tela).
- **Distribuição do cenário**: chão contínuo, plataformas elevadas e obstáculos redistribuídos pela seção extensa, mantendo o padrão aprovado (alturas de topo ≤ 130 px, vãos alcançáveis com a física atual).
- **Slime reposicionado**: mantido no percurso, com a mecânica de derrota por pisada, `DEFEAT` e impulso `-690` intactos.
- **Renderização pixel-perfect preservada**: `pixelArt` e `roundPixels` continuam habilitados; a câmera usa arredondamento de pixel para não borrar a arte.

## Capabilities

### New Capabilities

- `fase-camara-horizontal`: fase horizontalmente extensa com câmera que acompanha o personagem no eixo horizontal, respeitando os limites do mundo e preservando a jogabilidade de plataforma existente.

### Modified Capabilities

- `cenario-plataformas`: deixa de exigir que a seção caiba na área visível e passa a distribuir plataformas, obstáculos e o slime por uma fase extensa com rolagem de câmera.
- `jogo-inicial`: o "limite horizontal da tela" passa a ser o "limite horizontal do mundo", e a cena inicial passa a respeitar os limites do mundo.
- `inimigo-base`: a preservação dos "limites horizontais da área de jogo" passa a se referir aos limites do mundo.
- `personagem-coxinha`: a preservação dos "limites horizontais da área de jogo" passa a se referir aos limites do mundo.

## Impact

- **Código**: `src/scenes/GameScene.ts` — novo comprimento de mundo, chão estendido, novas posições de plataformas/obstáculos/slime, configuração da câmera (`startFollow` + `setBounds` + clamping vertical) e do `physics.world.setBounds`. `src/main.ts` permanece intocado (800×600, `pixelArt`, `roundPixels`, gravidade 1840).
- **Física**: **inalterada** — gravidade `1840`, salto `-920`, velocidades `200`/`350`, impulso da pisada `-690`, hitbox `30×30` preservados.
- **Assets**: nenhum PNG criado ou alterado; sprites existentes intocados.
- **Fora de escopo**: zoom de câmera, rolagem vertical, transições entre fases, checkpoints, vidas, pontuação, novos inimigos/habilidades, sprites novos, dependências novas.
- **Verificação**: `npm run build` (exit 0) + `openspec validate --strict` + harness de navegador (câmera para esquerda/direita, clamp nos limites, saltos/aterrissagens em pontos distintos, slime com pisada, animações sem regressão, console limpo).
