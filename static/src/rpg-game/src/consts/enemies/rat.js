import { EntityDrops } from "../../models/EntityDrops";

export const Rat = [
  // Down
  {
    atlas: "rat",
    key: "rat-idle-down",
    frameRate: 1,
    prefix: "rat/idle-down/",
    start: 0,
    end: 3,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "rat",
    key: "rat-atk-down",
    frameRate: 2,
    prefix: "rat/atk-down/",
    start: 0,
    end: 3,
    zeroPad: 2,
    repeat: 0,
  },
  {
    atlas: "rat",
    key: "rat-walk-down",
    frameRate: 4,
    prefix: "rat/walk-down/",
    start: 0,
    end: 3,
    zeroPad: 2,
    repeat: -1,
  },

  // Right
  {
    atlas: "rat",
    key: "rat-idle-right",
    frameRate: 1,
    prefix: "rat/idle-right/",
    start: 0,
    end: 1,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "rat",
    key: "rat-walk-right",
    frameRate: 4,
    prefix: "rat/walk-right/",
    start: 0,
    end: 2,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "rat",
    key: "rat-atk-right",
    frameRate: 2,
    prefix: "rat/atk-right/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: 0,
  },
  // UP
  {
    atlas: "rat",
    key: "rat-idle-up",
    frameRate: 1,
    prefix: "rat/idle-up/",
    start: 0,
    end: 3,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "rat",
    key: "rat-walk-up",
    frameRate: 4,
    prefix: "rat/walk-up/",
    start: 0,
    end: 3,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "rat",
    key: "rat-atk-up",
    frameRate: 2,
    prefix: "rat/atk-up/",
    start: 0,
    end: 3,
    zeroPad: 2,
    repeat: 0,
  },
];

export const RatConfig = {
  id: 1,
  name: "Rat",
  texture: "rat",
  baseHealth: 10,
  atack: 5,
  defense: 1,
  speed: 25,
  flee: 2,
  hit: 5,
  exp: 25,
  healthBarOffsetX: -5,
  healthBarOffsetY: 16,
  drops: [
    new EntityDrops(
      1, // Red Potion
      100, // 100% chance of dropping the item
    ),
  ],
};
