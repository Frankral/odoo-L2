from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class CommandeVente(models.Model):
    _inherit = "sale.order"

    automatise_invoice = fields.Boolean(string = 'Automatiser la facturation', default=True)
    
    auto_invoice_date_selection = fields.Selection([
        ('today', "Date du jour"),
        ('custom', 'Date personnalisé')
    ], string='Date des factures automatiques', default="today")
    auto_invoice_date = fields.Date(string="Date sur les factures", default=datetime.today(), compute='_compute_auto_invoice_date', inverse="_inverse_auto_invoice_date", store=True)
    auto_invoice_ref = fields.Char(string="Référence des factures automatiques")
    auto_invoice_payment_ref = fields.Char(string="Référence de paiement des factures")
    auto_invoice_payment_term_id = fields.Many2one('account.payment.term', string='Condition de paiement des factures')
    auto_invoice_incoterm_id = fields.Many2one('account.incoterms', string='Incoterm des factures')
    auto_invoice_incoterm_location = fields.Char("Emplacement associé à l'incoterm")
    auto_invoice_auto_post = fields.Selection([
        ('no', "Non"),
        ('at_date', 'À la date'),
        ('monthly','Mensuel'),
        ('quarterly','Trimestriel'),
        ('yearly','Annuel')
    ], string="Publication automatique", default="no")
    auto_invoice_delivery_date = fields.Date("Date de livraison")


    # -------------------------- compute ------------------------------
    @api.onchange('auto_invoice_date_selection')
    def _compute_auto_invoice_date(self):
        for record in self:
            if record.auto_invoice_date_selection == 'today':
                record.auto_invoice_date = datetime.today()
    
    def _inverse_auto_invoice_date(self):
        for record in self:
            record.auto_invoice_date = self.auto_invoice_date


    #  -------------------------- actions --------------------
    def creer_facture(self):
        for record in self:
            if record.automatise_invoice:
                try:
                    record._create_invoices()
                    nb_facture = record.invoice_count
                    created_invoice = record.invoice_ids[nb_facture - 1]
                    created_invoice.invoice_date = record.auto_invoice_date
                    created_invoice.ref = record.auto_invoice_ref
                    created_invoice.payment_reference = record.auto_invoice_payment_ref
                    created_invoice.invoice_payment_term_id = record.auto_invoice_payment_term_id
                    created_invoice.invoice_incoterm_id = record.auto_invoice_incoterm_id
                    created_invoice.incoterm_location = record.auto_invoice_incoterm_location
                    created_invoice.auto_post = record.auto_invoice_auto_post
                    created_invoice.delivery_date = record.auto_invoice_delivery_date
                except:
                    return

    def confirmer_commande(self):
        for record in self:
            record.action_confirm()
            record.creer_facture()

        
