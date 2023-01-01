# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def _remove_order_line(self):
        order_lines = self.env['purchase.order.line'].search([('order_id', 'in', self.ids)])
        if not order_lines:
            return
        to_delete = order_lines.filtered(lambda x: x.qty_invoiced == 0)
        if not to_delete:
            raise UserError(
                _('You can not update the order line on an order where it was already invoiced!\n\nThe following delivery lines (product, invoiced quantity and price) have already been processed:\n\n')
                + '\n'.join(['- %s: %s x %s' % (line.product_id.with_context(display_default_code=False).display_name, line.qty_invoiced, line.price_unit) for line in delivery_lines])
            )
        to_delete.unlink()


    def _get_order_lines(self):
        value_list = []
        for line in self.partner_id.vendor_price_line:
            data_line = self.env['vendor.price.line'].search([('rel_partner_id', '=', self.partner_id.id), ('product_id', '=', line.product_id.id)])
            if data_line:
                pre_pol = self.env['purchase.order.line'].search([('partner_id', '=', self.partner_id.id), ('product_id', '=', data_line.product_id.id)])
                unit_price = 0.0
                if pre_pol:
                    unit_price = sum([x.price_unit for x in pre_pol])/len(pre_pol)
                value = {
                    'order_id': self.id,
                    'name': data_line.product_id.name,
                    'product_qty': line.product_qty,
                    'product_uom': data_line.product_id.uom_id.id,
                    'product_id': data_line.product_id.id,
                    'price_unit': unit_price,
                }
                value_list.append(value)

        return value_list


    def set_order_line(self):
        self._remove_order_line()
        for order in self:
            PurchaseOrderLine = self.env['purchase.order.line']            
            values = order._get_order_lines()
            # Create the purchase order line
            for val in values:
                if order.order_line:
                    val['sequence'] = order.order_line[-1].sequence + 1
                pol = PurchaseOrderLine.sudo().create(val)

        return True


    # Override this function to create multiple Receipt for PO based on delivery date selected in POL.
    def _create_picking(self):
        StockPicking = self.env['stock.picking']
        for order in self.filtered(lambda po: po.state in ('purchase', 'done')):
            if any(product.type in ['product', 'consu'] for product in order.order_line.product_id):

                datalines = []
                for line in order.order_line:
                    data = self.env['purchase.order.line'].search([('order_id', '=', self.id), ('date_planned', '=', line.date_planned)])
                    if data not in datalines:
                        datalines.append(data)

                order = order.with_company(order.company_id)
                                
                for dline in datalines:
                    res = order._prepare_picking()
                    picking = StockPicking.with_user(SUPERUSER_ID).create(res)
                    moves = dline._create_stock_moves(picking)
                    moves = moves.filtered(lambda x: x.state not in ('done', 'cancel'))._action_confirm()
                    seq = 0

                    for move in sorted(moves, key=lambda move: move.date):
                        seq += 5
                        move.sequence = seq
                    moves._action_assign()
                    picking.message_post_with_view('mail.message_origin_link',
                        values={'self': picking, 'origin': order},
                        subtype_id=self.env.ref('mail.mt_note').id)
                    
        return True
