import Phaser from 'phaser';
import idleSheetUrl from '../../assets/coxinha/animations/coxinha_idle_spritesheet.png';
import walkSheetUrl from '../../assets/coxinha/animations/coxinha_walk_spritesheet.png';
import runSheetUrl from '../../assets/coxinha/animations/coxinha_run_spritesheet.png';
import jumpSheetUrl from '../../assets/coxinha/animations/coxinha_jump_spritesheet.png';
import fallSheetUrl from '../../assets/coxinha/animations/coxinha_fall_spritesheet.png';
import landSheetUrl from '../../assets/coxinha/animations/coxinha_land_spritesheet.png';
import slimeIdleSheetUrl from '../../assets/enemies/slime/slime_idle_spritesheet.png';
import slimeDefeatSheetUrl from '../../assets/enemies/slime/slime_defeat_spritesheet.png';

/** Estados de animação do Coxinha (chaves de animação registradas no Phaser). */
type CoxinhaAnim = 'idle' | 'walk' | 'run' | 'jump' | 'fall' | 'land';

/** Definição de uma spritesheet aprovada e da animação correspondente. */
interface CoxinhaSheetDef {
  anim: CoxinhaAnim;
  frames: number;    // quantidade de quadros da spritesheet (0-based no loader)
  frameRate: number; // FPS da animação
  repeat: number;    // -1 = loop; 0 = reprodução única (LAND)
  url: string;
}

// Spritesheets aprovadas em assets/coxinha/animations/ (PNG RGBA, células 48×32 px).
const FRAME_WIDTH = 48;
const FRAME_HEIGHT = 32;

// Linha de base dos pés: o pixel opaco mais baixo de todos os quadros é a linha
// y=30 (y=31 fica transparente). A origem 31/32 alinha a base dos pés com
// body.bottom — mesmo efeito do ajuste 908/1024 do asset anterior, que
// compensava o padding transparente inferior do PNG.
const VISUAL_ORIGIN_Y = 31 / 32;

// Escala inteira ×2: caixa exibida 96×64 px, idêntica à do Coxinha anterior.
const VISUAL_SCALE = 2;

// Dimensões do mundo (3 × a viewport de 800 px, múltiplo exato).
const WORLD_WIDTH = 2400;
const WORLD_HEIGHT = 600;

const SHEET_DEFS: readonly CoxinhaSheetDef[] = [
  { anim: 'idle', frames: 4, frameRate: 6, repeat: -1, url: idleSheetUrl },
  { anim: 'walk', frames: 8, frameRate: 10, repeat: -1, url: walkSheetUrl },
  { anim: 'run', frames: 8, frameRate: 14, repeat: -1, url: runSheetUrl },
  { anim: 'jump', frames: 6, frameRate: 8, repeat: -1, url: jumpSheetUrl },
  { anim: 'fall', frames: 4, frameRate: 8, repeat: -1, url: fallSheetUrl },
  { anim: 'land', frames: 4, frameRate: 12, repeat: 0, url: landSheetUrl },
];

/** Chave de textura de uma spritesheet (separada da chave da animação). */
function sheetKey(anim: CoxinhaAnim): string {
  return `${anim}-sheet`;
}

/** Estados de animação do inimigo slime (chaves de animação no Phaser). */
type SlimeAnim = 'slime-idle' | 'slime-defeat';

/** Definição de uma spritesheet aprovada do inimigo slime. */
interface SlimeSheetDef {
  anim: SlimeAnim;
  frames: number;    // quantidade de quadros da spritesheet
  frameRate: number; // FPS da animação
  repeat: number;    // -1 = loop; 0 = reprodução única (DEFEAT)
  url: string;
}

// Spritesheets aprovadas em assets/enemies/slime/ (PNG RGBA, quadros 64×48 px).
const SLIME_FRAME_WIDTH = 64;
const SLIME_FRAME_HEIGHT = 48;

// Linha de base dos pés do slime: nos quadros de IDLE o pixel opaco mais baixo é a
// linha y=39 (y=40..47 transparentes). A origem 40/48 alinha a base com body.bottom.
const SLIME_VISUAL_ORIGIN_Y = 40 / 48;

const SLIME_SHEET_DEFS: readonly SlimeSheetDef[] = [
  { anim: 'slime-idle', frames: 4, frameRate: 6, repeat: -1, url: slimeIdleSheetUrl },
  { anim: 'slime-defeat', frames: 4, frameRate: 12, repeat: 0, url: slimeDefeatSheetUrl },
];

