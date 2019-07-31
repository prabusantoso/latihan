# -*- coding: utf-8 -*-
from odoo import http

# class Latihan(http.Controller):
#     @http.route('/latihan/latihan/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/latihan/latihan/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('latihan.listing', {
#             'root': '/latihan/latihan',
#             'objects': http.request.env['latihan.latihan'].search([]),
#         })

#     @http.route('/latihan/latihan/objects/<model("latihan.latihan"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('latihan.object', {
#             'object': obj
#         })