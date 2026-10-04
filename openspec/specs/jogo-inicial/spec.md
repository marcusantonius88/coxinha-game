# jogo-inicial Specification

## Purpose

Configurar o projeto 2D para navegador utilizando TypeScript, Phaser 3 e Vite e criar uma primeira cena jogável com um personagem temporário capaz de andar, correr e pular.

Esta change tem como objetivo validar a infraestrutura inicial do jogo e a mecânica básica de movimentação. Não contempla a implementação do personagem definitivo Coxinha nem outras mecânicas do jogo.

## Requirements

### Requirement: Projeto configurado para Phaser com TypeScript

O sistema SHALL incluir uma configuração de projeto utilizando TypeScript, Phaser 3 e Vite, com compilação direcionada para navegadores modernos.

O projeto SHALL possuir um comando de desenvolvimento que inicie o servidor local e disponibilize o jogo em uma página HTML.

#### Scenario: Servidor de desenvolvimento ativo

- **WHEN** o desenvolvedor executa o comando de desenvolvimento
- **THEN** o servidor de desenvolvimento é iniciado e o jogo pode ser acessado em `http://localhost:5173`
- **AND** uma cena Phaser é carregada no navegador

### Requirement: Cena inicial jogável

A cena inicial SHALL possuir um personagem e uma plataforma que funcione como chão.

O personagem SHALL utilizar `assets/coxinha/coxinha-idle.png` como representação visual estática, substituindo a representação geométrica temporária anterior.

`assets/coxinha/coxinha-sprite-sheet.png` permanece no projeto como asset para uso futuro e não participa da implementação desta change.

#### Scenario: Cena inicial carregada

- **WHEN** a cena inicial é carregada
- **THEN** o personagem Coxinha é exibido acima da plataforma
- **AND** a pose exibida é `IDLE`
- **AND** a plataforma funciona como superfície de suporte
- **AND** o personagem é afetado pela gravidade
- **AND** o personagem permanece sobre a plataforma quando estiver em contato com ela
- **AND** os controles existentes continuam funcionando
- **AND** os limites horizontais da área de jogo continuam sendo respeitados

### Requirement: Personagem temporário controlável

O sistema SHALL exibir um personagem temporário controlável pelo teclado.

O personagem SHALL ser representado por uma forma geométrica simples ou sprite temporário e possuir um corpo físico compatível com a física ARCADE.

#### Scenario: Movimento para a esquerda

- **WHEN** o jogador pressiona e mantém `ArrowLeft`
- **THEN** o personagem se move horizontalmente para a esquerda

#### Scenario: Movimento para a direita

- **WHEN** o jogador pressiona e mantém `ArrowRight`
- **THEN** o personagem se move horizontalmente para a direita

#### Scenario: Parada do movimento

- **WHEN** o jogador solta `ArrowLeft` ou `ArrowRight`
- **THEN** a velocidade horizontal do personagem retorna a zero
- **AND** o personagem deixa de se deslocar horizontalmente

### Requirement: Corrida

O sistema SHALL permitir que o jogador aumente a velocidade horizontal do personagem mantendo `Shift` pressionado simultaneamente com uma tecla de movimento horizontal.

A velocidade de corrida SHALL ser maior que a velocidade normal de movimento.

#### Scenario: Corrida para a esquerda

- **WHEN** o jogador mantém `Shift` e `ArrowLeft` pressionados simultaneamente
- **THEN** o personagem se move para a esquerda utilizando a velocidade de corrida

#### Scenario: Corrida para a direita

- **WHEN** o jogador mantém `Shift` e `ArrowRight` pressionados simultaneamente
- **THEN** o personagem se move para a direita utilizando a velocidade de corrida

#### Scenario: Retorno à velocidade normal

- **WHEN** o jogador libera `Shift` enquanto mantém uma tecla de movimento pressionada
- **THEN** o personagem continua se movendo na mesma direção utilizando a velocidade normal

### Requirement: Pulo

O sistema SHALL permitir que o personagem pule utilizando `ArrowUp` ou `Space`.

O personagem SHALL poder iniciar um salto somente quando estiver apoiado sobre a plataforma.

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

### Requirement: Gravidade

O sistema SHALL aplicar gravidade ao personagem utilizando a física ARCADE do Phaser.

#### Scenario: Personagem retorna ao chão

- **WHEN** o personagem está no ar após iniciar um salto
- **THEN** a velocidade vertical do personagem é afetada pela gravidade
- **AND** o personagem retorna à plataforma

### Requirement: Limite horizontal da tela

O sistema SHALL impedir que o personagem ultrapasse os limites horizontais da área de jogo.

#### Scenario: Personagem atinge o limite esquerdo

- **WHEN** o personagem tenta ultrapassar o limite esquerdo da área de jogo
- **THEN** o personagem permanece dentro da área visível

#### Scenario: Personagem atinge o limite direito

- **WHEN** o personagem tenta ultrapassar o limite direito da área de jogo
- **THEN** o personagem permanece dentro da área visível
