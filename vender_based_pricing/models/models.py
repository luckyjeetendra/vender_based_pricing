# -*- coding: utf-8 -*-

from odoo import api, fields, models

class VendorPriceLine(models.Model):
    _name = 'vendor.price.line'
    _description = 'vendor based pricing'

    rel_partner_id = fields.Many2one('res.partner', string='Partner Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one(
        'product.product', string='Product', required=True,
        change_default=True, ondelete='restrict')
    product_qty = fields.Float('Quantity', required=True, digits='Product Price', default=0.0)



class ResPartner(models.Model):
    _inherit = 'res.partner'

    vendor_price_line = fields.One2many('vendor.price.line', 'rel_partner_id', string='vendor Price Lines', copy=True)

