# Design — cenario-visual-nordestino

## Context

A cena atual (`src/scenes/GameScene.ts`) exibe um fundo de cor sólida (`#87CEEB` definido em `src/main.ts`). O mundo tem 2400×600 px (3× a viewport de 800×600), com câmera horizontal seguindo o `playerBody` (`lerpX = 0.1`, `lerpY = 0`, `roundPixels = true`) limitada aos bounds do mundo. As plataformas, obstáculos, slime e spawn estão definidos e funcionam. Não há camadas de fundo visuais além da cor sólida.

Restrições técnicas verificadas no código e no Phaser:

- `render.pixelArt: true` e `render.roundPixels: true` em `main.ts` — texturas usam filtro nearest-neighbor e desenho em posições inteiras.
- Zoom da câmera é 1, rotação 0 — nenhuma escala fracionária.
- `Camera.preRender()` aplica `Linear()` no follow, depois `Math.floor` (roundPixels) e só então `clampX`/`clampY`.
- A altura do mundo (600) é igual à altura da viewport (600), então `clampY` devolve sempre 0 — a câmera é verticalmente fixa.
- O `scrollX` da câmera varia de 0 a 1600 px (2400 − 800) durante a travessia completa.

## Goals / Non-Goals

**Goals:**
- Adicionar até 4 camadas de fundo (tileSprites) com tema Nordeste brasileiro (céu, serras, caatinga, vegetação).
- Cada camada rola em velocidade diferente proporcional ao `scrollX` da câmera (parallax).
- Renderização pixel-perfect preservada (nenhum borrão, escala inteira, posições inteiras).
- Nenhuma colisão; camadas são puramente visuais e ficam atrás de todos os elementos jogáveis.
- Compatível com o mundo 2400×600, câmera existente e física inalterada.

**Non-Goals:**
- Novos inimigos, habilidades, colisões em fundo, transições de fase, checkpoints, zoom/rotação de câmera, rolagem vertical.
- Alterar `src/main.ts` (resolução, cor de fundo, configurações de render).
- Alterar física, spawn, plataformas, slime ou animações existentes.

## Decisions

### Decisão 1 — Técnica: Phaser `tileSprite` para cada camada

Usar `this.add.tileSprite(0, 0, layerWidth, 600, textureKey)` para cada camada, posicionadas em `y = 0` com largura suficiente para cobrir o deslocamento de parallax.

Em `update()`, definir `layer.tilePositionX = -Math.floor(this.cameras.main.scrollX * parallaxFactor)` para cada camada.

Justificativa: `tileSprite` repete a textura horizontalmente, ideal para cenários contínuos; `tilePositionX` controla o deslocamento sem recriar objetos; o `Math.floor` garante posições inteiras (pixel-perfect).

### Decisão 2 — Fatores de parallax por camada

| Camada | Conteúdo | Fator | Deslocamento total (x 0→1600) |
|--------|----------|-------|-------------------------------|
| 1 (céu) | Céu azul com nuvens sutis | 0.0 (estático) | 0 px |
| 2 (serra distante) | Silhuetas de serras | 0.25 | 400 px |
| 3 (caatinga média) | Cacti, formações rochosas | 0.50 | 800 px |
| 4 (vegetação próxima) | Plantas ralas, pedras | 0.75 | 1200 px |

Justificativa: fatores < 1 fazem as camadas moverem mais devagar que a câmera, criando profundidade; o céu estático (0.0) serve como base; a camada mais próxima (0.75) ainda é mais lenta que o primeiro plano do jogo (1.0), preservando a legibilidade das plataformas.

### Decisão 3 — Dimensões das camadas

Cada tileSprite terá altura 600 px (mesma do mundo/viewport) e largura:

- Largura = 800 + (2400 − 800) × fator = 800 + 1600 × fator

Isso garante cobertura completa durante todo o deslocamento de parallax sem áreas vazias.

| Camada | Largura da textura |
|--------|-------------------|
| 1 (céu) | 800 px |
| 2 (serra) | 1200 px |
| 3 (caatinga) | 1600 px |
| 4 (vegetação) | 2000 px |

