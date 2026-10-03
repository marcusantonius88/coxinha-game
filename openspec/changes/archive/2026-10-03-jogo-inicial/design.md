# Design

## Context

O projeto será estruturado como um aplicativo web 2D utilizando Phaser 3 com TypeScript e Vite.

A primeira cena será simples e terá como objetivo validar o núcleo de movimentação do jogo. O personagem será representado inicialmente por um retângulo ou outro elemento visual simples, sem utilização dos sprites definitivos do Coxinha.

Esta change representa o primeiro incremento técnico do projeto. O foco é estabelecer uma base funcional sobre a qual as demais mecânicas poderão ser desenvolvidas posteriormente.

## Goals / Non-Goals

### Goals

- Configurar um projeto web 2D utilizando TypeScript, Phaser 3 e Vite.
- Criar uma cena Phaser inicial executável no navegador.
- Configurar a física ARCADE do Phaser.
- Criar um personagem temporário com corpo físico retangular.
- Implementar movimentação horizontal para esquerda e direita.
- Implementar corrida utilizando a tecla `Shift`.
- Implementar salto utilizando `ArrowUp` ou `Space`.
- Permitir que o personagem permaneça sobre uma plataforma.
- Manter a implementação preparada para futuras expansões do jogo.

### Non-Goals

- Implementar os sprites definitivos do Coxinha.
- Criar animações ou sprite sheets.
- Implementar ataques ou combate.
- Criar inimigos.
- Criar coletáveis.
- Criar fases completas.
- Criar chefes.
- Implementar sons ou efeitos sonoros.
- Criar telas de menu ou HUD.
- Implementar persistência ou salvamento.
- Implementar multiplayer ou networking.
- Implementar controles para dispositivos móveis nesta change.

## Decisions

### Estrutura do Projeto

- **Escolhido:** Estrutura padrão de projeto TypeScript utilizando `src/` para o código-fonte e `dist/` para os arquivos gerados pelo build.

- **Alternativa considerada:** Estrutura plana com todos os arquivos na raiz.

- **Rationale:** A separação entre código-fonte e arquivos gerados facilita a manutenção, organização e evolução do projeto.

### Framework de Build

- **Escolhido:** Vite.

- **Alternativa considerada:** Webpack com `ts-loader`.

- **Rationale:** Vite oferece configuração mínima, desenvolvimento rápido, Hot Module Replacement (HMR) e uma experiência adequada para um projeto TypeScript pequeno.

### Framework de Jogo

- **Escolhido:** Phaser 3.

- **Alternativa considerada:** Implementação própria utilizando diretamente Canvas API ou Web APIs.

- **Rationale:** Phaser fornece abstrações específicas para jogos 2D, incluindo gerenciamento de cenas, entrada, física, renderização e ciclo de atualização, reduzindo a quantidade de infraestrutura que precisaria ser implementada manualmente.

### Física do Personagem

- **Escolhida:** Física ARCADE do Phaser com corpo retangular simples.

- **Alternativa considerada:** Física personalizada ou corpos geométricos mais complexos.

- **Rationale:** A física ARCADE é suficiente para um platformer 2D básico e oferece uma implementação simples e adequada para o protótipo inicial.

### Sistema de Input

- **Escolhido:** Sistema de entrada do Phaser utilizando `Phaser.Input.Keyboard.Key`.

- **Alternativa considerada:** Manipulação direta de eventos DOM `keydown` e `keyup`.

- **Rationale:** A integração nativa com o Phaser facilita a sincronização dos controles com o ciclo de atualização da cena e fornece métodos utilitários para consultar o estado das teclas.

### Controles

Os controles iniciais serão:

| Ação | Tecla |
|---|---|
| Mover para esquerda | `ArrowLeft` |
| Mover para direita | `ArrowRight` |
| Correr | `Shift` |
| Pular | `ArrowUp` ou `Space` |

A velocidade normal de deslocamento deverá ser menor que a velocidade utilizada durante a corrida.

Os valores exatos de velocidade e força do salto deverão ser definidos durante a implementação de acordo com o comportamento desejado e registrados na especificação correspondente.

### Personagem Temporário

O personagem será representado inicialmente por uma forma geométrica simples, preferencialmente um retângulo.

O objetivo é validar a mecânica de movimentação sem introduzir dependência de assets gráficos nesta etapa.

A substituição do personagem temporário pelo sprite definitivo do Coxinha será realizada em uma change futura.

## Risks / Trade-offs

### Performance

O uso da física ARCADE pode ser menos preciso ou completo que soluções físicas mais avançadas, mas é adequado para um platformer 2D e reduz a complexidade da implementação inicial.

### Limitação Visual

A utilização de um personagem temporário limita o feedback visual e não representa a identidade final do jogo. Isso é intencional nesta etapa para manter o foco na validação das mecânicas básicas.

### Dependência de Framework

A utilização do Phaser cria uma dependência de um framework externo, reduzindo a flexibilidade de uma implementação baseada diretamente nas APIs do navegador. Em contrapartida, acelera significativamente o desenvolvimento das funcionalidades comuns de um jogo 2D.

### Escopo Inicial

Limitar esta change à movimentação básica reduz a quantidade de funcionalidades disponíveis no primeiro protótipo, mas permite validar a arquitetura e o ciclo de desenvolvimento antes da introdução de sistemas mais complexos.