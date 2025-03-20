import { EntityDrops } from "../../models/EntityDrops";

export const Bat = [
  // Down
  {
    atlas: "bat",
    key: "bat-idle-down",
    frameRate: 8,
    prefix: "bat/idle-down/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "bat",
    key: "bat-atk-down",
    frameRate: 5,
    prefix: "bat/atk-down/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: 0,
  },
  {
    atlas: "bat",
    key: "bat-walk-down",
    frameRate: 8,
    prefix: "bat/walk-down/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: -1,
  },
  // Right
  {
    atlas: "bat",
    key: "bat-idle-right",
    frameRate: 8,
    prefix: "bat/idle-right/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "bat",
    key: "bat-atk-right",
    frameRate: 5,
    prefix: "bat/atk-right/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: 0,
  },
  {
    atlas: "bat",
    key: "bat-walk-right",
    frameRate: 8,
    prefix: "bat/walk-right/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: -1,
  },
  // Up
  {
    atlas: "bat",
    key: "bat-idle-up",
    frameRate: 8,
    prefix: "bat/idle-up/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: -1,
  },
  {
    atlas: "bat",
    key: "bat-atk-up",
    frameRate: 5,
    prefix: "bat/atk-up/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: 0,
  },
  {
    atlas: "bat",
    key: "bat-walk-up",
    frameRate: 8,
    prefix: "bat/walk-up/",
    start: 0,
    end: 4,
    zeroPad: 2,
    repeat: -1,
  },
];

export const BatConfig = {
  id: 2,
  name: "Bat",
  texture: "bat",
  baseHealth: 10,
  atack: 7,
  defense: 1,
  speed: 30,
  flee: 3,
  hit: 5,
  exp: 50,
  hit: 5,
  healthBarOffsetX: -6,
  healthBarOffsetY: 16,
  drops: [
    new EntityDrops(
      1, // Red Potion
      50, // 50% chance of dropping the item
    ),
    new EntityDrops(
      2, // black Potion
      5, // 5% chance of dropping the item
    ),
    new EntityDrops(
      3, // Treasure Chest
      2, // 1% chance of dropping the item
    ),
  ],
};
