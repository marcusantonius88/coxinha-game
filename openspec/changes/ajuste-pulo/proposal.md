# Proposal

## Why

O salto atual do Coxinha tem permanência no ar excessiva: com `jumpForce = -400` e gravidade `y: 300`, o tempo teórico de voo é de ~2,7 s (o relato de uso indica até ~4 s), gerando uma sensação de flutuação ruim para um jogo de plataforma 2D e dificultando o controle de precisão — inclusive para pisar nos inimigos. O objetivo é tornar o salto mais curto e responsivo, mantendo uma altura de salto adequada e preservando o sentimento de controle.

## What Changes

- Ajustar exclusivamente os parâmetros físicos responsáveis pelo salto (força inicial do salto e gravidade), para o preset **Equilibrado** aprovado:
  - tempo total no ar de um salto pleno: alvo ~1,2 s (faixa de aceitação 1,0–1,4 s);
  - altura do salto pleno: alvo ~240 px (faixa de aceitação 220–260 px; hoje ~267 px).
- Escalar o impulso vertical da pisada nos inimigos proporcionalmente à nova gravidade (de `-300` para ~`-600`), preservando a relação atual entre o bounce da pisada e o salto normal, de modo que a mecânica de pisada continue funcionando com a mesma sensação.
- Não alterar: velocidade horizontal, corrida, hitbox, controles, colisões, inimigos (lógica/posições), sistema de dano, animações, sons, HUD, coletáveis ou fases.

## Capabilities

### New Capabilities

(nenhuma)

### Modified Capabilities

- `jogo-inicial`: o requisito "Pulo" passa a exigir tempo de voo e altura de salto dentro de faixas observáveis (preset Equilibrado), mantendo as regras existentes de pulo somente no chão e ausência de segundo salto no ar.

A capacidade `inimigo-base` não precisa de delta: o requisito "Impulso para cima após a pisada" (impulso menor que o salto, elevação acima do inimigo, sem segundo salto) e "Derrota por pisada" continuam sendo atendidos com os novos parâmetros — a constante do impulso é detalhe de implementação. O requisito "Preservação das mecânicas existentes" de `inimigo-base` restringe a implementação daquela change (já arquivada e cumprida); esta change altera gravidade/força do salto de forma autorizada, mantendo a interação de pisada preservada.

## Impact

- Código: `src/main.ts` (gravidade `arcade.gravity.y`) e `src/scenes/GameScene.ts` (`jumpForce` na `update()` e `setVelocityY` do impulso da pisada em `handleEnemyContact()`).
- Sem novas dependências, sem mudanças de asset, build ou configuração de ferramentas.
- Verificação posterior: `npm run build` + medição real no navegador (tempo no ar, altura, pisada) durante a aplicação.
