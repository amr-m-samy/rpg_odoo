# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import os


class InfoBox(models.Model):
    _name = "info.box"
    _description = "Info Box"

    _single_record = models.Constraint(
        [
            ("_check_single_record", "unique record"),
        ],
        "Only one configuration record is allowed!",
    )

    name = fields.Char(default="Info Box", readonly=True)
    active = fields.Boolean(default=True, tracking=100)
    background_asset_id = fields.Many2one(
        "game.assets.manager", string="Background Asset"
    )
    background_texture_name = fields.Char(
        related="background_asset_id.name_key",
        string="Background Texture Name",
        store=True,
    )
    background_texture_image = fields.Binary(
        related="background_asset_id.file", string="Background Texture Image"
    )
    title_text_font_size = fields.Integer("Title Text Font Size", default=10)
    title_text_font_family = fields.Char(
        "Title Text Font Family", default="Press Start 2P"
    )
    nine_slice_offset = fields.Integer("Nine Slice Offset", default=10)

    def info_box_config_code_generator(self):
        """Generate a unique code for the info box configuration"""

        """
        sample code:
            export const infoBoxConfig = {
                InfoBox: {
                    backgroundTexture: "info_box",
                    titleTextFontSize: 10,
                    titleFontFamily: "'Press Start 2P'",
                    nineSliceOffset: 10,
                  },
                };
        """
        self = self.search([])[0]
        info_box_config_code = "export const infoBoxConfig = {" + "\n"
        info_box_config_code += "InfoBox: {" + "\n"
        info_box_config_code += (
            f"backgroundTexture: '{self.background_texture_name}'," + "\n"
        )
        info_box_config_code += (
            f"titleTextFontSize: {self.title_text_font_size}," + "\n"
        )
        info_box_config_code += (
            f"titleFontFamily: '{self.title_text_font_family}'," + "\n"
        )
        info_box_config_code += f"nineSliceOffset: {self.nine_slice_offset}," + "\n"
        info_box_config_code += "}," + "\n"
        info_box_config_code += "};" + "\n"
        utils_model = self.env["rpg.game.utils"]
        info_box_config_file_path = utils_model.get_rpg_game_src_directory(
            "consts/InfoBoxConfig.js"
        )

        with open(info_box_config_file_path, "w", encoding="utf-8") as f:
            f.write(info_box_config_code)
        return info_box_config_code

    @api.model
    def create(self, vals):
        """Prevents creating multiple configuration records"""
        if self.search([]):
            raise ValidationError("Only one configuration record is allowed!")
        self.info_box_config_code_generator()
        res = super(InfoBox, self).create(vals)
        return res

    @api.model
    def write(self, vals):
        res = super(InfoBox, self).write(vals)
        """Generate the info box configuration code"""
        self.info_box_config_code_generator()
        return res

    def unlink(self):
        res = super(InfoBox, self).unlink()
        """Generate the info box configuration code"""
        self.info_box_config_code_generator()
        return res


