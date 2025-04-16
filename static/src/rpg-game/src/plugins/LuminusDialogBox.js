import Phaser from "phaser";
import { NineSlice } from "phaser3-nineslice";
import { Player } from "../entities/Player";
import { LuminusTypingSoundManager } from "./LuminusTypingSoundManager";
import { LuminusVideoOpener } from "./LuminusVideoOpener";
import { dialogBoxConfig } from "../consts/DialogBoxConfig";
import { InteractiveDialog } from "./InteractiveDialog";
/**
 * @class
 */
export class LuminusDialogBox {
  /**
   * This class allows one to create Dialogs.
   * It's possible to set the Action Hotkey, Action button Sprite, Dialog Sprite image,
   * Interaction icon above player.
   * @param { Phaser.Scene } scene Scene Context.
   * @param { Phaser.Physics.Arcade.Sprite } player Player Game Object.
   */
  constructor(scene, player) {
    this.dialogBoxConfig = dialogBoxConfig;
    /**
     * Scene Context.
     * @type { Phaser.Scene }  */
    this.scene = scene;
    /**
     * Player Game Object.
     * @type { Player }  */
    this.player = player;

    /**
     * Name of the sprite image that will be the dialog.
     *  @type { string }
     * @default
     * */
    this.dialogSpriteName = this.dialogBoxConfig.dialogSpriteName;

    /**
     * Name of the Sprite of the button action.
     * @type { string }
     * @default
     * */
    this.actionButtonSpriteName = this.dialogBoxConfig.actionButtonSpriteName;

    /**
     * Interaction sprite name.
     * @type { string }
     * @default
     * */
    this.interactionSpriteName = this.dialogBoxConfig.interactionSpriteName;

    /**
     * The name of the animation that the iteraction icon will play.
     * @type { string }
     * @default
     */
    this.animationIteractionIconName =
      this.dialogBoxConfig.animationIteractionIconName;

    /**
     * Name of the Sprite of the Mobile button action.
     * @type { string }
     * @default
     * */
    this.mobileActionButtonSpriteName = "buttonA";

    /**
     * Current action button key code.
     * @type { Phaser.Input.Keyboard.KeyCodes }
     * @default
     *  */
    this.actionButtonKeyCode = this.dialogBoxConfig.actionButtonKeyCode;
    /**
     * Dialog height.
     * @type { number }
     * @default
     *   */
    this.dialogWidthFactor = 1.05;
    this.dialogMobileFactor = 1;
    this.dialogHeight = this.dialogBoxConfig.dialogHeight; // 150; // Dialog Height
    /**
     * Margin of the dialog. Used to make spaces in the dialog.
     * @type { number }
     * @default
     *   */
    this.margin = this.dialogBoxConfig.margin;
    /**
     * Width and Height of the corner Slice.
     * @example
     * this.nineSliceOffsets = 25;
     * // Or
     * this.nineSliceOffsets = [10, 15, 5, 5];
     *
     * // Array Length	Use	Explanation
     * // 1	[ topRightBottomLeft ]	The first (only) element is used as the value for all four sides
     * // 2	[ topBottom, leftRight ]	The first element is used for the top and bottom, the second element is used as the for the left and right
     * // 3	[ top, rightLeft, bottom ]	The first element is used for the top, second is used for the right and left, and the third element is used for the bottom
     * // 4	[ top, right, bottom, left ]	Each element is assigned to a specific side
     * @type { number | Array<number> }
     * @default
     *   */
    this.nineSliceOffsets = this.dialogBoxConfig.nineSliceOffsets; // 23
    /**
     * Safe area of the scaling areas..
     * @type { number }
     * @default
     *   */
    this.nineSliceSafeArea = this.dialogBoxConfig.nineSliceSafeArea; // 14
    this.nineSliceTopArea = this.dialogBoxConfig.nineSliceTopArea; // 10
    this.nineSliceBottomArea = this.dialogBoxConfig.nineSliceBottomArea; // 10
    this.nineSliceLeftArea = this.dialogBoxConfig.nineSliceLeftArea; // 10
    this.nineSliceRightArea = this.dialogBoxConfig.nineSliceRightArea; // 10
    /**
     * Sacele of the action button sprite.
     * @type { number }
     * @default
     *   */
    this.actionSpriteScale = this.dialogBoxConfig.actionSpriteScale; // 0.5
    /**
     * Spelling speed of the text in the dialog box. Bigger is faster.
     * @type { number }
     * @default
     *  */
    this.dialogSpeed = this.dialogBoxConfig.dialogSpeed; // 20
    /**
     * Dialog font size.
     * @type { number }
     * @default
     *  */
    this.fontSize = this.dialogBoxConfig.fontSize; // 20
    /**
     * Current dialog page.
     * @type { number }
     * @default
     *  */
    this.currentPage = 0;
    /**
     * Dialog font width.
     * @type { number }
     * @default
     *   */
    this.fontWidth = this.fontSize - this.dialogBoxConfig.fontWidthMargin; // 5
    /**
     * Maximum number of lines.
     * @type { number }
     * @default
     *  */
    this.dialogMaxLines = this.dialogBoxConfig.dialogMaxLines; // 3
    /**
     * Space between lines of the dialog text.
     * @type { number }
     * @default
     *  */
    this.letterSpacing = this.dialogBoxConfig.letterSpacing; // 0
    /**
     * Width of the camera view port.
     * @type { number }
     */
    this.cameraWidth =
      this.scene.cameras.main.displayWidth +
      this.dialogBoxConfig.cameraWidthMargin; // this.scene.cameras.main.displayWidth + this.margin * 2;
    /**
     * Height of the camera view port.
     * @type { number }
     */
    this.cameraHeight =
      this.scene.cameras.main.displayHeight +
      this.dialogBoxConfig.cameraHeightMargin; // this.scene.cameras.main.displayHeight - this.margin * 2;
    /**
     * Max width of the text inside the dialog.
     * @type { number }  */
    this.textWidth =
      this.cameraWidth - this.margin * 3 + this.dialogBoxConfig.textWidthMargin; // this.cameraWidth - this.margin * 3;
    /**
     * Rather it can show de dialog of not.
     * @type { boolean }
     * @default
     *  */
    this.canShowDialog = this.dialogBoxConfig.canShowDialog; // true
    /**
     * Defines if the player is overlapping the text zone.
     * @type { boolean }
     * @default
     *  */
    this.isOverlapingChat = this.dialogBoxConfig.isOverlapingChat; // false
    /**
     * Defines if the text is in spelling/typping animation.
     * @type { boolean }
     * @default
     *  */
    this.isAnimatingText = this.dialogBoxConfig.isAnimatingText; // false

    /**
     * @type { number }
     */
    this.cameraZoom =
      this.scene.cameras.main.zoom + this.dialogBoxConfig.cameraZoomMargin; // this.scene.cameras.main.zoom + this.margin * 2;

    /**
     * Color of the font.
     * @type { Phaser.Display.Color }
     * @default
     */
    this.fontColor = this.dialogBoxConfig.fontColor; // new Phaser.Display.Color(61, 61, 61, 1);

    /**
     * Button A
     * @type { Button }
     * @default
     */
    this.buttonA = null;

    /**
     * Button B
     * @type { Button }
     * @default
     */
    this.buttonB = null;

    /**
     * Action Button for general devices.
     * @type { Phaser.GameObjects.Image }
     * @default
     */
    this.actionButton = null;

    /**
     * The Dialog that will show the text.
     * @type { NineSlice }
     * @default
     */
    this.dialog = null;

    /**
     * Checks if it's mobile so it can hide the buttons.
     * @type { boolean }
     * @default
     */
    this.isMobile = false;

    /**
     * Controls the has video state. If true it has a video to play.
     * @type { boolean }
     * @default
     */
    this.hasVideo = false;

    /**
     * Class to open the video, if there is a video property defined by the developer.
     * @type { LuminusVideoOpener }
     * @default
     */
    this.luminusVideoOpener = new LuminusVideoOpener(this.scene);

    /**
     * The Typing sound Manager. This will make sounds while typing the letters.
     * @type { LuminusTypingSoundManager }
     * @default
     */
    this.luminusTypingSoundManager = null;

    /**
     * Array with all properties that come with the Message Box. This will allow us to create videos, and more interactions
     * with the player as we wish.
     * @type { Array }
     * @default
     */
    this.allProperties = null;

    /**
     * If you are using the LuminusGamePadController this variable will be created with the gamepad that is being used.
     * But only if it's connected.
     * @type { Phaser.Input.Gamepad }
     * @default
     */
    this.gamepad = this.scene.input.gamepad.pad1;

    /**
     * Font family to be used. It has to be included in your Phaser project.
     * @type { string }
     * @default
     */
    this.fontFamily = 'Monospace, "Press Start 2P"';

    /**
     * The Current Chat Configuration that is being displayed.
     */
    this.currentChat = null;

    /**
     * This variable controls if the chat will be shown from an NPC or any other Chat Income for example.
     * @type { boolean }
     */
    this.showRandomChat = false;

    /**
     * The text object that displays the right side entity on the dialog.
     * @type { Phaser.GameObjects.Text}
     */
    this.rightNameText = null;

    /**
     * The right side Portrait image.
     * @type { Phaser.GameObjects.Image }
     */
    this.rightPortraitImage = null;
    this.rightPortraitAnimation = null;
    this.rightNameTextBox = null;
    this.rightPortraitBoxImage = null;

    /**
     * The text object that displays the left side entity on the dialog.
     * @type { Phaser.GameObjects.Text}
     */
    this.leftNameText = null;

    /**
     * The left side Portrait image.
     * @type { Phaser.GameObjects.Image }
     */
    this.leftPortraitAnimation = null;
    this.leftNameTextBox = null;
    this.leftPortraitBoxImage = null;

    this.groupLeftSpeaker = null;
    this.groupRightSpeaker = null;

    this.speakerMarginX = 0;
    this.speakerMarginY = 0;
    this.portraitMarginX = 0;
    this.portraitMarginY = 0;

    this.startTextMessageX = 0;
    this.startTextMessageY = 0;
    this.interactiveDialog = new InteractiveDialog(this);

    this.animationTextBuffer = [];
  }

