# Proposal

## Why

O jogo Coxinha precisa de um núcleo jogável inicial para validar a integração do TypeScript com o Phaser e estabelecer uma primeira base de movimentação do personagem (andar, correr e pular).

Esta change representa o primeiro incremento técnico do projeto e não tem como objetivo implementar as demais mecânicas do jogo.

## What Changes

- Criar projeto 2D para navegador com TypeScript e Phaser
- Estruturar a cena inicial com um personagem temporário
- Implementar controles de movimento: andar, correr e pular

## Capabilities

### New Capabilities

- `jogo-inicial`: Configurar projeto Phaser com TypeScript e criar cena jogável com personagem controlável (andar, correr, pular)

### Modified Capabilities

<!-- Nenhuma -->

## Impact

- Criação dos arquivos de configuração (`package.json`, `tsconfig.json`)
- Estrutura do jogo com fonte em TypeScript
- Primeira cena jogável no navegador