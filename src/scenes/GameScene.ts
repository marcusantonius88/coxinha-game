import Phaser from 'phaser';
import coxinhaIdleUrl from '../../assets/coxinha/coxinha-idle.png';

export class GameScene extends Phaser.Scene {
  private playerBody!: Phaser.GameObjects.Rectangle;  // corpo físico (invisível)
  private playerVisual!: Phaser.GameObjects.Image;    // representação visual
  private enemy!: Phaser.GameObjects.Rectangle;       // primeiro inimigo (hitbox própria)
  private enemyCollider!: Phaser.Physics.Arcade.Collider;
  private enemyDefeated = false;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private shiftKey!: Phaser.Input.Keyboard.Key;

  constructor() {
    super({ key: 'GameScene' });
  }

  preload(): void {
    // Carregar imagem única da pose IDLE do Coxinha.
    // URL resolvida/emitida pelo Vite para garantir o asset no build de produção.
    this.load.image('coxinha-idle', coxinhaIdleUrl);
  }

  create(): void {
    // --- Corpo físico invisível (hitbox 30x30 preservada do jogo-inicial) ---
    this.playerBody = this.add.rectangle(400, 500, 30, 30);
    this.playerBody.setVisible(false);
    this.physics.add.existing(this.playerBody);
    const body = this.playerBody.body as unknown as Phaser.Physics.Arcade.Body;
    body.setCollideWorldBounds(true);
    body.setVelocity(0);

    // --- Representação visual separada (imagem Coxinha, segue o corpo) ---
    // Origem no "pé" do Coxinha dentro do PNG (linha 908 de 1024), compensando
    // o padding transparente inferior do asset (~115px) sem alterar a hitbox.
    this.playerVisual = this.add.image(400, 515, 'coxinha-idle');
    this.playerVisual.setOrigin(0.5, 908 / 1024);
    // Escala uniforme (asset 1536x1024 -> 96x64), preservando a proporção 3:2.
    this.playerVisual.setScale(64 / 1024);

    // --- Ground / platform (brown rectangle, static) ---
    const ground = this.add.rectangle(400, 560, 800, 10, 0x8b4513);
    this.physics.add.existing(ground, true);

    // Collision between player body and ground
    this.physics.add.collider(this.playerBody, ground);

    // --- Inimigo base (primeiro inimigo da cena, permanece parado) ---
    // Retângulo temporário 40x40 (nenhum asset de inimigo existe no projeto).
    // Topo da plataforma = 560 - 10/2 = 555 => centro y = 555 - 40/2 = 535.
    // Posicionado à direita do ponto de aparição do Coxinha (x: 400).
    this.enemy = this.add.rectangle(600, 535, 40, 40, 0x2e8b57);
    this.physics.add.existing(this.enemy, true); // corpo estático: inimigo parado

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

    // Pisada confirmada: derrota o inimigo (deixa de ser exibido e de colidir).
    this.enemyDefeated = true;
    this.enemyCollider.active = false;
    this.enemy.destroy();

    // Impulso para cima menor que o salto normal (-920), razão 0,75
    // (-690/-920). O inimigo estático
    // zera a velocidade na separação, então aplicamos o impulso em seguida.
    playerBody.setVelocityY(-690);
  }
}