class PanelComponent(models.Model):
    _name = "panel.component"
    _description = "Panel Component"

    name = fields.Char(string="Panel Name", help="Name of the panel")

    active = fields.Boolean(default=True, tracking=100)
    background_asset_id = fields.Many2one(
        "game.assets.manager", string="Background Asset"
    )
    background_texture_name = fields.Char(
        related="background_asset_id.name_key",
        string="Background Texture Name",
        store=True,
    )

    background_texture_image = fields.Binary(
        related="background_asset_id.file", string="Background Texture Image"
    )
    title_text_font_size = fields.Integer("Title Text Font Size", default=13)
    title_text_font_family = fields.Char(
        "Title Text Font Family", default="Press Start 2P"
    )
    nine_slice_offset = fields.Integer("Nine Slice Offset", default=10)
    vertical_background_padding = fields.Integer(
        "Vertical Background Padding", default=25
    )
    background_main_content_padding_top = fields.Integer(
        "Background Main Content Padding Top", default=100
    )

    panel_title_texture_id = fields.Many2one(
        "game.assets.manager", string="Panel Title Asset"
    )
    panel_title_texture_name = fields.Char(
        related="panel_title_texture_id.name_key",
        string="Panel Title Texture Name",
        store=True,
    )
    panel_title_texture_image = fields.Binary(
        related="panel_title_texture_id.file", string="Title Texture Image"
    )
    panel_close_texture_id = fields.Many2one(
        "game.assets.manager", string="Close Btn Asset"
    )
    panel_close_texture_name = fields.Char(
        related="panel_close_texture_id.name_key",
        string="Close Btn Texture Name",
        store=True,
    )
    panel_close_texture_image = fields.Binary(
        related="panel_close_texture_id.file", string="Close Btn Texture Image"
    )
    # restrict the panel name to be chars and numbers only
    panel_name = fields.Char("Panel Name", default="Inventory")
    panel_max_width = fields.Integer("Panel Max Width", default=512)
    panel_max_height = fields.Integer("Panel Max Height", default=512)
    panel_screen_margin = fields.Integer("Panel Screen Margin", default=30)

    @api.onchange("panel_name")
    def _onchange_panel_name(self):
        if self.panel_name:
            if not self.panel_name.isalnum():
                raise ValidationError(
                    _("Panel Name should contain only characters and numbers.")
                )

    def _panel_config_code_generator(self):
        """Generate a unique code for the panel configuration"""

        """
        sample code:
            
            export const panelConfig = {
                InventoryPanel: {
                    backgroundTexture: "panel_background",
                    panelTitleTexture: "panel_title",
                    panelCloseTexture: "close_button",
                    panelName: "Inventory",
                    backgroundMainContentPaddingTop: 100,
                    verticalBackgroundPadding: 25,
                    titleTextFontSize: 13,
                    panelMaxWidth: 512,
                    panelMaxHeight: 512,
                    panelScreenMargin: 30,
                    titleFontFamily: "'Press Start 2P'",
                    titleTextFontSize: 13,
                    nineSliceOffset: 10,
                  },

                };
        """
        panel_config_code = "export const panelsConfig = {" + "\n"
        for panel in self.search([]):
            panel_config_code += f"{panel.panel_name}Panel: {{" + "\n"
            panel_config_code += (
                f"backgroundTexture: '{panel.background_texture_name}'," + "\n"
            )
            panel_config_code += (
                f"panelTitleTexture: '{panel.panel_title_texture_name}'," + "\n"
            )
            panel_config_code += (
                f"panelCloseTexture: '{panel.panel_close_texture_name}'," + "\n"
            )
            panel_config_code += f"panelName: '{panel.panel_name}'," + "\n"
            panel_config_code += (
                f"backgroundMainContentPaddingTop: {panel.background_main_content_padding_top},"
                + "\n"
            )
            panel_config_code += (
                f"verticalBackgroundPadding: {panel.vertical_background_padding},"
                + "\n"
            )
            panel_config_code += (
                f"titleTextFontSize: {panel.title_text_font_size}," + "\n"
            )
            panel_config_code += f"panelMaxWidth: {panel.panel_max_width}," + "\n"
            panel_config_code += f"panelMaxHeight: {panel.panel_max_height}," + "\n"
            panel_config_code += (
                f"panelScreenMargin: {panel.panel_screen_margin}," + "\n"
            )
            panel_config_code += (
                f"titleFontFamily: '{panel.title_text_font_family}'," + "\n"
            )
            panel_config_code += f"nineSliceOffset: {panel.nine_slice_offset}," + "\n"
            panel_config_code += "}," + "\n"
        panel_config_code += "};" + "\n"
        utils_model = self.env["rpg.game.utils"]
        rpg_game_src = utils_model.get_rpg_game_src_directory()
        panel_config_file_path = os.path.join(rpg_game_src, "consts/PanelsConfig.js")

        with open(panel_config_file_path, "w", encoding="utf-8") as f:
            f.write(panel_config_code)
        return panel_config_code

    @api.model
    def create(self, vals):
        res = super(PanelComponent, self).create(vals)
        """Generate the panel configuration code"""
        self._panel_config_code_generator()
        return res

    @api.model
    def write(self, vals):
        res = super(PanelComponent, self).write(vals)
        """Generate the panel configuration code"""
        self._panel_config_code_generator()
        return res

    def unlink(self):
        res = super(PanelComponent, self).unlink()
        """Generate the panel configuration code"""
        self._panel_config_code_generator()
        return res


class AssignPanelComponent(models.Model):
    _name = "assign.panel.component"
    _description = "Assign Panel Component"

    name = fields.Char(string="Assign Panel Component", required=True)
    panel_id = fields.Many2one("panel.component", string="Panel", required=True)
    panel_name = fields.Char(
        related="panel_id.panel_name", string="Panel Name", store=True
    )

    def assign_panel_code_generator(self):
        """Generate a unique code for the assign panel configuration"""

        """
        sample code:
        import { panelsConfig } from "./PanelsConfig";

        export const assignPanelConfig = {
            AttributeScene: panelsConfig["InventoryPanel"],
            SettingScene: panelsConfig["InventoryPanel"],
            InventoryScene: panelsConfig["InventoryPanel"],
            MainMenuScene: panelsConfig["InventoryPanel"],
        };
        """
        assign_panel_code = "import { panelsConfig } from './PanelsConfig';" + "\n\n"
        assign_panel_code += "export const assignPanelConfig = {" + "\n"
        for assign_panel in self.search([]):
            assign_panel_code += (
                f"  {assign_panel.name}: panelsConfig['{assign_panel.panel_name}Panel'],"
                + "\n"
            )
        assign_panel_code += "};" + "\n"
        utils_model = self.env["rpg.game.utils"]
        rpg_game_src = utils_model.get_rpg_game_src_directory()
        assign_panel_config_file_path = os.path.join(
            rpg_game_src, "consts/AssignPanelConfig.js"
        )

        with open(assign_panel_config_file_path, "w", encoding="utf-8") as f:
            f.write(assign_panel_code)
        return assign_panel_code

    @api.model
    def create(self, vals):
        res = super(AssignPanelComponent, self).create(vals)
        """Generate the assign panel configuration code"""
        self.assign_panel_code_generator()
        return res

    @api.model
    def write(self, vals):
        res = super(AssignPanelComponent, self).write(vals)
        """Generate the assign panel configuration code"""
        self.assign_panel_code_generator()
        return res

    def unlink(self):
        res = super(AssignPanelComponent, self).unlink()
        """Generate the assign panel configuration code"""
        self.assign_panel_code_generator()
        return res
