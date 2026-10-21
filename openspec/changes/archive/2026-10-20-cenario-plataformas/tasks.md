# Tasks

## 1. Estruturas do cenário

- [x] 1.1 Implementar no `create()` o grupo de estruturas sólidas (StaticGroup) com os 4 retângulos do layout do design (Obstáculo A x280–320 topo505; P1 x40–230 topo455; Obstáculo B x330–370 topo495; P2 x650–760 topo425), cor `0x8b4513`, coordenadas inteiras — verificação: `npm run build` exit 0 e as 4 estruturas visíveis no cenário entre x=40 e x=760, nenhuma sobre o spawn (x≈400) nem sobre o slime (x=568..632).
- [x] 1.2 Adicionar o `collider` entre `playerBody` e o grupo de estruturas, sem tocar nos colisores existentes (chão/slime) — verificação: `npm run build` exit 0 e no navegador o Coxinha pousa sobre P1/P2, é bloqueado pela lateral e pela base delas, sem atravessar nenhuma estrutura.

## 2. Viabilidade do percurso

- [x] 2.1 Validar no navegador os saltos de alcance: chão→P1 (100 px), chão→P2 (130 px), pulo dos Obstáculos A/B (50/60 px), apoio estável e novo salto a partir de cada plataforma — verificação: harness/screenshot mostram o Coxinha em repouso sobre P1 e sobre P2 (`bottom` no topo da plataforma) e passando por cima dos obstáculos.
- [x] 2.2 Validar travessia sem bloqueio permanente: andar sob P1 (folga 80 px) e sob P2 (folga 110 px), bonk na base de P2 volta ao chão sem aprisionar, descida livre de P1/P2, percurso completo nos dois sentidos até os limites da tela — verificação: harness percorre a seção nos dois sentidos sem o personagem ficar preso; screenshot da seção completa registrada.
- [x] 2.3 Confirmar preservação dos sistemas existentes: slime (pisada ⇒ `DEFEAT` ⇒ remoção; lateral não derrota), animações do Coxinha nos 6 estados, física (gravidade 1840, salto −920, pisada −690, hitbox 30×30) e limites horizontais — verificação: harness de regressão existente passa (cenários de IDLE/jump/fall/pisada) e `git diff` não altera constantes de física nem `handleEnemyContact`.

## 3. Verificação integrada

- [x] 3.1 Rodar `npm run build` após todos os ajustes — verificação: exit code 0 (`tsc` sem erros + bundle Vite gerado).
- [x] 3.2 Executar o harness de navegador cobrindo: aterrissar nas plataformas, colisões laterais/superiores, travessia no dois sentidos, slime intacto, zero erros de console — verificação: harness reporta todos os checks passando; screenshots inspecionados visualmente.
- [x] 3.3 Validar os artefatos da change — verificação: `openspec validate cenario-plataformas --strict` retorna exit 0 e `openspec status --change cenario-plataformas` mostra 4/4 artefatos completos.
