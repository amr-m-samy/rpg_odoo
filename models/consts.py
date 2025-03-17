# -*- coding: utf-8 -*-
from odoo import models, fields, api


class BuffType(models.Model):
    _name = "buff.type"
    _description = "Buff Type"

    name = fields.Char(string="Name", required=True)
    buff_id = fields.Integer(string="ID", required=True)
    key = fields.Char(string="Key", required=True)

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "A name must be unique!",
    )
    _key_unique = models.Constraint(
        "UNIQUE(key)",
        "A key must be unique!",
    )
    _buff_id_unique = models.Constraint(
        "UNIQUE(buff_id)",
        "A buff_id must be unique!",
    )

    def buff_type_code_generator(self):
        """Generate a new buff type code"""
        """
        sample code:

            import { BuffType } from '../../models/BuffType';

            export const BUFF_TYPES = {     
                ATK01: new BuffType(1, 'Atack 01'),
                ATK02: new BuffType(2, 'Atack 02'),
            };
        """
        buff_types = self.search([])
        buff_types_code = "import { BuffType } from '../../models/BuffType';\n\n export const BUFF_TYPES = {\n"
        for buff_type in buff_types:
            buff_types_code += f"  {buff_type.key}: new BuffType({buff_type.buff_id}, '{buff_type.name}'),\n"
        buff_types_code += "};"

        utils_model = self.env["rpg.game.utils"]
        buff_type_const_path = utils_model.get_rpg_game_src_directory(
            "consts/DB_SEED/BuffTypes.js"
        )
        with open(buff_type_const_path, "w") as f:
            f.write(buff_types_code)

        return buff_types_code

    @api.model
    def create(self, vals):
        res = super(BuffType, self).create(vals)
        res.buff_type_code_generator()
        return res

    @api.model
    def write(self, vals):
        res = super(BuffType, self).write(vals)
        self.buff_type_code_generator()
        return res

    def unlink(self):
        res = super(BuffType, self).unlink()
        self.buff_type_code_generator()
        return res
