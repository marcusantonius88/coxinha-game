# Spec Delta

## MODIFIED Requirements

### Requirement: Pulo

O sistema SHALL permitir que o personagem pule utilizando `ArrowUp` ou `Space`.

O personagem SHALL poder iniciar um salto somente quando estiver apoiado sobre a plataforma.

Um salto pleno (iniciado a partir do repouso sobre a plataforma e completado sem colisões intermediárias) SHALL ter duração total aproximada de 1,2 s, dentro da faixa aceitável de 1,0 s a 1,4 s.

Um salto pleno SHALL alcançar altura máxima aproximada de 240 px, dentro da faixa aceitável de 220 px a 260 px.

O ajuste de duração e altura do salto SHALL preservar a sensação de controle responsiva sem alterar a velocidade horizontal, a corrida ou a hitbox do personagem.

#### Scenario: Pulo utilizando ArrowUp

- **WHEN** o jogador pressiona `ArrowUp` enquanto o personagem está apoiado sobre a plataforma
- **THEN** o personagem recebe uma velocidade vertical inicial para cima

#### Scenario: Pulo utilizando Space

- **WHEN** o jogador pressiona `Space` enquanto o personagem está apoiado sobre a plataforma
- **THEN** o personagem recebe uma velocidade vertical inicial para cima

#### Scenario: Pulo durante o salto

- **WHEN** o jogador pressiona `ArrowUp` ou `Space` enquanto o personagem está no ar
- **THEN** o sistema ignora a solicitação de pulo
- **AND** o personagem não inicia um segundo salto

#### Scenario: Duração e altura do salto pleno

- **WHEN** o jogador pressiona `ArrowUp` ou `Space` com o personagem apoiado sobre a plataforma e o salto se completa sem colisões intermediárias
- **THEN** o personagem retorna à plataforma em um tempo total entre 1,0 s e 1,4 s
- **AND** a altura máxima alcançada pelo personagem fica entre 220 px e 260 px
