# Tasks

## 1. Criação do inimigo na cena

- [x] 1.1 Criar o inimigo em `src/scenes/GameScene.ts` como retângulo temporário (40x40) posicionado sobre a plataforma e verificar que ele é exibido na cena ao carregar, sem ficar cortado pelo chão nem flutuando
- [x] 1.2 Adicionar um corpo físico próprio ao inimigo (`physics.add.existing(enemy, true)`) e verificar que a hitbox do inimigo é independente da hitbox do Coxinha (30x30 preservada)
- [x] 1.3 Verificar que o inimigo permanece parado durante toda a execução da cena, sem cair, deslizar ou se mover por conta própria

## 2. Colisão e derrota por pisada

- [x] 2.1 Registrar `physics.add.collider(playerBody, enemy)` e verificar que o Coxinha colide fisicamente com o inimigo pelos lados sem atravessá-lo
- [x] 2.2 Implementar a detecção de pisada na callback da colisão (contato pelo topo + aproximação de cima, conforme design.md) e verificar que a derrota só ocorre quando o Coxinha cai sobre a parte superior durante um salto
- [x] 2.3 Verificar que colisão lateral não derrota o inimigo e que o inimigo permanece na cena
- [x] 2.4 Verificar que colisão por baixo (pulo atingindo o inimigo por baixo) não derrota o inimigo e que o inimigo permanece na cena
- [x] 2.5 Implementar a remoção do inimigo na pisada (`destroy()` + flag anti reprocessamento) e verificar que ele deixa de ser exibido e deixa de colidir com o personagem

## 3. Impulso após a pisada

- [x] 3.1 Aplicar `setVelocityY(-300)` no corpo do Coxinha no momento da pisada e verificar que ele recebe um pequeno impulso para cima e é retido pela gravidade até retornar à plataforma
- [x] 3.2 Verificar que, durante o impulso, o Coxinha não executa segundo salto ao pressionar `ArrowUp` ou `Space` antes de encostar na plataforma

## 4. Preservação das mecânicas existentes

- [x] 4.1 Verificar que movimentação normal, corrida com `Shift`, salto com `ArrowUp`/`Space`, gravidade, colisão com a plataforma e limites horizontais continuam funcionando sem alteração
- [x] 4.2 Verificar que velocidades (200/350), força do salto (-400), gravidade (y: 300), hitbox 30x30 e controles não foram alterados em relação à implementação anterior

## 5. Verificação final

- [x] 5.1 Executar `npm run build` e confirmar que o projeto compila sem erros
- [x] 5.2 Executar o jogo no navegador e validar manualmente todos os cenários de `specs/inimigo-base/spec.md` (presença do inimigo, pisada, colisão lateral, colisão por baixo, impulso, preservação)
- [x] 5.3 Executar `npm run preview` e validar o build de produção no navegador
- [x] 5.4 Confirmar que não foram implementados itens fora do escopo: IA/movimentação do inimigo, vida/dano do Coxinha, animações, sons, HUD, coletáveis ou novas fases
- [x] 5.5 Confirmar que nenhuma dependência nova foi adicionada e que `package.json`, `tsconfig.json` e `vite.config.ts` permanecem inalterados
- [x] 5.6 Executar `openspec validate inimigo-base --strict` e confirmar que os artefatos da change são válidos