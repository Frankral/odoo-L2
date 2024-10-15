from odoo import api, fields, models, _

class ComptaJustificatif(models.Model):
    _name = 'compta.justificatif'
    _description = 'Justificatif'
    _rec_name = "numJustificatif"

    numJustificatif = fields.Char(string="Numéro justificatif", default="Nouveau")
    dateJustificatif = fields.Date(string="Date du justificatif")
    montantJustificatif = fields.Char(string="Montant du justificatif")

    mode_paiement_id = fields.Many2one('compta.mode.paiement', string='Mode de paiement')

    # client_id = fields.Many2one('compta.Justificatif', string='Justificatif')
    facture_id = fields.Many2one('compta.facture', string='Facture')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numJustificatif') or vals['numJustificatif'] == 'Nouveau':
                vals['numJustificatif'] = self.env['ir.sequence'].next_by_code('compta.justificatif')
        return super().create(vals_list)