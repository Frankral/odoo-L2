from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class CommandeAchat(models.Model):
    _inherit = "purchase.order"

    automatise_invoice = fields.Boolean(string='Automatiser la facturation', default=True)
    
    invoice_date_selection = fields.Selection([
        ('today', "Date du jour"),
        ('custom', 'Date personnalisé')
    ], string='Date des factures automatiques', default="today")
    invoice_date = fields.Date(string="Date sur les factures", default=datetime.today(), compute='_compute_invoice_date', inverse="_inverse_invoice_date", store=True)
    invoice_ref = fields.Char(string="Référence des factures automatiques")
    invoice_payment_ref = fields.Char(string="Référence de paiement des factures")
    invoice_payment_term_id = fields.Many2one('account.payment.term', string='Condition de paiement des factures')
    invoice_incoterm_id = fields.Many2one('account.incoterms', string='Incoterm des factures')
    invoice_incoterm_location = fields.Char("Emplacement associé à l'incoterm")
    invoice_auto_post = fields.Selection([
        ('no', "Non"),
        ('at_date', 'À la date'),
        ('monthly','Mensuel'),
        ('quarterly','Trimestriel'),
        ('yearly','Annuel')
    ], string="Publication automatique", default="no")
    invoice_delivery_date = fields.Date("Date de livraison")


    # -------------------------- compute ------------------------------
    @api.onchange('invoice_date_selection')
    def _compute_invoice_date(self):
        for record in self:
            if record.invoice_date_selection == 'today':
                record.invoice_date = datetime.today()
    
    def _inverse_invoice_date(self):
        for record in self:
            record.invoice_date = record.invoice_date


    # ------------------------- actions -------------------------------------
    def creer_facture(self):
        for record in self:
            if record.automatise_invoice:
                try:
                    record.action_create_invoice()
                    nb_facture = record.invoice_count
                    created_invoice = record.invoice_ids[nb_facture - 1]
                    created_invoice.invoice_date = record.invoice_date
                    created_invoice.ref = record.invoice_ref
                    created_invoice.payment_reference = record.invoice_payment_ref
                    created_invoice.invoice_payment_term_id = record.invoice_payment_term_id
                    created_invoice.invoice_incoterm_id = record.invoice_incoterm_id
                    created_invoice.incoterm_location = record.invoice_incoterm_location
                    created_invoice.auto_post = record.invoice_auto_post
                    created_invoice.delivery_date = record.invoice_delivery_date
                except:
                    return

    def confirmer_commande(self):
        for record in self:
            record.button_confirm()
            record.creer_facture()
