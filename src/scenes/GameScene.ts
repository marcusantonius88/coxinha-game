import Phaser from 'phaser';
import coxinhaIdleUrl from '../../assets/coxinha/coxinha-idle.png';

export class GameScene extends Phaser.Scene {
  private playerBody!: Phaser.GameObjects.Rectangle;  // corpo físico (invisível)
  private playerVisual!: Phaser.GameObjects.Image;    // representação visual
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
    const jumpForce = -400;

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
}
