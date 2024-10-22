from odoo import api, fields, models, _

class ComptaFacture(models.Model):
    _name = 'compta.facture'
    _description = 'Facture'
    _rec_name = "numFacture"

    numFacture = fields.Char(string="Numéro de facture", default="Nouveau")
    dateFacture = fields.Date(string="Date du facture")
    montantTotalFacture = fields.Integer(string="Montant total de la facture")
    etatFacture = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('envoyee', 'Envoyée'),
        ('cours', 'En cours de paiement'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée')
    ], string='Etat de la facture')

    commande_id = fields.Many2one('compta.commande', string='Commande')

    ligne_facture_ids = fields.One2many('compta.ligne.facture', 'facture_id', string='Lignes de facture')


    # ------------- simulation one to one -------------------
    creance_id = fields.Many2one('compta.creance', compute='compute_creance', inverse='creance_inverse')
    creance_ids = fields.One2many('compta.creance', 'facture_id')

    @api.depends('creance_ids')
    def compute_creance(self):
        if len(self.creance_ids) > 0:
            self.creance_id = self.creance_ids[0]

    def creance_inverse(self):
        if len(self.creance_ids) > 0:
            # delete previous reference
            creance = self.env['compta.creance'].browse(self.creance_ids[0].id)
            creance.facture_id = False
        # set new reference
        self.creance_id.facture_id = self
    #----------- fin simulation ----------------

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numFacture') or vals['numFacture'] == 'Nouveau':
                vals['numFacture'] = self.env['ir.sequence'].next_by_code('compta.facture')
        return super().create(vals_list)