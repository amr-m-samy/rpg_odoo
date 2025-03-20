import { Bat } from "./enemies/bat";
import { Ogre } from "./enemies/ogre";
import { Rat } from "./enemies/rat";
import { Player } from "./player/Player";
import { PlayerConfig } from "./player/PlayerConfig";
//import { YellowHair } from "./player/YellowHair";

export const Animations = [
  ...Bat,
  ...Rat,
  ...Ogre,
  ...Player[PlayerConfig.texture],
  //...YellowHair,

  // Chat iteraction box.
  {
    atlas: "chat_bubble_animation",
    key: "chat_bubble_animation",
    frameRate: 3,
    prefix: "chatbox/",
    start: 1,
    end: 4,
    zeroPad: 2,
    repeat: -1,
  },

  // Slash atack animation
  {
    atlas: "slash",
    key: "slash",
    frameRate: 16,
    prefix: "slash/",
    start: 1,
    end: 4,
    zeroPad: 2,
    repeat: 0,
  },
];
