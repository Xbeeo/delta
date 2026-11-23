import re

from odoo import models

CODE_MARKER = re.compile(r'\t--(.+?)--')

def _name_first_display_name(records, compute_super):
    ctx = records.env.context
    if ctx.get('formatted_display_name') or not ctx.get('display_default_code', True):
        return compute_super(records)
    formatted = records.with_context(formatted_display_name=True)
    compute_super(formatted)
    for record, formatted_record in zip(records, formatted):
        value = formatted_record.display_name
        record.display_name = CODE_MARKER.sub(r' [\1]', value) if value else value


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_display_name(self):
        _name_first_display_name(
            self, lambda recs: super(ProductTemplate, recs)._compute_display_name()
        )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _compute_display_name(self):
        _name_first_display_name(
            self, lambda recs: super(ProductProduct, recs)._compute_display_name()
        )