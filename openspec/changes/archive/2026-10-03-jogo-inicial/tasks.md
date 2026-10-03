# Tasks

## 1. Setup do Projeto

- [x] 1.1 Inicializar o projeto Node.js e criar o `package.json`.

- [x] 1.2 Instalar TypeScript, Phaser 3 e Vite como dependências do projeto e verificar que a instalação foi concluída sem erros.

- [x] 1.3 Criar `tsconfig.json` com `target` ES2020, `module` ESNext, `strict` habilitado e diretório de saída configurado para `dist/`. Verificar que a configuração TypeScript é válida.

- [x] 1.4 Criar `vite.config.ts` com a configuração mínima necessária para o projeto e configurar o diretório de saída do build como `dist/`.

- [x] 1.5 Criar `index.html` na raiz do projeto com o ponto de entrada necessário para inicialização do jogo.

- [x] 1.6 Adicionar os scripts npm:
  - `dev`: inicia o servidor de desenvolvimento;
  - `build`: executa a verificação TypeScript e gera o build de produção;
  - `preview`: inicia o servidor para visualização do build de produção.

- [x] 1.7 Executar `npm run dev` e confirmar que o servidor de desenvolvimento inicia corretamente.

## 2. Estrutura Base do Jogo

- [x] 2.1 Criar `src/main.ts` e inicializar uma instância de `Phaser.Game` com uma resolução inicial de 800×600 e física ARCADE habilitada.

- [x] 2.2 Criar `src/scenes/GameScene.ts` estendendo `Phaser.Scene`, incluindo os métodos necessários para o ciclo de vida da cena.

- [x] 2.3 Registrar `GameScene` na configuração do Phaser e garantir que ela seja carregada como a cena inicial.

- [x] 2.4 Executar o jogo no navegador e confirmar que a cena Phaser é carregada sem erros no console.

## 3. Personagem Temporário e Física

- [x] 3.1 Criar uma representação visual temporária para o personagem utilizando uma forma geométrica ou outro recurso simples disponível no Phaser.

- [x] 3.2 Posicionar o personagem inicialmente acima da plataforma, próximo à região central da área de jogo.

- [x] 3.3 Adicionar física ARCADE ao personagem e configurar gravidade suficiente para que ele seja atraído em direção à plataforma.

- [x] 3.4 Configurar o personagem para permanecer dentro dos limites horizontais da área de jogo.

- [x] 3.5 Criar uma plataforma estática cobrindo a região inferior da área de jogo.

- [x] 3.6 Configurar a colisão entre o personagem e a plataforma e verificar que o personagem permanece sobre ela após cair.

## 4. Sistema de Movimento

- [x] 4.1 Configurar as teclas `ArrowLeft`, `ArrowRight`, `ArrowUp`, `Space` e `Shift` utilizando o sistema de entrada do Phaser.

- [x] 4.2 Implementar movimento horizontal para a esquerda utilizando `ArrowLeft`.

- [x] 4.3 Implementar movimento horizontal para a direita utilizando `ArrowRight`.

- [x] 4.4 Definir uma velocidade normal de movimento horizontal.

- [x] 4.5 Implementar corrida utilizando `Shift` simultaneamente com `ArrowLeft` ou `ArrowRight`, utilizando uma velocidade maior que a velocidade normal.

- [x] 4.6 Fazer o personagem parar horizontalmente quando nenhuma tecla de movimento estiver pressionada.

- [x] 4.7 Implementar salto utilizando `ArrowUp` quando o personagem estiver apoiado sobre a plataforma.

- [x] 4.8 Implementar salto utilizando `Space` quando o personagem estiver apoiado sobre a plataforma.

- [x] 4.9 Impedir que o personagem execute um novo salto enquanto estiver no ar.

## 5. Limites e Ajustes

- [x] 5.1 Confirmar que o personagem não ultrapassa os limites horizontais da área de jogo.

- [x] 5.2 Ajustar os parâmetros de velocidade normal, velocidade de corrida, gravidade e força do salto para produzir um controle adequado ao protótipo.

- [x] 5.3 Testar a sequência de movimentação, corrida, salto e aterrissagem.

- [x] 5.4 Corrigir eventuais problemas identificados durante os testes manuais.

## 6. Verificação Final

- [x] 6.1 Executar `npm run build` e confirmar que o projeto é compilado sem erros.

- [x] 6.2 Confirmar que o diretório `dist/` é gerado corretamente.

- [x] 6.3 Executar `npm run preview` e verificar o build de produção no navegador.

- [x] 6.4 Executar todos os cenários definidos em `specs/jogo-inicial/spec.md`.

- [x] 6.5 Confirmar que o personagem consegue andar, correr, pular e retornar ao chão sem erros.

- [x] 6.6 Confirmar que o personagem permanece dentro dos limites horizontais da tela.

- [x] 6.7 Confirmar que a primeira cena jogável funciona no navegador sem erros no console.