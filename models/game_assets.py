# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
import json
import base64
import os


class AtlasConfig(models.Model):
    _name = "game.atlas.config"
    _description = "Model for Atlas Config"
    _rec_name = "key"

    name = fields.Char(string="Atlas name", required=True)
    key = fields.Char(string="key", required=True)
    frame_rate = fields.Integer(string="Frame Rate", default=8, required=True)
    prefix = fields.Char(string="Prefix", required=True)
    start = fields.Integer(string="Start", default=0, required=True)
    end = fields.Integer(string="End", default=0, required=True)
    zero_pad = fields.Integer(string="Zero Pad", required=True)
    repeat = fields.Integer(string="Repeat", default=-1, required=True)
    game_asset = fields.Many2one("game.assets.manager", string="Game Asset")

    _key_unique = models.Constraint(
        "UNIQUE(key)",
        "A key must be unique!",
    )


class GameAsset(models.Model):
    _name = "game.assets.manager"
    _description = "Model for Game Assets"
    _rec_name = "name_key"

    name_key = fields.Char(string="Name", required=True)
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
    atlas_config_ids = fields.One2many(
        "game.atlas.config", "game_asset", string="Atlas"
    )

    _name_key_unique = models.Constraint(
        "UNIQUE(name_key)",
        "A name must be unique!",
    )

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

    def _get_assets_directory(self):
        this_directory = os.path.dirname(os.path.abspath(__file__))
        module_directory = os.path.dirname(this_directory)
        assets_directory = os.path.join(
            module_directory, "static/src/rpg-game/src/assets/"
        )
        if not os.path.exists(assets_directory):
            raise Exception(f"Assets directory not found: {assets_directory}")
        return assets_directory

    def _add_asset(self):
        """
        Add a new asset to the assets folder.
        """
        for record in self:
            assets_directory = self._get_assets_directory()
            file_path = ""
            json_file_path = ""
            if record.file_path:
                file_path = os.path.join(assets_directory, str(record.file_path))
            if record.json_file_path:
                json_file_path = os.path.join(
                    assets_directory, str(record.json_file_path)
                )
            if file_path and record.file:
                with open(file_path, "wb") as f:
                    file_data = base64.b64decode(record.file)
                    f.write(file_data)
            if json_file_path and record.json_file:
                json_data = base64.b64decode(record.json_file).decode(
                    "utf-8"
                )  # Decode from base64 and convert to string
                json_obj = json.loads(json_data)  # Parse JSON to validate it
                with open(json_file_path, "w", encoding="utf-8") as f:
                    json.dump(json_obj, f, indent=4)  # Save it as a readable JSON file

    def _remove_asset(self):
        """
        Remove an asset from the assets folder.
        """
        for record in self:
            assets_directory = self._get_assets_directory()

            file_path = ""
            json_file_path = ""
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

    def create_atlas_config_records(self):
        """
        Create atlas config  records from the atlas json files.
        """
        self.env["game.atlas.config"].search([]).unlink()
        collect_frames_keys = []
        organized_frames = self._organize_atlas_json_frames()
        for key, value in organized_frames.items():
            for frame_name, numbers in value.items():
                if len(numbers) > 0 and numbers != [""]:
                    prefix = frame_name
                    start = int(numbers[0])
                    end = int(numbers[-1])
                    zero_pad = len(numbers[-1])
                    repeat = -1

                    self.env["game.atlas.config"].create(
                        {
                            "name": key,
                            "key": frame_name.replace("/", "-")[:-1],
                            "frame_rate": 8,
                            "prefix": prefix,
                            "start": start,
                            "end": end,
                            "zero_pad": zero_pad,
                            "repeat": repeat,
                            "game_asset": self.env["game.assets.manager"]
                            .search([("name_key", "=", key)])
                            .id,
                        }
                    )
        return collect_frames_keys

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
                import_name = f"tile_{name}"

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

        const_directory = self._get_assets_directory().replace("/assets/", "/consts/")
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
        records._add_asset()
        records.generate_game_assets_import_and_export()
        return records

    def write(self, vals):
        self._remove_asset()
        res = super(GameAsset, self).write(vals)
        # self.create_atlas_config_records()
        self._add_asset()
        self.generate_game_assets_import_and_export()
        return res

    def unlink(self):
        for record in self:
            record._remove_asset()

        self.generate_game_assets_import_and_export()
        return super(GameAsset, self).unlink()
