# Spec Delta

## MODIFIED Requirements

### Requirement: Preservação das mecânicas existentes

A interação com o inimigo SHALL preservar as mecânicas já implementadas das capacidades `jogo-inicial` e `personagem-coxinha`.

A implementação desta change SHALL NÃO alterar:

- velocidade normal de movimento;
- velocidade de corrida;
- força do salto;
- gravidade;
- hitbox do personagem;
- colisão do personagem com a plataforma;
- controles de teclado;
- limites horizontais do mundo.

#### Scenario: Movimentação preservada

- **WHEN** o jogador utiliza os controles existentes
- **THEN** o personagem continua podendo andar para esquerda e direita
- **AND** o personagem continua podendo correr utilizando `Shift`
- **AND** o personagem continua podendo pular utilizando `ArrowUp` ou `Space`
- **AND** o personagem continua impedido de executar um segundo salto enquanto estiver no ar

#### Scenario: Física preservada

- **WHEN** o personagem está sujeito à gravidade na cena com o inimigo
- **THEN** ele continua sendo afetado pela física ARCADE
- **AND** continua colidindo com a plataforma
- **AND** retorna à plataforma após um salto
