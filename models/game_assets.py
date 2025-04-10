# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
import json
import base64
import os
import shutil

from odoo.exceptions import ValidationError


class AtlasConfig(models.Model):
    _name = "game.atlas.config"
    _description = "Model for Atlas Config"
    _rec_name = "key"

    name = fields.Char(string="Atlas name", required=True)
    active = fields.Boolean(string="Active", default=True)
    key = fields.Char(string="key", required=True)
    frame_rate = fields.Integer(string="Frame Rate", default=8, required=True)
    prefix = fields.Char(string="Prefix", required=True)
    start = fields.Integer(string="Start", default=0, required=True)
    end = fields.Integer(string="End", default=0, required=True)
    zero_pad = fields.Integer(string="Zero Pad", required=True)
    repeat = fields.Integer(string="Repeat", default=-1, required=True)
    game_asset_id = fields.Many2one(
        "game.assets.manager", string="Game Asset", ondelete="cascade"
    )

    _key_unique = models.Constraint(
        "UNIQUE(key)",
        "A key must be unique!",
    )


class DropConfig(models.Model):
    _name = "game.drop.config"
    _description = "Model for Drop Config"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    asset_id = fields.Many2one(
        "game.assets.manager",
        string="Asset",
        required=True,
        readonly=True,
        ondelete="cascade",
    )
    item_id = fields.Many2one("game.items", string="Item", required=True)
    chance = fields.Integer(string="Chance", required=True)

    def create(self, vals):
        for val in vals:
            val["name"] = (
                self.env["game.assets.manager"]
                .browse(val["asset_id"])
                .name_key.capitalize()
                + " - "
                + self.env["game.items"].browse(val["item_id"]).name
                + " - "
                + "Drop"
            )
        res = super(DropConfig, self).create(vals)
        return res

    def write(self, vals):
        if vals.get("item_id"):
            self.name = (
                self.asset_id.name_key.capitalize()
                + " - "
                + self.env["game.items"].browse(vals["item_id"]).name
                + " - "
                + "Drop"
            )

        res = super(DropConfig, self).write(vals)
        return res


