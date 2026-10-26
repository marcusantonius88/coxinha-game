# inimigo-base Specification

## Purpose

Introduzir o primeiro inimigo da cena inicial, com hitbox própria e comportamento parado, estabelecendo a mecânica básica de derrota por pisada: Coxinha derrota o inimigo ao cair sobre a sua parte superior durante um salto e recebe um pequeno impulso para cima, enquanto colisões laterais ou por baixo não o derrotam.

## Requirements

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

### Requirement: Representação visual animada do inimigo

O sistema SHALL representar o inimigo na cena com a arte pixel art aprovada do slime, contida em `assets/enemies/slime/`, com quadros consistentes e fundo transparente.

A representação visual SHALL permanecer independente do corpo físico do inimigo: o corpo mantém sua hitbox própria e inalterada, e o visual não participa da detecção de colisões nem interfere na movimentação.

Enquanto o inimigo estiver ativo, o sistema SHALL exibir a animação `IDLE` do slime em loop.

O visual SHALL ser renderizado em escala inteira, preservando a renderização pixel-perfect do jogo, com a base alinhada à parte inferior do corpo físico do inimigo.

O sistema SHALL utilizar exclusivamente os PNGs existentes; SHALL NOT gerar, redesenhar ou modificar artes de inimigo.

#### Scenario: Cena inicial com slime ativo

- **WHEN** a cena inicial é carregada
- **THEN** o inimigo é exibido sobre a plataforma com a aparência do slime
- **AND** a animação `IDLE` é reproduzida em loop enquanto o inimigo estiver ativo
- **AND** o corpo físico do inimigo permanece invisível na cena

#### Scenario: Corpo físico independente do visual

- **WHEN** o personagem interage fisicamente com o inimigo
- **THEN** as colisões são calculadas exclusivamente pelo corpo físico do inimigo
- **AND** o sprite visual não altera hitbox, posição física ou comportamento de colisão

#### Scenario: Renderização pixel-perfect preservada

- **WHEN** o slime é desenhado na cena
- **THEN** o sprite é exibido em escala inteira, sem distorção de proporção
- **AND** a renderização pixel-perfect existente permanece em vigor

### Requirement: Derrota por pisada

O sistema SHALL derrotar o inimigo quando o personagem cai sobre a parte superior do inimigo durante um salto.

No momento da derrota, a interação física do inimigo com o personagem SHALL cessar imediatamente.

A animação `DEFEAT` do slime SHALL ser reproduzida uma única vez; ao concluí-la, o inimigo — visual e corpo físico — SHALL ser removido da cena.

Após a derrota concluída, o inimigo SHALL deixar de ser exibido e SHALL deixar de interagir fisicamente com o personagem.

Derrotas duplicadas SHALL ser impedidas: uma vez derrotado, contatos posteriores não SHALL reiniciar a animação de derrota nem reprocessar a derrota.

#### Scenario: Pisada sobre a parte superior

- **WHEN** o personagem, durante um salto, cai com sua hitbox sobre a parte superior da hitbox do inimigo
- **THEN** o inimigo é derrotado
- **AND** a interação física entre personagem e inimigo cessa imediatamente
- **AND** a animação `DEFEAT` é reproduzida uma única vez
- **AND** ao concluir `DEFEAT` o inimigo deixa de ser exibido na cena e seu corpo físico é removido

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

#### Scenario: Derrota não se repete

- **WHEN** o inimigo já foi derrotado e um novo contato ocorre durante ou após a animação de derrota
- **THEN** nenhuma nova derrota é processada
- **AND** a animação `DEFEAT` não é reiniciada
- **AND** o inimigo é removido normalmente ao fim da animação

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
