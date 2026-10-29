# Proposal

## Why

A cena atual (`GameScene`) exibe apenas um fundo de cor sólida (`#87CEEB` em `main.ts`). Não há cenário de fundo visual, apenas plataformas e obstáculos marrons sobre o céu liso. Para o próximo arco do jogo — *A Busca pelo Petisco Perdido* — o mundo precisa de ambientação que remeta ao Nordeste brasileiro (caatinga, serras, formações rochosas, céu azul), com camadas de parallax que acompanhem a câmera horizontal e reforcem a sensação de profundidade durante a travessia da fase extensa (2400×600).

## What Changes

- **Camadas de fundo visual (parallax)**: adicionar 4 camadas de tileSprites (céu, serras distantes, vegetação da caatinga, elementos do primeiro plano) que se movem a velocidades diferentes proporcionalmente ao `scrollX` da câmera, criando efeito de profundidade.
- **Assets pré-aprovados**: os 4 PNGs de fundo serão fornecidos e aprovados externamente (fora do Cline) antes de qualquer implementação. O Cline se limita à integração dos assets já aprovados.
- **Somente visual**: nenhuma camada possui corpo físico ou colisão; não afeta jogabilidade, física, spawn, plataformas, slime ou animações.
- **Renderização pixel-perfect preservada**: todas as camadas usam texturas PNG com filtro nearest-neighbor, posições inteiras e escala inteira, alinhadas às configurações existentes (`pixelArt: true`, `roundPixels: true`, zoom 1).
- **Bloqueio de implementação**: nenhuma alteração em código será iniciada até que os 4 assets finais estejam presentes no repositório e aprovados.

## Capabilities

### New Capabilities

- `cenario-visual-nordestino`: camadas de fundo em pixel art inspiradas no Nordeste brasileiro, com rolagem paralaxe horizontal vinculada à câmera, sem colisões e sem impacto na jogabilidade.

### Modified Capabilities

- Nenhuma. Esta change é puramente aditiva e visual; não altera requisitos de especificações existentes.

## Impact

- **Código**: `src/scenes/GameScene.ts` — carregamento de texturas de fundo (4 PNGs pré-aprovados), criação dos tileSprites em `create()` e atualização de `tilePositionX` em `update()` para sincronizar com `camera.scrollX`. `src/main.ts` permanece intocado (800×600, `pixelArt`, `roundPixels`, gravidade 1840).
- **Física**: inalterada — gravidade `1840`, salto `-920`, velocidades `200`/`350`, impulso `-690`, hitbox `30×30` preservados.
- **Assets**: 4 PNGs de fundo em `assets/background/nordestino/`, fornecidos e aprovados externamente antes da implementação.
- **Fora de escopo**: produção/desenho de assets pelo Cline (Aseprite ou qualquer outra ferramenta), novos inimigos, novas habilidades, transições de fase, checkpoints, colisões em camadas de fundo, zoom/rotação de câmera, rolagem vertical.
- **Verificação**: `npm run build` (exit 0) + `openspec validate --strict` + inspeção visual no navegador (parallax suave, sem borrão, sem áreas vazias, camadas alinhadas ao chão, console limpo) — executado apenas após os 4 assets aprovados estarem presentes.