from odoo import api, fields, models, _

class ComptaJustificatif(models.Model):
    _name = 'compta.justificatif'
    _description = 'Justificatif'
    _rec_name = "numJustificatif"

    numJustificatif = fields.Char(string="Numéro justificatif", default="New")
    dateJustificatif = fields.Date(string="Date du justificatif")
    montantJustificatif = fields.Char(string="Montant du justificatif")

    mode_paiement_id = fields.Many2one('compta.mode.paiement', string='Mode de paiement')

    # client_id = fields.Many2one('compta.client', string='Client')
    facture_id = fields.Many2one('compta.facture', string='Facture')