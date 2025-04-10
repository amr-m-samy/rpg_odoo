# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RpgScene(models.Model):
    _name = "rpg.scene"
    _description = "RPG Scene"

    name = fields.Char(string="Scene Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    description = fields.Text(string="Description")
    zoom = fields.Float(string="Zoom", default=1.0)
    map_name = fields.Char(string="Map Name", required=True)
    is_sound = fields.Boolean(string="Is Sound", default=False)
    sound_id = fields.Many2one(
        "game.assets.manager", string="Sound", domain="[('asset_type','=','audio')]"
    )
    sound_volume = fields.Float(string="Sound Volume", default=1.0)
    sound_loop = fields.Boolean(string="Sound Loop", default=False)
    is_enemy_zone = fields.Boolean(string="Is Enemy Zone", default=False)
    tileset_image_config_ids = fields.Many2many(
        "tileset.image.config", string="Tileset Image Configs"
    )

    @api.constrains("sound_volume")
    def _check_sound_volume(self):
        for record in self:
            if record.sound_volume < 0.0 or record.sound_volume > 1.0:
                raise ValidationError("Sound volume must be between 0.0 and 1.0.")

    def _generate_scene_info_code(self):
        """Generate scene information js code.

        import { TilesetImageConfig } from "../models/TilesetImageConfig";

        export default function SceneInfo(sceneName) {
          const sceneInfo = {
            tutorial: {
              mapName: "tutorial",
              zoom: 5,
              isSound: true,
              volume: 0.1,
              isSoundLoop: true,
              soundAssetKey: "path_to_lake_land",
              isParticles: false,
              tileImages: [
                new TilesetImageConfig("tutorial_tileset_extruded", "tutorial_tileset"),
                new TilesetImageConfig("collision", "collision_tile"), // Add these lines to use the Collision tiles.
                new TilesetImageConfig("overworld", "tiles_overworld"), // Add these lines to use the Overworld Tileset.
                new TilesetImageConfig("inner", "inner"), // Add this for inner
              ],
              isEnemyZone: false,
            },
          };

          return sceneInfo[sceneName] || sceneInfo.mainscene;
        }
        """

        scenes = self.search([])
        scene_info_code = ""
        scene_info_code += (
            "import { TilesetImageConfig } from '../models/TilesetImageConfig';\n\n"
        )
        scene_info_code += "export default function SceneInfo(sceneName) {\n"
        scene_info_code += "  const sceneInfo = {\n"
        for scene in scenes:
            scene_info_code += f"    {scene.name}: {{\n"
            scene_info_code += f"      mapName: '{scene.map_name}',\n"
            scene_info_code += f"      zoom: {scene.zoom},\n"
            scene_info_code += f"      isSound: {str(scene.is_sound).lower()},\n"
            if scene.sound_id:
                scene_info_code += (
                    f"      soundAssetKey: '{scene.sound_id.name_key}',\n"
                )
                scene_info_code += f"      volume: {scene.sound_volume},\n"
                scene_info_code += (
                    f"      isSoundLoop: {str(scene.sound_loop).lower()},\n"
                )
            scene_info_code += "      tileImages: [\n"
            for tileset in scene.tileset_image_config_ids:
                if tileset.is_advanced:
                    scene_info_code += f"        new TilesetImageConfig('{tileset.name}', '{tileset.asset_id.name_key}', {tileset.width}, {tileset.height}, {tileset.margin}, {tileset.spacing}),\n"
                else:
                    scene_info_code += f"        new TilesetImageConfig('{tileset.name}', '{tileset.asset_id.name_key}'),\n"
            scene_info_code += "      ],\n"
            scene_info_code += (
                f"      isEnemyZone: {str(scene.is_enemy_zone).lower()},\n"
            )
            scene_info_code += "    },\n"

        scene_info_code += "  };\n"
        scene_info_code += "  return sceneInfo[sceneName] || sceneInfo.mainscene;\n"
        scene_info_code += "}\n"

        return scene_info_code

    def generate_scene_info_code_file(self):
        """Generate scene information js code and save it to a file."""
        scene_info_code = self._generate_scene_info_code()

        consts_path = self.env["rpg.game.utils"].get_rpg_game_src_directory(
            "consts/SceneInfo.js"
        )
        with open(consts_path, "w") as file:
            file.write(scene_info_code)

    @api.model
    def create(self, vals):
        # Custom logic before creating a scene
        res = super(RpgScene, self).create(vals)
        # Generate the scene info code and save it to a file
        res.generate_scene_info_code_file()
        return res

    def write(self, vals):
        # Custom logic before updating a scene
        res = super(RpgScene, self).write(vals)
        # Generate the scene info code and save it to a file
        self.generate_scene_info_code_file()
        return res


class TilesetImageConfig(models.Model):
    _name = "tileset.image.config"
    _description = "Tileset Image Config"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string="Active", default=True)
    asset_id = fields.Many2one(
        "game.assets.manager",
        string="Asset",
        domain="[('asset_type','=','image')]",
        required=True,
    )
    is_advanced = fields.Boolean(string="Is Advanced", default=False)
    width = fields.Integer(string="Width")
    height = fields.Integer(string="Height")
    margin = fields.Integer(string="Margin")
    spacing = fields.Integer(string="Spacing")
