# -*- coding: utf-8 -*-

import os
from odoo import models


class RpgGameUtils(models.AbstractModel):

    _name = "rpg.game.utils"
    _description = "RPG Game Utils"

    def get_rpg_game_src_directory(self, path=None):
        this_directory = os.path.dirname(os.path.abspath(__file__))
        module_directory = os.path.dirname(this_directory)
        src_directory = os.path.join(module_directory, "static/src/rpg-game/src/")
        if not os.path.exists(src_directory):
            raise Exception(f"Assets directory not found: {src_directory}")
        if path:
            src_directory = os.path.join(src_directory, path)
        return src_directory
