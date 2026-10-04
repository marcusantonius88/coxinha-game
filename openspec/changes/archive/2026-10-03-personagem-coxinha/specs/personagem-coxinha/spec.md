# Spec Delta

## Purpose

Definir a identidade visual inicial do personagem Coxinha na cena jogável, substituindo o personagem geométrico temporário pela pose estática `IDLE` do asset `assets/coxinha/coxinha-idle.png`.

A mudança deve preservar o comportamento já implementado na capacidade `jogo-inicial`, incluindo movimentação, corrida, salto, física, colisões, hitbox e limites da área de jogo.

## ADDED Requirements

### Requirement: Pose IDLE do Coxinha na cena

O sistema SHALL utilizar o asset `assets/coxinha/coxinha-idle.png` como fonte visual do personagem.

O asset SHALL ser tratado como uma imagem única correspondente à pose estática `IDLE`.

O sistema SHALL NOT utilizar `assets/coxinha/coxinha-sprite-sheet.png` como fonte visual ativa nesta change.

As demais poses existentes na sprite sheet permanecem no projeto para uso em changes futuras.

#### Scenario: Coxinha exibido na cena

- **WHEN** a cena inicial `GameScene` é carregada
- **THEN** o personagem exibido utiliza `assets/coxinha/coxinha-idle.png`
- **AND** a representação visual possui estilo pixel art 16-bit
- **AND** o personagem não é mais representado pelo retângulo temporário
- **AND** nenhuma animação é executada

#### Scenario: Asset IDLE carregado

- **WHEN** a cena inicial é carregada
- **THEN** `assets/coxinha/coxinha-idle.png` é carregado antes de ser utilizado pelo personagem
- **AND** o asset é tratado como uma imagem única
- **AND** a imagem corresponde à pose `IDLE` do Coxinha

#### Scenario: Sprite sheet futura não utilizada

- **WHEN** a cena inicial é carregada
- **THEN** `assets/coxinha/coxinha-sprite-sheet.png` não é utilizado como representação visual do personagem
- **AND** nenhuma animação é criada a partir da sprite sheet

### Requirement: Preservação da física e movimentação

O sistema SHALL preservar o comportamento físico e de movimentação existente da capacidade `jogo-inicial`.

A substituição do visual SHALL NOT alterar intencionalmente:

- velocidade normal;
- velocidade de corrida;
- força do salto;
- gravidade;
- hitbox;
- colisão com a plataforma;
- controles de teclado;
- limites horizontais da área de jogo.

#### Scenario: Movimentação preservada

- **WHEN** o jogador utiliza os controles existentes
- **THEN** o personagem continua podendo andar para esquerda e direita
- **AND** o personagem continua podendo correr utilizando `Shift`
- **AND** o personagem continua podendo pular utilizando `ArrowUp` ou `Space`
- **AND** o personagem continua impedido de executar um segundo salto enquanto estiver no ar

#### Scenario: Física preservada

- **WHEN** o personagem está sujeito à gravidade
- **THEN** ele continua sendo afetado pela física ARCADE
- **AND** continua colidindo com a plataforma
- **AND** retorna à plataforma após um salto

### Requirement: Hitbox preservada

O sistema SHALL manter a hitbox utilizada pelo personagem antes da substituição visual.

A alteração da representação visual SHALL NOT alterar intencionalmente as dimensões ou o comportamento da hitbox.

#### Scenario: Sprite visual possui dimensões diferentes

- **WHEN** o tamanho visual do sprite do Coxinha for diferente do personagem temporário
- **THEN** a escala ou o posicionamento visual poderá ser ajustado
- **AND** a hitbox existente permanece preservada

### Requirement: Estrutura preparada para futuras animações

O sistema SHALL manter a representação visual do personagem estruturada de forma que futuras animações possam ser adicionadas sem exigir a reimplementação da lógica de movimentação e física existente.

As animações `WALK`, `RUN`, `JUMP`, `FALL`, `LAND` e `HIT` NÃO fazem parte desta change.

#### Scenario: Preparação para futuras animações

- **WHEN** a implementação atual é analisada
- **THEN** a lógica de movimentação e física existente permanece reutilizável
- **AND** a representação visual `IDLE` pode futuramente ser substituída por um sistema de animação
- **AND** nenhuma das animações futuras é executada nesta change

## REMOVED Requirements

<!-- Nenhuma -->