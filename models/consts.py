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


class RPGBaseEnity(models.Model):
    _name = "rpg.base.entity"
    _description = "RPG Base Enteity"

    name = fields.Char(string="Name", required=True)
    entity_id = fields.Char(string="ID", default="null")
    is_atacking = fields.Boolean(string="Is Atacking", default=False)
    can_atack = fields.Boolean(string="Can Atack", default=True)
    can_move = fields.Boolean(string="Can Move", default=True)
    can_take_damage = fields.Boolean(string="Can Take Damage", default=True)
    show_hit_box = fields.Boolean(string="Show Hit Box", default=False)
    perception_range = fields.Float(string="Perception Range", default=75)

    def rpg_base_entity_code_generator(self):
        """
        Generate a new RPG Base Entity code

        export const BaseEntity = {
          /**
           * A Unique ID to identify the Entity.
           * @type { string }
           * @default
           */
          id: null,
          /**
           * Controls if the entity is atacking.
           * @type { boolean }
           * @default
           */
          isAtacking: false,

          /**
           * Controls if the player can atack.
           * @type { boolean }
           * @default
           */
          canAtack: true,

          /**
           * Controls if the player can move.
           * @type { boolean }
           * @default
           */
          canMove: true,

          /**
           * Controls if the entity can take damage.
           * @type { boolean }
           * @default
           */
          canTakeDamage: true,

          /**
           * This variable controls when the atack hitbox will appear.
           * @type { boolean }
           * @default
           */
          showHitBox: false,

          /**
           * The perception range of the entity. Usualy the field of view. For enemies it should be used to atack the player onde it's inside the perception radius.
           * @type { number }
           * @default
           */
          perceptionRange: 75,
        };
        """
        rpg_base_entity_code = "export const BaseEntity = {\n"
        rpg_base_entity_code += "  /**\n"
        rpg_base_entity_code += "   * A Unique ID to identify the Entity.\n"
        rpg_base_entity_code += "   * @type { string }\n"
        rpg_base_entity_code += "   * @default\n"
        rpg_base_entity_code += f"   * {self.entity_id}\n"
        rpg_base_entity_code += "   */\n"
        rpg_base_entity_code += f"  id: {self.entity_id},\n"
        rpg_base_entity_code += "  /**\n"
        rpg_base_entity_code += "   * Controls if the entity is atacking.\n"
        rpg_base_entity_code += "   * @type { boolean }\n"
        rpg_base_entity_code += "   * @default\n"
        rpg_base_entity_code += f"   * {self.is_atacking}\n"
        rpg_base_entity_code += "   */\n"
        rpg_base_entity_code += f"  isAtacking: {str(self.is_atacking).lower()},\n"
        rpg_base_entity_code += "  /**\n"
        rpg_base_entity_code += "   * Controls if the player can atack.\n"
        rpg_base_entity_code += "   * @type { boolean }\n"
        rpg_base_entity_code += "   * @default\n"
        rpg_base_entity_code += f"   * {self.can_atack}\n"
        rpg_base_entity_code += "   */\n"
        rpg_base_entity_code += f"  canAtack: {str(self.can_atack).lower()},\n"
        rpg_base_entity_code += "  /**\n"
        rpg_base_entity_code += "   * Controls if the player can move.\n"
        rpg_base_entity_code += "   * @type { boolean }\n"
        rpg_base_entity_code += "   * @default\n"
        rpg_base_entity_code += f"   * {self.can_move}\n"
        rpg_base_entity_code += "   */\n"
        rpg_base_entity_code += f"  canMove: {str(self.can_move).lower()},\n"
        rpg_base_entity_code += "  /**\n"
        rpg_base_entity_code += "   * Controls if the entity can take damage.\n"
        rpg_base_entity_code += "   * @type { boolean }\n"
        rpg_base_entity_code += "   * @default\n"
        rpg_base_entity_code += f"   * {self.can_take_damage}\n"
        rpg_base_entity_code += "   */\n"
        rpg_base_entity_code += (
            f"  canTakeDamage: {str(self.can_take_damage).lower()},\n"
        )
        rpg_base_entity_code += "  /**\n"
        rpg_base_entity_code += (
            "   * This variable controls when the atack hitbox will appear.\n"
        )
        rpg_base_entity_code += "   * @type { boolean }\n"
        rpg_base_entity_code += "   * @default\n"
        rpg_base_entity_code += f"   * {self.show_hit_box}\n"
        rpg_base_entity_code += "   */\n"
        rpg_base_entity_code += f"  showHitBox: {str(self.show_hit_box).lower()},\n"
        rpg_base_entity_code += "  /**\n"
        rpg_base_entity_code += "   * The perception range of the entity. Usualy the field of view. For enemies it should be used to atack the player onde it's inside the perception radius.\n"
        rpg_base_entity_code += "   * @type { number }\n"
        rpg_base_entity_code += "   * @default\n"
        rpg_base_entity_code += f"   * {self.perception_range}\n"
        rpg_base_entity_code += "   */\n"
        rpg_base_entity_code += f"  perceptionRange: {self.perception_range},\n"
        rpg_base_entity_code += "};"
        rpg_base_entity_code += "\n"

        utils_model = self.env["rpg.game.utils"]
        rpg_base_entity_const_path = utils_model.get_rpg_game_src_directory(
            "entities/BaseEntity.js"
        )
        # Check if the file exists
        with open(rpg_base_entity_const_path, "w") as f:
            f.write(rpg_base_entity_code)

        return rpg_base_entity_code

    @api.model
    def create(self, vals):
        existing_entities = self.search([], limit=1)
        if existing_entities:
            raise ValueError("There can be only one RPG Base Entity.")

        res = super(RPGBaseEnity, self).create(vals)
        res.rpg_base_entity_code_generator()
        return res

    @api.model
    def write(self, vals):
        res = super(RPGBaseEnity, self).write(vals)
        self.rpg_base_entity_code_generator()
        return res
