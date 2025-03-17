# -*- coding: utf-8 -*-
{
    "name": "rpg_game",
    "summary": "Short (1 phrase/line) summary of the module's purpose",
    "description": """
Long description of module's purpose
    """,
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Uncategorized",
    "version": "0.1",
    # any module necessary for this one to work correctly
    "depends": ["base"],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "views/ui_components_views.xml",
        "views/game_assets_views.xml",
        "views/views.xml",
        "views/templates.xml",
        "views/consts_views.xml",
        "data/game_assets_data.xml",
        "data/ui_components_data.xml",
        "data/consts_data.xml",
    ],
    "assets": {"web.assets_backend": ["/rpg_game/static/src/scss/rpg.scss"]},
    # only loaded in demonstration mode
    "demo": [],
}
