from odoo import api, fields, models
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    metadata_line_ids = fields.One2many(
        'sale.order.metadata.line', 'order_id', string=_("Metadata"))

    def get_metadata_value(self, key):
        return self.metadata_line_ids.filtered(
            lambda meta: meta.key == key
        ).value
