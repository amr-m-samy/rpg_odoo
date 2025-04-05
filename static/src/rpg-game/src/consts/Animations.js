import { Player } from "./player/Player";
import { PlayerConfig } from "./player/PlayerConfig"
import { Misc } from "./misc/Misc";import { Bat } from "./enemies/bat";
import { Rat } from "./enemies/rat";
import { Ogre } from "./enemies/ogre";
import { Skeleton_one } from "./enemies/skeleton_one";
import { Goblin_monika } from "./enemies/goblin_monika";
export const Animations = [
  ...Player[PlayerConfig.texture],
  ...Misc,
  ...Bat,
  ...Rat,
  ...Ogre,
  ...Skeleton_one,
  ...Goblin_monika,
];
