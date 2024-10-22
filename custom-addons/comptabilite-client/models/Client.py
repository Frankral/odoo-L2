from odoo import api, fields, models, _

class ComptaClient(models.Model):
    _name = 'compta.client'
    _description = 'Client'
    _rec_name = "denomination"

    numClient = fields.Char(string="Numéro client", default="Nouveau")
    denomination = fields.Char(string="Denomination")
    adresse = fields.Char(string="Adresse")
    telephone = fields.Char(string="Numéro de téléphone")
    email = fields.Char(string="Email")
    typeClient = fields.Selection([
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
    ], string='Type du client')

    creance_ids = fields.One2many('compta.creance', 'client_id', string='Creances')
    commande_ids = fields.One2many('compta.commande', 'client_id', string='Commandes')
    justificatif_ids = fields.One2many('compta.justificatif', 'client_id', string='Justificatifs')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numClient') or vals['numClient'] == 'Nouveau':
                vals['numClient'] = self.env['ir.sequence'].next_by_code('compta.client')
        return super().create(vals_list)