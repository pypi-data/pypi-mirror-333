from odoo import models, fields
from odoo.tools.translate import _


class SaleOrderMetadataLine(models.Model):
    _name = 'sale.order.metadata.line'
    _inherit = 'metadata.line'

    order_id = fields.Many2one(
        'sale.order', string=_("Sale Order"), ondelete='cascade')