  create() {
    this.luminusTypingSoundManager = new LuminusTypingSoundManager(this.scene);
    this.luminusTypingSoundManager.create();
    // First thing to do is to check if it's mobile.
    this.isMobile = !this.scene.sys.game.device.os.desktop ? true : false;
    if (this.isMobile) {
      this.dialogMobileFactor = 1.5;
      this.dialogWidthFactor = 1.05;
    } else {
      this.dialogWidthFactor = 1.2;
    }
    if (this.cameraWidth < 1200 && !this.isMobile) {
      this.fontSize = this.cameraWidth / 60;
      this.fontWidth = this.fontSize - this.dialogBoxConfig.fontWidthMargin;
      this.dialogWidthFactor = 1.05;
    }
    if (this.cameraWidth < 1000 && !this.isMobile) {
      this.fontSize = this.cameraWidth / 50;
      this.fontWidth = this.fontSize - this.dialogBoxConfig.fontWidthMargin;
      this.dialogWidthFactor = 1.05;
    }
    if (this.cameraWidth < 500 && !this.isMobile) {
      this.fontSize = this.cameraWidth / 40;
      this.fontWidth = this.fontSize - this.dialogBoxConfig.fontWidthMargin;
      this.dialogWidthFactor = 1.05;
    }

    this.createDialogueBox();

    this.startTextMessageX =
      this.dialog.x - this.dialog.width / 2 + this.margin * 2;
    this.startTextMessageY =
      this.dialog.y - this.dialogHeight / 2 + this.margin * 2.5;
    this.createInteractionButtons();
    this.createDialogueElements();

    if (this.gamepad) {
      this.setGamepadTextures();
    }
    this.scene.input.gamepad.on("connected", (pad) => {
      this.gamepad = pad;
      this.setGamepadTextures();
    });
    this.scene.input.gamepad.on("down", (pad) => {
      this.gamepad = pad;
      this.checkButtonDown();
    });
  }

