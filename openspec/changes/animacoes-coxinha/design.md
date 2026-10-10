# Design

## Context

Ver `proposal.md` (seção Why) para a motivação. O estado atual que limita a abordagem:

- `src/scenes/GameScene.ts` mantém `playerBody` (Rectangle invisível 30×30, corpo Arcade) e `playerVisual` (`Phaser.GameObjects.Image` com textura `coxinha-idle`, origem `(0.5, 908/1024)` e escala `64/1024` → ~96×64 px na tela). O `update()` sincroniza o visual no corpo físico a cada frame via `setPosition(body.center.x, body.bottom)` — separação visual↔física já estabelecida.
- `preload()` usa `this.load.image('coxinha-idle', url)` com URL resolvida pelo Vite (import de módulo), não caminho estático.
- Física calibrada e congelada por esta change: gravidade `1840` (`src/main.ts`), `jumpForce -920`, pisada `-690`, velocidades 200/350, hitbox 30×30, inimigo estático 40×40 em x=600.
- Assets existentes: `coxinha-idle.png` e `coxinha-sprite-sheet.png`, ambos 1536×1024 RGBA de **apresentação** — sem grade regular de frames, não servem para recorte automático (restrição do usuário e do requisito da spec).
- **Dependência aberta desta change:** os assets de arte das animações (22 frames) **ainda não existem no projeto** — a primeira versão será obtida por geração assistida com IA (Decisão 1) em etapa separada da integração; a implementação não pode ser concluída sem eles (nenhuma task dependente de arte pode ser marcada antes da entrega + aprovação).
- Stack: Phaser 3.80 + TypeScript 5.4 + Vite 5; build `tsc && vite build`; sem framework de testes (verificação por harness de navegador, como na change arquivada `ajuste-pulo`).

## Goals / Non-Goals

**Goals:**

- Arte pixel art das 6 animações **produzida (primeira versão por geração assistida com IA) e aprovada em etapa separada da integração**, com identidade do Coxinha preservada (pelagem caramelo, focinho escuro, peito creme, orelhas eretas, corpo compacto) e tamanho visual compatível com o exibido hoje.
- Sprite sheet técnica nova (grade fixa, RGBA transparente) **convertida a partir da arte aprovada sem distorção**, integrada via loader do Phaser.
- 6 animações (`IDLE`, `WALK`, `RUN`, `JUMP`, `FALL`, `LAND`) com seleção automática pelo estado físico real, sem reinício da animação corrente.
- Zero alteração de física/hitbox/controles/colisões; visual continua objeto não-físico preso ao corpo por frame.

**Non-Goals:**

- Reprocessar `coxinha-sprite-sheet.png`/`coxinha-idle.png` como fonte de frames (ficam intocados, sem uso ativo).
- Animações de ataque, dano, morte; `HIT`; inimigos animados/móveis; sons; HUD; coletáveis; fases.
- Retoque de física (valores congelados) ou mudanças de build/runtime do jogo.
- Usar gerador procedural de desenho como **primeira** opção da arte (é apenas o último recurso; Decisão 1), integrar a primeira versão gerada por IA sem aprovação visual, ou integrar arte não aprovada de forma geral.

## Decisions

