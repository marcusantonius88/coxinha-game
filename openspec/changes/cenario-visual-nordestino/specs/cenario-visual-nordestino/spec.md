# Spec Delta

## Purpose

Adicionar camadas de fundo em pixel art inspiradas no Nordeste brasileiro, com rolagem paralaxe horizontal vinculada à câmera, enriquecendo visualmente a fase de 2400×600 sem alterar jogabilidade, física ou colisões.

## ADDED Requirements

### Requirement: Camadas de fundo do Nordeste brasileiro (assets pré-aprovados)

O sistema SHALL incluir exatamente 4 camadas de fundo com tema nordestino (céu, serras distantes, caatinga, vegetação do primeiro plano), dispostas atrás de todas as plataformas e obstáculos existentes.

Os 4 PNGs de fundo SHALL ser fornecidos e aprovados externamente (fora do Cline) antes de qualquer implementação. O Cline se limita à integração dos assets já aprovados.

Cada camada SHALL ser representada por textura PNG com as seguintes especificações:

- **Dimensões**: altura 600 px (igual à altura do mundo/viewport); largura mínima calculada para cobrir o deslocamento máximo de parallax (ver tabela na seção de dimensões).
- **Transparência**: fundo transparente (alpha canal) onde não houver arte, permitindo que camadas atrás sejam visíveis.
- **Paleta**: cores terrosas (areia, ocre, terracota, verde seco, azul céu), coerentes com o estilo pixel art já existente no projeto.
- **Repetição horizontal**: textura projetada para tiling horizontal sem costura visível.
- **Estilo**: cores sólidas, contornos nítidos de 1–2 px, sem degradês, sem antialiasing, sem borrão.

#### Scenario: Fundo preenche toda a fase

- **WHEN** a cena é carregada com os 4 assets aprovados presentes
- **THEN** as 4 camadas de fundo cobrem integralmente a área do mundo (2400×600 px)
- **AND** não há áreas vazias ou sem textura atrás do cenário em nenhum ponto da travessia (x de 0 a 2400)

#### Scenario: Estilo pixel art preservado

- **WHEN** as camadas de fundo são renderizadas
- **THEN** as texturas usam filtro nearest-neighbor (sem borrão)
- **AND** as posições de renderização são inteiras (sem sub-pixel)
- **AND** a escala de exibição é inteira (sem deformação)
- **AND** as 4 texturas correspondem exatamente aos assets aprovados externamente

#### Scenario: Bloqueio até aprovação dos assets

- **WHEN** os 4 PNGs de fundo não estão presentes no repositório ou não foram aprovados
- **THEN** nenhuma alteração de implementação é iniciada em `src/scenes/GameScene.ts`
- **AND** a change permanece em estado de planejamento apenas

### Requirement: Rolagem paralaxe vinculada à câmera

O sistema SHALL fazer cada camada de fundo se mover horizontalmente a uma velocidade proporcional ao `scrollX` da câmera principal, criando efeito de profundidade.

A camada mais distante SHALL se mover mais lentamente que a câmera; camadas mais próximas SHALL se mover mais rapidamente, mas sempre mais devagar que o primeiro plano do jogo.

#### Scenario: Parallax suave durante a travessia

- **WHEN** o jogador caminha da esquerda para a direita pela fase
- **THEN** as camadas de fundo deslocam-se horizontalmente na mesma direção, com velocidades distintas
- **AND** o deslocamento vertical permanece fixo (sem rolagem Y)

#### Scenario: Sem tremor sub-pixel

- **WHEN** a câmera rola horizontalmente
- **THEN** as posições das camadas de fundo são arredondadas para inteiros
- **AND** não há tremor ou borrão na arte pixelada durante o scroll

### Requirement: Cenário exclusivamente visual (sem colisão)

O sistema SHALL garantir que nenhuma camada de fundo possua corpo físico, colisão ou interação com o personagem, plataformas, obstáculos ou slime.

As camadas SHALL ficar atrás (z-index inferior) de todos os elementos jogáveis.

#### Scenario: Sem colisão nas camadas de fundo

- **WHEN** o personagem caminha, salta ou colide com plataformas/obstáculos
- **THEN** as camadas de fundo não afetam o movimento nem a física
- **AND** o personagem continua sendo bloqueado apenas pelo chão, plataformas e obstáculos sólidos

#### Scenario: Camadas atrás do cenário jogável

- **WHEN** o personagem se move sobre o chão ou plataformas
- **THEN** as camadas de fundo permanecem visíveis atrás dele
- **AND** não cobrem ou ocultam elementos jogáveis

### Requirement: Compatibilidade com limites do mundo e câmera existente

O sistema SHALL funcionar com o mundo de 2400×600 px já configurado e com a câmera horizontal limitada aos limites do mundo.

A rolagem paralaxe SHALL parar nos extremos do mundo (x=0 e x=2400), sem exibir áreas vazias além das bordas.

#### Scenario: Parallax respeita limites do mundo

- **WHEN** o jogador atinge o limite esquerdo (x=0) ou direito (x=2400) do mundo
- **THEN** as camadas de fundo param de rolar nos respectivos extremos
- **AND** nenhuma área vazia é exibida além das bordas do mundo

#### Scenario: Nenhuma alteração na física existente

- **WHEN** as camadas de fundo são adicionadas
- **THEN** gravidade (1840), salto (-920), velocidades (200/350), hitbox (30×30) e impulso da pisada (-690) permanecem inalterados
- **AND** spawn, plataformas, slime e animações continuam funcionando como antes