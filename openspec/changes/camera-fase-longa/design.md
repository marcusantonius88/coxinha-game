# Design — camera-fase-longa

## Context

A cena atual (`src/scenes/GameScene.ts`) é uma seção de plataforma que cabe inteira na viewport 800×600. Ver `proposal.md` para a motivação.

Restrições técnicas relevantes (verificadas no código e em `node_modules/phaser`):

- O corpo do jogador é um `Phaser.GameObjects.Rectangle` **invisível** (`playerBody`); o sprite visível (`playerVisual`) é reposicionado manualmente a cada `update()` em `body.center.x, body.bottom`. Portanto a câmera **não** pode seguir o sprite: ela deve seguir o `Rectangle`.
- O `Rectangle` NÃO é sincronizado de volta pelo `Body.postUpdate()` — o Arcade Body escreve de volta apenas em game objects que são `Sprite`/`Image` com `body` (ver `node_modules/phaser/src/physics/arcade/Body.js`). A posição do `Rectangle` do jogador é gerenciada pelo `update()` da cena.
- `this.physics.world.bounds` é o retângulo do mundo do Arcade; `body.setCollideWorldBounds(true)` respeita esses bounds. Hoje o world bound default é 800×600, o que já limita o jogador à tela.
- O mundo da câmera (`camera.setBounds`) usa `clampX`/`clampY` com `displayWidth`/`displayHeight`; com zoom 1 e `roundPixels` ativo, `clampX` devolve valores inteiros.
- `Camera.preRender()` (linhas 500-570) aplica `Linear()` no follow, depois `Math.floor` (roundPixels) e só então `clampX`/`clampY` — a ordem é favorável: o arredondamento precede o clamp.

## Goals / Non-Goals

- Goals: mundo 2400×600, câmera horizontal suave e limitada ao mundo, cenário e slime redistribuídos, física intacta.
- Non-Goals (detalhados em `proposal.md`): zoom, rolagem vertical, rotação, transições de fase, checkpoints, vidas, pontuação, novos inimigos, novas dependências.

## Decisions

### Decisão 1 — Largura do mundo: 2400 px (múltiplo exato de 800)

`WORLD_WIDTH = 2400` (= 3 × a largura da viewport) atende ao requisito de "múltiplo exato da largura da viewport" da spec `fase-camara-horizontal`.

*Alternativas consideradas*: 1600 (2×) — fase curta, não transmite sensação de mundo; 3200 (4×) — fase longa demais para o conteúdo existente, aumenta o risco de trecho vazio.

O chão passa a ser `rectangle(WORLD_WIDTH / 2, 560, WORLD_WIDTH, 10)`, cobrindo `x ∈ [0, 2400]`.

### Decisão 2 — A câmera segue o `Rectangle` do corpo, não o sprite

`cameras.main.startFollow(this.playerBody, true, 0.1, 0, 0, 0)`.

- `startFollow` lê `target.x`/`target.y`. Como `playerBody` é um `Rectangle` com posição sincronizada no `update()` (via `body.position` → `body.x`), o alvo acompanha o corpo.
- `roundPixels = true` (2º argumento) → o `Camera.preRender()` arredonda `scrollX`/`scrollY` para inteiros, evitando tremor sub-pixel na arte pixelada. `main.ts` já usa `render.roundPixels: true`, e o zoom é 1 (inteiro), então `renderRoundPixels` fica ativo.
- `lerpX = 0.1` dá rolagem suave (sem saltos bruscos), sem tremor: o arredondamento é aplicado depois do `Linear()`.

### Decisão 3 — Vertical fixo com `lerpY = 0` e bounds de altura igual à viewport

`startFollow` também interpola `scrollY` em direção ao alvo vertical, o que **violaria** o requisito "câmera verticalmente fixa". Esta versão do Phaser (3.90) **não oferece `camera.lockY`**, então a fixação vertical é obtida por dois mecanismos combinados:

1. `lerpY = 0` — desliga a interpolação vertical do follow (`Camera.startFollow` → `this.lerp.set(lerpX, lerpY)`).
2. Altura dos bounds da câmera igual à altura da viewport (`setBounds(0, 0, WORLD_WIDTH, 600)`) — em `BaseCamera.clampY`, com `displayHeight === height === 600`: `by = bounds.y + (dh - height)/2 = 0` e `bh = max(by, by + bounds.height - dh) = 0`. Logo `clampY(y)` devolve **sempre 0**, e como `Camera.preRender()` aplica `clampY` depois do `Linear()` do follow, o `scrollY` permanece 0 em todos os frames.

O enquadramento vertical original (chão em y=555 visível, personagem enquadrado) é preservado: `scrollY = 0` corresponde exatamente à vista atual, sem zoom e sem rotação.

