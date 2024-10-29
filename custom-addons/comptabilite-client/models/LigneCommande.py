from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class ComptaLigneCommande(models.Model):
    _name = 'compta.ligne.commande'
    _description = 'Ligne de commande'
    _rec_name = "name_field"
    _rec_names_search  = ["numLigneCommande", "ressource_id"]
    
    numLigneCommande = fields.Char(string="Numéro de ligne de commande", default="Nouvelle ligne")
    qteTotalRessource = fields.Float(string="Quantité totale de ressource", required=True)
    qteTotalFacturee = fields.Float(string="Quantité totale facturée", required=True, default=0, compute="_compute_qte_facturee")

    commande_id = fields.Many2one('compta.commande', string="Commande", required=True, ondelete="cascade")
    ressource_id = fields.Many2one('compta.ressource', string="Ressource", required=True)

    ligne_facture_ids = fields.One2many('compta.ligne.facture', 'ligne_commande_id', string='Ligne de facture')

    unite = fields.Char(string="Unité", compute="_compute_unite")

    name_field = fields.Char(string="Nom", compute='_compute_fields_combination')

    # previous_total_facturee = fields.Float(compute='_compute_previous_total_facturee', store=True)

    ressource_stock = fields.Float(related='ressource_id.stock')
    
    # ------------------------------- create ---------------------------- 
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('numLigneCommande') or vals['numLigneCommande'] == 'Nouveau':
                vals['numLigneCommande'] = self.env['ir.sequence'].next_by_code('compta.ligne.commande')
        return super().create(vals_list)
    

    # ---------------------------- check --------------------------------
    @api.onchange('qteTotalRessource', 'qteTotalFacturee')
    def _check_positive(self):
        if self.qteTotalRessource < 0:
            raise ValidationError('La valeur de la quantite totale de ressource doit être positive')
        if self.qteTotalFacturee < 0:
            raise ValidationError('La valeur de la quantite facturée de ressource doit être positive')
    
    def check_qte_facturee(self):
        for record in self:
            total = sum(record.ligne_facture_ids.mapped('qteFacturee'))
            if total > record.qteTotalRessource:
                return False
            return True
            


    # -------------------- compute --------------------------
    @api.depends("numLigneCommande", "ressource_id")
    def _compute_fields_combination(self):
        for record in self:
            libelle = record.ressource_id.libelle
            record.name_field = f"{record.numLigneCommande} - {libelle}"
    
    @api.depends("qteTotalRessource")
    def _compute_qteTotalRessource_unite(self):
        self.qteTotalRessource_unite = f"{self.qteTotalRessource} {self.ressource_id.unite}"
    
        
    @api.depends("ressource_id")
    def _compute_unite(self):
        for record in self:
            record.unite = record.ressource_id.unite
    
    @api.depends("ligne_facture_ids", "ligne_facture_ids.qteFacturee", "ligne_facture_ids.commande_id")
    def _compute_qte_facturee(self):
        for record in self:
            total = sum(record.ligne_facture_ids.mapped('qteFacturee'))
            record.qteTotalFacturee = total