/** Chave de textura de uma spritesheet do slime. */
function slimeSheetKey(anim: SlimeAnim): string {
  return `${anim}-sheet`;
}

/** Estrutura estática do cenário: retângulo sólido (centro x,y e tamanho). */
interface SceneStructure {
  x: number;
  y: number;
  width: number;
  height: number;
}

// Layout aprovado da change camera-fase-longa (design.md, Decisão 5):
// 3 atos de 800 px, 12 estruturas cobrindo x ∈ [140, 2330].
// coordenadas inteiras e cor idêntica ao chão — renderização pixel-perfect.
// Corredor spawn (x 0..120) → slime (x=600) livre de estruturas.
const SCENE_STRUCTURE_COLOR = 0x8b4513;

const SCENE_STRUCTURES: readonly SceneStructure[] = [
  // Ato 1 (x 0..800)
  { x: 235, y: 465, width: 190, height: 20 },  // P1: x=140..330, topo y=455 (+100 px)
  { x: 380, y: 530, width: 40, height: 50 },   // Obstáculo A: x=360..400, topo y=505 (+50 px)
  { x: 430, y: 525, width: 40, height: 60 },   // Obstáculo B: x=410..450, topo y=495 (+60 px)
  { x: 610, y: 435, width: 180, height: 20 },  // P2: x=520..700, topo y=425 (+130 px)
  // Ato 2 (x 800..1600)
  { x: 1010, y: 455, width: 220, height: 20 }, // P3: x=900..1120, topo y=445 (+110 px)
  { x: 1220, y: 530, width: 40, height: 50 },  // Obstáculo C: x=1200..1240, topo y=505 (+50 px)
  { x: 1270, y: 525, width: 40, height: 60 },  // Obstáculo D: x=1250..1290, topo y=495 (+60 px)
  { x: 1470, y: 445, width: 180, height: 20 }, // P4: x=1380..1560, topo y=435 (+120 px)
  // Ato 3 (x 1600..2400)
  { x: 1800, y: 465, width: 200, height: 20 }, // P5: x=1700..1900, topo y=455 (+100 px)
  { x: 2020, y: 530, width: 40, height: 50 },  // Obstáculo E: x=2000..2040, topo y=505 (+50 px)
  { x: 2070, y: 525, width: 40, height: 60 },  // Obstáculo F: x=2050..2090, topo y=495 (+60 px)
  { x: 2240, y: 435, width: 180, height: 20 }, // P6: x=2150..2330, topo y=425 (+130 px)
];

export class GameScene extends Phaser.Scene {
  private playerBody!: Phaser.GameObjects.Rectangle;  // corpo físico (invisível)
  private playerVisual!: Phaser.GameObjects.Sprite;   // representação visual (sprite animado)
  private enemy!: Phaser.GameObjects.Rectangle;       // primeiro inimigo (corpo físico invisível)
  private enemyVisual!: Phaser.GameObjects.Sprite;    // representação visual do inimigo (slime)
  private platforms!: Phaser.Physics.Arcade.StaticGroup; // plataformas e obstáculos do cenário
  private enemyCollider!: Phaser.Physics.Arcade.Collider;
  private enemyDefeated = false;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private shiftKey!: Phaser.Input.Keyboard.Key;

  /** Animação atualmente exibida — guarda anti-restart da mesma animação. */
  private currentAnim: CoxinhaAnim | null = null;
  /** true enquanto o corpo está no ar (detecção da transição ar → chão). */
  private wasAirborne = false;
  /** true enquanto a aterrissagem (LAND) estiver pendente de exibição. */
  private landPending = false;

  constructor() {
    super({ key: 'GameScene' });
  }

  preload(): void {
    // Carrega as spritesheets aprovadas do Coxinha (células 48×32 px, RGBA).
    // URLs resolvidas/emitidas pelo Vite para garantir os assets no build de produção.
    for (const def of SHEET_DEFS) {
      this.load.spritesheet(sheetKey(def.anim), def.url, {
        frameWidth: FRAME_WIDTH,
        frameHeight: FRAME_HEIGHT,
      });
    }
    // Carrega as spritesheets aprovadas do inimigo slime (quadros 64×48, RGBA).
    for (const def of SLIME_SHEET_DEFS) {
      this.load.spritesheet(slimeSheetKey(def.anim), def.url, {
        frameWidth: SLIME_FRAME_WIDTH,
        frameHeight: SLIME_FRAME_HEIGHT,
      });
    }
  }

