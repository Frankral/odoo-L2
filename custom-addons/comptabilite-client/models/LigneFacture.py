from odoo import api, fields, models, _

class ComptaLigneFacture(models.Model):
    _name = 'compta.ligne.facture'
    _description = 'Ligne de facture'
    _rec_name = "numLigneFacture"

    numLigneFacture = fields.Char(string="Numéro de ligne de facture", default="Nouveau")
    qteFacturee = fields.Float(string ='Quantite facturée', required=True)

    facture_id = fields.Many2one('compta.facture', string='Facture', required=True, ondelete="cascade")

    ligne_commande_id = fields.Many2one('compta.ligne.commande', string='Ligne de commande', required=True, ondelete="cascade")

    ressource_id = fields.Many2one(related='ligne_commande_id.ressource_id', string="Ressource")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numLigneFacture') or vals['numLigneFacture'] == 'Nouveau':
                vals['numLigneFacture'] = self.env['ir.sequence'].next_by_code('compta.ligne.facture')
        return super().create(vals_list)
