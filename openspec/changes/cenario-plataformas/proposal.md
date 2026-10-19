# Proposal

## Why

O jogo funciona em um cenário plano único: chão reto de 800 px, um slime e nenhuma estrutura vertical — todo desafio se resume a um salto no mesmo nível. Com o Coxinha animado, o inimigo visual e a física de salto já aprovados (≈225 px de altura, 1,0 s no ar), o próximo passo natural é dar volume ao cenário: plataformas elevadas e obstáculos que transformem a cena em uma pequena seção de plataforma 2D jogável, sem tocar nas mecânicas congeladas.

## What Changes

- Adicionar **plataformas elevadas sólidas** no cenário inicial, nas quais o Coxinha pode aterrissar, apoiar-se e saltar novamente, mantendo a colisão sólida por baixo e pelas laterais.
- Adicionar **obstáculos sólidos simples** no percurso, superáveis com os controles de salto existentes (`Space`/`ArrowUp`, com ou sem `Shift`).
- Posicionar e dimensionar as estruturas dentro do envelope alcançável com a física atual (gravidade `1840`, salto `-920`, velocidades `200`/`350`, hitbox `30×30` — **nenhum desses parâmetros muda**), garantindo que todo o percurso seja viável e que nada bloqueie permanentemente o caminho.
- Manter o chão, os limites horizontais da área de jogo, a interação com o slime (pisada, `DEFEAT`, impulso) e todas as animações aprovadas do Coxinha.
- Representar as estruturas com formas e cores coerentes com o estilo pixel art atual (retângulos de cor sólida da paleta de terra existente, coordenadas inteiras, renderização pixel-perfect preservada).
- Fora de escopo (não implementar nesta change): inimigos novos, dano, vidas, pontuação, checkpoints, sistema de fases, câmera com rolagem (a seção inteira cabe na tela fixa de 800×600), sprites novos, sons e qualquer alteração de física/hitbox/controles/animações.

## Capabilities

### New Capabilities

- `cenario-plataformas`: seção de plataforma do cenário — plataformas elevadas sólidas, obstáculos sólidos, viabilidade do percurso com a física existente e preservação dos elementos do cenário atual (chão, limites, slime, animações).

### Modified Capabilities

(nenhuma — `jogo-inicial`, `personagem-coxinha` e `inimigo-base` permanecem satisfatórios: o chão continua existindo, os requisitos de salto/gravidade/limites são invariantes preservados, e a interação com o slime não muda.)

## Impact

- Código: `src/scenes/GameScene.ts` — `create()` cria as estruturas estáticas (grupo Arcade estático ou retângulos com corpos estáticos) e um colisor com o `playerBody`; nenhum outro sistema tocado (update, máquina de animações, stomp e `handleEnemyContact` permanecem intactos).
- Assets: nenhum PNG criado ou alterado (estruturas são formas sólidas como o chão atual).
- Sem mudanças de física, controles, renderização (`main.ts` intocado) ou de build.
- Verificação posterior na aplicação: `npm run build` (exit 0) + `openspec validate --strict` + harness de navegador (aterrissar nas plataformas, colisões laterais/superiores, travessia do percurso, slime intacto, sem erros de console).
