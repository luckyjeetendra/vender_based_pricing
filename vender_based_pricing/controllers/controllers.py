# -*- coding: utf-8 -*-
# from odoo import http


# class VenderBasedPricing(http.Controller):
#     @http.route('/vender_based_pricing/vender_based_pricing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vender_based_pricing/vender_based_pricing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vender_based_pricing.listing', {
#             'root': '/vender_based_pricing/vender_based_pricing',
#             'objects': http.request.env['vender_based_pricing.vender_based_pricing'].search([]),
#         })

#     @http.route('/vender_based_pricing/vender_based_pricing/objects/<model("vender_based_pricing.vender_based_pricing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vender_based_pricing.object', {
#             'object': obj
#         })
