# Proposal

## Why

O Coxinha ainda é exibido como imagem estática (pose `IDLE`): durante o gameplay não há distinção visual entre parado, andando, correndo, subindo, caindo ou aterrissando, o que reduz a leitura do estado do personagem e a sensação de vitalidade do jogo de plataforma. Com a identidade visual (`personagem-coxinha`) e a física do salto (`ajuste-pulo`) já estabilizadas, este é o próximo passo natural. O asset `assets/coxinha/coxinha-sprite-sheet.png` existente é de apresentação — não possui grade regular de frames — e portanto não está preparado para recorte automático; é necessário preparar assets de pixel art técnicos para a integração.

## What Changes

- Produzir (etapa de arte **separada**, com revisão e aprovação antes de qualquer integração ao jogo) e integrar asset(s) de pixel art 16-bit do Coxinha com frames consistentes, fundo transparente e aparência fiel ao personagem (Bulldog Francês de pelagem caramelo, focinho escuro, peito creme e orelhas eretas). A sprite sheet de apresentação existente **não** será utilizada como sprite sheet técnica (sem recorte automático a partir dela), e `coxinha-idle.png` deixa de ser a fonte visual ativa, embora ambos os assets permaneçam no projeto. **Dependência registrada:** os assets de arte das animações ainda não existem — a integração depende deles.
- Criar no Phaser as 6 animações do protagonista: `IDLE` (parado), `WALK` (andando), `RUN` (correndo), `JUMP` (subindo), `FALL` (descendo) e `LAND` (aterrissando).
- Seleção automática da animação conforme o estado real do personagem: `IDLE` quando parado no chão; `WALK` ao caminhar; `RUN` ao correr; `JUMP` durante a subida; `FALL` durante a descida; `LAND` ao aterrissar.
- Evitar reiniciar continuamente a mesma animação durante o gameplay: a animação só é solicitada quando o estado muda, mantendo o loop atual em execução enquanto o estado persistir.
- Preservar integralmente a física ARCADE, a hitbox de 30×30, a gravidade atual, a força do salto, o impulso da pisada, as velocidades horizontais, os controles, as colisões e a mecânica de derrotar o inimigo ao pular sobre ele. O visual continua separado do corpo físico (sincronizado a cada frame), sem interferir no posicionamento, na detecção de colisões ou na movimentação.
- Fora de escopo (não implementar nesta change): animação de ataque, dano, morte do Coxinha, inimigos móveis, sons, HUD, coletáveis ou novas fases — o objetivo é exclusivamente estabelecer o sistema de animações básicas do protagonista.

## Capabilities

### New Capabilities

(nenhuma)

### Modified Capabilities

- `personagem-coxinha`: os requisitos "Pose IDLE do Coxinha na cena" e "Estrutura preparada para futuras animações" são substituídos por novos requisitos ("Representação visual animada do Coxinha" — fonte ativa = novo asset técnico de frames, sem recorte da sprite sheet de apresentação; "Seleção automática de animação conforme o estado" — 6 estados com guarda contra reinício da mesma animação, `HIT` permanece fora de escopo), com os motivos/migrações registrados no delta; o requisito "Preservação da física e movimentação" é estendido com o impulso da pisada e a derrota do inimigo entre os comportamentos preservados. O requisito "Hitbox preservada" permanece sem alteração.

A capacidade `jogo-inicial` não precisa de delta: velocidades, controles, salto (faixas de tempo/altura), gravidade e limites horizontais não mudam — a animação é puramente visual e herda integralmente o comportamento já especificado. A capacidade `inimigo-base` também não precisa de delta: a mecânica de derrota por pisada, o impulso para cima e a regra de segundo salto permanecem idênticos; a constante do impulso é detalhe de implementação já coberto pelo requisito existente.

## Impact

- Código: `src/scenes/GameScene.ts` — `preload()` carrega a nova sprite sheet técnica (URL resolvida pelo Vite); `create()` registra as animações; `update()` seleciona a animação pelo estado real com guarda de mudança de estado, mantendo o vínculo visual↔corpo físico. Possível fatoração em módulo de animações (ex.: `src/animations/`) se ajudar na organização, sem alterar a lógica de física.
- Assets: novo(s) PNG técnico(s) em `assets/coxinha/` (frames consistentes, RGBA transparente); `coxinha-idle.png` e `coxinha-sprite-sheet.png` permanecem no projeto sem uso ativo.
- Sem mudanças de física, hitbox, controles ou de runtime/build do jogo. A arte será produzida e aprovada fora do código (dependência aberta: assets ainda não produzidos); a conversão para sprite sheet técnica usa script Node técnico (cópia pixel a pixel, sem dependências de runtime). A sprite sheet de apresentação existente não é reutilizada como fonte.
- Verificação posterior durante a aplicação: `npm run build` (exit 0) + inspeção no navegador (animações corretas por estado) + regressão da mecânica existente (pisada/controles/salto intactos).
