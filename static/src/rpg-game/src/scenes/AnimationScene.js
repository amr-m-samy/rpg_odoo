import { Animations } from "../consts/Animations";
const COLOR_MAIN = 0x4e342e;
const COLOR_LIGHT = 0x7b5e57;
const COLOR_DARK = 0x260e04;

function simpleDropDownList(scene, x, y, options, name) {
  const style = {
    label: {
      space: { left: 10, right: 10, top: 10, bottom: 10 },
      background: {
        color: COLOR_MAIN,
      },
      text: {
        fixedWidth: 150,
      },
    },

    track: { width: 10, color: COLOR_MAIN },
    thumb: { width: 14, height: 14, color: COLOR_LIGHT },

    button: {
      space: { left: 10, right: 10, top: 10, bottom: 10 },
      background: {
        color: COLOR_DARK,
        strokeWidth: 0,
        "hover.strokeColor": 0xffffff,
        "hover.strokeWidth": 2,
      },
      text: {
        fontSize: 20,
      },
    },

    list: {
      maxHeight: 200,
      sliderAdaptThumbSize: true,
      mouseWheelScroller: {
        focus: true,
        speed: 0.1,
      },
    },
  };
  return scene.rexUI.add
    .simpleDropDownList(style)
    .resetDisplayContent(name)
    .setOptions(options)
    .setPosition(x, y)
    .layout();
}
export class AnimationScene extends Phaser.Scene {
  constructor() {
    super({
      key: "AnimationScene",
    });
  }

  preload() {}

  create() {
    const scene = this;

    const cameraHeight = scene.cameras.main.displayHeight;
    const cameraWidth = scene.cameras.main.displayWidth;
    scene.add.tileSprite(
      cameraWidth / 2,
      cameraHeight / 2,
      cameraWidth / 2,
      cameraHeight / 1.6,
      "transparent_grid_2",
    );

    let options = {};
    const AnimationsObject = Animations.map((animation) => {
      const splitArray = animation.key.split("-");
      const key = splitArray.shift();
      const value = splitArray.join("-");
      if (!options[key]) {
        options[key] = [value];
      } else {
        options[key].push(value);
      }
    });

    const dropDownListAnimation = simpleDropDownList(
      scene,
      cameraWidth / 5,
      cameraHeight / 2 - 50,
      Object.keys(options),
      "Animation",
    );
    console.log(options);
    var print = this.add.text(0, 0, "");
    let animationKey = "";
    let animationPlay = null;
    scene.dropDownlistDirection = null;
    dropDownListAnimation.on(
      "button.click",
      function (dropDownList, listPanel, button, index, pointer, event) {
        print.text = "";
        animationKey = "";

        if (animationPlay) {
          animationPlay.destroy();
        }
        const btnValueAnimationDropDown = button.value;
        if (scene.dropDownlistDirection) {
          scene.dropDownlistDirection.destroy();
        }
        if (options[button.value][0] !== "") {
          scene.dropDownlistDirection = simpleDropDownList(
            scene,
            cameraWidth / 5,
            cameraHeight / 2 + 50,
            options[button.value],
            "Direction",
          );
          scene.dropDownlistDirection.on(
            "button.click",
            function (dropDownList, listPanel, button, index, pointer, event) {
              if (animationPlay) {
                animationPlay.destroy();
              }
              animationKey = `${btnValueAnimationDropDown}-${button.value}`;
              dropDownList.setText(button.text);
              animationPlay = scene.add
                .sprite(cameraWidth / 2, cameraHeight / 2, "view")
                .play(animationKey)
                .setScale(8);
            },
          );
        } else {
          animationPlay = scene.add
            .sprite(cameraWidth / 2, cameraHeight / 2, "view")
            .play(btnValueAnimationDropDown)
            .setScale(4);
        }
        dropDownList.setText(button.text);
      },
    );
  }

  update() {}
}
