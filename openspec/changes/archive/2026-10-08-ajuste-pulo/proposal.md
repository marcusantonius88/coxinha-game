# Proposal

## Why

O salto atual do Coxinha tem permanência no ar excessiva: com `jumpForce = -400` e gravidade `y: 300`, o tempo teórico de voo é de ~2,7 s (o relato de uso indica até ~4 s), gerando uma sensação de flutuação ruim para um jogo de plataforma 2D e dificultando o controle de precisão — inclusive para pisar nos inimigos. O objetivo é tornar o salto mais curto e responsivo, mantendo uma altura de salto adequada e preservando o sentimento de controle.

Após a 1ª iteração (alvos de ~1,2 s / ~240 px) e teste manual, a permanência no ar ainda pareceu um pouco lenta: o alvo foi refinado para ~1,0 s no ar com altura em torno de 220–230 px — mais responsivo, sem tornar o salto excessivamente baixo ou brusco.

## What Changes

- Ajustar exclusivamente os parâmetros físicos responsáveis pelo salto (força inicial do salto e gravidade) para os alvos refinados:
  - tempo total no ar de um salto pleno: alvo ~1,0 s (faixa de aceitação 0,9–1,1 s);
  - altura do salto pleno: alvo ~225 px (faixa de aceitação 220–230 px; original ~267 px);
  - valores coerentes com os alvos (equações de projectile `g = 8h/T²` e `v0 = 4h/T`): `jumpForce` de `-400` para `-920` e `arcade.gravity.y` de `300` para `1840`.
- Ajustar proporcionalmente o impulso vertical da pisada nos inimigos (de `-300` para `-690`, razão 0,75 em relação à nova força do salto), preservando a relação bounce/salto ≈0,56 e um bounce pequeno e controlado (~130 px teórico), de modo que a mecânica de pisada continue funcionando com a mesma sensação.
- Não alterar: velocidade horizontal, corrida, hitbox, controles, colisões, inimigos (lógica/posições), sistema de dano, animações, sons, HUD, coletáveis ou fases.

## Capabilities

### New Capabilities

(nenhuma)

### Modified Capabilities

- `jogo-inicial`: o requisito "Pulo" passa a exigir tempo de voo e altura de salto dentro de faixas observáveis refinadas (~1,0 s no ar, 220–230 px), mantendo as regras existentes de pulo somente no chão e ausência de segundo salto no ar.

A capacidade `inimigo-base` não precisa de delta: o requisito "Impulso para cima após a pisada" (impulso menor que o salto, elevação acima do inimigo, sem segundo salto) e "Derrota por pisada" continuam sendo atendidos com os novos parâmetros — a constante do impulso é detalhe de implementação. O requisito "Preservação das mecânicas existentes" de `inimigo-base` restringe a implementação daquela change (já arquivada e cumprida); esta change altera gravidade/força do salto de forma autorizada, mantendo a interação de pisada preservada.

## Impact

- Código: `src/main.ts` (gravidade `arcade.gravity.y`) e `src/scenes/GameScene.ts` (`jumpForce` na `update()` e `setVelocityY` do impulso da pisada em `handleEnemyContact()`), incluindo os comentários que relacionam esses três valores.
- Sem novas dependências, sem mudanças de asset, build ou configuração de ferramentas.
- Verificação posterior: `npm run build` + medição real no navegador (tempo no ar, altura, pisada) durante a aplicação.