  createNameText(whoTalks) {
    if (whoTalks === "left") {
      this.leftNameText = this.scene.add
        .text(
          this.dialog.x > this.dialog.width / 2
            ? this.startTextMessageX
            : this.dialog.width / 2 - this.dialog.x + this.margin * 3.5,
          this.dialog.y - this.dialogHeight / 2 - this.margin / 4,
          ` ${this.leftName} `,
          {
            fontSize: this.fontSize,
            letterSpacing: this.letterSpacing,
            fontFamily: this.fontFamily,
            fontStyle: "bold",
            color: this.fontColor,
          },
        )
        .setScrollFactor(0, 0)
        .setDepth(99999999999999999);
    }
    if (whoTalks === "right") {
      this.rightNameText = this.scene.add
        .text(
          this.dialog.x + this.dialog.width / 2 - this.margin * 2,
          this.dialog.y - this.dialogHeight / 2 - this.margin / 4,
          ` ${this.rightName} `,
          {
            fontSize: this.fontSize,
            letterSpacing: this.letterSpacing,
            fontFamily: this.fontFamily,
            fontStyle: "bold",
            color: this.fontColor,
          },
        )
        .setScrollFactor(0, 0)
        .setDepth(99999999999999999);
      this.rightNameText.setX(this.rightNameText.x - this.rightNameText.width);
    }
  }
  createTextBox() {
    return this.scene.add
      .nineslice(
        0,
        0,
        "dialog_box",
        0,
        this.leftNameText.width + this.margin,
        this.leftNameText.height + this.margin,
        10,
        10,
        10,
        10,
      )
      .setScrollFactor(0, 0)
      .setDepth(102)
      .setVisible(false);
  }
  createNameTextBox(whoTalks) {
    if (whoTalks === "left") {
      this.leftNameTextBox = this.createTextBox().setPosition(
        this.leftNameText.x + this.leftNameText.width / 2,
        this.leftNameText.y + this.leftNameText.height / 2 - 2,
      );
    }
    if (whoTalks === "right") {
      this.rightNameTextBox = this.createTextBox().setPosition(
        this.rightNameText.x + this.rightNameText.width / 2,
        this.rightNameText.y + this.rightNameText.height / 2 - 2,
      );
    }
  }

