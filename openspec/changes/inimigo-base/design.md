# Design

## Context

A cena inicial (`src/scenes/GameScene.ts`) já implementa a capacidade `jogo-inicial` e a capacidade `personagem-coxinha`: Coxinha é um corpo físico ARCADE invisível de 30x30 (hitbox) com representação visual separada, gravidade `y: 300`, colisão com a plataforma, controles de movimento/corrida/salto e limites horizontais.

Não existe nenhum inimigo, nenhuma colisão entre jogador e inimigo e nenhum asset de inimigo no projeto (`assets/` contém apenas `coxinha-idle.png` e `coxinha-sprite-sheet.png`).

Ver `proposal.md` - Why para a motivação desta change; os requisitos comportamentais estão em `specs/inimigo-base/spec.md`.

## Goals / Non-Goals

### Goals

- Criar o primeiro inimigo na cena inicial, sobre a plataforma, com hitbox própria.
- Manter o inimigo parado (sem IA e sem movimentação própria).
- Detectar a pisada: queda do Coxinha sobre a parte superior do inimigo durante um salto.
- Derrotar o inimigo na pisada, removendo-o da cena.
- Aplicar um pequeno impulso vertical para cima no Coxinha após a pisada.
- Tratar colisões laterais e por baixo como colisão física normal, sem derrotar o inimigo.
- Preservar integralmente física, hitbox, controles, velocidades, gravidade, colisões e limites existentes.
- Manter a implementação dentro da estrutura existente (cena única, sem novas dependências).

### Non-Goals

- IA ou movimentação do inimigo (patrulha, perseguição, etc.).
- Sistema de vida ou dano do Coxinha.
- Animações (do inimigo ou do Coxinha).
- Sons e efeitos sonoros.
- HUD, pontuação ou placar.
- Coletáveis.
- Novas fases ou novas cenas.
- Novos assets de imagem de inimigo.
- Alterar `package.json`, `tsconfig.json` ou `vite.config.ts`.

## Decisions

### Representação do inimigo

- **Escolhido:** retângulo temporário criado com `this.add.rectangle()` acompanhado de corpo físico próprio, na mesma abordagem geométrica usada pela capacidade `jogo-inicial` para o personagem.
- **Alternativa considerada:** criar um novo asset PNG de inimigo. Rejeitada porque não existe asset de inimigo no projeto e introduzir arte nova está fora do escopo desta change; uma change futura poderá substituir a forma geométrica por um sprite sem alterar a lógica.

Tamanho provisório: 40x40, posicionado sobre a plataforma (topo da plataforma em `y: 555`, portanto centro em `y: 535`), afastado do ponto de aparição do Coxinha (`x: 400`) para viabilizar o teste do salto — posição exata é ajuste de implementação, validada visualmente.

### Corpo físico do inimigo

- **Escolhido:** corpo estático (`physics.add.existing(enemy, true)`), como já feito para a plataforma.
- **Por quê:** garante que o inimigo permaneça parado sem depender de gravidade, velocidade zero ou `setImmovable`, e não exige colisão com a plataforma.
- **Alternativa considerada:** corpo dinâmico com gravidade, `setImmovable(true)` e velocidade zerada. Rejeitada por ser mais complexa sem benefício enquanto o inimigo não se move; uma change futura com IA/movimentação poderá migrar para corpo dinâmico.

### Colisão sólida e detecção da direção do contato

- **Escolhido:** `physics.add.collider(playerBody, enemyBody, callback)` — o inimigo é um obstáculo sólido em todas as direções; na callback, a condição de pisada é avaliada por direção do contato:
  - `playerBody.touching.down && enemyBody.touching.up` (contato pelo topo) **E**
  - a posição do personagem no frame anterior (`body.prev`) indica que sua base estava acima (ou no nível) do topo do inimigo, com pequena tolerância — ou seja, a aproximação veio de cima, durante a queda.
- **Por quê:** os flags `touching` sozinhos podem produzir falso positivo em contato de canto; combinar direção + posição anterior garante que apenas quedas sobre a parte superior contem como pisada. Colisões laterais (`touching.right`/`touching.left`) e por baixo (`playerBody.touching.up`) não satisfazem a condição e portanto não derrotam o inimigo.
- **Alternativa considerada:** usar `overlap()` apenas para a pisada. Rejeitada porque permitiria que o Coxinha atravessasse o inimigo lateralmente; a colisão sólida mantém o inimigo como obstáculo físico.

### Derrota do inimigo

- **Escolhido:** na pisada, marcar o inimigo como derrotado (flag para evitar reprocessamento naquele frame) e removê-lo da cena com `destroy()`. Depois disso ele não é mais exibido e não possui mais corpo físico, portanto não colide mais.
- **Observação:** sem HUD ou pontuação nesta change; "derrota" é observável apenas como desaparecimento do inimigo e ausência de colisão.

### Impulso após a pisada

- **Escolhido:** `setVelocityY(-300)` no corpo do Coxinha no momento da pisada — impulso vertical para cima, menor em módulo que a força de salto existente (`-400`), caracterizando um "pequeno impulso".
- **Por quê:** como o corpo estará no ar após o impulso, a regra existente `body.onFloor()` impede um segundo salto até retornar à plataforma, preservando a mecânica de pulo.
- **Alternativa considerada:** usar um bounce proporcional à velocidade de queda. Rejeitada por adicionar complexidade sem necessidade nesta primeira mecânica.

### Preservação das mecânicas existentes

Nenhuma das seguintes definições será alterada: velocidades (`200` normal, `350` corrida), força de salto (`-400`), gravidade (`y: 300`), hitbox 30x30 do jogador, controles, colisão com a plataforma e `setCollideWorldBounds(true)`.

A nova colisão e o novo callback serão adicionados sem modificar a lógica de movimentação já existente em `update()`.

### Estrutura do código

- **Escolhido:** manter tudo em `src/scenes/GameScene.ts`, seguindo a convenção atual do projeto (cena única, lógica organizada em blocos comentados).
- **Alternativa considerada:** extrair uma classe `Enemy`. Rejeitada nesta change por não haver comportamento próprio do inimigo além da colisão; a refactorização pode ocorrer quando houver IA ou animações.

## Risks / Trade-offs

- [Falso positivo de pisada em contato de canto] → Mitigação: combinar flags `touching` com a posição anterior do corpo (`body.prev`) e tolerância mínima; validar manualmente contatos laterais rasantes.
- [Inimigo "atravessável" em alta velocidade (tunneling)] → Aceitável: velocidades atuais (350 máx.) contra corpo de 40x40 não causam tunneling perceptível; se necessário, aumentar tolerância da detecção.
- [Corpo estático não reagirá a futuras forças] → Aceitável e intencional: quando IA/movimentação forem adicionadas, o corpo poderá ser migrado para dinâmico sem mudar os requisitos desta capacidade.
- [Posicionamento visual do inimigo sobre a plataforma] → Mitigação: calcular a posição pelo topo da plataforma (`555`) e validar visualmente no navegador que o retângulo não fica cortado nem flutuando.
- [Impulso pós-pisada pode parecer salto duplo] → Mitigação: impulso é disparado apenas pela pisada, é menor que o salto normal e a regra de segundo salto permanece ativa por `onFloor()`.