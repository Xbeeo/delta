# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class ProductTemplateInheritOD(models.Model):
    _inherit = 'product.template'

    conversion_value = fields.Float(string="Conversion Value", )
    conversion_uom_id = fields.Many2one("uom.uom", string="UOM")
    converted_value = fields.Float(string="Converted Value", compute='_compute_converted_value')

    @api.depends('conversion_value', 'conversion_uom_id', 'converted_value')
    def _compute_converted_value(self):
        for rec in self:

            if rec.conversion_value and rec.qty_available:
                rec.converted_value = rec.qty_available * rec.conversion_value
            else:
                rec.converted_value = 0