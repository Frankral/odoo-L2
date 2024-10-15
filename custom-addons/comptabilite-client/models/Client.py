from odoo import api, fields, models, _

class ComptaClient(models.Model):
    _name = 'compta.client'
    _description = 'Client'
    _rec_name = "raisonSocial"

    numClient = fields.Char(string="Numéro client", default="New")
    raisonSocial = fields.Char(string="Raison social")
    adresse = fields.Char(string="Adresse")
    telephone = fields.Char(string="Numéro de téléphone")
    email = fields.Char(string="Email")
    montantDette = fields.Integer(string="Montant de dette")