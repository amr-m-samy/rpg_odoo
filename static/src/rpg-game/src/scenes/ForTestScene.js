export class ForTestScene extends Phaser.Scene {
  constructor() {
    super({
      key: "ForTestScene",
    });
  }

  preload() {}

  create() {
    //const tags = this.anims.createFromAseprite("goblin_monika_aseprite");
    //console.log(tags);
    //var div = document.getElementById("luminus-rpg");
    //div.style.backgroundColor = "#4488AA";
    const sprite = this.add
      .sprite(500, 300)
      .play({ key: "minotaur-walk-down", repeat: -1 })
      .setScale(6);
  }

  update() {}
}
