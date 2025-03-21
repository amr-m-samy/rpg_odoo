import { LuminusUtils } from "../utils/LuminusUtils";

/**
 * @class
 */
export class PanelComponent {
  /**
   * Creates a Panel to display invormation on it.
   * @param { Phaser.Scene } scene
   */
  constructor(scene, panelConfig) {
    /**
     * The Phaser Scene that the Panel will be created on.
     * @type { Phaser.Scene }
     */
    this.scene = scene;
    this.panelConfig = panelConfig;
    /**
     * The Offset of the Nine Slice background. It's used to protect the background from streching.
     * It will make it responsive in any scale size without losing resolution.
     * @type { number }
     * @default
     */
    this.nineSliceOffset = this.panelConfig.nineSliceOffset;

    /**
     * The vertical padding between the Background edge and the content.
     * @type { number }
     * @default
     */
    this.verticalBackgroundPadding = this.panelConfig.verticalBackgroundPadding;

    /**
     * The Padding of the main content to the Top of the Inventory Background.
     * @type { number }
     * @default
     */
    this.backgroundMainContentPaddingTop =
      this.panelConfig.backgroundMainContentPaddingTop;

    /**
     * Default font size of the Title Text.
     * @type { number }
     * @default
     */
    this.titleTextFontSize = this.panelConfig.titleTextFontSize;

    /**
     * The name of the sprite texture of the Inventory Background.
     * @type { string }
     * @default
     */
    this.backgroundTexture = this.panelConfig.backgroundTexture;

    /**
     * The name of the sprite texture of the Inventory Title.
     * @type { string }
     */
    this.panelTitleTexture = this.panelConfig.panelTitleTexture;

    /**
     * The name of the sprite texture of the Close Button.
     * @type { string }
     * @default
     */
    this.panelCloseTexture = this.panelConfig.panelCloseTexture;

    /**
     * The name of the panel. AKA Text Title that will be shown on the title panel.
     * @type { string }
     */
    this.panelName = this.panelConfig.panelName;

    /**
     * The panel background sprite.
     * @type { NineSlice }
     */
    this.panelBackground = null;

    /**
     * The inventory title sprite.
     * @type { Phaser.GameObjects.Image }
     */
    this.panelTitle = null;

    /**
     * The inventory title sprite.
     * @type { Phaser.GameObjects.Image }
     */
    this.panelTitleText = null;

    /**
     * The default font family of the Inventory Text.
     * @type { string }
     * @default
     */
    this.titleFontFamily = this.panelConfig.titleFontFamily;

    /**
     * The max width of the panel.
     * @type { number }
     */
    this.panelMaxWidth = this.panelConfig.panelMaxWidth;

    /**
     * The max height of the panel.
     * @type { number }
     */
    this.panelMaxHeight = this.panelConfig.panelMaxHeight;

    /**
     * The margin between the Screen and the panel.
     * @type { number }
     */
    this.panelScreenMargin = this.panelConfig.panelScreenMargin;

    this.createBackground();
    this.createTitle();
    this.createCloseButton();
  }

  /**
   * Sets the new Title Text.
   * @param { string } title
   */
  setTitleText(title) {
    this.panelTitleText.setText(title);
  }

  /**
   * Creates the Panel Background Layer.
   */
  createBackground() {
    if (LuminusUtils.isMobile()) {
      this.panelMaxWidth =
        this.scene.cameras.main.width - this.panelScreenMargin * 4;
      this.panelMaxHeight =
        this.scene.cameras.main.height - this.panelScreenMargin * 4;
    }
    this.panelBackground = this.scene.add
      .nineslice(
        this.scene.scale.width / 2 - this.panelMaxWidth / 2,
        this.scene.scale.height / 2 - this.panelMaxHeight / 2,
        this.backgroundTexture, // a key to an already loaded image
        this.panelMaxWidth,
        this.panelMaxHeight, // the width and height of your object
        this.nineSliceOffset, // the width and height to offset for a corner slice
        this.nineSliceOffset, // (optional) pixels to offset when computing the safe usage area
      )
      .setScrollFactor(0, 0)
      .setOrigin(0, 0);
  }

  /**
   * Creates the panel Title.
   */
  createTitle() {
    this.panelTitle = this.scene.add
      .image(
        this.panelBackground.x +
          (this.panelBackground.width * this.panelBackground.scaleX) / 2,
        this.panelBackground.y + 54,
        this.panelTitleTexture,
      )
      .setScrollFactor(0, 0)
      .setOrigin(0.5, 0.5);
    this.panelTitleText = this.scene.add
      .text(this.panelTitle.x + 11, this.panelTitle.y + 7, this.panelName, {
        fontSize: this.titleTextFontSize,
        fontFamily: `${this.titleFontFamily}`,
      })
      .setScrollFactor(0, 0)
      .setOrigin(0.5, 0.5);
  }

  /**
   * Creates the close Button.
   */
  createCloseButton() {
    this.closeButton = this.scene.add
      .image(
        this.panelBackground.x +
          this.panelBackground.width * this.panelBackground.scaleX -
          this.verticalBackgroundPadding * 1.5,
        this.panelBackground.y + this.verticalBackgroundPadding * 1.5,
        this.panelCloseTexture,
      )
      .setInteractive()
      .setOrigin(0.5, 0.5)
      .setScale(0.8);
  }

  destroy() {
    this.panelBackground.destroy();
    this.panelTitle.destroy();
    this.panelTitleText.destroy();
    this.closeButton.destroy();
  }
}
