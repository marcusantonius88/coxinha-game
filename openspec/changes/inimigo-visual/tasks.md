# Tasks

## 1. Carregamento e animações do inimigo

- [ ] 1.1 Adicionar os imports Vite e o carregamento no `preload()` das spritesheets `slime_idle_spritesheet.png` e `slime_defeat_spritesheet.png` com `frameWidth: 64`/`frameHeight: 48` (nenhum outro sheet carregado) — verificação: `npm run build` exit 0 e os 2 PNGs aparecem no bundle de `dist/assets/`.
- [ ] 1.2 Implementar `createEnemyAnimations()` registrando `slime-idle` (4 quadros @6 FPS, loop) e `slime-defeat` (4 quadros @12 FPS, `repeat: 0`) com guarda `anims.exists()`, chamada no `create()` — verificação: `npm run build` exit 0 e as duas chaves respondem `anims.exists(...) === true` na cena carregada (harness).

## 2. Corpo físico invisível + sprite visual do slime

- [ ] 2.1 Manter o retângulo do inimigo como único ator físico (posição 600/535, corpo estático 40×40 intocáveis) tornando-o invisível, e criar `enemyVisual` (`Sprite`, sem corpo) posicionado em `(enemy.x, enemy.bottom)` com `setOrigin(0.5, 40/48)` reproduzindo `slime-idle` — verificação: `npm run build` exit 0 e no navegador o quadrado verde é substituído pelo slime parado em loop `IDLE`, com os pés na linha do chão e as colisões de pisada/lateral funcionando igual.

## 3. Derrota com animação DEFEAT

- [ ] 3.1 Em `handleEnemyContact()`, manter intactos os testes de pisada (`touching`/`prev.y`/tolerância), a flag `enemyDefeated`, a desativação do colisor e o impulso `-690`, substituindo o `enemy.destroy()` imediato por `enemyVisual.play('slime-defeat')` — verificação: `npm run build` exit 0 e no navegador a pisada válida inicia a animação de derrota sem alterar o salto do personagem.
- [ ] 3.2 Registrar em `create()` um listener `animationcomplete` da chave `slime-defeat` que destrói `enemyVisual` e o corpo `enemy` (com guarda de destruição única) — verificação: no navegador, após a pisada o `DEFEAT` roda uma única vez, ao concluírem slime e corpo somem da cena, e nenhum contato posterior processa nova derrota nem reinicia a animação.

## 4. Verificação integrada

- [ ] 4.1 Rodar `npm run build` após todos os ajustes — verificação: exit code 0 (`tsc` sem erros + bundle Vite gerado).
- [ ] 4.2 Executar o harness de navegador cobrindo: slime ativo com `IDLE` em loop, pisada ⇒ `DEFEAT` ⇒ remoção, colisão lateral/por baixo sem derrota, ausência de erros de console — verificação: harness reporta todos os checks passando e nenhum erro de console.
- [ ] 4.3 Executar a regressão do Coxinha existente (6 animações, pés no chão, física/controles/impulso da pisada preservados) — verificação: harness reporta os checks de regressão passando (mesmos cenários das changes anteriores).
- [ ] 4.4 Validar os artefatos da change — verificação: `openspec validate inimigo-visual --strict` retorna exit 0 e `openspec status --change inimigo-visual` mostra 4/4 artefatos completos.
