from odoo import api, fields, models, _

class ComptaCommande(models.Model):
    _name = 'compta.commande'
    _description = 'Commande'
    _rec_name = "numCommande"

    numCommande = fields.Char(string="Numéro commande", default="Nouveau")
    dateCommande = fields.Date(string="Date de commande")
    montantTotal = fields.Integer(string="Montant total")
    etatCommande = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('confirmee', 'Confirmée'),
        ('cours', 'En cours de facturation'),
        ('facturee', 'Facturée'),
        ('payee', 'Payée'),
        ('archivee', 'Archivée'),
        ('annulee', 'Annulée'),
    ], string='Etat de la commande')

    client_id = fields.Many2one('compta.client', string='Client')

    ligne_commande_ids = fields.One2many('compta.ligne.commande', 'commande_id', string='Ligne de commande')
    
    facture_ids = fields.One2many('compta.facture', 'commande_id', string='Factures')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numCommande') or vals['numCommande'] == 'Nouveau':
                vals['numCommande'] = self.env['ir.sequence'].next_by_code('compta.commande')
        return super().create(vals_list)