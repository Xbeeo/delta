# -*- coding: utf-8 -*-

from odoo import fields, models,api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    custom_qty = fields.Float(string="C. Qty")

    custom_uom_id = fields.Many2one(
        "uom.uom",
        string="C. UOM",
        related="product_id.conversion_uom_id",
        store=True,
        readonly=True,
    )

    @api.onchange("custom_qty", "product_id")
    def _onchange_custom_qty(self):
        for line in self:
            if line.custom_qty and line.product_id.conversion_value:
                line.quantity = (
                        line.custom_qty * line.product_id.conversion_value
                )
            else:
                line.quantity = 0