import { NineSlice } from "phaser3-nineslice";
import { infoBoxConfig } from "../consts/InfoBoxConfig.js";
export class InfoBox {
  constructor(
    scene,
    x,
    y,
    width,
    height,
    config = { name: "", description: "", translate, image: "" },
  ) {
    /**
     * The phaser scene that this infobox belongs.
     * @type { Phaser.Scene}
     */
    this.scene = scene;

    this.infoBoxConfig = infoBoxConfig["InfoBox"];
    /**
     * @type { NineSlice }
     */
    this.backgroundSprite = null;

    /**
     * The name displayed on the info box.
     * @type { Phaser.GameObjects.Text }
     */
    this.name = null;
    /**
     * The description displayed on the info box.
     * @type { Phaser.GameObjects.Text }
     */
    this.description = null;
    /**
     * The image displayed on the info box.
     * @type { Phaser.GameObjects.Image }
     */
    this.translate = null;

    this.image = null;

    this.x = x;
    this.y = y;
    this.panelMaxWidth = width;
    this.panelMaxHeight = height;
    this.backgroundTexture = this.infoBoxConfig.backgroundTexture;
    this.config = config;
    /**
     * Default font size of the Title Text.
     * @type { number }
     * @default
     */
    this.titleTextFontSize = this.infoBoxConfig.titleTextFontSize;
    /**
     * The default font family of the Inventory Text.
     * @type { string }
     * @default
     */
    this.titleFontFamily = this.infoBoxConfig.titleFontFamily;

    /**
     * The Offset of the Nine Slice background. It's used to protect the background from streching.
     * It will make it responsive in any scale size without losing resolution.
     * @type { number }
     * @default
     */
    this.nineSliceOffset = this.infoBoxConfig.nineSliceOffset;

    this.createBackground();
    this.createInformation();
  }

  createBackground() {
    this.backgroundSprite = this.scene.add
      .nineslice(
        this.x,
        this.y,
        this.backgroundTexture, // a key to an already loaded image
        this.panelMaxWidth,
        this.panelMaxHeight, // the width and height of your object
        this.nineSliceOffset, // the width and height to offset for a corner slice
        this.nineSliceOffset, // (optional) pixels to offset when computing the safe usage area
      )
      .setScrollFactor(0, 0)
      .setOrigin(0, 0)
      .setDepth(9999999);
    this.backgroundSprite.alpha = 0.7;
  }

  createInformation() {
    const baseX = this.backgroundSprite.x + 15;
    const baseY = this.backgroundSprite.y + 15;
    const wrap = this.backgroundSprite.width - 15;
    this.name = this.scene.add.text(baseX, baseY, this.config.name, {
      fontSize: this.titleTextFontSize,
      fontFamily: `${this.titleFontFamily}`,
      wordWrap: { width: wrap },
    });
    this.name.setOrigin(0, 0.5);
    this.name.setScrollFactor(0, 0).setDepth(9999999);
    if (this.config.translate) {
      this.translate = this.scene.add
        .text(
          baseX + this.backgroundSprite.width - 30,
          this.name.y + this.name.height + 10,
          this.config.translate,
          {
            fontSize: 18,
            //fontFamily: `${this.titleFontFamily}`,
            wordWrap: { width: wrap },
            rtl: true,
          },
        )
        .setDepth(9999999);
    }

    this.description = this.scene.add.text(
      baseX,
      this.translate.y + this.translate.height + 10,
      this.config.description,
      {
        fontSize: this.titleTextFontSize - 2,
        fontFamily: `${this.titleFontFamily}`,
        wordWrap: { width: wrap },
      },
    );
    this.description.setScrollFactor(0, 0).setDepth(9999999);
    if (this.config.image) {
      this.image = this.scene.add
        .image(
          baseX + this.backgroundSprite.width / 2,
          this.description.y + this.description.height + 30,
          this.config.image,
        )
        .setDepth(9999999);
      this.image.setScale(this.backgroundSprite.width / 2 / this.image.width);
    }
  }
}
