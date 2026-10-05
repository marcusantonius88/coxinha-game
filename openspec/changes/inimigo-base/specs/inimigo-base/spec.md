# Spec Delta

## Purpose

Introduzir o primeiro inimigo da cena inicial, com hitbox própria e comportamento parado, estabelecendo a mecânica básica de derrota por pisada: Coxinha derrota o inimigo ao cair sobre a sua parte superior durante um salto e recebe um pequeno impulso para cima, enquanto colisões laterais ou por baixo não o derrotam.

## ADDED Requirements

### Requirement: Inimigo presente na cena inicial

O sistema SHALL exibir um inimigo na cena inicial, posicionado sobre a plataforma.

O inimigo SHALL possuir uma hitbox própria, independente da hitbox do personagem.

O inimigo SHALL permanecer parado, sem se movimentar por conta própria.

O inimigo SHALL ter representação visual visível na cena.

#### Scenario: Cena inicial carregada

- **WHEN** a cena inicial é carregada
- **THEN** um inimigo é exibido sobre a plataforma
- **AND** o inimigo permanece em repouso durante o decorrer da cena
- **AND** o inimigo não se desloca por conta própria

#### Scenario: Hitbox própria

- **WHEN** o personagem e o inimigo coexistem na cena
- **THEN** cada um possui sua própria hitbox física
- **AND** a hitbox do inimigo é independente da hitbox do personagem

### Requirement: Derrota por pisada

O sistema SHALL derrotar o inimigo quando o personagem cai sobre a parte superior do inimigo durante um salto.

Após a derrota, o inimigo SHALL deixar de ser exibido e SHALL deixar de interagir fisicamente com o personagem.

#### Scenario: Pisada sobre a parte superior

- **WHEN** o personagem, durante um salto, cai com sua hitbox sobre a parte superior da hitbox do inimigo
- **THEN** o inimigo é derrotado
- **AND** o inimigo deixa de ser exibido na cena
- **AND** o inimigo deixa de colidir com o personagem

#### Scenario: Colisão lateral

- **WHEN** o personagem colide com o inimigo pelos lados
- **THEN** o inimigo não é derrotado
- **AND** o inimigo permanece na cena
- **AND** o contato é tratado como colisão física normal, sem atravessar o inimigo

#### Scenario: Colisão por baixo

- **WHEN** o personagem colide com o inimigo por baixo
- **THEN** o inimigo não é derrotado
- **AND** o inimigo permanece na cena
- **AND** o contato é tratado como colisão física normal, sem atravessar o inimigo

### Requirement: Impulso para cima após a pisada

O sistema SHALL aplicar ao personagem um pequeno impulso vertical para cima no momento exato da pisada que derrota o inimigo.

O impulso SHALL elevar o personagem acima do inimigo após a derrota, sem alterar a regra existente de que um novo salto só pode ser iniciado quando o personagem está apoiado sobre a plataforma.

#### Scenario: Personagem recebe impulso após a pisada

- **WHEN** o personagem derrota o inimigo ao cair sobre a sua parte superior
- **THEN** o personagem recebe uma velocidade vertical inicial para cima
- **AND** o personagem se afasta do local onde o inimigo estava
- **AND** a gravidade retorna o personagem à plataforma

#### Scenario: Sem segundo salto durante o impulso

- **WHEN** o personagem está no ar logo após o impulso da pisada
- **THEN** o sistema ignora a solicitação de pulo
- **AND** o personagem não inicia um segundo salto antes de retornar à plataforma

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
- limites horizontais da área de jogo.

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