  createPortraitAnimation(whoTalks) {
    if (whoTalks === "left") {
      this.leftPortraitAnimation = this.scene.add.sprite(
        this.leftNameTextBox.x - this.margin,
        this.leftNameTextBox.y - this.margin * 3,
        "",
      );
      this.leftPortraitAnimation.depth = 999;
      this.leftPortraitAnimation.flipX = false;
    }
    if (whoTalks === "right") {
      this.rightPortraitAnimation = this.scene.add.sprite(
        this.rightNameTextBox.x - this.margin,
        this.rightNameTextBox.y - this.margin * 3,
        "",
      );
      this.rightPortraitAnimation.depth = 999;
      this.rightPortraitAnimation.flipX = true;
    }
  }

  createPortraitBoxImage(whoTalks) {
    if (whoTalks === "left") {
      this.leftPortraitBoxImage = this.scene.add.image(
        this.leftNameTextBox.x - this.margin,
        this.leftNameTextBox.y - this.margin * 3,
        "portrait_box",
      );
      this.leftPortraitBoxImage.depth = 101;
    }
    if (whoTalks === "right") {
      this.rightPortraitBoxImage = this.scene.add.image(
        this.rightNameTextBox.x - this.margin,
        this.rightNameTextBox.y - this.margin * 3,
        "portrait_box",
      );
      this.rightPortraitBoxImage.depth = 101;
    }
  }
  groupSpeaker(whoTalks) {
    if (whoTalks === "left") {
      this.groupLeftSpeaker = this.scene.add.group();
      this.groupLeftSpeaker.add(this.leftNameTextBox);
      this.groupLeftSpeaker.add(this.leftNameText);
      this.groupLeftSpeaker.add(this.leftPortraitAnimation);
      this.groupLeftSpeaker.add(this.leftPortraitBoxImage);
      this.groupLeftSpeaker.getChildren().forEach((child) => {
        child.visible = false;
      });
    }
    if (whoTalks === "right") {
      this.groupRightSpeaker = this.scene.add.group();
      this.groupRightSpeaker.add(this.rightNameTextBox);
      this.groupRightSpeaker.add(this.rightNameText);
      this.groupRightSpeaker.add(this.rightPortraitAnimation);
      this.groupRightSpeaker.add(this.rightPortraitBoxImage);
      this.groupRightSpeaker.getChildren().forEach((child) => {
        child.visible = false;
      });
    }
  }
  /**
   * @private
   * Creates the dialogue elements.
   * Left and Right side talkers. Boxes with names and portraits.
   */
  createDialogueElements() {
    this.createNameText("left");
    this.createNameTextBox("left");
    this.createPortraitAnimation("left");
    this.createPortraitBoxImage("left");
    this.groupSpeaker("left");
    this.createNameText("right");
    this.createNameTextBox("right");
    this.createPortraitAnimation("right");
    this.createPortraitBoxImage("right");
    this.groupSpeaker("right");
  }