*Alternativas rejeitadas*: `lockY` — não existe no Phaser 3.90 (`Camera`/`BaseCamera` não têm essa propriedade); deadzone (`setDeadzone`) — a deadzone é reposicionada a cada frame e, no eixo Y, ainda permite deriva quando o alvo sai da faixa, além de afetar o eixo X de forma não desejada.

### Decisão 4 — Limites do mundo: `physics.world.setBounds` + `camera.setBounds`

- `this.physics.world.setBounds(0, 0, WORLD_WIDTH, 600)` — define o mundo do Arcade; `body.setCollideWorldBounds(true)` passa a limitar o jogador às bordas do **mundo** (2400), e não mais à tela. Atende à spec de "Limite horizontal do mundo".
- `this.cameras.main.setBounds(0, 0, WORLD_WIDTH, 600)` — habilita `useBounds` e faz `clampX`/`clampY` pararem o scroll nas bordas do mundo, sem áreas vazias.
- `physics.world.setBounds` também garante o limite vertical (chão no y=555) — inalterado.

Como `WORLD_WIDTH` é múltiplo exato de 800 e o zoom é 1, `clampX` nunca produz enquadramento parcial nas bordas.

### Decisão 5 — Distribuição do cenário preservando a física aprovada

Restrições da spec `cenario-plataformas` (inalteradas): topo das plataformas ≤ 130 px acima do chão (topo do chão = 555), vãos horizontais alcançáveis com `jumpForce = -920` e `gravity = 1840` (≈225 px de altura, ≈1,0 s de voo ⇒ ≈200 px de alcance a 200 px/s, ≈350 px a 350 px/s).

Layout em 3 "atos" de 800 px, com o jogador nascendo no primeiro:

- Ato 1 (x 0..800): corredor de spawn livre (x 0..120), plataforma P1 (x 140..330, topo 455), obstáculos A/B (x 360..400 e 410..450), plataforma P2 (x 520..700, topo 425), slime em x=600.
- Ato 2 (x 800..1600): entrada livre, plataforma P3 (x 900..1120, topo 445), obstáculos C/D (x 1200..1240, 1250..1290), P4 (x 1380..1560, topo 435).
- Ato 3 (x 1600..2400): entrada livre, plataforma P5 (x 1700..1900, topo 455), obstáculos E/F (x 2000..2040, 2050..2090), plataforma P6 (x 2150..2330, topo 425).

Todos os vãos entre estruturas ficam ≤ 200 px (alcance com velocidade de caminhada) e ≤ 130 px de desnível — dentro do alcance aprovado. O chão é contínuo, então o percurso é sempre refazível a pé.

### Decisão 6 — Slime reposicionado, mecânica intacta

## Risks / Trade-offs

- **[O `Rectangle` do jogador não é sincronizado pelo Arcade Body]** → o alvo da câmera leria `playerBody.x` desatualizado. *Mitigação*: no `update()` da cena, sincronizar `playerBody.setPosition(body.center.x, body.center.y)` a partir do `body` (fonte de verdade da física); a hitbox 30×30 não muda, pois o `Rectangle` mantém 30×30.
- **[Câmera mirando `playerBody.x` e não o centro]** → `startFollow` usa o `x` cru do game object. *Mitigação*: manter o `Rectangle` com origem padrão (0.5) ⇒ `x` é o centro do hitbox, idêntico a `body.center.x`.
- **[Câmera rolando antes de o jogador existir]** → `startFollow` é chamado em `create()`, após o `playerBody` ser criado.
- **[Tremor da câmera por arredondamento]** → `roundPixels = true` no `startFollow` + `render.roundPixels: true` em `main.ts` + zoom 1.
- **[Trechos "vazios" de cenário na fase extensa]** → mitigado pela distribuição dos atos acima, com espaçamento regular.
- **[Regressão na seleção de animação]** → `updateAnimation()` não é tocado; a animação continua derivada da física.

## Migration Plan

1. Editar `src/scenes/GameScene.ts` (constantes, cenário, slime, câmera, world bounds).
2. `npm run build` deve passar com exit 0 e `tsc` sem erros.
3. `openspec validate camera-fase-longa --strict` deve passar.
4. Verificação manual no navegador: câmera rola para esquerda/direita, para nas bordas, personagem sempre enquadrado, slime com pisada, animações sem regressão, console limpo.
5. Rollback: reverter `src/scenes/GameScene.ts` (change isolada, sem migração de dados).

## Open Questions

Nenhuma — largura do mundo, comportamento da câmera e distribuição do cenário estão definidos nas specs desta change.

O slime (corpo estático 40×40, base no chão) é movido para `x = 600`, mantendo a mesma lógica de `handleEnemyContact()` (derrota só por pisada, `DEFEAT` uma vez, impulso `-690`). Nenhuma alteração em `inimigo-base` além do texto da spec que passa a citar "limites do mundo".
