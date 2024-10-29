from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ComptaFacture(models.Model):
    _name = 'compta.facture'
    _description = 'Facture'
    _rec_name = "numFacture"

    numFacture = fields.Char(string="Numéro de facture", default="Nouveau")
    dateFacture = fields.Date(string="Date du facture", required=True)
    montantTotalFacture = fields.Integer(string="Montant total de la facture", compute="_compute_montantTotal")
    etatFacture = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('envoyee', 'Envoyée'),
        ('cours', 'En cours de paiement'),
        ('payee', 'Payée'),
        ('annulee', 'Annulée')
    ], string='Etat de la facture', required=True, default='brouillon')

    commande_id = fields.Many2one('compta.commande', string='Commande', required=True, ondelete="cascade")

    ligne_facture_ids = fields.One2many('compta.ligne.facture', 'facture_id', string='Lignes de facture')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id.id)

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


    # -------------------------- create ---------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numFacture') or vals['numFacture'] == 'Nouveau':
                vals['numFacture'] = self.env['ir.sequence'].next_by_code('compta.facture')
        return super().create(vals_list)
    


    # -------------------------------------- check ----------------------------------
    @api.onchange('montantTotalFacture')
    def _check_positive(self):
        if self.montantTotalFacture < 0:
            raise ValidationError('La valeur du montant total doit être positive')

    # --------------------------- compute ------------------------------
    @api.depends('ligne_facture_ids', 'ligne_facture_ids.qteFacturee')
    def _compute_montantTotal(self):
        for record in self:
            for ligne in record.ligne_facture_ids:
                if not ligne.ligne_commande_id.check_qte_facturee():
                    raise ValidationError('On ne peut plus facturer le produit %s de ce nombre' % ligne.ressource_id.libelle)
            record.montantTotalFacture = sum(record.ligne_facture_ids.mapped(lambda ligne: ligne.ressource_id.prixUnitaire * ligne.qteFacturee))


    # ------------------------- actions ------------------------------
    def action_facture(self):
        print("*--------------------------*", self.env.context)
        return {
            'name': 'Créer une facture pour la commande',
            'type': 'ir.actions.act_window',
            'res_model': 'compta.facture',  # Model of the form to display in the modal
            'view_mode': 'form',
            'view_id': self.env.ref("comptabilite-client.view_facture_form_modal_modify").id,
            'target': 'new',  # Opens in a new window (modal)
            'res_id': self.id,
            'context': {'default_commande_id': self.commande_id.id},  # Pass context values to the modal form
        }