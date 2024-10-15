from odoo import api, fields, models, _

class ComptaFacture(models.Model):
    _name = 'compta.facture'
    _description = 'Facture'
    _rec_name = "numFacture"

    numFacture = fields.Char(string="Numéro de facture", default="New")
    dateFacture = fields.Date(string="Date du facture")
    montantTotal = fields.Integer(string="Montant total")
    restePayer = fields.Integer(string="Reste à payer")
    dateFinPaiement = fields.Char(string="Date fin de paiement")

    commande_id = fields.Many2one('compta.commande', string='Commande')
    # client_id = fields.Many2one('compta.client', string='Client')