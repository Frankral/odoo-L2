from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class ComptaRessource(models.Model):
    _name = 'compta.ressource'
    _description = 'Ressource'
    _rec_name = "libelle"


    codeRessource = fields.Char(string="Code de ressource", default="Nouveau")
    libelle = fields.Char(string="Libelle", required=True)
    prixUnitaire = fields.Integer(string="Prix unitaire", required=True, )
    stock = fields.Float(string="Stock", default=0,compute="_compute_stock", inverse="_inverse_stock", store=True )
    unite = fields.Selection([
        (' ', ' '),
        ('kg', 'Kilogramme'),
        ('l', 'Litre'),
        ('h', "Nombre d'heures"),
    ], string='Unite', required=True)

    ligne_commande_ids = fields.One2many('compta.ligne.commande', 'ressource_id', string='ligne_commande')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('codeRessource') or vals['codeRessource'] == 'Nouveau':
                vals['codeRessource'] = self.env['ir.sequence'].next_by_code('compta.ressource')
        return super().create(vals_list)
    
    @api.onchange('ligne_commande_ids', 'ligne_commande_ids.qteTotalRessource')
    def _compute_stock(self):
        last_stock = self.stock
        last_sum = sum(self._origin.ligne_commande_ids._origin.mapped('qteTotalRessource'))
        print(last_sum)
        diff = last_sum - sum(self.ligne_commande_ids.mapped('qteTotalRessource'))
        self.stock = last_stock + diff 

    def _inverse_stock(self):
        self.stock = self.stock


    @api.onchange('prixUnitaire', 'stock')
    def _check_positive(self):
        if self.prixUnitaire < 0:
            raise ValidationError('La valeur du prix unitaire doit être positive')
        if self.stock < 0:
            raise ValidationError('La valeur du stock doit être positive')

   