# -*- coding: utf-8 -*-
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError



class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    total_pcs = fields.Float(
        string='Total Pcs',
        compute='_compute_total_pcs',
        store=True
    )

    @api.depends(
        'order_line.product_uom_qty',
        'order_line.product_uom_id.relative_factor'
    )
    def _compute_total_pcs(self):
        for order in self:
            total = 0.0
            for line in order.order_line:
                if not line.display_type:
                    factor = line.product_uom_id.relative_factor or 0.0
                    total += line.product_uom_qty * factor

            order.total_pcs = total


