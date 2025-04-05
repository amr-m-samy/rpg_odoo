import { EntityDrops } from '../../models/EntityDrops';

export const MinotaurConfig = {
  id: 1,
  name: "Minotaur",
  texture: "minotaur",
  baseHealth: 10,
  atack: 3,
  defense: 3,
  speed: 20,
  flee: 3,
  hit: 10,
  exp: 600,
  healthBarOffsetX: 16,
  healthBarOffsetY: -10,
  scale: 0.7,
  drops: [
    new EntityDrops(
      1,
      100,
    ),
  ],
};

