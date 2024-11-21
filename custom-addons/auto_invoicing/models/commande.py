from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class CommandeVente(models.Model):
    _inherit = "sale.order"

    automatise_invoice = fields.Boolean(string = 'Automatiser la facturation', default=True)

    def confirmer_commande(self):
        self.action_confirm()
        
        if self.automatise_invoice:
            try:
                self._create_invoices()
            except:
                return

class CommandeAchat(models.Model):
    _inherit = "purchase.order"

    automatise_invoice = fields.Boolean(string = 'Automatiser la facturation', default=True)

    def confirmer_commande(self):
        self.button_confirm()
        if self.automatise_invoice:
            try:
                self.action_create_invoice()
            except:
                return
        
