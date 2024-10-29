from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class ComptaRessource(models.Model):
    _name = 'compta.ressource'
    _description = 'Ressource'
    _rec_name = "libelle"


    codeRessource = fields.Char(string="Code de ressource", default="Nouveau")
    libelle = fields.Char(string="Libelle", required=True)
    prixUnitaire = fields.Integer(string="Prix unitaire", required=True, )
    stock = fields.Float(string="Stock", default=0,compute="compute_stock", inverse="_inverse_stock", store=True )
    unite = fields.Selection([
        (' ', ' '),
        ('kg', 'Kilogramme'),
        ('l', 'Litre'),
        ('h', "Nombre d'heures"),
    ], string='Unite', required=True)

    ligne_commande_ids = fields.One2many('compta.ligne.commande', 'ressource_id', string='ligne_commande')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)

    last_sum = fields.Float(string="last sum", default=0, store=True, compute='_compute_last_sum')

    # ----------------------- create ------------------------------- 
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('codeRessource') or vals['codeRessource'] == 'Nouveau':
                vals['codeRessource'] = self.env['ir.sequence'].next_by_code('compta.ressource')
        return super().create(vals_list)
    

    # -------------------------- check ----------------------------
    @api.onchange('prixUnitaire', 'stock')
    def _check_positive(self):
        if self.prixUnitaire < 0:
            raise ValidationError('La valeur du prix unitaire doit être positive')
        if self.stock < 0:
            raise ValidationError('La valeur du stock doit être positive')


    # ----------------------------- compute ----------------------------------
    @api.depends('ligne_commande_ids', 'ligne_commande_ids.qteTotalRessource')
    def compute_stock(self):
        summed = sum(self.ligne_commande_ids.mapped('qteTotalRessource'))
        diff = self.last_sum - summed
        if self.stock + diff >= 0: 
            self.stock += diff
            self._compute_last_sum()
        else:
            raise ValidationError("Il n'y a plus de stock pour le produit %s" % self.libelle)
    
    def _inverse_stock(self):
        self.stock = self.stock
    
    def _compute_last_sum(self):
        self.last_sum = sum(self.ligne_commande_ids.mapped('qteTotalRessource'))