1. **Separação entre produção artística e implementação técnica**: a arte é produzida e revisada **antes e fora** da integração ao jogo. Ordem de preferência de produção: (1) **geração assistida com IA** — caminho preferencial para obter a primeira versão das 22 frames; (2) **revisão visual + ajustes ou produção complementar em ferramenta de pixel art** (Aseprite, Piskel, edição manual) — etapa prevista para corrigir inconsistências da geração (proporções, paleta, alinhamento, estilo) e completar frames, entregando PNGs individuais **48×32 RGBA** (rascunho maior é exportado por nearest-neighbor na própria ferramenta, nunca no conversor); (3) **último recurso**, apenas se (1)+(2) forem inviáveis: desenho procedural — rebaixado de primeira opção para fallback. A primeira versão gerada por IA **nunca é integrada sem aprovação visual**: geração → revisão/ajustes → aprovação → conversão → integração. Restrições inegociáveis em qualquer método: saída final como sheet técnica (grade fixa 48×32, RGBA transparente, sem textos/cenários/decoração), identidade do Coxinha e zero impacto em runtime/build. Alternativas sempre rejeitadas: recortar, alterar ou remover `coxinha-sprite-sheet.png`/`coxinha-idle.png` (não são técnicos; ficam intocados).
2. **Uma sprite sheet única + `this.load.spritesheet`** com `frameWidth: 48`/`frameHeight: 32` e `anims.create` por estado. Alternativa: atlas JSON (TexturePacker) — peso desnecessário para 6 animações.
3. **Frames 48×32 com escala inteira ×2 no display (caixa exibida 96×64 px)** — revisão do formato 32×32 pedida pelo usuário: o Coxinha atual ocupa a caixa exibida de 96×64 px (PNG 1536×1024 × escala `64/1024`); um frame quadrado 32×32 ×2 resultaria em 64×64 px, encolhendo a largura em 1/3 ou forçando distorção de proporções. Com 48×32 ×2 a caixa exibida fica **idêntica à atual**, com escala inteira (sem resampling) e arte em resolução pixel-art autêntica. `setOrigin(0.5, 1)` (pés na última linha do frame) remove o ajuste `908/1024` e ancora no `body.bottom`. A confirmação final de "mesmo tamanho do de hoje" é visual, na aprovação da arte (comparação lado a lado com o jogo rodando). Alternativa considerada: frame 96×64 nativo ×1 — descartada por perder o caráter chunky pixel-art 16-bit (pode ser reconsiderada se a arte aprovada exigir). Hitbox intocada.
4. **Máquina de estados derivada da física, sem novo estado físico** — decidida em `update()` a partir de `body.blocked.down`, `body.velocity` e `shiftKey`:
   - no ar: `v.y < 0` → `JUMP`; `v.y > 0` → `FALL`; `v.y == 0` (ápice) → mantém o estado anterior;
   - em terra: `|v.x| > 0` → `RUN` (Shift) ou `WALK`; `|v.x| == 0` → `LAND` enquanto a aterrissagem estiver pendente, senão `IDLE`;
   - aterrissagem detectada por transição ar→chão (flag `wasAirborne`); `LAND` roda uma vez (`repeat: 0`) e termina via evento `animationcomplete`. Prioridade: iniciar a movimentação (`WALK`/`RUN`) imediatamente substitui `LAND` (responsividade > fidelidade cosmética).
5. **Guard anti-re_restart por estado explícita**: campo `currentAnim: string` — `anims.play()` somente quando `nextState !== currentAnim`. Alternativa: `play(key, true)` (`ignoreIfPlaying`) — dependente do frame atual e menos explícito; a variável de estado é verificável por inspeção.
6. **Troca `Image` → `Sprite`** (`this.add.sprite`), mantendo posição/sincronia com o corpo; `setFlipX(body.velocity.x < 0)` como detalhe visual puramente cosmético (espelha andar/correr; não entra em spec por ser detalhe de apresentação sem comportamento observável novo).
7. **Organização**: animações registradas em método `createAnimations()` dentro de `GameScene` com chaves de textura/animação centralizadas como constantes; extrair módulo `src/animations/` fica para quando houver mais cenas (evita estrutura prematura de uma cena só).

## Composição das animações

As 22 frames (48×32 px cada; sheet final 1056×32 px, IDs 0–21) devem manter as proporções fixas do personagem — Bulldog Francês de pelagem caramelo, focinho escuro, peito creme, orelhas eretas, corpo compacto (cabeça grande, patas curtas). Diretriz de consistência para quem produz a arte: partir de um **corpo base único** e variar apenas deltas mínimos por frame (1–2 px), nunca redesenhar frames de forma independente; paleta e silhuetas são as mesmas nos 6 estados (a identidade não muda com a animação). O conversor técnico apenas monta a sheet — nunca redesenha nem redimensiona.

