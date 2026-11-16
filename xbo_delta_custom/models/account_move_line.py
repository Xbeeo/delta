# -*- coding: utf-8 -*-

from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    sr_no = fields.Integer(
        string='Sr#',
        compute='_compute_sr_no',
        store=False
    )

    @api.depends(
        'move_id.invoice_line_ids.sequence',
        'move_id.invoice_line_ids.display_type',
    )
    def _compute_sr_no(self):
        for line in self:
            line.sr_no = 0

        for move in self.move_id:
            product_lines = move.invoice_line_ids.filtered(
                lambda l: l.display_type == 'product'
            ).sorted(lambda l: (l.sequence, l.id))

            numbering = {
                l: index for index, l in enumerate(product_lines, start=1)
            }

            for line in self.filtered(lambda l: l.move_id == move):
                line.sr_no = numbering.get(line, 0)