  create(): void {
    // --- Animações (6 estados do protagonista + 2 do inimigo slime) ---
    this.createAnimations();
    this.createEnemyAnimations();

    // --- Limites do mundo (Arcade physics): o jogador fica restrito ao mundo,
    // não mais à viewport (task 1.2).
    this.physics.world.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT);

    // --- Corpo físico invisível (hitbox 30x30 preservada do jogo-inicial) ---
    this.playerBody = this.add.rectangle(400, 500, 30, 30);
    this.playerBody.setVisible(false);
    this.physics.add.existing(this.playerBody);
    const body = this.playerBody.body as unknown as Phaser.Physics.Arcade.Body;
    body.setCollideWorldBounds(true);
    body.setVelocity(0);

    // --- Câmera horizontal: segue o Coxinha no eixo X, limitada ao mundo ---
    // lerpX=0.1 = rolagem suave; lerpY=0 = câmera verticalmente fixa;
    // roundPixels=true = sem tremor sub-pixel na arte pixelada (task 3.1).
    this.cameras.main.setBounds(0, 0, WORLD_WIDTH, WORLD_HEIGHT);
    this.cameras.main.startFollow(this.playerBody, true, 0.1, 0);

    // --- Representação visual separada (sprite animado Coxinha, segue o corpo) ---
    // Sprite 48×32 com a origem alinhando a base dos pés (linha y=30 do frame)
    // na base do corpo físico — mesmo papel do ajuste 908/1024 do asset anterior.
    this.playerVisual = this.add.sprite(400, 515, sheetKey('idle'), 0);
    this.playerVisual.setOrigin(0.5, VISUAL_ORIGIN_Y);
    // Escala inteira ×2 (48x32 -> caixa exibida 96x64), sem deformar a arte.
    this.playerVisual.setScale(VISUAL_SCALE);
    // A cena inicia exibindo IDLE; a partir daí a seleção de estado assume.
    this.playerVisual.play('idle');
    this.currentAnim = 'idle';
    // LAND é reproduzido uma vez; ao concluir, o estado em terra é reavaliado.
    this.playerVisual.on('animationcomplete', this.handleAnimationComplete, this);

    // --- Ground / platform (brown rectangle, static) ---
    const ground = this.add.rectangle(WORLD_WIDTH / 2, 560, WORLD_WIDTH, 10, 0x8b4513);
    this.physics.add.existing(ground, true);

    // Collision between player body and ground
    this.physics.add.collider(this.playerBody, ground);

    // --- Cenário: plataformas elevadas e obstáculos sólidos (cenario-plataformas) ---
    // Retângulos estáticos, sólidos em todas as direções, cor idêntica ao chão.
    // Nenhum parâmetro de física, controle ou animação é afetado por eles.
    this.platforms = this.physics.add.staticGroup();
    for (const structureDef of SCENE_STRUCTURES) {
      const structure = this.add.rectangle(
        structureDef.x,
        structureDef.y,
        structureDef.width,
        structureDef.height,
        SCENE_STRUCTURE_COLOR
      );
      this.physics.add.existing(structure, true); // corpo estático: sólido imóvel
      this.platforms.add(structure);
    }
    this.physics.add.collider(this.playerBody, this.platforms);

    // --- Inimigo base (primeiro inimigo da cena, permanece parado) ---
    // Corpo físico estático 40x40 (topo y=515, base y=555 = linha do chão),
    // invisível: a colisão usa exclusivamente este corpo.
    // Topo da plataforma = 560 - 10/2 = 555 => centro y = 555 - 40/2 = 535.
    // Posicionado à direita do ponto de aparição do Coxinha (x: 400).
    this.enemy = this.add.rectangle(600, 535, 40, 40, 0x2e8b57);
    this.enemy.setVisible(false);
    this.physics.add.existing(this.enemy, true); // corpo estático: inimigo parado

    // --- Visual do inimigo: sprite do slime, independente do corpo físico ---
    // Ancorado pelos pés na base do corpo (origem medida nos PNGs, baseline y=39).
    const enemyBody = this.enemy.body as Phaser.Physics.Arcade.StaticBody;
    this.enemyVisual = this.add.sprite(
      enemyBody.x + enemyBody.width / 2,
      enemyBody.bottom,
      slimeSheetKey('slime-idle'),
      0
    );
    this.enemyVisual.setOrigin(0.5, SLIME_VISUAL_ORIGIN_Y);
    this.enemyVisual.play('slime-idle'); // IDLE em loop enquanto o inimigo estiver ativo
    // DEFEAT roda uma única vez; ao concluir, visual e corpo são removidos juntos.
    this.enemyVisual.on('animationcomplete', this.handleEnemyDefeatComplete, this);