### Decisão 4 — Ordem de renderização (z-index)

As camadas são adicionadas antes do chão e plataformas, em ordem de trás para frente (céu primeiro, vegetação por último entre as camadas de fundo). Assim, plataformas, obstáculos, slime e jogador ficam sempre sobrepostas ao fundo.

### Decisão 5 — Especificação de assets (fornecidos e aprovados externamente)

Os 4 PNGs de fundo são produzidos e aprovados externamente (fora do Cline). O Cline não desenha nem produz assets. A integração só inicia após os 4 arquivos estarem presentes no repositório e aprovados.

Especificação contratada para cada asset:

| Item | Especificação |
|------|--------------|
| Quantidade | 4 PNGs (céu, serra, caatinga, vegetação) |
| Pasta | `assets/background/nordestino/` |
| Altura | 600 px (igual à altura do mundo/viewport) |
| Largura | Mínimo conforme tabela da Decisão 3; múltiplo de 800 px para tiling |
| Transparência | Canal alpha onde não houver arte; camadas atrás visíveis em áreas transparentes |
| Paleta | Cores terrosas (areia, ocre, terracota, verde seco, azul céu) coerentes com o estilo existente |
| Estilo | Pixel art: cores sólidas, contornos nítidos 1–2 px, sem degradês, sem antialiasing, sem borrão |
| Repetição | Tiling horizontal sem costura visível |
| Filtro | nearest-neighbor (sem interpolação) |

## Risks / Trade-offs

- **[tilePositionX com valores não inteiros]** → tremor sub-pixel na arte pixelada. *Mitigação*: aplicar `Math.floor()` antes de atribuir a `tilePositionX`; `roundPixels: true` já está ativo.
- **[Áreas vazias nas extremidades do parallax]** → camada não cobre todo o deslocamento. *Mitigação*: dimensões calculadas na Decisão 3 cobrem o pior caso (fator 0.75 → deslocamento 1200 px); largura mínima dos assets garante cobertura.
- **[Desalinhamento vertical com o chão]** → fundo parece "flutuar". *Mitigação*: todas as camadas têm altura 600 px e `y = 0`, alinhadas ao topo do mundo; o chão fica em y=555 como antes.
- **[Impacto de desempenho]** → 4 tileSprites adicionais. *Mitigação*: tileSprites são leves (uma textura repetida), sem física; impacto desprezível em desktop/mobile.
- **[Assets ausentes ou não aprovados]** → implementação bloqueada. *Mitigação*: tarefa 1.1 verifica presença e aprovação dos 4 assets antes de qualquer alteração de código.

## Risks / Trade-offs

- **[tilePositionX com valores não inteiros]** → tremor sub-pixel na arte pixelada. *Mitigação*: aplicar `Math.floor()` antes de atribuir a `tilePositionX`; `roundPixels: true` já está ativo.
- **[Áreas vazias nas extremidades do parallax]** → camada não cobre todo o deslocamento. *Mitigação*: dimensões calculadas na Decisão 3 cobrem o pior caso (fator 0.75 → deslocamento 1200 px).
- **[Desalinhamento vertical com o chão]** → fundo parece "flutuar". *Mitigação*: todas as camadas têm altura 600 px e `y = 0`, alinhadas ao topo do mundo; o chão fica em y=555 como antes.
- **[Impacto de desempenho]** → 4 tileSprites adicionais. *Mitigação*: tileSprites são leves (uma textura repetida), sem física; impacto desprezível em desktop/mobile.

## Migration Plan

1. Criar assets de fundo em `assets/background/nordestino/` (4 PNGs).
2. Editar `src/scenes/GameScene.ts`: pré-carregar texturas, criar tileSprites em `create()`, atualizar `tilePositionX` em `update()`.
3. `npm run build` deve passar com exit 0.
4. `openspec validate cenario-visual-nordestino --strict` deve passar.
5. Verificação visual no navegador: parallax suave, sem borrão, sem áreas vazias, camadas atrás do cenário, console limpo.

## Open Questions

Nenhuma — estratégia de parallax, dimensões e ordem de renderização estão definidas.