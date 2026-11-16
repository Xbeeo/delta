from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_pcs = fields.Float(
        string='Total Pcs',
        compute='_compute_total_pcs',
        store=True
    )

    @api.depends(
        'invoice_line_ids.quantity',
        'invoice_line_ids.product_uom_id',
        'invoice_line_ids.product_uom_id.relative_factor'
    )
    def _compute_total_pcs(self):
        for move in self:
            total = 0.0

            for line in move.invoice_line_ids:
                if line.display_type == 'product':
                    qty = line.quantity or 0.0
                    factor = line.product_uom_id.relative_factor or 0.0

                    total += qty * factor

            move.total_pcs = total