    // Colisão sólida em todas as direções; a callback decide se é uma pisada.
    this.enemyCollider = this.physics.add.collider(
      this.playerBody,
      this.enemy,
      () => this.handleEnemyContact()
    );

    // --- Input ---
    this.cursors = this.input!.keyboard!.createCursorKeys();
    this.shiftKey = this.input!.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.SHIFT);
  }

  update(): void {
    const body = this.playerBody.body as unknown as Phaser.Physics.Arcade.Body;

    // Sincronizar o Rectangle com o corpo físico (fonte de verdade).
    // O Rectangle não é atualizado pelo Arcade Body automaticamente; sem isso
    // a câmera leria playerBody.x desatualizado (task 3.3).
    this.playerBody.setPosition(body.center.x, body.center.y);

    // Sincronizar visual com corpo físico (separação arquitetural)
    // Ancorar as patas no bottom-center do corpo físico.
    if (this.playerVisual && body) {
      this.playerVisual.setPosition(body.center.x, body.bottom);
    }

    const normalSpeed = 200;
    const runSpeed = 350;
    const jumpForce = -920; // Alvo refinado: com gravity.y=1840 (main.ts) → 1,0 s no ar / 230 px teórico (~225 px medido)

    // --- Horizontal movement ---
    if (this.cursors.left.isDown) {
      body.setVelocityX(this.shiftKey.isDown ? -runSpeed : -normalSpeed);
    } else if (this.cursors.right.isDown) {
      body.setVelocityX(this.shiftKey.isDown ? runSpeed : normalSpeed);
    } else {
      // Stop when no movement key is pressed
      body.setVelocityX(0);
    }

    // --- Jump (only when on the ground) ---
    if (
      body.onFloor() &&
      (Phaser.Input.Keyboard.JustDown(this.cursors.up) ||
        Phaser.Input.Keyboard.JustDown(this.cursors.space))
    ) {
      body.setVelocityY(jumpForce);
    }

    // --- Seleção de animação pelo estado físico real (guard anti-restart) ---
    this.updateAnimation(body);
  }

  /**
   * Registra as 6 animações do Coxinha a partir das spritesheets aprovadas.
   * `land` é reproduzido uma vez (repeat 0); os demais estados em loop.
   */
  private createAnimations(): void {
    for (const def of SHEET_DEFS) {
      if (this.anims.exists(def.anim)) {
        continue;
      }
      this.anims.create({
        key: def.anim,
        frames: this.anims.generateFrameNumbers(sheetKey(def.anim), {
          start: 0,
          end: def.frames - 1,
        }),
        frameRate: def.frameRate,
        repeat: def.repeat,
      });
    }
  }

  /**
   * Registra as animações do inimigo slime a partir das spritesheets aprovadas.
   * `slime-idle` em loop enquanto ativo; `slime-defeat` reproduzida uma única vez.
   */
  private createEnemyAnimations(): void {
    for (const def of SLIME_SHEET_DEFS) {
      if (this.anims.exists(def.anim)) {
        continue;
      }
      this.anims.create({
        key: def.anim,
        frames: this.anims.generateFrameNumbers(slimeSheetKey(def.anim), {
          start: 0,
          end: def.frames - 1,
        }),
        frameRate: def.frameRate,
        repeat: def.repeat,
      });
    }
  }

  /**
   * Deriva o estado de animação da física real do corpo e troca de animação
   * somente quando o estado muda — a animação corrente nunca é reiniciada.
   * Escreve apenas no visual; física e controles não são afetados.
   */
  private updateAnimation(body: Phaser.Physics.Arcade.Body): void {
    const onGround = body.onFloor();

    if (onGround) {
      // Transição ar → chão: aterrissagem pendente de exibir (LAND uma vez).
      if (this.wasAirborne) {
        this.landPending = true;
      }
      this.wasAirborne = false;
    } else {
      this.wasAirborne = true;
      this.landPending = false;
    }

    const next = this.resolveAnimState(body, onGround);
    if (next !== this.currentAnim) {
      this.playAnim(next);
    }

    // Espelha o sprite apenas durante o movimento horizontal, preservando a
    // face anterior quando o personagem para ou está no ar sem input.
    if (Math.abs(body.velocity.x) > 0) {
      this.playerVisual.setFlipX(body.velocity.x < 0);
    }
  }

  /**
   * Estado-alvo da animação conforme a física atual:
   * - no ar: subindo → `jump`, descendo → `fall`, ápice (v.y == 0) mantém o anterior;
   * - em terra: movendo → `run` (Shift) / `walk`; parado → `land` enquanto a
   *   aterrissagem estiver pendente, senão `idle`.
   */
  private resolveAnimState(
    body: Phaser.Physics.Arcade.Body,
    onGround: boolean
  ): CoxinhaAnim {
    if (!onGround) {
      const vy = body.velocity.y;
      if (vy < 0) {
        return 'jump';
      }
      if (vy > 0) {
        return 'fall';
      }
      // Ápice do salto: mantém o estado anterior para não flutuar nas bordas.
      return this.currentAnim ?? 'idle';
    }

    if (Math.abs(body.velocity.x) > 0) {
      // WALK/RUN têm prioridade sobre LAND: iniciar a movimentação no instante
      // do pouso substitui a aterrissagem imediatamente (responsividade).
      this.landPending = false;
      return this.shiftKey.isDown ? 'run' : 'walk';
    }

    if (this.landPending) {
      return 'land';
    }
    return 'idle';
  }

  /** Aplica a animação (chamada apenas em mudança de estado). */
  private playAnim(anim: CoxinhaAnim): void {
    this.playerVisual.play(anim);
    this.currentAnim = anim;
  }

  /** Ao concluir o LAND, libera a aterrissagem e reavalia o estado em terra. */
  private handleAnimationComplete(animation: Phaser.Animations.Animation): void {
    if (animation.key === 'land') {
      this.landPending = false;
    }
  }

  /**
   * Chamada durante a colisão Coxinha x inimigo (física).
   * Derrota o inimigo somente na pisada: contato pelo topo combinado com
   * aproximação de cima. Colisão lateral ou por baixo não derrota.
   */
  private handleEnemyContact(): void {
    // Flag anti-reprocessamento: após a derrota a colisão não pode reexecutar a lógica.
    if (this.enemyDefeated || !this.enemy.active) {
      return;
    }

    const playerBody = this.playerBody.body as unknown as Phaser.Physics.Arcade.Body;
    const enemyBody = this.enemy.body as Phaser.Physics.Arcade.StaticBody | undefined;
    if (!enemyBody) {
      return;
    }

    // Contato pelo topo: base do Coxinha voltada para baixo e topo do inimigo atingido.
    // (No mesmo passo da física o contato lateral define left/right, e o contato
    // por baixo define up/down invertido — não passam aqui.)
    const contatoPeloTopo = playerBody.touching.down && enemyBody.touching.up;

    // A aproximação veio de cima: no início deste frame a base do Coxinha ainda
    // estava acima do topo do inimigo (tolerância cobre a penetração do passo).
    // Impede falsos positivos de canto em abordagens laterais.
    const tolerancia = 8;
    const estavaAcima =
      playerBody.prev.y + playerBody.height <= enemyBody.top + tolerancia;

    if (!contatoPeloTopo || !estavaAcima) {
      // Colisão lateral ou por baixo: inimigo permanece na cena.
      return;
    }

    // Pisada confirmada: derrota o inimigo imediatamente — a flag impede
    // reprocessamento, o colisor desativa a participação em novas colisões e
    // o DEFEAT do slime é reproduzido uma única vez (a remoção do visual e do
    // corpo acontece na animationcomplete, ponto único de destruição).
    this.enemyDefeated = true;
    this.enemyCollider.active = false;
    this.enemyVisual.play('slime-defeat');

    // Impulso para cima menor que o salto normal (-920), razão 0,75
    // (-690/-920). O inimigo estático
    // zera a velocidade na separação, então aplicamos o impulso em seguida.
    playerBody.setVelocityY(-690);
  }

  /**
   * Ao concluir o `slime-defeat`, remove visual e corpo físico do inimigo.
   * Proteção contra execução duplicada: cada elemento só é destruído se ainda
   * estiver ativo (a flag `enemyDefeated` + colisor inativo já bloqueiam novas
   * derrotas; este método é o ponto único de remoção).
   */
  private handleEnemyDefeatComplete(animation: Phaser.Animations.Animation): void {
    if (animation.key !== 'slime-defeat') {
      return;
    }
    if (this.enemyVisual.active) {
      this.enemyVisual.destroy();
    }
    if (this.enemy.active) {
      this.enemy.destroy();
    }
  }
}