  /**
   * @private
   * Creates the interaction buttons.
   * The buttons are used to drive the dialogue, skip, and close.
   */
  createInteractionButtons() {
    this.actionButton = this.scene.add
      .image(
        this.cameraWidth - this.margin * 4,
        this.cameraHeight -
          // this.dialog_height -
          this.margin * 3,
        this.isMobile
          ? this.mobileActionButtonSpriteName
          : this.actionButtonSpriteName,
      )
      .setDepth(9999)
      .setScrollFactor(0, 0)
      .setScale(this.actionSpriteScale)
      .setInteractive();
    this.actionButton.visible = false;
    this.actionButton.on("pointerdown", (b) => {
      this.actionButton.clicked = true;
      this.checkButtonDown();
    });

    this.interactionIcon = this.scene.add
      .sprite(
        this.scene.cameras.main.midPoint.x,
        this.scene.cameras.main.midPoint.y -
          this.player.container.body.height / 2,
        this.interactionSpriteName,
      )
      .setDepth(99999)
      .setScale(2);

    this.interactionIcon.play(this.animationIteractionIconName);
    this.interactionIcon.visible = false;

    this.scene.tweenKey = this.scene.add.tween({
      targets: this.actionButton,
      yoyo: true,
      repeat: -1,
      scale: {
        from: this.actionSpriteScale,
        to: this.actionSpriteScale - 0.15,
      },
      duration: 1000,
    });

    this.keyObj = this.scene.input.keyboard.addKey(this.actionButtonKeyCode);

    this.scene.input.keyboard.on("keydown", (key) => {
      if (key.keyCode === 32) this.checkButtonDown();
    });

    const joystickScene = this.scene.scene.get("JoystickScene");
    joystickScene.events.on("JoystickReady", (done) => {
      if ((joystickScene && joystickScene.buttonA) || joystickScene.buttonB) {
        this.buttonA = joystickScene.buttonA;
        this.buttonB = joystickScene.buttonB;
        if (this.buttonA)
          this.buttonA.on("down", (b) => this.checkButtonDown());
        if (this.buttonB)
          this.buttonB.on("down", (b) => this.checkButtonDown());
      }
    });
  }

  /**
   * @private
   * Creates the dialogue box itself.
   */
  createDialogueBox() {
    this.dialog = this.scene.add.nineslice(
      this.cameraWidth / 2,
      this.cameraHeight - this.dialogHeight / this.dialogMobileFactor,
      this.dialogSpriteName,
      0,
      this.cameraWidth / this.dialogWidthFactor,
      this.dialogHeight,
      this.nineSliceLeftArea,
      this.nineSliceRightArea,
      this.nineSliceTopArea,
      this.nineSliceBottomArea,
    );
    this.dialog.setScrollFactor(0, 0);
    this.dialog.depth = 99;
    this.dialog.visible = false;
  }

  /**
   * Sets the GamePad Textures.
   * If the gamepad is connected, it should use the gamepad textures.
   */
  setGamepadTextures() {
    this.actionButton.setTexture(this.mobileActionButtonSpriteName);
  }

  /**
   * Resets the Dialogue Speakers alpha to the default value
   */
  resetSpeakersAlpha() {
    this.groupLeftSpeaker.getChildren().forEach((child) => {
      child.alpha = 0.5;
    });
    this.groupRightSpeaker.getChildren().forEach((child) => {
      child.alpha = 0.5;
    });
  }
  updateLeftSpeaker() {
    if (this.currentChat && this.currentChat.leftName) {
      this.leftNameText.setPosition(
        this.dialog.x > this.dialog.width / 2
          ? this.dialog.x -
              this.dialog.width / 2 +
              this.margin * 2 +
              this.speakerMarginX
          : this.dialog.width / 2 -
              this.dialog.x +
              this.margin * 3.5 +
              this.speakerMarginX,
        this.dialog.y -
          this.dialogHeight / 2 -
          this.margin / 4 +
          this.speakerMarginY,
      );
      this.leftNameTextBox.setPosition(
        this.leftNameText.x + this.leftNameText.width / 2,
        this.leftNameText.y + this.leftNameText.height / 2 - 2,
      );
      this.leftNameTextBox.setSize(
        this.leftNameText.width + this.margin,
        this.leftNameText.height + this.margin,
      );
      const leftNameTextBoxX = this.leftNameTextBox.x + this.portraitMarginX;
      const leftNameTextBoxY =
        this.leftNameTextBox.y - this.margin * 3 + this.portraitMarginY;
      this.leftPortraitAnimation.setPosition(
        leftNameTextBoxX,
        leftNameTextBoxY,
      );
      this.leftPortraitBoxImage.setPosition(leftNameTextBoxX, leftNameTextBoxY);
    } else {
      this.groupLeftSpeaker.getChildren().forEach((child) => {
        child.visible = false;
      });
    }
    if (this.currentChat && this.currentChat.leftPortraitName) {
      this.leftPortraitAnimation.play({
        key: this.currentChat.leftPortraitName,
        repeat: -1,
      });
    } else {
      this.leftPortraitAnimation.visible = false;
      this.leftPortraitBoxImage.visible = false;
    }
  }
  updateRightSpeaker() {
    this.rightNameText.setPosition(
      this.dialog.x +
        this.dialog.width / 2 -
        this.margin * 2 -
        this.rightNameText.width -
        this.speakerMarginX,
      this.dialog.y -
        this.dialogHeight / 2 -
        this.margin / 4 +
        this.speakerMarginY,
    );
    this.rightNameTextBox.setPosition(
      this.rightNameText.x + this.rightNameText.width / 2,
      this.rightNameText.y + this.rightNameText.height / 2 - 2,
    );
    this.rightNameTextBox.setSize(
      this.rightNameText.width + this.margin,
      this.rightNameText.height + this.margin,
    );
    const rightNameTextBoxX = this.rightNameTextBox.x + this.portraitMarginX;
    const rightNameTextBoxY =
      this.rightNameTextBox.y - this.margin * 3 + this.portraitMarginY;
    this.rightPortraitAnimation.setPosition(
      rightNameTextBoxX,
      rightNameTextBoxY,
    );
    this.rightPortraitBoxImage.setPosition(
      rightNameTextBoxX,
      rightNameTextBoxY,
    );
    if (this.currentChat && this.currentChat.rightPortraitName) {
      this.rightPortraitAnimation.play({
        key: this.currentChat.rightPortraitName,
        repeat: -1,
      });
    }
  }

