from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class LigneCommandeAchat(models.Model):
    _inherit = "purchase.order.line"

    product_invoice_policy = fields.Selection(related='product_id.purchase_method', string="Politique de facturation", readonly=False)
