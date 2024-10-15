from odoo import api, fields, models, _

class ComptaRessource(models.Model):
    _name = 'compta.ressource'
    _description = 'Ressource'
    _rec_name = "libelle"

    codeRessource = fields.Char(string="Code de ressource", default="New")
    libelle = fields.Char(string="Libelle")
    prixUnitaire = fields.Integer(string="Prix unitaire")
    stock = fields.Integer(string="Stock")