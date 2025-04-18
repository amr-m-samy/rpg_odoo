import { words } from "lodash";
import { InfoBox } from "../components/InfoBox";

export class InteractiveDialog {
  constructor(dialogBox) {
    this.dialogBox = dialogBox;
    this.interactionText = null;
    this.interactionTextObjects = null;
    this.translatePanel = null;
    this.translateIcon = null;
    this.hiddenText = null;
  }

  dictionary(word) {
    const dictionary = this.dialogBox.dictionary;
    if (dictionary[word.toLowerCase()]) {
      return dictionary[word.toLowerCase()];
    } else {
      return null;
    }
  }
  splitString(input) {
    // Regular expression to match **any characters** or ##any characters##
    const regex = /(\*\*.*?\*\*|##.*?##)/g;

    // Split the string using the regex and filter out empty strings
    const result = input.split(regex).filter(Boolean);
    if (result.length === 0) {
      return [input];
    }
    return result;
  }
  extractText(
    message,
    delimiter,
    endDelimiter,
    type,
    xPos,
    yPos,
    recursionFlag = false,
  ) {
    let tempMessage = "";
    let startIndex = delimiter.length;

    let isEnd = true;
    let originalMessageLength = 0;

    while (
      startIndex < message.length &&
      message.slice(startIndex, startIndex + delimiter.length) !== endDelimiter
    ) {
      tempMessage += message[startIndex++];
    }
    if (
      message.slice(startIndex, startIndex + delimiter.length) !== endDelimiter
    ) {
      isEnd = false;
    }
    if (!recursionFlag) {
      originalMessageLength = tempMessage.length;
    }
    const delimiterDetection = this.delimiterDetection(tempMessage, 0);
    if (delimiterDetection) {
      tempMessage = tempMessage.slice(delimiter.length - 1);
      tempMessage = this.extractText(
        tempMessage,
        delimiterDetection.delimiter,
        delimiterDetection.endDelimiter,
        delimiterDetection.type,
        xPos,
        yPos,
        true,
      ).message;
    }
    return {
      message: tempMessage,
      type: type,
      delimiter: delimiter,
      positionX: xPos,
      positionY: yPos,
      isEnd: isEnd,
      originalMessageLength: originalMessageLength,
    };
  }
  showVideo(videoId) {
    this.dialogBox.luminusVideoOpener.checkHasVideo([
      {
        name: "videoId",
        value: videoId,
        //value: "ZZAvB0N07aE",
      },
    ]);
  }
  showImage(imageName) {
    const screenWidth = this.dialogBox.scene.sys.game.config.width;
    const screenHeight = this.dialogBox.scene.sys.game.config.height;
    //this.dialogBox.frame = this.dialogBox.scene.add
    //  .image(screenWidth / 2, screenHeight / 2, "panel_background")
    //  .setOrigin(0, 0.2);
    this.dialogBox.image = this.dialogBox.scene.add.image(
      this.dialogBox.scene.scale.width / 2,
      this.dialogBox.scene.scale.height / 2 -
        (this.dialogBox.scene.scale.height / 2) * 0.2,
      imageName,
    );
    this.dialogBox.image.setScale(0.35);
    if (this.dialogBox.scene.scale.height / this.dialogBox.image.height > 0.7) {
      this.dialogBox.image.setScale(0.9);
    }
    //this.dialogBox.mask = this.dialogBox.scene.make.graphics({ x: 400, y: 300, add: false });
    //this.dialogBox.mask.fillRect(-150, -100, 300, 200);
    //this.dialogBox.image.setMask(this.dialogBox.mask.createGeometryMask());
    //this.dialogBox.frame.setDisplaySize(screenWidth * 0.8, ((screenWidth * 0.8) / 4) * 3);
    //this.dialogBox.image.setDisplaySize(screenWidth * 0.7, screenHeight * 0.7);
    //this.dialogBox.image.setScale(0.6);
    //this.dialogBox.image.setPosition(400, 300);
    //this.dialogBox.frame.setDisplaySize(300, 200);
    this.dialogBox.scene.input.keyboard.on("keydown", (key) => {
      if (key.keyCode === 32) {
        //this.dialogBox.frame.destroy();
        this.dialogBox.image.destroy();
      }
    });
    //if (this.dialogBox.buttonA) {
    //  this.dialogBox.buttonA.on("down", (b) => {
    //    console.log("buttonA");
    //    this.dialogBox.image.destroy();
    //  });
    //}
    //if (this.dialogBox.buttonB) {
    //  console.log("buttonB");
    //  this.dialogBox.buttonB.on("down", (b) => this.dialogBox.image.destroy());
    //}
    //if (this.dialogBox.actionButton) {
    //  console.log("actionButton");
    //  this.dialogBox.actionButton.on("down", (b) => this.dialogBox.image.destroy());
    //}
  }

  createInfoBox(interactionDate, interactionObject) {
    const dictionary = this.dictionary(interactionDate.message);
    if (!dictionary) {
      return;
    }
    const imageName = dictionary.image || "";
    const translatedMessage = dictionary.translatedMessage || "";
    this.translatePanel = new InfoBox(
      this.dialogBox.scene,
      interactionObject.x,
      interactionObject.y - 200,
      200,
      200,
      {
        name: dictionary.name,
        translate: translatedMessage,
        description: dictionary.description,
        image: imageName,
        //description: interactionText.tem.description,
      },
    );
  }

  destroyTranslationPanel() {
    if (this.translatePanel) {
      this.translatePanel.backgroundSprite.destroy();
      this.translatePanel.name.destroy();
      if (this.translatePanel.description) {
        this.translatePanel.description.destroy();
      }
      if (this.translatePanel.image) {
        this.translatePanel.image.destroy();
      }
      if (this.translatePanel.translate) {
        this.translatePanel.translate.destroy();
      }
      this.translatePanel = null;
    }
  }
  showTranslationBox(element, textObject) {
    //this.graphics = this.dialogBox.scene.add.graphics();
    //this.graphics.lineStyle(2, 0xff0000, 1);
    ////console.log(element);
    //this.graphics
    //  .strokeRect(
    //    element.positionX,
    //    element.positionY,
    //    textObject.width,
    //    textObject.height,
    //  )
    //  .setDepth(99999999999999999);
    const translateIconX = element.rightTextObjectX || element.positionX;
    const translateIconY = element.rightTextObjectY || element.positionY;
    this.translateIcon = this.dialogBox.scene.add
      .image(
        translateIconX + textObject.width + 4,
        translateIconY - 4,
        "translate_icon",
      )
      .setScale(0.5)
      .setDepth(999999999);
    this.interactionTextObjects.push(this.translateIcon);
    textObject.text = "";
    const btn = this.translateIcon;
    btn.setInteractive({ useHandCursor: true });
    btn.on("pointerover", () => {
      this.createInfoBox(element, textObject);
    });
    btn.on("pointerout", () => {
      this.destroyTranslationPanel();
      //this.graphics.destroy();
    });
  }

  createDictionaryBtn(element, textObject) {
    const btn = textObject.setStyle({
      color: "#d35400",
      fontStyle: "bold",
      fixedHeight: 25,
      fixedWidth: textObject.text.length * 12,
      align: "center",
      radius: 10,
      borderColor: "#ff501f",
      backgroundColor: "#f39c12",
    });
    btn.setInteractive({ useHandCursor: true });
    btn.on("pointerover", () => {
      btn.setBackgroundColor("#8d8d8d");
    });
    btn.on("pointerout", () => {
      btn.setBackgroundColor("#f39c12");
    });
    btn.on("pointerdown", () => {
      this.dialogBox.scene.scene.launch("DictionaryScene", {
        wordId: element.message,
        player: this.dialogBox.player,
      });
      console.log("dictionary");
    });
  }
  interactionTextPositionCalculation() {
    this.interactionTextObjects = [];
    this.interactionText.forEach((element, i) => {
      const textObject = this.createTextObject();
      const rightTextObject = this.createTextObject();
      this.interactionTextObjects.push(textObject);
      this.interactionTextObjects.push(rightTextObject);

      if (this.hiddenText) {
        this.hiddenText.destroy();
      }
      this.hiddenText = this.createHiddentTextObject(0);
      const tempInteractiveText = this.hiddenText.setText(element.message);
      console.log(
        element.message,
        tempInteractiveText.width + element.positionX,
        this.dialogBox.dialog.width +
          this.dialogBox.startTextMessageX -
          this.dialogBox.margin * 2,
      );
      if (
        tempInteractiveText.width + element.positionX >=
        this.dialogBox.cameraWidth - this.dialogBox.startTextMessageX
      ) {
        const words = this.hiddenText.text.split(/\s+/);
        for (let i = 1; i <= words.length; i++) {
          const splitIndex = words.length - i;
          const leftPart = words.slice(0, splitIndex).join(" ");
          const rightPart = words.slice(splitIndex).join(" ");
          const leftWidth = this.hiddenText.setText(leftPart).width;
          if (
            leftWidth + element.positionX <=
            this.dialogBox.cameraWidth - this.dialogBox.startTextMessageX
          ) {
            textObject.setText(leftPart);
            rightTextObject.setText(rightPart);
            rightTextObject.setX(this.dialogBox.startTextMessageX);
            rightTextObject.setY(
              element.positionY +
                this.dialogBox.fontSize +
                this.dialogBox.lineSpacing,
            );
            break;
          }
        }
      } else {
        textObject.setText(element.message);
      }
      let tempTextObject = this.hiddenText.setText(textObject.text);
      textObject.setFixedSize(tempTextObject.width, tempTextObject.height);
      if (rightTextObject.text !== "" && rightTextObject.text !== undefined) {
        tempTextObject = this.hiddenText.setText(rightTextObject.text);
        rightTextObject.setFixedSize(
          tempTextObject.width,
          tempTextObject.height,
        );
      }

      tempTextObject.destroy();
      //tempTextObject = tempText.setText(rightTextObject.text);
      ////rightTextObject.setFixedSize(tempTextObject.width, tempTextObject.height);

      tempInteractiveText.destroy();
      if (element.type === "important") {
        const importStyle = {
          color: "#af7ac5",
          //fontStyle: "bold",
          stroke: "#512e5f",
          strokeThickness: 2,
        };
        textObject.setStyle(importStyle);
        if (rightTextObject.text !== "") {
          rightTextObject.setStyle(importStyle);
        }
      } else if (element.type === "dictionary") {
        this.createDictionaryBtn(element, textObject);
        if (rightTextObject.text !== "") {
          this.createDictionaryBtn(element, rightTextObject);
        }
      } else if (element.type === "image") {
        this.dialogBox.scene.scene.launch("ImagePreviewScene", {
          imageName: element.message,
        });
      } else if (element.type === "video") {
        this.showVideo(element.message);
      } else if (element.type === "translation") {
        //console.log(rightTextObject.text);
        if (rightTextObject.text !== "") {
          element.rightTextObjectX = this.dialogBox.startTextMessageX;
          element.rightTextObjectY = rightTextObject.y;
          this.showTranslationBox(element, rightTextObject);
        } else {
          this.showTranslationBox(element, textObject);
        }
        //const translationStyle = {
        //  color: "#d35400",
        //  fontStyle: "bold",
        //  //stroke: "#512e5f",
        //  //strokeThickness: 2,
        //};
        //this.dialogBox.scene.add
        //  .graphics()
        //  .strokeRectShape(textObject.getBounds())
        //  .setDepth(99999999999999999);
        //textObject.setStyle(translationStyle);
      }
      textObject.setX(element.positionX);
      textObject.setY(element.positionY - 2);
      //textObject.visible = false;
      //textObject.alpha = 0.5;
    });
  }
  delimiterDetection(message, i) {
    const maybeDelimiter = ["*", "#", "["].includes(message[i]);
    if (maybeDelimiter) {
      const delimiter = message[i];
      if (delimiter === "*" && message[i + 1] === "*") {
        return { delimiter: "**", endDelimiter: "**", type: "important" };
      }
      if (delimiter === "#" && message[i + 1] === "#") {
        return { delimiter: "##", endDelimiter: "##", type: "dictionary" };
      }
      if (delimiter === "[") {
        return { delimiter: "[", endDelimiter: "]", type: "translation" };
      }
      return;
    }
    return maybeDelimiter;
  }
  parseInteractiveMessage(message, i) {
    const animationText = this.dialogBox.animationText;
    const delimiterDetection = this.delimiterDetection(animationText, i);
    const delimiter = delimiterDetection?.delimiter;
    const type = delimiterDetection?.type;
    const endDelimiter = delimiterDetection?.endDelimiter;
    if (!delimiter) {
      return false;
    }

    const wrappedTextLength =
      this.dialogBox.dialog.textMessage.getWrappedText().length;

    if (this.hiddenText) {
      this.hiddenText.destroy();
    }
    this.hiddenText = this.createHiddentTextObject(wrappedTextLength - 1);
    this.hiddenText.setText(
      this.dialogBox.dialog.textMessage.getWrappedText()[wrappedTextLength - 1],
    );

    animationText.splice(i, delimiter.length);
    const posX = this.hiddenText.x + this.hiddenText.width;
    const posY = this.hiddenText.y;
    const result = this.extractText(
      message,
      delimiter,
      endDelimiter,
      type,
      posX,
      posY,
    );
    this.interactionText.push(result);

    if (
      animationText
        .slice(
          i + result.originalMessageLength,
          i + result.originalMessageLength + delimiter.length,
        )
        .join("") === endDelimiter
    ) {
      animationText.splice(i + result.originalMessageLength, delimiter.length);
      //}
      return true;
    }
  }

  /**
   * Creates the text Game Object
   * @private
   */

  createHiddentTextObject(lineNumber) {
    return this.dialogBox.scene.add
      .text(
        this.dialogBox.dialog.x -
          this.dialogBox.dialog.width / 2 +
          this.dialogBox.margin * 2,
        this.dialogBox.dialog.y -
          this.dialogBox.dialogHeight / 2 +
          this.dialogBox.margin * 2.5 +
          (this.dialogBox.fontSize +
            this.dialogBox.fontSize / 5 +
            this.dialogBox.lineSpacing) *
            lineNumber,
        "",
        {
          wordWrap: {
            width: this.dialogBox.dialog.width - this.dialogBox.margin * 2,
          },
          fontSize: this.dialogBox.fontSize,
          maxLines: this.dialogBox.dialogMaxLines,
          letterSpacing: this.dialogBox.letterSpacing,
          fontFamily: this.dialogBox.fontFamily,
          color: "#0eefff",
          lineSpacing: this.dialogBox.lineSpacing,
        },
      )
      .setDepth(999999999999999999)
      .setVisible(false);
  }
  createTextObject() {
    return this.dialogBox.scene.add
      .text(
        this.dialogBox.dialog.x -
          this.dialogBox.dialog.width / 2 +
          this.dialogBox.margin * 2,
        this.dialogBox.dialog.y -
          this.dialogBox.dialogHeight / 2 +
          this.dialogBox.margin * 2.5,
        "",
        {
          wordWrap: {
            width: this.dialogBox.dialog.width - this.dialogBox.margin * 2,
          },
          fontSize: this.dialogBox.fontSize,
          maxLines: this.dialogBox.dialogMaxLines,
          letterSpacing: this.dialogBox.letterSpacing,
          fontFamily: this.dialogBox.fontFamily,
          color: this.dialogBox.fontColor,
          lineSpacing: this.dialogBox.lineSpacing,
        },
      )
      .setScrollFactor(0, 0)
      .setDepth(99999999999999999)
      .setFixedSize(
        this.dialogBox.cameraWidth - this.dialogBox.margin * 3,
        this.dialogBox.dialogHeight,
      );
  }
}
