from odoo import api, fields, models, _

class ComptaLigneCommande(models.Model):
    _name = 'compta.ligne.commande'
    _description = 'Ligne de commande'
    
    commande_id = fields.Many2one('compta.commande', string="Commande")
    ressource_id = fields.Many2one('compta.ressource', string="Ressource")
    quantite = fields.Integer(string="Quantité de ressource")

    