| Animação | Frames | FPS | Repeat | Composição dos frames |
|---|---|---|---|---|
| `IDLE` | 4 (0–3) | 6 | loop | Respiração: peito sobe/desce 1 px (frames 1 e 3), cabeça/orelhas com micro-deslocamento ≤1 px, patas paradas na linha de base. |
| `WALK` | 6 (4–9) | 10 | loop | Ciclo de passo de 2 tempos (patas dianteiras/traseiras alternadas), balanço corporal vertical ≤1 px, cabeça estável, orelhas eretas firmes. |
| `RUN` | 6 (10–15) | 14 | loop | Passada mais aberta que `WALK`, inclinação frontal de 1–2 px, orelhas levemente achatadas para trás, balanço vertical ≤2 px — pés seguem na linha de base. |
| `JUMP` | 2 (16–17) | 8 | loop | Subida: patas recolhidas sob o corpo (frame de impulso → frame esticado), orelhas para cima, peito projeta. |
| `FALL` | 2 (18–19) | 8 | loop | Descida: patas preparadas para o pouso, corpo compacto, orelhas elevadas pelo "vento". |
| `LAND` | 2 (20–21) | 12 | 1× | Aterrissagem: squash vertical de 1–2 px (corpo mais baixo/largo) + frame de recuperação; termina via `animationcomplete`. |

Duração total de `LAND` ≈ 170 ms; `JUMP`/`FALL` apenas indicam o estado — quem garante a troca é a máquina de estados (Decisão 4), então a troca de frames nunca atrasa a transição.

## Alinhamento visual ↔ corpo físico (30×30)

Regra de ouro: **a linha de base dos pés é idêntica nos 22 frames** (pixel opaco mais baixo na faixa y=30–31, variação ≤1 px) e o personagem fica centrado horizontalmente no frame 48×32 (bbox centrado em x=24 ±1 px). A arte deve ser entregue **já no tamanho final 48×32**; se o rascunho for maior, o redimensionamento (nearest-neighbor) acontece na ferramenta de arte, **nunca** no conversor. Combinação em runtime:

- `setOrigin(0.5, 1)` + `setPosition(body.center.x, body.bottom)`: a borda inferior do frame 48×32 coincide exatamente com `body.bottom` do retângulo físico 30×30 — os pés tocam a mesma linha de solo física em qualquer estado, sem flutuação entre frames.
- Escala inteira ×2 (frame 48×32 → caixa exibida 96×64 px, idêntica à do Coxinha atual): mesmo fator para todos os frames, sem resampling fracionário — proporções e alinhamento preservados na tela.
- O visual (caixa 96×64 px) segue maior que a hitbox (30×30), como já é hoje: a hitbox governa colisão e movimentação, o visual é apresentação — nenhum dos dois lê propriedades do outro.
- O conversor técnico (`scripts/build-coxinha-sheet.mjs`) **monta a sheet por cópia pixel a pixel** (sem escala, interpolação ou alteração de paleta) e **valida e falha alto** (exit nonzero) se: algum frame não for 48×32 RGBA, algum canto tiver alpha ≠ 0, a linha de base variar >1 px entre frames, o centro horizontal desviar >1 px ou a silhueta extrapolar a caixa. Arte em tamanho/formato errados é devolvida para correção na produção — o conversor nunca corrige, escala ou redesenha.

## Risks / Trade-offs

