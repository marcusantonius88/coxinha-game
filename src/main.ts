import Phaser from 'phaser';
import { GameScene } from './scenes/GameScene';

const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  backgroundColor: '#87CEEB',
  parent: 'game',
  // Renderização pixel-art: texturas com filtro NEAREST (sem borrão na ampliação
  // ×2 das spritesheets 48×32) e desenho em posições inteiras. Correção apenas
  // de renderização — física, controles e animações permanecem intactos.
  render: {
    pixelArt: true,
    roundPixels: true,
  },
  physics: {
    default: 'arcade',
    arcade: {
      gravity: { x: 0, y: 1840 }, // Alvo refinado: pareado com jumpForce=-920 (GameScene.ts) → 1,0 s no ar / 230 px teórico (~225 px medido)
    },
  },
  scene: [GameScene],
};

new Phaser.Game(config);
