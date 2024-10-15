from odoo import api, fields, models, _

class ComptaCommande(models.Model):
    _name = 'compta.commande'
    _description = 'Commande'
    _rec_name = "numCommande"

    numCommande = fields.Char(string="Numéro commande", default="New")
    dateCommande = fields.Date(string="Date de commande")
    montantTotal = fields.Integer(string="Montant total")

    client_id = fields.Many2one('compta.client', string='Client')

    ligne_commande_ids = fields.One2many('compta.ligne.commande', 'commande_id', string='Ligne de commande')

