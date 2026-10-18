# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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
