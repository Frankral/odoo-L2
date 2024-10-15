from odoo import api, fields, models, _

class ComptaJustificatif(models.Model):
    _name = 'compta.justificatif'
    _description = 'Justificatif'
    _rec_name = "numJustificatif"

    numJustificatif = fields.Char(string="Numéro justificatif", default="New")
    dateJustificatif = fields.Char(string="Date du justificatif")
    montantJustificatif = fields.Char(string="Montant du justificatif")