  /**
   * Checks what Speaker should have the highlight. Highlights the current Speaker, and makes the secondary speaker alpha lower.
   */
  checkSpeaker() {
    this.resetSpeakersAlpha();
    this.groupLeftSpeaker.getChildren().forEach((child) => {
      child.visible = true;
    });
    if (this.currentChat.left) {
      this.leftNameText.setText(` ${this.currentChat.leftName} `);
      this.updateLeftSpeaker();
      this.groupLeftSpeaker.getChildren().forEach((child) => {
        child.alpha = 1;
      });
    }
    if (this.currentChat.right) {
      this.rightNameText.setText(` ${this.currentChat.rightName} `);
      this.updateRightSpeaker();
      this.groupRightSpeaker.getChildren().forEach((child) => {
        child.visible = true;
        child.alpha = 1;
      });
    }
    this.executeDialogueAnimations();
  }

  /**
   * Executes the dialogue animations.
   */
  executeDialogueAnimations() {
    if (this.currentChat.leftExit) this.exitFromScene("left");
    if (this.currentChat.rightExit) this.exitFromScene("right");
  }

  /**
   * Moves the dialogue speaker out of the screen.
   * @param { string }  orientation  - The dialogue speaker side to move away from screen.
   */
  exitFromScene(orientation) {
    if (orientation === "right") {
      this.groupRightSpeaker.getChildren().forEach((child) => {
        if (
          child === this.rightPortraitAnimation ||
          child === this.rightPortraitBoxImage
        ) {
          this.scene.tweens.add({
            targets: child,
            x: child.x + 500,
            duration: 1000,
            onStart: () => {
              child.visible = true;
            },
            onComplete: () => {
              child.visible = false;
              child.x = child.x - 500;
            },
          });
        } else {
          child.visible = false;
        }
      });
    }
    if (orientation === "left") {
      this.groupLeftSpeaker.getChildren().forEach((child) => {
        if (
          child === this.leftPortraitAnimation ||
          child === this.leftPortraitBoxImage
        ) {
          this.scene.tweens.add({
            targets: child,
            x: child.x - 500,
            duration: 1000,
            onStart: () => {
              child.visible = true;
            },
            onComplete: () => {
              child.visible = false;
              child.x = child.x + 500;
            },
          });
        } else {
          child.visible = false;
        }
      });
    }
  }

  /**
   * Checks what to do when the player presses the action button.
   */
  checkButtonDown() {
    if (
      (this.isOverlapingChat || this.showRandomChat) &&
      this.checkButtonsPressed() &&
      !this.dialog.visible
    ) {
      // First time, show the Dialog.
      this.currentChat = this.chat[0];
      this.currentChat.index = 0;
      this.dialogMessage = this.currentChat.message;
      this.checkSpeaker();
      this.showDialog();
      this.player.container.body.maxSpeed = 0;
    } else if (this.isAnimatingText && this.checkButtonsPressed()) {
      // Skips the typping animation.
      this.setText(this.pagesMessage[this.currentPage], false); // my change
    } else if (
      !this.isAnimatingText &&
      this.currentPage !== this.pagesNumber - 1 &&
      this.dialog.visible &&
      this.checkButtonsPressed()
    ) {
      // Has more pages.
      this.currentPage++;
      this.dialog.textMessage.text = "";
      this.setText(this.pagesMessage[this.currentPage], true);
    } else if (
      this.currentChat &&
      this.currentChat.index < this.chat.length - 1
    ) {
      let index = this.currentChat.index;
      this.currentChat = this.chat[index + 1];
      this.currentChat.index = index + 1;
      this.checkSpeaker();
      this.dialogMessage = this.currentChat.message;
      this.pagesMessage = [];
      this.setText("", false);
      this.showDialog(false);
    } else if (
      this.checkButtonsPressed() &&
      this.dialog.visible &&
      this.dialog.textMessage &&
      this.dialog.textMessage.active
    ) {
      // Finishes the Dialog. Destroys the text and sets all variables to initial state.
      this.dialog.textMessage.destroy();
      this.luminusVideoOpener.checkHasVideo(this.allProperties);
      this.dialog.visible = false;
      this.groupLeftSpeaker.getChildren().forEach((child) => {
        child.visible = false;
      });

      this.canShowDialog = true;
      this.actionButton.visible = false;
      this.interactionIcon.visible = false;
      this.player.container.body.maxSpeed = this.player.speed;
    }
    this.actionButton.clicked = false;
  }

