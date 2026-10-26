# Spec Delta

## Purpose

Permitir que o jogador avance por um mundo horizontalmente mais largo que a área visível da tela, com uma câmera que acompanha o Coxinha no eixo horizontal e respeita os limites do mundo, preservando integralmente a jogabilidade de plataforma já aprovada.

## ADDED Requirements

### Requirement: Mundo horizontalmente extenso

O sistema SHALL configurar um mundo de jogo mais largo que a viewport de 800×600 px.

O chão SHALL se estender por toda a largura do mundo, mantendo-se uma superfície contínua e uniforme sobre a qual o personagem possa caminhar de ponta a ponta.

O limite horizontal aplicável ao personagem SHALL ser o limite do mundo, e não o da área visível.

A largura do mundo SHALL ser um múltiplo exato da largura da viewport, de modo que o enquadramento da câmera nunca exiba áreas vazias nas bordas.

#### Scenario: Mundo mais largo que a tela

- **WHEN** a cena é carregada
- **THEN** a largura do mundo é maior que 800 px
- **AND** o chão cobre toda a largura do mundo
- **AND** o personagem pode caminhar para além da borda direita da viewport

#### Scenario: Limite horizontal no limite do mundo

- **WHEN** o jogador caminha continuamente para a direita até o fim do mundo
- **THEN** o personagem para no limite direito do mundo
- **AND** não atravessa para fora da área do mundo

#### Scenario: Limite horizontal esquerdo no mundo

- **WHEN** o jogador caminha continuamente para a esquerda até o início do mundo
- **THEN** o personagem para no limite esquerdo do mundo
- **AND** não atravessa para fora da área do mundo

### Requirement: Câmera acompanha o personagem no eixo horizontal

O sistema SHALL configurar a câmera principal para acompanhar o Coxinha no eixo horizontal.

A câmera SHALL rolar horizontalmente quando o personagem se desloca horizontalmente, para a esquerda e para a direita.

O acompanhamento horizontal SHALL ser suave, sem saltos bruscos de enquadramento.

A câmera SHALL permanecer fixa verticalmente nesta change: ela SHALL NOT rolar no eixo Y, SHALL NOT aplicar zoom e SHALL NOT aplicar rotação.

A câmera SHALL manter o personagem visível durante todo o percurso.

#### Scenario: Câmera rola para a direita

- **WHEN** o jogador caminha ou corre para a direita
- **THEN** a câmera desloca-se horizontalmente para a direita acompanhando o personagem
- **AND** o deslocamento vertical da câmera permanece constante

#### Scenario: Câmera rola para a esquerda

- **WHEN** o jogador caminha ou corre para a esquerda
- **THEN** a câmera desloca-se horizontalmente para a esquerda acompanhando o personagem
- **AND** o deslocamento vertical da câmera permanece constante

#### Scenario: Câmera verticalmente fixa

- **WHEN** o personagem salta, sobe sobre plataformas ou cai
- **THEN** o enquadramento vertical da câmera não se altera
- **AND** não há zoom nem rotação aplicados à câmera

#### Scenario: Personagem permanece visível

### Requirement: Câmera respeita os limites do mundo

A câmera SHALL ser limitada às extensões do mundo, sem revelar áreas vazias além das bordas esquerda e direita.

Quando o personagem se aproxima de uma borda do mundo, a câmera SHALL parar de rolar ao atingir o limite correspondente, mantendo o personagem enquadrado.

A câmera SHALL continuar agile e responsiva após atingir um limite, retomando o acompanhamento quando o personagem se afasta da borda.

#### Scenario: Câmera para no limite direito

- **WHEN** o jogador caminha para a direita até o fim do mundo
- **THEN** a câmera para de rolar
- **AND** nenhuma área vazia é exibida além do limite direito do mundo

#### Scenario: Câmera para no limite esquerdo

- **WHEN** o jogador caminha para a esquerda até o início do mundo
- **THEN** a câmera para de rolar
- **AND** nenhuma área vazia é exibida além do limite esquerdo do mundo

#### Scenario: Retomada do acompanhamento após o limite

- **WHEN** o jogador se afasta da borda do mundo após ter atingido um limite
- **THEN** a câmera volta a acompanhar o personagem

### Requirement: Percurso distribuído em fase extensa

O chão, as plataformas elevadas e os obstáculos SHALL ser distribuídos por uma seção de fase mais extensa e atravessável de ponta a ponta.

O percurso SHALL permanecer viável com a física atual: toda estrutura SHALL ser alcançável ou superável dentro do alcance do salto existente, e nenhuma estrutura SHALL bloquear permanentemente o caminho.

Nenhuma plataforma ou obstáculo SHALL criar situação impossível de superar, e o percurso SHALL poder ser percorrido nos dois sentidos.

O slime SHALL permanecer posicionado no percurso, e a mecânica de derrota por pisada SHALL permanecer funcional na nova posição.

#### Scenario: Percurso atravessável de ponta a ponta

- **WHEN** o jogador percorre a fase da esquerda até a direita
- **THEN** ele avança por toda a extensão do mundo
- **AND** nenhuma estrutura impede o avanço

#### Scenario: Percurso reversível

- **WHEN** o jogador percorre a fase da direita até a esquerda
- **THEN** ele retorna por toda a extensão do mundo
- **AND** nenhuma estrutura impede o retorno

#### Scenario: Plataformas e obstáculos continuam funcionais

- **WHEN** o jogador interage com as plataformas elevadas e os obstáculos na nova distribuição
- **THEN** ele aterrissa sobre as plataformas, é bloqueado pelos obstáculos e pode saltar a partir delas
- **AND** o comportamento é o mesmo aprovado na seção anterior

#### Scenario: Slime permanece no percurso

- **WHEN** o jogador chega à posição do slime na fase extensa
- **THEN** o slime está presente no percurso
- **AND** ao cair sobre ele durante um salto o slime é derrotado, com a animação de derrota e o impulso já existentes

- **WHEN** o personagem percorre a fase inteira, em terra e no ar
### Requirement: Renderização pixel-perfect preservada

A renderização SHALL permanecer nítida, com filtragem nearest-neighbor e desenho em posições inteiras habilitados.

A câmera SHALL arredondar sua posição para pixels inteiros, evitando borrão ou tremulação na arte pixelada durante a rolagem.

O sistema SHALL NOT aplicar zoom nem rotação à câmera, preservando a escala de exibição aprovada.

#### Scenario: Arte pixelada nítida durante a rolagem

- **WHEN** a câmera rola horizontalmente pelo cenário
- **THEN** os sprites permanecem nítidos, sem borrão de filtragem
- **AND** não há tremor sub-pixel no enquadramento

#### Scenario: Escala de exibição preservada

- **WHEN** a cena é carregada com a câmera configurada
- **THEN** o zoom da câmera permanece em 1
- **AND** a rotação da câmera permanece em 0

- **THEN** ele permanece enquadrado pela câmera
- **AND** não desaparece para fora da área visível
