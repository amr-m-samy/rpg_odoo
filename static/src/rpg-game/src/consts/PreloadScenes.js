import { MainScene } from "../scenes/MainScene";
import { DialogScene } from "../scenes/DialogScene";
import { JoystickScene } from "../scenes/JoystickScene";
import { HUDScene } from "../scenes/HUDScene";
import { PreloadScene } from "../scenes/PreloadScene";
import { VideoPlayerScene } from "../scenes/VideoPlayerScene";
import { IntroScene } from "../scenes/IntroScene";
import { SettingScene } from "../scenes/SettingScene";
import { MobileCheckScene } from "../scenes/MobileCheckScene";
import { DungeonScene } from "../scenes/DungeonScene";
import { InventoryScene } from "../scenes/InventoryScene";
import { TutorialScene } from "../scenes/TutorialScene";
import { MainMenuScene } from "../scenes/MainMenuScene";
import { AttributeScene } from "../scenes/AttributeScene";
import { AnimationScene } from "../scenes/AnimationScene";
import { ForTestScene } from "../scenes/ForTestScene";
import { ImagePreviewScene } from "../scenes/ImagePreviewScene";
import { DictionaryScene } from "../scenes/DictionaryScene";

export default function PreloadScenes() {
  return [
    // Preload should come first
    PreloadScene,
    IntroScene,
    MainScene,
    DungeonScene,
    MobileCheckScene,
    TutorialScene,
    MainMenuScene,
    AnimationScene,
    ForTestScene,
    ImagePreviewScene,
    DictionaryScene,

    // UI Scenes should be loaded after the game Scenes.
    JoystickScene,
    DialogScene,
    HUDScene,
    InventoryScene,
    SettingScene,
    VideoPlayerScene,
    AttributeScene,
  ];
}
