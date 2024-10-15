from odoo import api, fields, models, _

class ComptaClient(models.Model):
    _name = 'compta.client'
    _description = 'Client'
    _rec_name = "raisonSocial"

    numClient = fields.Char(string="Numéro client", default="Nouveau")
    raisonSocial = fields.Char(string="Raison social")
    adresse = fields.Char(string="Adresse")
    telephone = fields.Char(string="Numéro de téléphone")
    email = fields.Char(string="Email")
    montantDette = fields.Integer(string="Montant de dette")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numClient') or vals['numClient'] == 'Nouveau':
                vals['numClient'] = self.env['ir.sequence'].next_by_code('compta.client')
        return super().create(vals_list)