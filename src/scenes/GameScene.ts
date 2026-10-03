import Phaser from 'phaser';

export class GameScene extends Phaser.Scene {
  private player!: Phaser.GameObjects.Rectangle;
  private cursors!: Phaser.Types.Input.Keyboard.CursorKeys;
  private shiftKey!: Phaser.Input.Keyboard.Key;

  constructor() {
    super({ key: 'GameScene' });
  }

  preload(): void {
    // No external assets for the initial prototype
  }

  create(): void {
    // --- Character (temporary: red rectangle) ---
    this.player = this.add.rectangle(400, 500, 30, 30, 0xff0000);
    this.physics.add.existing(this.player);

    // Configure player physics (body guaranteed after add.existing)
    const body = this.player.body as unknown as Phaser.Physics.Arcade.Body;
    body.setCollideWorldBounds(true);
    body.setVelocity(0);

    // --- Ground / platform (brown rectangle, static) ---
    const ground = this.add.rectangle(400, 560, 800, 10, 0x8b4513);
    this.physics.add.existing(ground, true);

    // Collision between player and ground
    this.physics.add.collider(this.player, ground);

    // --- Input ---
    this.cursors = this.input!.keyboard!.createCursorKeys();
    this.shiftKey = this.input!.keyboard!.addKey(Phaser.Input.Keyboard.KeyCodes.SHIFT);
  }

  update(): void {
    const body = this.player.body as unknown as Phaser.Physics.Arcade.Body;

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
