from odoo import api, fields, models, _

class ComptaLigneCommande(models.Model):
    _name = 'compta.ligne.commande'
    _description = 'Ligne de commande'
    _rec_name = "numLigneCommande"
    
    numLigneCommande = fields.Char(string="Numéro de ligne de commande", default="Nouveau")
    qteTotalRessource = fields.Float(string="Quantité totale de ressource")
    qteTotalFacturee = fields.Float(string="Quantité totale facturée")
    
    commande_id = fields.Many2one('compta.commande', string="Commande")
    ressource_id = fields.Many2one('compta.ressource', string="Ressource")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numLigneCommande') or vals['numLigneCommande'] == 'Nouveau':
                vals['numLigneCommande'] = self.env['ir.sequence'].next_by_code('compta.ligne.commande')
        return super().create(vals_list)
