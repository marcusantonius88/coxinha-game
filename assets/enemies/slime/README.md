# Coxinha — slime enemy sprites (ready for Phaser)

Technical pixel-art sprites created as clean native assets, not extracted from the reference sheet.

- PNG RGBA with true transparent background.
- Frame size: 64×48 px (native pixel art drawn at 32×24 and enlarged with nearest-neighbor).
- Horizontal spritesheets: `slime_idle_spritesheet.png`, `slime_walk_spritesheet.png`, `slime_hit_spritesheet.png`, `slime_defeat_spritesheet.png`.
- Four frames per state; individual frame PNGs included.
- First integration recommendation: IDLE looping; DEFEAT once after stomp. WALK/HIT are optional.
- Keep physics body separate from the visual sprite; align visual bottom to body bottom.
- Existing game code and Coxinha assets were not modified.
