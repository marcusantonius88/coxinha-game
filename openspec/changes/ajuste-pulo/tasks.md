# Tasks

## 1. Baseline e referência

- [x] 1.1 Iniciar o servidor de desenvolvimento (`npm run dev`) e medir no navegador o salto atual do Coxinha (tempo total no ar e altura máxima), anotando os valores obtidos — verificação: valores medidos registrados (ref. teórica hoje: ~2,67 s / ~267 px)
  - Medido em 07/10/2026 via Chromium headless no build de produção (`npm run preview`): réplicas 2,575 / 2,665 / 2,667 s → mediana **2,665 s**; altura **263 px**.
- [x] 1.2 Medir o bounce atual da pisada (altura/tempo) e registrar a relação bounce/salto como referência — verificação: valor medido anotado (ref. teórica hoje: ~150 px / relação ~0,56)
  - Medido em 07/10/2026 (mesmo setup): rise do bounce **148 px**, voo ~2,2 s; relação bounce/salto = 148/263 ≈ **0,56**.

## 2. Ajuste dos parâmetros físicos *(1ª iteração — valores refinados na seção 5)*

- [x] 2.1 Alterar `jumpForce` de `-400` para `-800` em `src/scenes/GameScene.ts`, com comentário relacionando o valor à gravidade (preset Equilibrado) — verificação: `npm run build` passa e o diff mostra apenas a constante do salto alterada
- [x] 2.2 Alterar `arcade.gravity.y` de `300` para `1330` em `src/main.ts`, com comentário indicando o preset Equilibrado — verificação: `npm run build` passa e o diff mostra apenas a gravidade alterada
- [x] 2.3 Alterar o impulso da pisada de `-300` para `-600` em `handleEnemyContact()` em `src/scenes/GameScene.ts`, com comentário registrando a razão 0,75 em relação à nova força do salto — verificação: `npm run build` passa e o diff mostra apenas a constante do impulso alterada

## 3. Validação de comportamento *(1ª iteração)*

- [x] 3.1 Executar `npm run build` após as alterações e confirmar que compila sem erros — verificação: exit code 0 do comando
- [x] 3.2 Medir o salto pleno no navegador e confirmar tempo total entre 1,0 e 1,4 s (alvo ~1,2 s) e altura entre 220 e 260 px (alvo ~240 px) — verificação: medições dentro das faixas do spec
- [x] 3.3 Validar a pisada no inimigo: cair em cima derrota o inimigo (some da tela e da física), o personagem rebota para cima (~135 px de bounce) e não ganha segundo salto no ar — verificação: comportamento observado no navegador
- [x] 3.4 Regressão de preservação: velocidade normal/corrida (`Shift`), controles (`ArrowLeft`/`ArrowRight`/`ArrowUp`/`Space`), colisão com a plataforma, limites horizontais e HUD intactos — verificação: checklist manual na cena inicial sem mudanças percebidas

## 4. Validação OpenSpec

- [x] 4.1 Executar `openspec validate ajuste-pulo --strict` e confirmar zero violações — verificação: `All specs valid!`
- [x] 4.2 Executar `openspec status --change ajuste-pulo` e confirmar que não há artefato pendente na mudança — verificação: proposal, specs, design e tasks todos marcados como concluídos

## 5. Refino dos alvos (após teste manual — permanência no ar ~1,0 s)

- [ ] 5.1 Alterar `jumpForce` de `-800` para `-920` em `src/scenes/GameScene.ts`, atualizando o comentário para o novo alvo (gravidade 1840, T ≈ 1,0 s, h teórico 230 px) — verificação: `npm run build` passa e o diff mostra apenas a constante do salto alterada
- [ ] 5.2 Alterar `arcade.gravity.y` de `1330` para `1840` em `src/main.ts`, atualizando o comentário para o alvo refinado — verificação: `npm run build` passa e o diff mostra apenas a gravidade alterada
- [ ] 5.3 Alterar o impulso da pisada de `-600` para `-690` em `handleEnemyContact()` em `src/scenes/GameScene.ts`, mantendo o comentário da razão 0,75 em relação ao `jumpForce` — verificação: `npm run build` passa e o diff mostra apenas a constante do impulso alterada
- [ ] 5.4 Executar `npm run build` após as alterações e confirmar exit code 0 — verificação: compila sem erros
- [ ] 5.5 Medir o salto pleno no navegador e confirmar tempo total entre 0,9 e 1,1 s (alvo ~1,0 s) e altura entre 220 e 230 px (alvo ~225 px) — verificação: medições dentro das faixas do spec
- [ ] 5.6 Validar a pisada no inimigo: derrota o inimigo, bounce ~125 px medido (faixa 90–155 px; teórico ~129 px) e sem segundo salto no ar — verificação: comportamento observado no navegador
- [ ] 5.7 Regressão de preservação: velocidade normal/corrida, controles (`ArrowLeft`/`ArrowRight`/`ArrowUp`/`Space`/`Shift`), colisão com a plataforma, limites horizontais, HUD e ausência de erros de console intactos — verificação: harness de regressão com 23/23 checks
- [ ] 5.8 Executar `openspec validate ajuste-pulo --strict` e `openspec status --change ajuste-pulo` após as alterações — verificação: change válida e artefatos proposal/specs/design/tasks completos

