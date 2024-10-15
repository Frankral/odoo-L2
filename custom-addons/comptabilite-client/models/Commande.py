from odoo import api, fields, models, _

class ComptaCommande(models.Model):
    _name = 'compta.commande'
    _description = 'Commande'
    _rec_name = "numCommande"

    numCommande = fields.Char(string="Numéro commande", default="New")
    dateCommande = fields.Date(string="Date de commande")
    montantTotal = fields.Integer(string="Montant total")