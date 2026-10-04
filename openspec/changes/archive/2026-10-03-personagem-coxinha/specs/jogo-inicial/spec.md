# Spec Delta

## MODIFIED Requirements

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
- **AND** os limites horizontais da área de jogo continuam sendo respeitados