  /**
   * Checks if any action buttons is pressed.
   * Is it Keyboard / Mobile / GamePad.
   */
  checkButtonsPressed() {
    return (
      this.keyObj.isDown ||
      this.isMobileButtonPressed() ||
      (this.gamepad && this.gamepad.A)
    );
  }

  /**
   * Checks if the Button A or the Button B is pressed.
   * Returns true if any of those is pressed, otherwise returns false.
   * @returns { boolean }
   */
  isMobileButtonPressed() {
    return (
      (this.buttonA && this.buttonA.isDown) ||
      (this.buttonB && this.buttonB.isDown) ||
      (this.actionButton && this.actionButton.clicked)
    );
  }

  /**
   * Shows the dialog with the message from the zone it's overlaping.
   * Make sure you have only one overlaping zone with the player.
   */
  showDialog(createText = true) {
    this.currentPage = 0;
    // this.actionButton.visible = false;
    this.dialog.visible = true;
    this.canShowDialog = false;
    const maxLettersPage =
      Math.floor(this.dialog.width / this.fontWidth) * this.dialogMaxLines;
    this.pagesMessage = [];
    let sumMessagesLength = 0;
    let pageMessage = "";
    for (let i = 0; i < this.dialogMessage.length; i++) {
      const message = this.dialogMessage[i];
      const messageLength = message.originalMessageLength;

      if (sumMessagesLength + messageLength <= maxLettersPage) {
        sumMessagesLength += messageLength;
        pageMessage += message.interactiveMessage + " ";
      } else {
        this.pagesMessage.push(pageMessage.trim());
        pageMessage = message.interactiveMessage + " ";
        sumMessagesLength = messageLength;
      }

      if (i === this.dialogMessage.length - 1) {
        this.pagesMessage.push(pageMessage.trim());
      }
    }
    // if this.dialogMessage.length =1 or if all the messages are in the same page
    if (this.pagesMessage.length === 0) {
      this.pagesMessage.push(pageMessage);
    }

    this.pagesNumber = this.pagesMessage.length;
    if (createText) this.createText();
    // Animates the text
    this.setText(this.pagesMessage[0], true);
  }

  /**
   * Sets the text for the dialog window.
   * @param { string } text The text string to be shown in the dialog.
   * @param { boolean } animate Rather it should animate the text or not. If it's false, it will stop the animation text in process.
   */
  setText(text, animate = false) {
    // in case of interaction text is separated in 2 dialog pages one is on the last word of the first page and the other is on the first of the second page
    if (this.interactiveDialog.interactionText) {
      const lastElement = this.interactiveDialog.interactionText.length - 1;
      if (
        lastElement >= 0 &&
        !this.interactiveDialog.interactionText[lastElement].isEnd
      ) {
        text =
          this.interactiveDialog.interactionText[lastElement].delimiter +
          this.interactiveDialog.interactionText[lastElement].message +
          " " +
          text;
      }
    }
    // Reset the dialog
    this.eventCounter = 0;

    this.animationTextTime = 1;
    this.interactiveDialog.interactionText = [];

    this.animationText = text.split("");
    if (this.animationTextBuffer.length > 0) {
      this.animationText.splice(0, 0, ...this.animationTextBuffer);
      this.animationTextBuffer = [];
    }
    if (this.timedEvent) this.timedEvent.remove();

    this.interactiveDialog.interactionTextObjects &&
      this.interactiveDialog.interactionTextObjects.forEach((element) => {
        element.destroy();
      });

    if (animate) {
      this.isAnimatingText = true;
      this.timedEvent = this.scene.time.addEvent({
        delay: Math.floor(this.dialogSpeed),

        callback: this.animateText,
        callbackScope: this,
        loop: true,
      });
    } else {
      if (this.timedEvent) {
        this.timedEvent.remove();
      }
      this.dialog.textMessage.setText("");

      this.timedEvent = this.scene.time.addEvent({
        delay: 0.1,

        callback: this.animateText,
        callbackScope: this,
        loop: true,
      });

      this.isAnimatingText = false;
    }
    this.interactiveDialog.interactionTextPositionCalculation();
  }

