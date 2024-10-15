from odoo import api, fields, models, _

class ComptaModePaiement(models.Model):
    _name = 'compta.mode.paiement'
    _description = 'Mode de paiement'
    _rec_name = "modePaiement"

    modePaiement = fields.Selection([('espece', "Espèce"), ("virement", "Virement Bancaire"), ("carte", "Par carte")], string="Mode de paiement")
   