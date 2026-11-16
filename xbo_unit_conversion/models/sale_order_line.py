from odoo import api, fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

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
                line.product_uom_qty = (
                         line.custom_qty * line.product_id.conversion_value
                )
            else:
                line.product_uom_qty = 0


    def _prepare_invoice_line(self, **optional_values):
        res = super()._prepare_invoice_line(**optional_values)
        res.update({
            'custom_qty': self.custom_qty or 0.0,
        })
        return res