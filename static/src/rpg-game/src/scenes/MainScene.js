import Phaser from "phaser";
import { LuminusWarp } from "../plugins/LuminusWarp";
import { LuminusObjectMarker } from "../plugins/LuminusObjectMarker";
import AnimatedTiles from "../plugins/AnimatedTiles";
import { EnvironmentParticles } from "../plugins/EnvironmentParticles";
import { LuminusOutlineEffect } from "../plugins/LuminusOutlineEffect";
import { LuminusEnemyZones } from "../plugins/LuminusEnemyZones";
import { LuminusMapCreator } from "../plugins/LuminusMapCreator";
import InfoScene from "../consts/SceneInfo";
import { Item } from "../entities/Item";

export class MainScene extends Phaser.Scene {
  constructor() {
    super({
      key: "MainScene",
    });
    this.player = null;
  }

  preload() {
    this.load.scenePlugin(
      "animatedTiles",
      AnimatedTiles,
      "animatedTiles",
      "animatedTiles",
    );
  }

  create() {
    // if (
    //     !this.scale.isFullscreen && !this.sys.game.device.os.desktop
    //         ? true
    //         : false
    // ) {
    //     this.scale.startFullscreen();
    // }

    const searchParams = new URLSearchParams(window.location.search);
    const activity = searchParams.get("activity");

    const sceneInfo = InfoScene(activity || "mainscene");
    this.cameras.main.setZoom(sceneInfo.zoom);

    this.mapCreator = new LuminusMapCreator(this);

    if (sceneInfo.tileImages) {
      this.mapCreator.mapName = sceneInfo.mapName;
      this.mapCreator.tilesetImages = sceneInfo.tileImages;
    }

    this.mapCreator.create();

    const camera = this.cameras.main;
    camera.startFollow(this.player.container);

    const luminusWarp = new LuminusWarp(this, this.player, this.mapCreator.map);
    luminusWarp.createWarps();
    const interactiveMarkers = new LuminusObjectMarker(
      this,
      this.mapCreator.map,
    );
    interactiveMarkers.create();

    this.scene.launch("DialogScene", {
      player: this.player,
      map: this.mapCreator.map,
      scene: this,
    });

    this.joystickScene = this.scene.get("JoystickScene");

    this.scene.launch("HUDScene", { player: this.player });

    this.sys.animatedTiles.init(this.mapCreator.map);
    if (sceneInfo.isParticles) {
      this.particles = new EnvironmentParticles(this, this.mapCreator.map);
      this.particles.create();
    }
    // this.outlineEffect = new LuminusOutlineEffect(this);

    if (sceneInfo.isSound) {
      this.sound.volume = sceneInfo.volume;
      this.themeSound = this.sound.add(sceneInfo.soundAssetKey, {
        loop: sceneInfo.isSoundLoop,
      });
      this.themeSound.play();
    }

    this.enemies = [];
    if (sceneInfo.isEnemyZone) {
      this.luminusEnemyZones = new LuminusEnemyZones(this, this.mapCreator.map);
      this.luminusEnemyZones.create();
    }

    // new Item(this, this.player.container.x, this.player.container.y - 40, 2);
    // new Item(this, this.player.container.x, this.player.container.y - 50, 2);
    // new Item(this, this.player.container.x, this.player.container.y - 60, 1);
  }

  /**
   * Stops all scene music.
   */
  stopSceneMusic() {
    this.themeSound.stop();
  }

  update(time, delta) {
    // this.outlineEffect.removeEffect(this.player.container);
    // this.physics.overlap(
    //     this.player,
    //     this.overplayer_layer,
    //     () => {
    //         this.outlineEffect.applyEffect(this.player.container);
    //     },
    //     (hitZone, tile) => tile.index > -1
    // );
  }
}