  /**
   * Slowly displays the text in the window to make it appear annimated
   * */
  animateText() {
    this.eventCounter++;
    const i = this.eventCounter - 1;
    const message = this.animationText
      .slice(i, this.animationText.length)
      .join("");

    const isInteractive = this.interactiveDialog.parseInteractiveMessage(
      message,
      i,
    );
    if (isInteractive) {
      this.eventCounter--;
      return;
    }

    if (this.animationText[this.eventCounter - 1]) {
      this.dialog.textMessage.setText(
        this.dialog.textMessage.text +
          this.animationText[this.eventCounter - 1],
      );
    }

    //// Stops the text animation.
    if (this.eventCounter > this.animationText.length) {
      this.isAnimatingText = false;
      this.timedEvent.remove();
      this.leftPortraitAnimation.stop();
      this.rightPortraitAnimation.stop();

      // because of fast delay don't destroy the interaction objects
      this.interactiveDialog.interactionTextObjects &&
        this.interactiveDialog.interactionTextObjects.forEach((element) => {
          element.destroy();
        });

      this.interactiveDialog.interactionTextPositionCalculation();
    }
  }

  /**
   * Checks if the player is moving.
   * @returns { boolean }
   */
  isMoving() {
    if (this.player && this.player.container && this.player.container.body) {
      // If is colliding should always show the trigger button.
      // Pressing space button, should show the chat.
      return (
        this.player.container.body.velocity.x !== 0 ||
        this.player.container.body.velocity.y !== 0
      );
    }
  }

  /**
   * Checks if the player is still overlaping the zone.
   * Hides the action button if it's not overlaping the zone.
   */
  checkUpdate() {
    if (
      this.actionButton &&
      this.isMoving() &&
      this.player.container.body.touching.none &&
      this.isOverlapingChat &&
      !this.dialog.visible
    ) {
      this.actionButton.visible = false;
      this.interactionIcon.visible = false;
      this.isOverlapingChat = false;
      this.player.canAtack = true;
    }
  }

  /**
   * Resizes all the elements of the dialog component.
   * @param { number } width new Width.
   * @param { number } height new Height.
   */
  //My ToDo
  resizeComponents(width, height) {
    if (width !== 0 && height !== 0 && this.player && this.player.active) {
      this.interactionIcon.setPosition(
        width / 2,
        height / 2 - this.player.container.body.height * 2.5,
      );

      this.cameraWidth = width;
      this.cameraHeight = height;
      this.textWidth = this.cameraWidth - this.margin * 3;
      this.dialog.x = this.cameraWidth / 2;
      this.dialog.y =
        (this.cameraHeight - this.dialogHeight - this.margin) /
        this.dialogMobileFactor; // this is the starting x/y location
      //this.dialog.resize(this.cameraWidth - this.margin * 2, this.dialogHeight);
      this.dialog.setSize(
        this.cameraWidth / this.dialogWidthFactor,
        this.dialogHeight,
      );

      this.actionButton.x = this.cameraWidth - this.margin * 4;
      this.actionButton.y = this.cameraHeight - this.margin * 3;

      this.updateLeftSpeaker();
      this.updateRightSpeaker();
      if (this.dialog.textMessage && this.dialog.textMessage.visible) {
        this.dialog.textMessage.setPosition(
          this.startTextMessageX,
          this.startTextMessageY,
        );
        this.dialog.textMessage.setStyle({
          wordWrap: {
            width: this.dialog.width - this.margin * 2,
          },
          wordWrapUseAdvanced: false,
          fontSize: this.fontSize,
          maxLines: this.dialogMaxLines,
          letterSpacing: this.letterSpacing,
          fontFamily: this.fontFamily,
        });
      } else {
        this.createText();
      }
    }
  }

  /**
   * Creates the text Game Object
   * @private
   */
  createText() {
    this.dialog.textMessage = this.scene.add
      .text(this.startTextMessageX, this.startTextMessageY, "", {
        wordWrap: {
          width: this.dialog.width - this.margin * 2,
        },
        fontSize: this.fontSize,
        maxLines: this.dialogMaxLines,
        letterSpacing: this.letterSpacing,
        fontFamily: this.fontFamily,
        color: this.fontColor,
      })
      .setScrollFactor(0, 0)
      .setDepth(99999999999999999)
      .setFixedSize(this.cameraWidth - this.margin * 3, this.dialogHeight);
  }
}
