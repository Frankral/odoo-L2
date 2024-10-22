from odoo import api, fields, models, _

class ComptaLigneFacture(models.Model):
    _name = 'compta.ligne.facture'
    _description = 'Ligne de facture'
    _rec_name = "numLigneFacture"

    numLigneFacture = fields.Char(string="Numéro de ligne de facture", default="Nouveau")
    qteFacturee = fields.Float(string ='Quantite facturée')

    facture_id = fields.Many2one('compta.facture', string='Facture')

    ligne_commande_id = fields.Many2one('compta.ligne.commande', string='Ligne de commande')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numLigneFacture') or vals['numLigneFacture'] == 'Nouveau':
                vals['numLigneFacture'] = self.env['ir.sequence'].next_by_code('compta.ligne.facture')
        return super().create(vals_list)
