from odoo import api, fields, models, _

class ComptaRessource(models.Model):
    _name = 'compta.ressource'
    _description = 'Ressource'
    _rec_name = "libelle"

    codeRessource = fields.Char(string="Code de ressource", default="Nouveau")
    libelle = fields.Char(string="Libelle")
    prixUnitaire = fields.Integer(string="Prix unitaire")
    stock = fields.Integer(string="Stock")
    unite = fields.Selection([
        (' ', ' '),
        ('kilo', 'Kilogramme'),
        ('litre', 'Litre'),
        ('heure', "Nombre d'heures"),
    ], string='Unite')

    ligne_commande_ids = fields.One2many('compta.ligne.commande', 'ressource_id', string='ligne_commande')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('codeRessource') or vals['codeRessource'] == 'Nouveau':
                vals['codeRessource'] = self.env['ir.sequence'].next_by_code('compta.ressource')
        return super().create(vals_list)