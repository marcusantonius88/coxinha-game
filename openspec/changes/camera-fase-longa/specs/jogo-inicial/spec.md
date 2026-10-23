# Spec Delta

## RENAMED Requirements

- FROM: `### Requirement: Limite horizontal da tela`
- TO: `### Requirement: Limite horizontal do mundo`

## MODIFIED Requirements

### Requirement: Limite horizontal do mundo

O sistema SHALL impedir que o personagem ultrapasse os limites horizontais do mundo, que é mais largo que a área de jogo visível.

O limite horizontal aplicável ao personagem SHALL ser o limite do mundo, e não o da borda da tela.

#### Scenario: Personagem atinge o limite esquerdo

- **WHEN** o personagem tenta ultrapassar o limite esquerdo do mundo
- **THEN** o personagem permanece dentro da área do mundo

#### Scenario: Personagem atinge o limite direito

- **WHEN** o personagem tenta ultrapassar o limite direito do mundo
- **THEN** o personagem permanece dentro da área do mundo

### Requirement: Cena inicial jogável

A cena inicial SHALL possuir um personagem e uma plataforma que funcione como chão.

O personagem SHALL utilizar `assets/coxinha/coxinha-idle.png` como representação visual estática, substituindo a representação geométrica temporária anterior.

`assets/coxinha/coxinha-sprite-sheet.png` permanece no projeto como asset para uso futuro e não participa da implementação desta change.

#### Scenario: Cena inicial carregada

- **WHEN** a cena inicial é carregada
- **THEN** o personagem Coxinha é exibido acima da plataforma
- **AND** a pose exibida é `IDLE`
- **AND** a plataforma funciona como superfície de suporte
- **AND** o personagem é afetado pela gravidade
- **AND** o personagem permanece sobre a plataforma quando estiver em contato com ela
- **AND** os controles existentes continuam funcionando
- **AND** os limites horizontais do mundo continuam sendo respeitados