- [Arte de animação ainda não produzida (dependência aberta)] → registrada no Context: as tasks de produção/aprovação/conversão/integração permanecem desmarcadas até a entrega + aprovação; a integração de código é trivial e independente do método de produção (só depende do formato 48×32).
- [Primeira versão gerada por IA produzir frames inconsistentes entre si (proporções, paleta, alinhamento, estilo)] → revisão visual obrigatória + rota prevista de ajustes/produção complementar em ferramenta de pixel art até a consistência passar (Decisão 1); se persistir, fallback procedural; o conversor valida alinhamento e falha alto.
- [Arte entregue com identidade/proporções inadequadas, em tamanho errado ou com elementos extras (texto, cenário, decoração)] → gate de aprovação visual antes da integração + validação técnica do conversor falha alto (devolve para correção na arte; o conversor nunca corrige, escala ou redesenha) + ajustes em ferramenta de pixel art antes de qualquer nova tentativa de integração.
- [Ferramenta de conversão poluir o runtime/build do jogo] → conversor usa Node nativo (`zlib`) ou, se necessário, `devDependencies` exclusiva; o jogo nunca importa essas libs e `npm run build` permanece o mesmo.
- [Inconsistência de linha de base ou centragem entre frames causando "flutuação" visual do personagem] → regra de linha de base documentada + validação programática no gerador (exit nonzero, roda antes da integração) + confirmação final na âncora `body.bottom` no navegador.
- [Reinício indevido da animação em bordas de estado (ex.: sinal de `v.y` no ápice ou micro-contato no chão)] → guarda por `currentAnim` + decisão de estado com `v.y == 0` mantendo estado anterior + `LAND` só na transição ar→chão com `wasAirborne`.
- [`LAND` atrasar a leitura de movimento logo após pousar] → `WALK`/`RUN` têm prioridade sobre `LAND`; a animação é cosmética curta (~170 ms) e nunca bloqueia input (input é da física, não do visual).
- [Novo visual mudar a "presença" do personagem sem tocar a hitbox] → escala inteira ×2, origem no pé, `playerBody` intocável; a regressão existente (hitbox, controles, pisada) segue como portão.
- [Automatizar a verificação de qual animação está ativa é mais difícil que medir física] → verificação no navegador por inspeção programática (estado da animação consultável via CDP/`anims.currentAnim`) somada à regressão comportamental 23/23 já usada em `ajuste-pulo`; cenários da spec mapeados 1:1 para checagens manuais/guiadas.
- [`setFlipX` introduzir comportamento visual inesperado em movimento parado] → flip aplicado somente quando `|v.x| > 0`, zero impacto em física.

## Migration Plan

1. **Produção da arte** (etapa externa ao código; dependência aberta): primeira versão das 22 frames 48×32 RGBA por **geração assistida com IA**, com ajustes ou produção complementar em ferramenta de pixel art se a geração não produzir frames consistentes (Decisão 1) — nada do código do jogo é tocado nesta etapa.
2. **Revisão visual + aprovação** (identidade: pelagem caramelo, focinho escuro, peito creme, orelhas eretas, corpo compacto; consistência de dimensões/proporções/alinhamento dos pés; ausência de textos, cenários ou decoração; comparação lado a lado com o tamanho atual exibido) — reprovação retorna para a produção.
3. **Conversão**: `scripts/build-coxinha-sheet.mjs` monta `assets/coxinha/coxinha-frames.png` (1056×32) por cópia pixel a pixel + validação técnica (falha alto devolve para a arte).
4. **Integração**: `preload()`→`load.spritesheet`, criar animações (`createAnimations()`), trocar `Image`→`Sprite` com origem/escala novos.
5. **Seleção de estado** + guard em `update()` (só leitura de `body.velocity`/`blocked` + escrita no visual).
6. `npm run build` (exit 0) → inspeção no navegador (6 estados + não-reinício + espelhamento + tamanho/âncora) → regressão de preservação (hitbox/controles/pisada) → `openspec validate --strict`.
7. Rollback: `git revert` puro — sem dados persistentes, sem mudança de contrato; os arquivos novos (conversor, PNGs de arte, sheet) são aditivos e os assets antigos nunca são removidos.

## Open Questions

- A composição das animações (frames/fps por estado) está documentada na seção acima como referência estrutural; polimento fino — ajustes de fps, duração de `LAND` ou micro-detalhes dos quadros — pode ocorrer durante a revisão visual sem alterar specs, abordagem ou quebra de tarefas. Nenhum outro ponto em aberto.

