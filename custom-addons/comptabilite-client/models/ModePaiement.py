from odoo import api, fields, models, _

class ComptaModePaiement(models.Model):
    _name = 'compta.mode.paiement'
    _description = 'Mode de paiement'
    _rec_name = "modePaiement"

    modePaiement = fields.Char(string="Mode de paiement")
   