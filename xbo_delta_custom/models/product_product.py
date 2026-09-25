# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class ProductProductInheritOD(models.Model):
    _inherit = 'product.product'

    conversion_value = fields.Float(
        related="product_tmpl_id.conversion_value",
        store=True,
        readonly=False,
    )

    conversion_uom_id = fields.Many2one(
        "uom.uom",
        related="product_tmpl_id.conversion_uom_id",
        store=True,
        readonly=False,
    )

    converted_value = fields.Float(
        related="product_tmpl_id.converted_value",
        store=True,
        readonly=True,
    )
