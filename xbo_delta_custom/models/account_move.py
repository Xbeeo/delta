from odoo import api, fields, models

# UoM names that are treated as "units" (not cartons)
UNIT_NAMES = ('units', 'unit', 'pcs', 'pc')


class AccountMove(models.Model):
    _inherit = 'account.move'

    total_pcs = fields.Float(
        string='Total Pcs',
        compute='_compute_total_pcs',
        store=True,
    )

    total_cartons = fields.Float(
        string='Total Cartons',
        compute='_compute_total_pcs',
        store=True,
    )

    @api.depends(
        'invoice_line_ids.display_type',
        'invoice_line_ids.quantity',
        'invoice_line_ids.product_id.type',
        'invoice_line_ids.product_uom_id',
        'invoice_line_ids.product_uom_id.name',
        'invoice_line_ids.product_uom_id.relative_factor',
    )
    def _compute_total_pcs(self):
        for move in self:
            total_pcs = 0.0
            total_cartons = 0.0

            for line in move.invoice_line_ids:
                # Only real product lines (skip sections, notes, taxes, etc.)
                if line.display_type != 'product':
                    continue

                qty = line.quantity or 0.0

                # Total Pcs: quantity multiplied by the UoM factor
                factor = line.product_uom_id.relative_factor or 0.0
                total_pcs += qty * factor

                # Skip lines without a UoM and combo lines for the carton total
                if not line.product_uom_id or line.product_id.type == 'combo':
                    continue

                # Read the UoM name in English so the result does not
                # depend on the language of the user who saves the invoice
                uom_name = (
                    line.product_uom_id.with_context(lang='en_US').name or ''
                ).strip().lower()

                # If the UoM is not unit/pcs, count it as cartons
                if uom_name not in UNIT_NAMES:
                    total_cartons += qty

            move.total_pcs = total_pcs
            move.total_cartons = total_cartons