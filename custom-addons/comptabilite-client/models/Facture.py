from odoo import api, fields, models, _

class ComptaFacture(models.Model):
    _name = 'compta.facture'
    _description = 'Facture'
    _rec_name = "numFacture"

    numFacture = fields.Char(string="Numéro de facture", default="Nouveau")
    dateFacture = fields.Date(string="Date du facture")
    montantTotal = fields.Integer(string="Montant total")
    restePayer = fields.Integer(string="Reste à payer")
    dateFinPaiement = fields.Char(string="Date fin de paiement")

    commande_id = fields.Many2one('compta.commande', string='Commande')
    # client_id = fields.Many2one('compta.Facture', string='Facture')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numFacture') or vals['numFacture'] == 'Nouveau':
                vals['numFacture'] = self.env['ir.sequence'].next_by_code('compta.facture')
        return super().create(vals_list)