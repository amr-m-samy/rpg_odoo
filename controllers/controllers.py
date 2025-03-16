# -*- coding: utf-8 -*-
from odoo import http

from odoo.http import request


class RpgGame(http.Controller):
    @http.route("/rpg_game", auth="public")
    def index(self, **kw):
        return request.render("rpg_game.game_view", {})


#     @http.route('/rpg_game/rpg_game/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('rpg_game.listing', {
#             'root': '/rpg_game/rpg_game',
#             'objects': http.request.env['rpg_game.rpg_game'].search([]),
#         })

#     @http.route('/rpg_game/rpg_game/objects/<model("rpg_game.rpg_game"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('rpg_game.object', {
#             'object': obj
#         })


# class SciRpg(http.Controller):
#     @http.route("/sci_rpg", type="http", auth="public")
#     def index(self, **kw):
#         return request.render("sci_rpg.game_view", {})
