from odoo import api, fields, models, _

class ComptaCreance(models.Model):
    _name = 'compta.creance'
    _description = 'Créance'
    _rec_name = "numCreance"

    numCreance = fields.Char(string="Numéro creance", default="Nouveau")
    dateCreance = fields.Date(string="Date de la créance")
    dateEcheanceCreance = fields.Date(string="Date d'échéance de la créance")
    montantCreance = fields.Integer(string="Montant de la créance")
    restePayerCreance = fields.Integer(string="Reste à payer de la créance")
    
    client_id = fields.Many2one('compta.client', string='Client')

    facture_id = fields.Many2one('compta.facture', string='Facture')

    justificatif_ids = fields.One2many('compta.justificatif', 'creance_id', string='Justificatifs')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numCreance') or vals['numCreance'] == 'Nouveau':
                vals['numCreance'] = self.env['ir.sequence'].next_by_code('compta.creance')
        return super().create(vals_list)