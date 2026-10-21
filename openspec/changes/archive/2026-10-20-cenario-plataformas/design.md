# Design

## Context

Ver `proposal.md` (seção Why). O estado atual que limita a abordagem:

- Cena fixa **800×600** (sem câmera/rolagem — restrição da change): todo o conteúdo precisa caber em `x ∈ [0, 800]`, visível de uma vez.
- `src/scenes/GameScene.ts`: chão `rectangle(400, 560, 800, 10)` → topo em **y=555**; inimigo slime (corpo estático 40×40 em x=580..620, topo y=515); Coxinha nasce em (400, 500), corpo 30×30 com `collideWorldBounds`; colisor player×chão e player×slime já existem; `update()` e máquina de animações independentes da geometria do cenário.
- Física aprovada e congelada: gravidade **1840**, salto **−920**, velocidades **200/350**, impulso da pisada **−690**. Alcance derivado (registrado no `main.ts` e na spec `jogo-inicial`): altura máxima **≈225 px** (220–230), tempo de voo **≈1,0 s** → alcance horizontal **≈200 px (andando) / ≈350 px (correndo)**.
- Renderização pixel-perfect (`pixelArt` + `roundPixels`) — coordenadas inteiras em todas as estruturas.
- Harnesses de regressão existentes (sessões anteriores) usam geometria do cenário: probe de IDLE no spawn (x≈400), pisada no slime a partir de x≈400–430 (corredor de voo x≈430..640), corrida até a borda direita, retorno pela esquerda — **o layout proposto mantém o corredor do spawn→slime livre de estruturas**, preservando essas verificações sem retoque.

## Goals / Non-Goals

**Goals:**

- Seção de plataforma jogável e viável de ponta a ponta com a física atual, dentro da tela.
- Estruturas sólidas (pisar em cima, bloquear por baixo/lateral), estilo pixel art coerente (retângulos, cor de terra existente, inteiros).
- Zero alteração de física, controles, animações, slime, chão, limites e render config.

**Non-Goals:**

- Plataformas de passagem (one-way), escadas, movimento de estruturas, blocos destrutíveis.
- Câmera com rolagem, novos inimigos, dano/vidas/pontuação/checkpoints/fases, sons, novos assets PNG.

## Decisions

1. **Estruturas como retângulos sólidos estáticos num grupo** (`StaticGroup` + um único `collider(playerBody, platforms)`): mesma primitiva física do chão (sólido em todas as direções, sem passagem), extensível e com uma linha de integração no `create()`. Alternativa descartada: one-way platforms (complexidade extra e regra nova de colisão não pedida).
2. **Layout proposto** (medidas derivadas do alcance; ajuste fino de ±20 px permitido na validação visual sem mudar specs):
   - **Obstáculo A**: x=280..320 (40 de largura), topo y=505 (50 px acima do chão — 22% do alcance) — à esquerda do spawn;
   - **Plataforma P1**: x=40..230 (190 de largura), topo y=455 (**100 px** — margem de 125 px sobre o alcance);
   - **Obstáculo B**: x=330..370 (40 de largura), topo y=495 (60 px) — entre o Obstáculo A e o spawn, desviando o percurso sem tocar no corredor do slime;
   - **Plataforma P2**: x=650..760 (110 de largura), topo y=425 (**130 px** — margem de 95 px) — à direita do slime.
   - **Corredor x≈400..640 no nível do chão fica livre** (chão + slime apenas): rotas de pisada aprovadas (lançamento em x∈373..443 → contato em x∈565..635) continuam exatas; o voo de pisada passa **acima** de qualquer estrutura (piso do corpo no voo ≈327 px em x=520, muito acima dos obstáculos de topo ≥495).
3. **Clima físico por estrutura** (validação aritmética): P1/P2 são puláveis do chão (100/130 < 225) e entre si (de P1, sobe 225 → alcança qualquer topo acima de 230; o salto horizontal de 200 px cobre os vãos); Obstáculos A/B são puláveis do chão (50/60 px); sob P1 ( folga de 80 px) e sob P2 (folga de 110 px) o Coxinha passa em pé (corpo 30, visual 64 → 491 > 475/445). Bonk sob P1/P2 devolve ao chão sem aprisionamento (abertura lateral sempre livre).
4. **Visual**: mesmíssimo preenchimento `0x8b4513` do chão (coerência pixel art, sem gradientes/traços — traços de retângulo gerariam antialias); `roundPixels` (já ativo) garante bordas inteiras; sem escala/rotação. Alternativa (faixa de destaque mais clara no topo) descartada: quebraria as checagens de silhueta dos harnesses existentes (que filtram por `0x8b4513`) sem ganho funcional — pode ser reapresentada em change futura de polimento.
5. **Colisões**: um `collider` novo player×plataformas, chamado à parte dos existentes (chão/slime intocados); inimigos não colidem com plataformas (corpo estático, não afetado por gravidade — nada a fazer). A presença de estruturas não toca `update()`, `resolveAnimState()` nem `handleEnemyContact()` — a seleção de animação deriva apenas de velocidade/contato com o **chão** (`onFloor` é verdadeiro também sobre plataformas, então `land`/`idle`/`walk` funcionam naturalmente ao subir/descer).

## Risks / Trade-offs

- [Arestas de plataforma "comem" o aterrissar (separação Arcade empurra o jogador para fora)] → corpos axis-aligned e o jogador cai de cima (contato pelo topo resolve para cima); cenário verificado no harness (parado sobre P1/P2).
- [Salto rasante de cabeça na base de P2 (130 px exigem aproximação bem posicionada)] → margem de 95 px sobre o alcance máximo; vãos de abordagem ≥ 130 px; ajuste fino de posição na validação visual.
- [Cabeça batendo na base de P2 ao saltar do chão embaixo dela] → comportamento esperado (sólido), sem aprisionamento (folga lateral sempre livre, sem poços); verificado no cenário "Sem bloqueio permanente".
- [Harnesses de regressão dependem da geometria] → corredor spawn→slime preservado livre (Decisão 2) e cor de estruturas idêntica ao chão mantém os filtros de silhueta válidos; ajustes de harness ficam para a aplicação, sem tocar em specs.
- [Layout cansaço do "corredor vazio" no meio] → aceito para preservar as rotas de pisada aprovadas; polimento de composição fica para futura change de arte/cenário (fora do escopo).

## Migration Plan

1. No `create()`: criar `platforms` (StaticGroup) com os 4 retângulos do layout + `collider` com `playerBody`.
2. `npm run build` (exit 0) → `openspec validate --strict` → harness de navegador: aterrissar/subir/PAREado em P1 e P2, bloqueio lateral dos Obstáculos A/B, passeio sob P1/P2, travessia completa no dois sentidos, slime (pisada/DEFEAT/lateral) intacto, zero erros de console + screenshots para inspeção visual.
3. Rollback: `git revert` puro — bloco aditivo no `create()`; nenhum asset ou sistema tocado.

## Open Questions

- Ajuste fino de ±20 px nas posições/alturas das estruturas durante a revisão visual, dentro do envelope de alcance já validado — sem mudar specs, abordagem ou o número de tarefas.
- Polimento visual futuro (faixa de destaque no topo das plataformas) fica para change de cenário dedicada; nenhum outro ponto em aberto.

