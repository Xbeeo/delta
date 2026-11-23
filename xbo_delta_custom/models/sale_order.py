from odoo import api, fields, models

# UoM names that are treated as "units" (not cartons)
UNIT_NAMES = ('units', 'unit', 'pcs', 'pc')


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

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
        'order_line.display_type',
        'order_line.product_type',
        'order_line.product_uom_qty',
        'order_line.product_uom_id',
        'order_line.product_uom_id.name',
        'order_line.product_uom_id.relative_factor',
    )
    def _compute_total_pcs(self):
        for order in self:
            total_pcs = 0.0
            total_cartons = 0.0

            for line in order.order_line:
                # Skip section/note lines and lines without a UoM
                if line.display_type or not line.product_uom_id:
                    continue

                # Total Pcs: quantity multiplied by the UoM factor
                factor = line.product_uom_id.relative_factor or 0.0
                total_pcs += line.product_uom_qty * factor

                # Combo lines are not counted as cartons
                if line.product_type == 'combo':
                    continue

                # Read the UoM name in English so the result does not
                # depend on the language of the user who saves the order
                uom_name = (
                    line.product_uom_id.with_context(lang='en_US').name or ''
                ).strip().lower()

                # If the UoM is not unit/pcs, count it as cartons
                if uom_name not in UNIT_NAMES:
                    total_cartons += line.product_uom_qty

            order.total_pcs = total_pcs
            order.total_cartons = total_cartons