from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    sr_no = fields.Integer(
        string='Sr#',
        compute='_compute_sr_no',
        store=False
    )

    @api.depends('order_id.order_line')
    def _compute_sr_no(self):
        for order in self.mapped('order_id'):
            sr = 1
            for line in order.order_line.sorted('sequence'):
                line.sr_no = sr
                sr += 1


