# Tasks

## 1. Assets de fundo (pixel art Nordeste)

- [ ] 1.1 Produzir 4 PNGs de fundo (céu, serra, caatinga, vegetação) em `assets/background/nordestino/`, estilo pixel art coerente, altura 600 px, largura múltipla de 800 px — verificação: arquivos existem e dimensões conferidas.
- [ ] 1.2 Confirmar que as texturas usam filtro nearest-neighbor (sem borrão/antialiasing) — verificação: inspeção visual dos PNGs.

## 2. Integração no GameScene

- [ ] 2.1 Adicionar pré-carregamento das 4 texturas de fundo em `preload()` — verificação: `npm run build` passa sem erro de asset ausente.
- [ ] 2.2 Criar os 4 `tileSprite` em `create()`, na ordem céu → serra → caatinga → vegetação, antes do chão e plataformas — verificação: camadas visíveis atrás do cenário no navegador.
- [ ] 2.3 Atualizar `tilePositionX` de cada camada em `update()` com `Math.floor(scrollX * fator)` — verificação: parallax suave durante a rolagem horizontal.

## 3. Validação visual e regressão

- [ ] 3.1 Confirmar que o parallax para nos limites do mundo (x=0 e x=2400), sem áreas vazias — verificação: navegador, câmera nos extremos.
- [ ] 3.2 Confirmar renderização pixel-perfect (sem tremor, sem borrão, posições inteiras) — verificação: inspeção visual durante scroll.
- [ ] 3.3 Testar regressão: spawn, salto, plataformas, slime (pisada), animações, limites do mundo continuam funcionando — verificação: checklist do `camera-fase-longa` reexecutado.
- [ ] 3.4 Executar `npm run build` (exit 0) e `openspec validate cenario-visual-nordestino --strict` — verificação: ambos passam.

## 4. Arquivamento

- [ ] 4.1 Arquivar a change com `openspec archive cenario-visual-nordestino` após aprovação dos artefatos e validação — verificação: change movida para `openspec/changes/archive/` com data.