# Tasks

## 1. Asset Visual

- [x] 1.1 Confirmar que `assets/coxinha/coxinha-idle.png` existe no projeto.
- [x] 1.2 Confirmar que `assets/coxinha/coxinha-idle.png` é uma imagem única contendo somente a pose estática `IDLE` do Coxinha.
- [x] 1.3 Confirmar que `assets/coxinha/coxinha-sprite-sheet.png` permanece no projeto como asset futuro e não será utilizado nesta change.
- [x] 1.4 Confirmar que nenhuma animação será registrada ou executada nesta change.

## 2. Integração no Jogo

- [x] 2.1 Carregar `assets/coxinha/coxinha-idle.png` utilizando `load.image()` durante o carregamento da cena `GameScene`.
- [x] 2.2 Não utilizar `load.spritesheet()` para o personagem nesta change.
- [x] 2.3 Substituir a representação geométrica temporária pela imagem `coxinha-idle`.
- [x] 2.4 Posicionar visualmente o Coxinha sobre a plataforma sem que o sprite seja cortado pelo chão ou pela área de jogo.
- [x] 2.5 Ajustar escala e/ou posicionamento visual do sprite, se necessário, sem alterar a hitbox existente.
- [x] 2.6 Manter `physics.add.existing()` e a estrutura física existente do personagem.
- [x] 2.7 Manter a hitbox existente.
- [x] 2.8 Manter a gravidade existente (`y: 300`).
- [x] 2.9 Manter a colisão com a plataforma.
- [x] 2.10 Manter `setCollideWorldBounds(true)` e os limites horizontais existentes.
- [x] 2.11 Manter os controles existentes para `ArrowLeft`, `ArrowRight`, `Shift`, `ArrowUp` e `Space`.
- [x] 2.12 Não alterar as velocidades de movimento, velocidade de corrida ou força do salto.

## 3. Estrutura para Futuras Animações

- [x] 3.1 Manter a representação visual do personagem organizada de forma que a imagem `IDLE` possa posteriormente ser substituída por um sistema de animações sem reimplementar a lógica de movimentação e física.
- [x] 3.2 Não criar nem registrar as animações `WALK`, `RUN`, `JUMP`, `FALL`, `LAND` ou `HIT` nesta change.

## 4. Verificação Funcional

- [x] 4.1 Executar `npm run build` e confirmar que o projeto compila sem erros.
- [x] 4.2 Executar o jogo no navegador e confirmar que o Coxinha é exibido no lugar do personagem temporário.
- [x] 4.3 Confirmar visualmente que somente um Coxinha é exibido.
- [x] 4.4 Confirmar que a pose exibida é `IDLE`.
- [x] 4.5 Confirmar que não aparecem partes da sprite sheet ou outros elementos gráficos no personagem.
- [x] 4.6 Confirmar que nenhuma animação é executada.
- [x] 4.7 Confirmar que o personagem continua andando para esquerda e direita.
- [x] 4.8 Confirmar que a corrida com `Shift` continua funcionando.
- [x] 4.9 Confirmar que o salto com `ArrowUp` continua funcionando.
- [x] 4.10 Confirmar que o salto com `Space` continua funcionando.
- [x] 4.11 Confirmar que o personagem não executa segundo salto enquanto estiver no ar.
- [x] 4.12 Confirmar que a gravidade e a colisão com a plataforma continuam funcionando.
- [x] 4.13 Confirmar que o personagem não fica visualmente cortado pela plataforma durante o movimento ou salto.
- [x] 4.14 Confirmar que a hitbox permanece funcionando conforme a implementação anterior.
- [x] 4.15 Confirmar que os limites horizontais da área de jogo continuam funcionando.
- [x] 4.16 Executar `npm run preview` e validar o build de produção no navegador.

## 5. Verificação Final

- [x] 5.1 Confirmar que não foram alteradas dependências do projeto.
- [x] 5.2 Confirmar que não foram introduzidas novas mecânicas de gameplay.
- [x] 5.3 Confirmar que `assets/coxinha/coxinha-sprite-sheet.png` não foi utilizado na implementação desta change.
- [x] 5.4 Confirmar que as alterações estão limitadas ao escopo definido nesta change.
- [x] 5.5 Confirmar que todos os requisitos da especificação foram validados.