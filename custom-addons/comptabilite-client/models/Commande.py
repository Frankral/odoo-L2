from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ComptaCommande(models.Model):
    _name = 'compta.commande'
    _description = 'Commande'
    _rec_name = "numCommande"

    numCommande = fields.Char(string="Numéro commande", default="")
    dateCommande = fields.Date(string="Date de commande", required=True)
    montantTotal = fields.Integer(string="Montant total", default=0, required=True, compute="_compute_montantTotal")
    etatCommande = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('confirmee', 'Confirmée'),
        ('cours', 'En cours de facturation'),
        ('facturee', 'Facturée'),
        ('payee', 'Payée'),
        ('archivee', 'Archivée'),
        ('annulee', 'Annulée'),
    ], string='Etat de la commande', default="brouillon", required=True)

    client_id = fields.Many2one('compta.client', string='Client', required=True)

    ligne_commande_ids = fields.One2many('compta.ligne.commande', 'commande_id', string='Ligne de commande')
    
    facture_ids = fields.One2many('compta.facture', 'commande_id', string='Factures')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)


    # -------------------------- create -----------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numCommande') or vals['numCommande'] == 'Nouveau':
                vals['numCommande'] = self.env['ir.sequence'].next_by_code('compta.commande')
        return super().create(vals_list)


    # -------------------------------- check ------------------------------
    @api.onchange('montantTotal')
    def _check_positive(self):
        if self.montantTotal < 0:
            raise ValidationError('La valeur du montant total doit être positive')
        

    # ---------------------------------- compute ----------------------------
    @api.depends('ligne_commande_ids','ligne_commande_ids.qteTotalRessource')
    def _compute_montantTotal(self):
        self.montantTotal = sum(self.ligne_commande_ids.mapped(lambda ligne: ligne.ressource_id.prixUnitaire * ligne.qteTotalRessource))


    # ---------------------- actions ------------------------

    def action_confirmer(self):
        self.etatCommande = 'confirmee'
    
    def action_creer_facture(self):
        print("*--------------------------*", self.id, self.env.context)
        print("/***************************/")
        return {
            'name': 'Créer une facture pour la commande ' + self.numCommande,
            'type': 'ir.actions.act_window',
            'res_model': 'compta.facture',  # Model of the form to display in the modal
            'view_mode': 'form',
            'view_id': self.env.ref("comptabilite-client.view_facture_form_modal_create").id,
            'target': 'new',  # Opens in a new window (modal)
            'context': {'default_commande_id': self.id},  # Pass context values to the modal form
        }

    def action_archiver(self):
         self.etatCommande = 'archivee'
    
    def action_annuler(self):
         self.etatCommande = 'annulee'

    def action_commande(self):
        pass