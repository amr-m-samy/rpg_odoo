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


class ItemTyps(models.Model):
    _name = "item.type"
    _description = "Item Type"

    name = fields.Char(string="Name", required=True)
    item_id = fields.Integer(string="ID", required=True)
    key = fields.Char(string="Key", required=True)

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "A name must be unique!",
    )
    _key_unique = models.Constraint(
        "UNIQUE(key)",
        "A key must be unique!",
    )
    _item_id_unique = models.Constraint(
        "UNIQUE(item_id)",
        "A item_id must be unique!",
    )

    def item_type_code_generator(self):
        """Generate a new item type code"""
        """
        sample code:
        
            import { ItemType } from '../../models/ItemType';

            export const ITEM_TYPE = {
                EQUIP: new ItemType(1, 'Equip'),
                USABLE: new ItemType(2, 'Usable'),
                MISC: new ItemType(3, 'Misc'),
            };

        """
        item_types = self.search([])
        item_types_code = "import { ItemType } from '../../models/ItemType';\n\n export const ITEM_TYPES = {\n"
        for item_type in item_types:
            item_types_code += f"  {item_type.key}: new ItemType({item_type.item_id}, '{item_type.name}'),\n"
        item_types_code += "};"

        utils_model = self.env["rpg.game.utils"]
        item_type_const_path = utils_model.get_rpg_game_src_directory(
            "consts/DB_SEED/ItemTypes.js"
        )
        with open(item_type_const_path, "w") as f:
            f.write(item_types_code)

        return item_types_code

    @api.model
    def create(self, vals):
        res = super(ItemTyps, self).create(vals)
        res.item_type_code_generator()
        return res

    @api.model
    def write(self, vals):
        res = super(ItemTyps, self).write(vals)
        self.item_type_code_generator()
        return res

    def unlink(self):
        res = super(ItemTyps, self).unlink()
        self.item_type_code_generator()
        return res


class Items(models.Model):
    _name = "game.items"
    _description = "Item"

    name = fields.Char(string="Name", required=True)
    item_type = fields.Many2one("item.type", string="Type", required=True)
    item_key = fields.Char(related="item_type.key", string="Key", store=True)
    buff_type = fields.Many2one("buff.type", string="Buff Type")
    buff_key = fields.Char(
        related="buff_type.key", string="Buff Key", store=True, default=0
    )
    description = fields.Text(string="Description", required=True)
    script = fields.Text(string="Script", required=True)
    texture = fields.Many2one("game.assets.manager", string="Texture", required=True)
    texture_image = fields.Binary(related="texture.file", string="Texture Image")
    sfx = fields.Many2one("game.assets.manager", string="SFX", required=True)
    stackable = fields.Boolean(string="Stackable", required=True, default=True)
    inventory_scale = fields.Float(string="Inventory Scale", required=True, default=1.7)

    _name_unique = models.Constraint(
        "UNIQUE(name)",
        "A name must be unique!",
    )

    def item_code_generator(self):
        """Generate a new item code"""
        item_types = self.search([])
        item_types_code = "import { ItemType } from '../../models/ItemType';\n"
        item_types_code += "import { BUFF_TYPES } from './BuffTypes';\n\n"
        item_types_code += """
        /**
            * @example
            * The 'script' works like this:
            * ACTION, WHAT, AMOUNT
            * ACTION: rec -> recover
            * WHAT: hp -> health
            * AMOUNT: 50
            * Will translate to -> Recover 50 HP.
            * Then the transpiles will take care to recover the HP.
        */

        """
        item_types_code += "export const DB_SEED_ITEMS = [\n"
        for item_type in item_types:
            item_types_code += f"  {{\n"
            item_types_code += f"    id: {item_type.id},\n"
            item_types_code += f'    name: "{item_type.name}",\n'
            item_types_code += f"    type: ItemType.{item_type.item_key},\n"
            item_types_code += f"    buffType: {f'BUFF_TYPES.{item_type.buff_key}' if item_type.buff_key else '0'},\n"
            item_types_code += f'    description: "{item_type.description}",\n'
            item_types_code += f'    script: "{item_type.script}",\n'
            item_types_code += f'    texture: "{item_type.texture.name_key}",\n'
            item_types_code += f'    sfx: "{item_type.sfx.name_key}",\n'
            item_types_code += f"    stackable: {str(item_type.stackable).lower()},\n"
            item_types_code += f"    inventoryScale: {item_type.inventory_scale},\n"
            item_types_code += f"  }},\n"
        item_types_code += "];"

        utils_model = self.env["rpg.game.utils"]
        item_type_const_path = utils_model.get_rpg_game_src_directory(
            "consts/DB_SEED/Items.js"
        )
        with open(item_type_const_path, "w") as f:
            f.write(item_types_code)

        return item_types_code

    @api.model
    def create(self, vals):
        res = super(Items, self).create(vals)
        res.item_code_generator()
        return res

    @api.model
    def write(self, vals):
        res = super(Items, self).write(vals)
        self.item_code_generator()
        return res

    def unlink(self):
        res = super(Items, self).unlink()
        self.item_code_generator()
        return res
