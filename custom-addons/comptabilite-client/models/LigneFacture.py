from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class ComptaLigneFacture(models.Model):
    _name = 'compta.ligne.facture'
    _description = 'Ligne de facture'
    _rec_name = "numLigneFacture"

    numLigneFacture = fields.Char(string="Numéro de ligne de facture", default="Nouveau")
    qteFacturee = fields.Float(string ='Quantite facturée', required=True)

    facture_id = fields.Many2one('compta.facture', string='Facture', required=True, ondelete="cascade")

    ligne_commande_id = fields.Many2one('compta.ligne.commande', string='Ligne de commande', required=True, ondelete="cascade")

    commande_id = fields.Many2one(related='ligne_commande_id.commande_id', string="Commande")

    ressource_id = fields.Many2one(related='ligne_commande_id.ressource_id', string="Ressource")

    # ---------------------------- create ------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numLigneFacture') or vals['numLigneFacture'] == 'Nouveau':
                vals['numLigneFacture'] = self.env['ir.sequence'].next_by_code('compta.ligne.facture')
        return super().create(vals_list)
    
    @api.onchange('qteFacturee')
    def check_change(self):
        diff = -self._origin.qteFacturee + self.qteFacturee
        if self.ligne_commande_id.qteTotalFacturee + diff > self.ligne_commande_id.qteTotalRessource:
            raise ValidationError("On ne peut plus facturer le ressource %s de cette quantité" % self.ligne_commande_id.ressource_id.libelle)