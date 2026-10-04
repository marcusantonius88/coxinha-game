# Design

## Context

A capacidade `jogo-inicial` está implementada com um personagem temporário representado por uma forma geométrica.

O asset `assets/coxinha/coxinha-idle.png` é uma imagem única que representa a pose estática `IDLE` do Coxinha e será utilizado nesta change.

O asset `assets/coxinha/coxinha-sprite-sheet.png` permanece no projeto como referência para futuras animações, mas não será utilizado pela implementação desta change.

Esta change substitui somente a representação visual do personagem, preservando a lógica de movimentação, física, controles, colisões e limites da área de jogo já implementados.

## Goals / Non-Goals

### Goals

- Substituir o personagem geométrico temporário pela pose estática `IDLE` do asset `assets/coxinha/coxinha-idle.png`.
- Utilizar o asset como uma imagem única, sem tratamento como sprite sheet.
- Utilizar o sistema de carregamento de imagens do Phaser para disponibilizar o asset na cena.
- Exibir o Coxinha utilizando a imagem carregada.
- Manter a física ARCADE existente.
- Manter a hitbox existente.
- Manter os controles existentes.
- Manter as velocidades de movimento e corrida existentes.
- Manter a gravidade existente.
- Manter as colisões existentes.
- Manter os limites horizontais da área de jogo.
- Manter `assets/coxinha/coxinha-sprite-sheet.png` no projeto como asset de referência para futuras animações.
- Manter a representação visual suficientemente separada da lógica de movimentação e física para permitir a implementação futura de animações.

### Non-Goals

- Implementar animações.
- Implementar `WALK`.
- Implementar `RUN`.
- Implementar `JUMP`.
- Implementar `FALL`.
- Implementar `LAND`.
- Implementar `HIT`.
- Utilizar `load.spritesheet()` para o personagem nesta change.
- Utilizar `coxinha-sprite-sheet.png` como fonte visual ativa nesta change.
- Alterar mecânicas de movimento.
- Alterar velocidades de movimento ou corrida.
- Alterar força do salto.
- Alterar gravidade.
- Alterar colisões.
- Alterar a hitbox existente.
- Alterar os controles.
- Alterar os limites horizontais.
- Alterar `package.json`.
- Alterar `tsconfig.json`.
- Alterar `vite.config.ts`.
- Adicionar sons ou efeitos sonoros.
- Adicionar HUD.
- Adicionar menus.
- Adicionar novas mecânicas de gameplay.

## Decisions

### Asset Visual

- **Escolhido:** `assets/coxinha/coxinha-idle.png`.
- **Tipo:** imagem única.
- **Pose:** `IDLE`.
- **Estilo:** pixel art inspirado em jogos 16-bit.
- **Personagem:** Bulldog Francês baseado nas referências visuais reais do Coxinha.

O asset representa exclusivamente a pose estática utilizada nesta change.

### Sprite Sheet Futura

O arquivo `assets/coxinha/coxinha-sprite-sheet.png` permanecerá no projeto como referência para futuras animações.

Esse arquivo não deverá ser carregado nem utilizado como representação visual do personagem nesta change.

Uma change futura poderá utilizar esse asset para implementar animações como:

- `IDLE`;
- `WALK`;
- `RUN`;
- `JUMP`;
- `FALL`;
- `LAND`;
- `HIT`.

### Carregamento do Asset

O asset deverá ser carregado pela cena Phaser antes de ser utilizado.

A implementação deverá utilizar o carregamento de imagem do Phaser, utilizando uma chave identificável, como:

`coxinha-idle`

A representação visual deverá utilizar a imagem carregada como um único recurso.

A implementação não deverá utilizar `load.spritesheet()` para o personagem nesta change.

### Representação Visual e Física

A substituição do personagem geométrico pelo sprite visual não deverá alterar intencionalmente o comportamento físico existente.

O corpo físico do personagem deverá permanecer separado da representação visual o suficiente para permitir ajustes visuais sem modificar a lógica de física.

A substituição do elemento visual SHALL NOT alterar as dimensões do corpo físico existente.

Caso o tamanho do sprite visual seja diferente do personagem temporário, a escala, posição visual ou offset poderão ser ajustados sem alterar a hitbox existente.

### Física e Hitbox

A física existente deverá permanecer inalterada.

Devem ser preservados:

- física ARCADE;
- gravidade `y: 300`;
- hitbox existente;
- colisão com a plataforma;
- `setCollideWorldBounds(true)`;
- limites horizontais da área de jogo;
- comportamento de aterrissagem.

A substituição do visual não deverá exigir alterações nas dimensões ou no comportamento da hitbox.

### Controles e Movimentação

Os controles existentes deverão permanecer inalterados:

| Ação | Tecla |
|---|---|
| Mover para esquerda | `ArrowLeft` |
| Mover para direita | `ArrowRight` |
| Correr | `Shift` + direção |
| Pular | `ArrowUp` ou `Space` |

As velocidades de movimento normal e corrida, assim como a força do salto, deverão permanecer iguais às definidas na implementação da capacidade `jogo-inicial`.

### Estrutura do Personagem

A referência utilizada pela lógica de controle deverá continuar representando o personagem controlável.

A representação visual deverá permanecer suficientemente separada da lógica de movimentação e física para permitir que uma futura change substitua a imagem estática por um sistema de animação.

Essa preparação não deverá introduzir um sistema de animação nesta change.

A implementação futura de animações deverá poder reutilizar a lógica existente de movimentação e física sem exigir sua reimplementação.

### Integração com a Cena

A cena `GameScene` deverá:

1. Carregar `assets/coxinha/coxinha-idle.png`.
2. Criar a representação visual do Coxinha utilizando a imagem carregada.
3. Preservar a estrutura física existente do personagem.
4. Preservar os controles existentes.
5. Preservar a colisão com a plataforma.
6. Preservar os limites horizontais da área de jogo.
7. Posicionar visualmente o Coxinha de forma adequada sobre a plataforma.
8. Garantir que a representação visual não seja cortada pela plataforma ou pela área de jogo.

## Risks / Trade-offs

### Asset Inicial

O asset `coxinha-idle.png` representa a primeira versão visual do protagonista e poderá ser refinado em changes futuras.

Isso não impede a evolução do personagem, pois a representação visual está sendo tratada separadamente da lógica física.

### Diferença de Dimensões

O tamanho do asset visual pode ser diferente do personagem temporário.

A escala ou o posicionamento visual poderão ser ajustados para adequar o personagem à cena, desde que a hitbox e o comportamento físico sejam preservados.

### Sprite Sheet Futura

A sprite sheet existente contém recursos destinados a futuras animações, mas sua utilização nesta change aumentaria desnecessariamente a complexidade da implementação.

Por isso, ela permanece no projeto como asset futuro e não participa da implementação atual.

### Evolução do Personagem

A utilização de uma imagem única nesta change mantém o escopo pequeno e permite validar a integração do personagem real antes da introdução do sistema de animações.

Uma change futura poderá substituir a imagem estática por uma estrutura de animação sem necessidade de reimplementar as mecânicas básicas de movimentação e física.