import Phaser from 'phaser';
import { GameScene } from './scenes/GameScene';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  backgroundColor: '#87CEEB',
  parent: 'game',
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 1330 }, // Preset Equilibrado: pareado com jumpForce=-800 (GameScene.ts) → ~1,2 s no ar / ~240 px
    },
  },
  scene: [GameScene],
};

new Phaser.Game(config);
