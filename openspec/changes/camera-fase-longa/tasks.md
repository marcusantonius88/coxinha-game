# Tasks

## 1. Mundo e limites

- [ ] 1.1 Declarar as constantes `WORLD_WIDTH = 2400` e `WORLD_HEIGHT = 600` em `src/scenes/GameScene.ts` (múltiplo exato de 3× a viewport de 800 px) — verificação: `grep -n 'WORLD_WIDTH' src/scenes/GameScene.ts` retorna as declarações e `npm run build` passa sem erros de tipo.
- [ ] 1.2 Configurar `this.physics.world.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT)` em `create()`, antes da criação do jogador, para que `body.setCollideWorldBounds(true)` limite o personagem às bordas do mundo (2400) e não mais à viewport — verificação: no navegador, o Coxinha para em x≈2400 à direita e em x≈0 à esquerda, sem sair da área do mundo.
- [ ] 1.3 Estender o chão para `rectangle(WORLD_WIDTH / 2, 560, WORLD_WIDTH, 10)`, mantendo a linha de superfície em y=555 idêntica à atual — verificação: o chão cobre `x ∈ [0, 2400]` e a base do jogador continua em y=555.

## 2. Cenário redistribuído

- [ ] 2.1 Redefinir `SCENE_STRUCTURES` em 3 atos de 800 px (P1/P2 no ato 1, P3/P4 no ato 2, P5/P6 no ato 3), com obstáculos duplos entre plataformas, respeitando topo ≤ 130 px acima do chão e vãos ≤ 200 px — verificação: `grep` em `src/scenes/GameScene.ts` mostra 12 estruturas cobrindo `x ∈ [140, 2330]`, e `npm run build` passa.
- [ ] 2.2 Verificar que o percurso é atravessável de ponta a ponta nos dois sentidos, sem alteração de gravidade (1840), salto (-920), velocidades (200/350) ou hitbox (30×30) — verificação: no navegador, o jogador percorre de x=0 a x=2400 e volta, aterrissando sobre as plataformas, sendo bloqueado pelos obstáculos e podendo saltar a partir delas.

## 3. Câmera horizontal

- [ ] 3.1 Configurar `this.cameras.main.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT)` e `this.cameras.main.startFollow(this.playerBody, true, 0.1, 0)` — `roundPixels = true`, `lerpX = 0.1`, `lerpY = 0`; nenhum zoom (1) nem rotação (0) — verificação: `grep -n 'startFollow' src/scenes/GameScene.ts` mostra o `lerpY = 0` e `zoom`/`rotation` permanecem inalterados.
- [ ] 3.2 Confirmar a fixação vertical: com `lerpY = 0` e bounds de altura igual à viewport, `clampY` mantém `scrollY = 0` em todos os frames — verificação: no navegador, ao pular, cair e aterrissar, `cameras.main.scrollY` permanece 0 e o enquadramento vertical não muda.
- [ ] 3.3 Sincronizar `playerBody.setPosition(body.center.x, body.center.y)` no `update()` da cena, antes do follow, para que o alvo da câmera refita a posição real da física (o `Rectangle` não é sincronizado pelo Arcade Body) — verificação: a câmera acompanha o Coxinha sem defasagem perceptível ao andar e correr.

## 4. Slime e mecânicas preservadas

- [ ] 4.1 Reposicionar o slime para `x = 600` (base no chão, corpo estático 40×40, visual com a mesma origem) e manter `handleEnemyContact()` inalterado — verificação: no navegador, o slime está no percurso, é derrotado por pisada uma única vez com animação `DEFEAT` e impulso -690, e colisões laterais não o derrotam.

## 5. Verificação integrada

- [ ] 5.1 Rodar `npm run build` após todos os ajustes — verificação: exit code 0 (`tsc` sem erros + bundle Vite gerado).
- [ ] 5.2 Conferir no navegador os cenários da spec `fase-camara-horizontal`: câmera rola para a esquerda/direita, para nos limites do mundo sem áreas vazias, retoma o acompanhamento ao afastar da borda, personagem sempre enquadrado, `scrollY` constante, zoom 1 e rotação 0, arte pixelada nítida sem tremor — verificação: checklist executado com o jogo rodando (`npm run preview`) e resultado registrado; console limpo.
- [ ] 5.3 Validar os artefatos da change — verificação: `openspec validate camera-fase-longa --strict` retorna exit 0 e `openspec status --change camera-fase-longa` mostra 4/4 artefatos completos com todas as tasks marcadas.
