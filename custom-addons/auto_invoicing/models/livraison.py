from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class Livraison(models.Model):
    _inherit = "stock.picking"

    def create_invoice(self):
        if self.picking_type_id.id == 1:
            if self.purchase_id.automatise_invoice:
                self.purchase_id.action_create_invoice()
        else:
            if self.sale_id.automatise_invoice:
                try:
                    self.sale_id._create_invoices()
                except:
                    return        


    def validate_button(self):
        action = self.button_validate()
        
        for move in self.move_ids:
            if move.product_uom_qty != move.quantity:
                return action
        
        self.create_invoice()