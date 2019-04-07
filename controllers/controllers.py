# -*- coding: utf-8 -*-
from odoo import http

# class ExitReenter(http.Controller):
#     @http.route('/exit_reenter/exit_reenter/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/exit_reenter/exit_reenter/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('exit_reenter.listing', {
#             'root': '/exit_reenter/exit_reenter',
#             'objects': http.request.env['exit_reenter.exit_reenter'].search([]),
#         })

#     @http.route('/exit_reenter/exit_reenter/objects/<model("exit_reenter.exit_reenter"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('exit_reenter.object', {
#             'object': obj
#         })