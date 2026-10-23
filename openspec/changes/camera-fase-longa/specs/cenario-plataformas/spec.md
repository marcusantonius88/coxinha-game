# Spec Delta

## MODIFIED Requirements

### Requirement: Percurso viável com a física existente

As posições e dimensões das plataformas e dos obstáculos SHALL ser compatíveis com os parâmetros físicos atuais (gravidade `1840`, força do salto `-920`, velocidades `200` e `350`, hitbox `30×30`), sem que esses parâmetros sejam alterados.

Toda estrutura SHALL ser alcançável ou superável dentro do alcance do salto atual (altura máxima aproximada de 225 px e alcance horizontal compatível com o tempo de voo de ≈1,0 s).

Nenhuma plataforma ou obstáculo SHALL bloquear permanentemente o caminho nem criar situação impossível de superar; o percurso SHALL poder ser percorrido nos dois sentidos, inclusive descendo de estruturas elevadas de volta ao chão.

A seção SHALL ocupar uma fase horizontalmente extensa, mais larga que a área de jogo visível, de modo que a travessia da fase dependa de rolagem de câmera horizontal.

O chão, as plataformas elevadas e os obstáculos SHALL ser distribuídos por essa extensão, e o slime SHALL permanecer no percurso, com a mecânica de derrota por pisada funcional na nova posição.

#### Scenario: Salto dentro do alcance

- **WHEN** o personagem precisa alcançar uma plataforma ou superar um obstáculo
- **THEN** a altura necessária está dentro do alcance do salto atual
- **AND** a tentativa é bem-sucedida sem alterar gravidade, força do salto ou velocidades

#### Scenario: Sem bloqueio permanente

- **WHEN** o personagem percorre a seção para a esquerda ou para a direita, em terra ou nas plataformas
- **THEN** nenhuma estrutura impede o avanço
- **AND** é possível descer de qualquer plataforma de volta ao chão e continuar

#### Scenario: Parâmetros de física preservados

- **WHEN** a seção de plataformas é adicionada ao cenário
- **THEN** gravidade, força do salto, impulso da pisada e hitbox do personagem permanecem inalterados

#### Scenario: Seção excede a área visível

- **WHEN** a fase é carregada
- **THEN** a seção é mais larga que a área de jogo visível
- **AND** a travessia completa depende de rolagem de câmera horizontal
- **AND** o percurso continua atravessável de ponta a ponta nos dois sentidos

### Requirement: Cenário e sistemas existentes preservados

A adição das plataformas e obstáculos SHALL preservar o chão existente, o limite horizontal do mundo e a interação completa com o slime (derrota por pisada, animação `DEFEAT`, impulso).

As animações aprovadas do Coxinha e a mecânica de pisada SHALL permanecer inalteradas.

O sistema SHALL NÃO adicionar inimigos novos, dano, vidas, pontuação, checkpoints nem sistema de fases.

O sistema SHALL implementar câmera com rolagem horizontal nesta change, limitada às bordas do mundo; a rolagem vertical, o zoom e a rotação de câmera SHALL NOT ser implementados.

#### Scenario: Chão e limites preservados

- **WHEN** o personagem transita pelo cenário
- **THEN** o chão original continua funcional como superfície de suporte
- **AND** o limite horizontal do mundo continua impedindo a saída da área do mundo

#### Scenario: Interação com o slime preservada

- **WHEN** o personagem executa uma pisada válida sobre o slime
- **THEN** o slime é derrotado com `DEFEAT` uma única vez, como antes
- **AND** o personagem recebe o impulso existente
- **AND** colisões laterais com o slime continuam não o derrotando

#### Scenario: Animações do Coxinha preservadas

- **WHEN** o personagem transita entre chão, obstáculos e plataformas
- **THEN** as animações `IDLE`, `WALK`, `RUN`, `JUMP`, `FALL` e `LAND` são selecionadas como atualmente
- **AND** a seleção de animação não é alterada pela presença das estruturas

#### Scenario: Câmera horizontal limitada ao mundo

- **WHEN** a fase é percorrida com a câmera ativa
- **THEN** a câmera rola apenas no eixo horizontal
- **AND** a câmera para nos limites do mundo, sem exibir áreas vazias além das bordas
- **AND** não há rolagem vertical, zoom nem rotação de câmera
