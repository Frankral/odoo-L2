from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class Livraison(models.Model):
    _inherit = "stock.picking"

    def create_invoice(self):
        for record in self:
            if record.picking_type_id.id == 1:
                record.purchase_id.invoice_delivery_date = datetime.today()
                record.purchase_id.creer_facture()
            else:
                record.sale_id.invoice_delivery_date = datetime.today()
                record.sale_id.creer_facture()


    def validate_button(self):
        for record in self:
            action = record.button_validate()

            for move in record.move_ids:
                if move.product_uom_qty != move.quantity:
                    return action

            record.create_invoice()