class GameAsset(models.Model):
    _name = "game.assets.manager"
    _description = "Model for Game Assets"
    _rec_name = "name_key"

    name_key = fields.Char(string="Name", required=True)
    # id = fields.Integer(
    #     string="Asset ID",
    #     readonly=True,
    #     help="ID of the entity the set on the tiled map",
    # )
    active = fields.Boolean(string="Active", default=True)
    asset_type = fields.Selection(
        [
            ("image", "Image"),
            ("audio", "Audio"),
            ("atlasconfig", "Atlas Config"),
            ("asepriteconfig", "Aseprite Config"),
            ("tilemapconfig", "Tilemap Config"),
        ],
        default="image",
        string="File Type",
        required=True,
    )
    animation_type = fields.Selection(
        [
            ("player", "Player"),
            ("enemy", "Enemy"),
            ("friend", "Friend"),
            ("misc", "Misc"),
        ],
        string="Animation Type",
    )
    file_path = fields.Char(
        string="File Path",
        default="",
        description="Relative path to the file in the assets folder with the file name and extension included (e.g. 'images/characters/hero.png'). File may be an image or audio file. note: don't start with a '/'",
    )
    json_file_path = fields.Char(
        string="JSON File Path",
        default="",
        description="Relative path to the JSON file in the assets folder with the file name and extension included (e.g. 'images/characters/hero.json'). File must be a JSON file. note: don't start with a '/'",
    )  # For atlas and aseprite
    file = fields.Binary(string="File")
    json_file = fields.Binary(string="JSON File")
    tiled_source = fields.Binary(
        string="Tiled Source",
        help="Tiled source for future updates. It is a tsx or tmx file.",
    )
    atlas_config_ids = fields.One2many(
        "game.atlas.config", "game_asset_id", string="Atlas"
    )
    # # Entity Config Fields
    # entity_config_id = fields.Integer(
    #     string="ID", help="ID of the entity the set on the tiled map"
    # )
    base_health = fields.Integer(string="Base Health", default=10)
    attack = fields.Integer(string="Attack", default=1)
    defense = fields.Integer(string="Defense", default=1)
    speed = fields.Integer(string="Speed", default=20)
    flee = fields.Float(string="Flee", default=0)
    hit = fields.Integer(string="Hit", default=3)
    exp = fields.Integer(string="Exp", default=50)
    health_bar_offset_x = fields.Integer(string="Health Bar Offset X")
    health_bar_offset_y = fields.Integer(string="Health Bar Offset Y")
    scale = fields.Float(string="Scale", default=1.0)
    drops_ids = fields.One2many("game.drop.config", "asset_id", string="Drops")

    _name_key_unique = models.Constraint(
        "UNIQUE(name_key)",
        "A name must be unique!",
    )

    # _entity_config_id_unique = models.Constraint(
    #     "UNIQUE(entity_config_id)",
    #     "A entity_config_id must be unique!",
    # )

    def upload_binary_to_file_field(self):
        """
        upload binary data to the file field.
        """
        assets_path = self.env["rpg.game.utils"].get_rpg_game_src_directory("assets/")
        all_assets = self.env["game.assets.manager"].search([])
        for record in all_assets:
            if record.file_path:
                file_path = os.path.join(assets_path, record.file_path)
                with open(file_path, "rb") as f:
                    record.file = base64.b64encode(f.read())
            if record.json_file_path:
                json_file_path = os.path.join(assets_path, record.json_file_path)
                with open(json_file_path, "rb") as f:
                    record.json_file = base64.b64encode(f.read())

    def _remove_characters_from_aesprite_json_filename(self, jsonObj):
        """
        Remove the character from the aseprite json filename.
        """
        for frame in jsonObj["frames"]:
            if type(frame) != str:
                frame["filename"] = "".join(filter(str.isdigit, frame["filename"]))
        return jsonObj

    def _add_asset_json_file(self):
        """
        Add a new asset to the assets folder.
        """
        for record in self:
            if record.json_file:
                assets_directory = self.env[
                    "rpg.game.utils"
                ].get_rpg_game_src_directory("assets/")
                json_file_path = os.path.join(
                    assets_directory, str(record.json_file_path)
                )
                json_data = base64.b64decode(record.json_file).decode(
                    "utf-8"
                )  # Decode from base64 and convert to string
                json_obj = json.loads(json_data)  # Parse JSON to validate it
                if record.asset_type == "asepriteconfig":
                    json_obj = self._remove_characters_from_aesprite_json_filename(
                        json_obj
                    )
                with open(json_file_path, "w", encoding="utf-8") as f:
                    json.dump(json_obj, f, indent=4)  # Save it as a readable JSON file

    def _add_asset_file(self):
        """
        Add a new asset to the assets folder.
        """
        for record in self:
            if record.file and record.file_path:
                assets_directory = self.env[
                    "rpg.game.utils"
                ].get_rpg_game_src_directory("assets/")
                file_path = os.path.join(assets_directory, str(record.file_path))
                with open(file_path, "wb") as f:
                    file_data = base64.b64decode(record.file)
                    f.write(file_data)

    def _add_asset_tileset_config(self):
        """
        Add a new asset to the assets folder.
        """
        for record in self:
            if record.tiled_source:
                maps_directory = self.env["rpg.game.utils"].get_rpg_game_src_directory(
                    f"assets/maps/{record.name_key}/"
                )
                try:
                    os.makedirs(maps_directory)
                    print("Directory created successfully")
                    if record.tiled_source:
                        with open(
                            os.path.join(maps_directory, f"{record.name_key}.tsx"),
                            "wb",
                        ) as f:
                            tiled_data = base64.b64decode(record.tiled_source)
                            f.write(tiled_data)
                    if record.json_file:
                        with open(
                            os.path.join(maps_directory, f"{record.name_key}.json"),
                            "wb",
                        ) as f:
                            json_data = base64.b64decode(record.json_file)
                            f.write(json_data)
                except FileExistsError:
                    print("Directory already exists")

    # def _add_asset(self, file_type="new"):
    #     """
    #     Add a new asset to the assets folder.
    #     """
    #     for record in self:
    #         assets_directory = self.env["rpg.game.utils"].get_rpg_game_src_directory(
    #             "assets/"
    #         )
    #         file_path = ""
    #         json_file_path = ""
    #         if record.file_path:
    #             file_path = os.path.join(assets_directory, str(record.file_path))
    #         if record.json_file_path:
    #             json_file_path = os.path.join(
    #                 assets_directory, str(record.json_file_path)
    #             )
    #         if file_path and record.file and file_type in ["file", "new", "update"]:
    #             with open(file_path, "wb") as f:
    #                 file_data = base64.b64decode(record.file)
    #                 f.write(file_data)
    #         if (
    #             json_file_path
    #             and record.json_file
    #             and file_type in ["json_file", "new"]
    #             and record.asset_type != "tilemapconfig"
    #         ):
    #             json_data = base64.b64decode(record.json_file).decode(
    #                 "utf-8"
    #             )  # Decode from base64 and convert to string
    #             json_obj = json.loads(json_data)  # Parse JSON to validate it
    #             if record.asset_type == "asepriteconfig":
    #                 json_obj = self._remove_characters_from_aesprite_json_filename(
    #                     json_obj
    #                 )
    #             with open(json_file_path, "w", encoding="utf-8") as f:
    #                 json.dump(json_obj, f, indent=4)  # Save it as a readable JSON file
    #         if (
    #             record.json_file
    #             and file_type in ["json_file", "new"]
    #             and record.asset_type == "tilemapconfig"
    #         ):
    #
    #             maps_directory = self.env["rpg.game.utils"].get_rpg_game_src_directory(
    #                 f"assets/maps/{record.name_key}/"
    #             )
    #             try:
    #                 os.makedirs(maps_directory)
    #                 print("Directory created successfully")
    #                 if record.tiled_source:
    #                     with open(
    #                         os.path.join(maps_directory, f"{record.name_key}.tsx"),
    #                         "wb",
    #                     ) as f:
    #                         tiled_data = base64.b64decode(record.tiled_source)
    #                         f.write(tiled_data)
    #                 if record.json_file:
    #                     with open(
    #                         os.path.join(maps_directory, f"{record.name_key}.json"),
    #                         "wb",
    #                     ) as f:
    #                         json_data = base64.b64decode(record.json_file)
    #                         f.write(json_data)
    #
    #             except FileExistsError:
    #                 print("Directory already exists")

    def _remove_asset(self):
        """
        Remove an asset from the assets folder.
        """
        for record in self:
            assets_directory = self.env["rpg.game.utils"].get_rpg_game_src_directory(
                "assets/"
            )

            file_path = ""
            json_file_path = ""

            if record.asset_type == "tilemapconfig":
                maps_directory = self.env["rpg.game.utils"].get_rpg_game_src_directory(
                    f"assets/maps/{record.name_key}/"
                )
                if os.path.exists(maps_directory):
                    shutil.rmtree(maps_directory)

            if record.file_path:
                file_path = os.path.join(assets_directory, str(record.file_path))
            if record.json_file_path:
                json_file_path = os.path.join(
                    assets_directory, str(record.json_file_path)
                )

            if file_path and os.path.exists(file_path):
                os.remove(file_path)
            if json_file_path and os.path.exists(json_file_path):
                os.remove(json_file_path)

    def _remove_enemy_js_file(self, enemy_name):
        """
        Remove the javascript file.
        """
        assets_path = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            f"consts/enemies/{enemy_name}.js"
        )
        if os.path.exists(assets_path):
            os.remove(assets_path)
            logging.info(f"File {assets_path} removed successfully.")
        else:
            logging.warning(f"File {assets_path} does not exist.")

    def _atlas_json_frame_collector(self):
        """
        Collect all the frames from the atlas json files.
        """
        atlas_frames = []
        assets = self.env["game.assets.manager"].search([])
        for asset in assets:
            if asset.asset_type == "atlasconfig":
                name = asset.name_key
                json_data = base64.b64decode(asset.json_file).decode("utf-8")
                json_obj = json.loads(json_data)
                frames = json_obj.get("frames")
                textures = json_obj.get("textures")
                if frames:  # For the case of the texture packer images
                    atlas_frames.append(
                        {
                            "name": name,
                            "frames_name": [frame for frame in frames.keys()],
                        }
                    )
                if textures:  # For the case of the texture packer folder
                    atlas_frames.append(
                        {
                            "name": name,
                            "frames_name": [
                                frame["filename"] for frame in textures[0].get("frames")
                            ],
                        }
                    )
        return atlas_frames

    def _split_number_from_end(self, string):
        """
        Split the number from the end of the string.
        """
        number = ""
        for char in string[::-1]:
            if char.isdigit():
                number += char
            else:
                break
        return number[::-1]

    def _remove_file_name(self, string):
        """
        Remove the file name from the string.
        """
        return string.rsplit("/", 1)[0]

    def _organize_atlas_json_frames(self):
        """
        Organize the atlas json frames in a dictionary.
        """
        atlas_frames = self._atlas_json_frame_collector()
        organized_frames = {}
        for atlas_frame in atlas_frames:
            name = atlas_frame["name"]
            frames_name = atlas_frame["frames_name"]
            organized_frames[name] = {}
            for frame_name in frames_name:
                number = self._split_number_from_end(frame_name)

                if number:
                    frame_name = frame_name.replace(number, "")
                if frame_name not in organized_frames[name]:
                    organized_frames[name][frame_name] = []
                organized_frames[name][frame_name].append(number)

        for key, value in organized_frames.items():
            for frame_name, numbers in value.items():
                numbers = [number for number in numbers]
                numbers.sort()
                organized_frames[key][frame_name] = numbers

        return organized_frames

    def _caculate_atlas_frame_rate(self, numbers):
        """
        Calculate the frame rate for the atlas config.
        """
        if numbers:
            if len(numbers) > 1:
                return len(numbers)
        return 0

    def _calculate_repeat(self, numbers, key):
        """
        Calculate the repeat for the atlas config.
        """
        is_atk = key.find("-atk-")
        if numbers:
            if len(numbers) > 1 and is_atk == -1:
                return -1
        return 0

    def create_atlas_config_records(self):
        """
        Create atlas config records from the atlas json files.
        """
        self.env["game.atlas.config"].search([]).unlink()
        collect_frames_keys = []
        organized_frames = self._organize_atlas_json_frames()
        for key, value in organized_frames.items():
            for frame_name, numbers in value.items():
                if len(numbers) > 0 and numbers != [""]:
                    frame_name_without_filename = ""
                    if frame_name[-1] != "/":
                        frame_name_without_filename = self._remove_file_name(frame_name)
                    else:
                        frame_name_without_filename = frame_name[:-1]
                    prefix = frame_name
                    start = int(numbers[0])
                    end = int(numbers[-1])
                    zero_pad = len(numbers[-1])
                    frame_key = frame_name_without_filename.replace("/", "-")
                    repeat = self._calculate_repeat(numbers, frame_key)

                    self.env["game.atlas.config"].create(
                        {
                            "name": key,
                            "key": frame_key,
                            "frame_rate": self._caculate_atlas_frame_rate(numbers),
                            "prefix": prefix,
                            "start": start,
                            "end": end,
                            "zero_pad": zero_pad,
                            "repeat": repeat,
                            "game_asset_id": self.env["game.assets.manager"]
                            .search([("name_key", "=", key)])
                            .id,
                        }
                    )
        return collect_frames_keys

    def _save_enemy_atla_and_aseprite_config_to_file(self, enemy_name, code):
        """
        Save the enemy atlas config code to a file.
        """
        assets_path = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            f"consts/enemies/{enemy_name}.js"
        )
        with open(assets_path, "w", encoding="utf-8") as f:
            f.write(code)

    def _generate_enemy_atlas_and_aseprite_config_code(self):
        """
        Generate the atlas config javascript file.

        import { EntityDrops } from "../../models/EntityDrops";

        export const Bat = [
          // Down
          {
            atlas: "bat",
            key: "bat-idle-down",
            frameRate: 8,
            prefix: "bat/idle-down/",
            start: 0,
            end: 4,
            zeroPad: 2,
            repeat: -1,
          },
          {
            atlas: "bat",
            key: "bat-atk-down",
            frameRate: 5,
            prefix: "bat/atk-down/",
            start: 0,
            end: 4,
            zeroPad: 2,
            repeat: 0,
          },
        ];

        export const BatConfig = {
          id: 2,
          name: "Bat",
          texture: "bat",
          baseHealth: 10,
          atack: 7,
          defense: 1,
          speed: 30,
          flee: 3,
          hit: 5,
          exp: 50,
          hit: 5,
          healthBarOffsetX: -6,
          healthBarOffsetY: 16,
          drops: [
            new EntityDrops(
              1, // Red Potion
              50, // 50% chance of dropping the item
            ),
          ],
        };
        """

        enimy_animation_type_ids = self.env["game.assets.manager"].search(
            [("animation_type", "in", ["enemy"])]
        )
        all_enemies_atlas_configs_code = []
        atlas_config_code = ""
        for atlas_config in enimy_animation_type_ids:
            atlas_config_code = (
                "import { EntityDrops } from '../../models/EntityDrops';\n\n"
            )
            if atlas_config.asset_type == "atlasconfig":
                atlas_config_code += (
                    f"export const {atlas_config.name_key.capitalize()} = [\n"
                )
                for atlas in atlas_config.atlas_config_ids:
                    atlas_config_code += (
                        f"  {{\n"
                        f'    atlas: "{atlas.name}",\n'
                        f'    key: "{atlas.key}",\n'
                        f"    frameRate: {atlas.frame_rate},\n"
                        f'    prefix: "{atlas.prefix}",\n'
                        f"    start: {atlas.start},\n"
                        f"    end: {atlas.end},\n"
                        f"    zeroPad: {atlas.zero_pad},\n"
                        f"    repeat: {atlas.repeat},\n"
                        f"  }},\n"
                    )
                atlas_config_code += "];\n\n"

            if atlas_config.animation_type == "enemy":
                atlas_config_code += (
                    f"export const {atlas_config.name_key.capitalize()}Config = {{\n"
                    f"  id: {atlas_config.id},\n"
                    f'  name: "{atlas_config.name_key.capitalize()}",\n'
                    f'  texture: "{atlas_config.name_key}",\n'
                    f"  baseHealth: {atlas_config.base_health},\n"
                    f"  atack: {atlas_config.attack},\n"  # atack -> attack with one 't'
                    f"  defense: {atlas_config.defense},\n"
                    f"  speed: {atlas_config.speed},\n"
                    f"  flee: {atlas_config.flee},\n"
                    f"  hit: {atlas_config.hit},\n"
                    f"  exp: {atlas_config.exp},\n"
                    f"  healthBarOffsetX: {atlas_config.health_bar_offset_x},\n"
                    f"  healthBarOffsetY: {atlas_config.health_bar_offset_y},\n"
                    f"  scale: {atlas_config.scale},\n"
                    f"  drops: [\n"
                )
                for drop in atlas_config.drops_ids:
                    atlas_config_code += (
                        f"    new EntityDrops(\n"
                        f"      {drop.item_id.id},\n"
                        f"      {drop.chance},\n"
                        f"    ),\n"
                    )
                atlas_config_code += "  ],\n};\n\n"
            all_enemies_atlas_configs_code.append(atlas_config_code)

            self._save_enemy_atla_and_aseprite_config_to_file(
                atlas_config.name_key, atlas_config_code
            )
            atlas_config_code = ""

        self._generate_enemies_seed_config_code()
        self._generate_misc_atlas_config_code()
        self._generate_Animation_code()
        return atlas_config_code

    def _generate_misc_atlas_config_code(self):
        """
        Generate the atlas config javascript file for the misc atlas.
        """
        atlas_configs_asset_ids = (
            self.env["game.atlas.config"]
            .search([("game_asset_id.animation_type", "=", "misc")])
            .game_asset_id
        )

        atlas_config_code = "export const Misc = [\n"
        for atlas_config in atlas_configs_asset_ids:

            for atlas in atlas_config.atlas_config_ids:
                atlas_config_code += f"// -------------- {atlas.name} --------------\n"
                atlas_config_code += (
                    f"  {{\n"
                    f'    atlas: "{atlas.name}",\n'
                    f'    key: "{atlas.key}",\n'
                    f"    frameRate: {atlas.frame_rate},\n"
                    f'    prefix: "{atlas.prefix}",\n'
                    f"    start: {atlas.start},\n"
                    f"    end: {atlas.end},\n"
                    f"    zeroPad: {atlas.zero_pad},\n"
                    f"    repeat: {atlas.repeat},\n"
                    f"  }},\n"
                )
        atlas_config_code += "];\n\n"
        self._save_misc_atla_config_to_file(atlas_config_code)
        return atlas_config_code

    def generate_player_config_code(self):
        """
        Generate the player config javascript file.

        export const PlayerConfig = {
          texture: "minotaur",
          variableName: "player",
          scale: 1.0,
        };
        """
        player_config_code = (
            "export const PlayerConfig = {\n"
            f"  texture: '{self.name_key}',\n"
            '  variableName: "player",\n'
            f"  scale: {self.scale},\n"
            "};\n"
        )
        assets_path = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            "consts/player/PlayerConfig.js"
        )
        with open(assets_path, "w", encoding="utf-8") as f:
            f.write(player_config_code)
        return player_config_code

    def _generate_Animation_code(self):
        """
                Generate the Animation javascript file.
        import { Bat } from "./enemies/bat";
        import { Ogre } from "./enemies/ogre";
        import { Rat } from "./enemies/rat";
        import { Player } from "./player/Player";
        import { PlayerConfig } from "./player/PlayerConfig";
        import { Misc } from "./misc/Misc";

        export const Animations = [
          ...Bat,
          ...Rat,
          ...Ogre,
          // ...Player[PlayerConfig.texture],
          ...Misc,
        ];
        """
        atlas_enemy_configs_asset_ids = (
            self.env["game.atlas.config"]
            .search([("game_asset_id.animation_type", "=", "enemy")])
            .game_asset_id
        )

        animation_code = ""
        # animation_code = 'import { Player } from "./player/Player";\n'
        # animation_code += 'import { PlayerConfig } from "./player/PlayerConfig"\n'
        animation_code += 'import { Misc } from "./misc/Misc";'
        for atlas_config in atlas_enemy_configs_asset_ids:
            animation_code += f'import {{ {atlas_config.name_key.capitalize()} }} from "./enemies/{atlas_config.name_key}";\n'
        animation_code += "export const Animations = [\n"
        # animation_code += "  ...Player[PlayerConfig.texture],\n"
        animation_code += "  ...Misc,\n"
        for atlas_config in atlas_enemy_configs_asset_ids:
            animation_code += f"  ...{atlas_config.name_key.capitalize()},\n"
        animation_code += "];\n"
        self._save_animation_to_file(animation_code)
        return animation_code

    def _save_misc_atla_config_to_file(self, code):
        """
        Save the misc atlas config code to a file.
        """
        assets_path = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            "consts/misc/Misc.js"
        )
        with open(assets_path, "w", encoding="utf-8") as f:
            f.write(code)

    def _save_enemies_seed_config_to_file(self, code):
        """
        Save the enemies seed config code to a file.
        """
        assets_path = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            "consts/enemies/EnemiesSeedConfig.js"
        )
        with open(assets_path, "w", encoding="utf-8") as f:
            f.write(code)

    def _save_animation_to_file(self, code):
        """
        Save the animation code to a file.
        """
        assets_path = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            "consts/Animations.js"
        )
        with open(assets_path, "w", encoding="utf-8") as f:
            f.write(code)

    def _generate_enemies_seed_config_code(self):
        """
        Generate the enemies seed config javascript file.

        example:

        import { BatConfig } from "./bat";
        import { OgreConfig } from "./ogre";
        import { RatConfig } from "./rat";
        export const EnemiesSeedConfig = [
          RatConfig,
          BatConfig,
          OgreConfig,
        ];
        """
        # atlas_configs_asset_ids = (
        #     self.env["game.atlas.config"]
        #     .search([("game_asset_id.animation_type", "=", "enemy")])
        #     .game_asset_id
        # )
        enimy_and_friend_animation_type_ids = self.env["game.assets.manager"].search(
            [("animation_type", "in", ["enemy", "friend"])]
        )
        enemies_seed_config_code = ""
        for atlas_config in enimy_and_friend_animation_type_ids:
            enemies_seed_config_code += f'import {{ {atlas_config.name_key.capitalize()}Config }} from "./{atlas_config.name_key}";\n'
        enemies_seed_config_code += "export const EnemiesSeedConfig = [\n"
        for atlas_config in enimy_and_friend_animation_type_ids:
            enemies_seed_config_code += (
                f"  {atlas_config.name_key.capitalize()}Config,\n"
            )
        enemies_seed_config_code += "];\n"

        self._save_enemies_seed_config_to_file(enemies_seed_config_code)
        return enemies_seed_config_code

    def generate_game_assets_import_and_export(self):
        """
        Generate the game assets javascript file from all record of game.assets.manager model  . import_statements and export_image, export_audio, export_atlas_config, export_asprite_config, export_tilemap_config
        example of import:
        import name_key from "../assets/file_path";
        import name_key_json from "../assets/json_file_path";
        import atlas_name_key_image from "../assets/file_path";
        import atlas_name_key_image_json from "../assets/json_file_path";

        example of export image:
        {
            name: "name_key",
            image: name_key,
        }
        example of export audio:
        {
            name: "name_key",
            audio: name_key,
        }
        example of export atlas:
        {
            name: "name_key",
            image: atlas_name_key_image,
            json: atlas_name_key_image_json,
        }
        example of export asprite:
        {
            name: "name_key",
            image: name_key,
            json: name_key_json,
        }
        example of export tilemap:
        {
            name: "name_key",
            json: name_key_json,
        }

        """
        import_statements = []
        export_image = []
        export_audio = []
        export_atlas_config = []
        export_asprite_config = []
        export_tilemap_config = []

        assets = self.env["game.assets.manager"].search([])
        for asset in assets:
            name = asset.name_key
            path = asset.file_path
            json_path = asset.json_file_path
            asset_type = asset.asset_type

            import_name = f"{name}"
            import_path = f"{path}"
            import_json_path = f"{json_path}"

            if asset_type == "tilemapconfig":
                import_name = f"tile_{name}_json"
                import_statements.append(
                    f'import {import_name} from "../assets/maps/{name}/{name}.json";'
                )

            if asset_type == "atlasconfig":
                import_name = f"atlas_{name}_image"

            if asset_type != "tilemapconfig":
                import_statements.append(
                    f'import {import_name} from "../assets/{import_path}";'
                )
            if json_path:
                import_statements.append(
                    f'import {import_name}_json from "../assets/{import_json_path}";'
                )

            if asset_type == "image":
                export_image.append(
                    {
                        "name": name,
                        "image": name,
                    }
                )
            elif asset_type == "audio":
                export_audio.append(
                    {
                        "name": name,
                        "audio": name,
                    }
                )
            elif asset_type == "atlasconfig":
                export_atlas_config.append(
                    {
                        "name": name,
                        "image": f"atlas_{name}_image",
                        "json": f"atlas_{name}_image_json",
                    }
                )
            elif asset_type == "asepriteconfig":
                export_asprite_config.append(
                    {
                        "name": name,
                        "image": f"{name}",
                        "json": f"{name}_json",
                    }
                )
            elif asset_type == "tilemapconfig":
                export_tilemap_config.append(
                    {
                        "name": name,
                        "json": f"tile_{name}_json",
                    }
                )

        import_statements = "\n".join(import_statements)
        export_image = json.dumps(export_image, indent=4)
        export_audio = json.dumps(export_audio, indent=4)
        export_atlas_config = json.dumps(export_atlas_config, indent=4)
        export_asprite_config = json.dumps(export_asprite_config, indent=4)
        export_tilemap_config = json.dumps(export_tilemap_config, indent=4)
        export_image_list = json.loads(export_image)

        export_image = (
            "[\n"
            + ",\n".join(
                [
                    f'    {{name: "{item["name"]}", image: {item["image"]}}}'
                    for item in export_image_list
                ]
            )
            + "\n];"
        )
        export_audio = (
            "[\n"
            + ",\n".join(
                [
                    f'    {{name: "{item["name"]}", audio: {item["audio"]}}}'
                    for item in json.loads(export_audio)
                ]
            )
            + "\n];"
        )
        export_atlas_config = (
            "[\n"
            + ",\n".join(
                [
                    f'    {{name: "{item["name"]}", image: {item["image"]}, json: {item["json"]}}}'
                    for item in json.loads(export_atlas_config)
                ]
            )
            + "\n];"
        )
        export_asprite_config = (
            "[\n"
            + ",\n".join(
                [
                    f'    {{name: "{item["name"]}", image: {item["image"]}, json: {item["json"]}}}'
                    for item in json.loads(export_asprite_config)
                ]
            )
            + "\n];"
        )
        export_tilemap_config = (
            "[\n"
            + ",\n".join(
                [
                    f'    {{name: "{item["name"]}", json: {item["json"]}}}'
                    for item in json.loads(export_tilemap_config)
                ]
            )
            + "\n];"
        )

        code = f"{import_statements}\n\nexport const Images = {export_image};\n\nexport const Audios = {export_audio};\n\nexport const AtlasConfig = {export_atlas_config};\n\nexport const ASEPRITE_CONFIG = {export_asprite_config};\n\nexport const TilemapConfig = {export_tilemap_config};"

        const_directory = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            "consts/"
        )
        file_path = os.path.join(const_directory, "GameAssets.js")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)
        return code

    # ---------------------------------------------------------
    # ORM Overrides
    # ---------------------------------------------------------

    @api.model_create_multi
    def create(self, vals_list):
        records = super(GameAsset, self).create(vals_list)
        for record in records:
            if record.json_file:
                record._add_asset_json_file()
            if record.file:
                record._add_asset_file()

            if records.asset_type == "tilemapconfig":
                record._add_asset_tileset_config()

        records._generate_enemy_atlas_and_aseprite_config_code()
        records.create_atlas_config_records()
        records.generate_game_assets_import_and_export()
        return records

    def write(self, vals):
        res = super(GameAsset, self).write(vals)
        if self.asset_type == "tilemapconfig":
            self._remove_asset()
            self._add_asset_tileset_config()
        elif vals.get("file"):
            self._add_asset_file()
        elif vals.get("json_file"):
            self._add_asset_json_file()

        if vals.get("animation_type"):
            raise ValidationError("You cannot change the animation type.")
        if vals.get("asset_type"):
            raise ValidationError("You cannot change the asset type.")

        self.generate_game_assets_import_and_export()
        return res

    def unlink(self):
        for record in self:
            record._remove_asset()
            record._remove_enemy_js_file(record.name_key)
        res = super(GameAsset, self).unlink()
        self._generate_enemies_seed_config_code()
        self._generate_Animation_code()
        self.generate_game_assets_import_and_export()
        return res
