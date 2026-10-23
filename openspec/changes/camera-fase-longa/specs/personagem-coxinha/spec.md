# Spec Delta

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
- limites horizontais do mundo;
- impulso vertical da pisada nos inimigos;
- mecânica de derrota do inimigo ao pular sobre ele.

#### Scenario: Movimentação preservada

- **WHEN** o personagem utiliza os controles existentes
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
