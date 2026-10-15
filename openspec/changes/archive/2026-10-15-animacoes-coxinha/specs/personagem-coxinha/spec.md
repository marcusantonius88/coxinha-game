# Spec Delta

## ADDED Requirements

### Requirement: Representação visual animada do Coxinha

O sistema SHALL utilizar como fonte visual ativa do personagem um asset de pixel art 16-bit preparado como sprite sheet técnica, com frames consistentes e fundo transparente.

O asset SHALL representar fielmente o Coxinha: Bulldog Francês de pelagem caramelo, focinho escuro, peito claro e orelhas eretas.

O sistema SHALL NOT utilizar `assets/coxinha/coxinha-sprite-sheet.png` como fonte de recorte automático de frames, nem tratar `assets/coxinha/coxinha-idle.png` como a fonte visual ativa. Ambos os assets permanecem no projeto para uso futuro.

O sistema SHALL exibir animações para os estados `IDLE`, `WALK`, `RUN`, `JUMP`, `FALL` e `LAND`.

A representação visual SHALL permanecer separada do corpo físico: o visual segue o corpo a cada frame e SHALL NOT interferir no posicionamento, na detecção de colisões ou na movimentação.

#### Scenario: Cena inicial com animações registradas

- **WHEN** a cena inicial `GameScene` é carregada
- **THEN** o asset técnico de frames é carregado antes de ser utilizado
- **AND** as animações `IDLE`, `WALK`, `RUN`, `JUMP`, `FALL` e `LAND` são registradas e disponíveis
- **AND** o personagem inicia exibindo `IDLE`
- **AND** o visual acompanha o corpo físico a cada frame

#### Scenario: Sprite sheet de apresentação não usada tecnicamente

- **WHEN** os frames das animações são obtidos
- **THEN** a origem dos frames é o novo asset técnico de pixel art com fundo transparente
- **AND** `assets/coxinha/coxinha-sprite-sheet.png` não é utilizada para recorte automático
- **AND** `assets/coxinha/coxinha-idle.png` não é a fonte visual ativa

### Requirement: Seleção automática de animação conforme o estado

O sistema SHALL selecionar automaticamente a animação correspondente ao estado real do personagem:

- `IDLE` quando o personagem está parado no chão;
- `WALK` quando o personagem está caminhando;
- `RUN` quando o personagem está correndo;
- `JUMP` durante a subida;
- `FALL` durante a descida;
- `LAND` durante a aterrissagem.

O sistema SHALL iniciar uma animação somente quando o estado do personagem muda, mantendo a animação atual em execução enquanto o estado persistir, sem reiniciar continuamente a mesma animação durante o gameplay.

A animação `LAND` SHALL ser exibida ao aterrissar e SHALL transitar para a animação do estado em terra assim que o aterrissar estiver concluído.

As animações SHALL mudar conforme o estado físico do personagem sem exigir alteração dos controles ou da física existente.

#### Scenario: Parado no chão

- **WHEN** o personagem está apoiado sobre a plataforma sem se mover horizontalmente
- **THEN** a animação exibida é `IDLE`

#### Scenario: Caminhando

- **WHEN** o personagem se move horizontalmente com a velocidade normal
- **THEN** a animação exibida é `WALK`

#### Scenario: Correndo

- **WHEN** o personagem se move horizontalmente com a velocidade de corrida
- **THEN** a animação exibida é `RUN`

#### Scenario: Subindo após o salto

- **WHEN** o personagem está no ar com movimento vertical para cima
- **THEN** a animação exibida é `JUMP`

#### Scenario: Descendo

- **WHEN** o personagem está no ar com movimento vertical para baixo
- **THEN** a animação exibida é `FALL`

#### Scenario: Aterrissando

- **WHEN** o personagem retorna à plataforma após estar no ar
- **THEN** a animação exibida é `LAND`
- **AND** ao concluir `LAND` a animação passa para o estado em terra correspondente ao movimento atual

#### Scenario: Mesma animação não reiniciada

- **WHEN** o estado do personagem permanece o mesmo entre frames consecutivos
- **THEN** a animação atual continua em execução do ponto em que estava
- **AND** a animação não é reiniciada

## MODIFIED Requirements

### Requirement: Preservação da física e movimentação

O sistema SHALL preservar o comportamento físico e de movimentação existente da capacidade `jogo-inicial`.

A introdução das animações SHALL NOT alterar intencionalmente:

- velocidade normal;
- velocidade de corrida;
- força do salto;
- gravidade;
- hitbox;
- colisão com a plataforma;
- controles de teclado;
- limites horizontais da área de jogo;
- impulso vertical da pisada nos inimigos;
- mecânica de derrota do inimigo ao pular sobre ele.

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

#### Scenario: Pisada preservada

- **WHEN** o personagem cai sobre o inimigo durante um salto
- **THEN** o inimigo é derrotado como antes
- **AND** o personagem recebe o impulso vertical para cima existente

## REMOVED Requirements

### Requirement: Pose IDLE do Coxinha na cena

**Reason:** A representação estática de imagem única é substituída pelo sistema de animações básicas desta change; o requisito descrevia exclusivamente a pose `IDLE` e a não-execução de animações, comportamento agora contradito pelo novo sistema.

**Migration:** A fonte visual e a exibição do personagem passam a ser cobertas pelos requisitos "Representação visual animada do Coxinha" e "Seleção automática de animação conforme o estado". Os assets `coxinha-idle.png` e `coxinha-sprite-sheet.png` permanecem no projeto sem uso ativo.

### Requirement: Estrutura preparada para futuras animações

**Reason:** As animações `WALK`, `RUN`, `JUMP`, `FALL` e `LAND` deixam de ser futuras e passam a fazer parte do comportamento exigido por esta change; `HIT` permanece fora do escopo (definido no escopo negativo da proposal, junto com ataque, dano e morte).

**Migration:** Coberto pelos requisitos "Representação visual animada do Coxinha" e "Seleção automática de animação conforme o estado"; a estrutura reutilizável existente (visual separado do corpo físico) permanece preservada pelo requisito "Preservação da física e movimentação".


