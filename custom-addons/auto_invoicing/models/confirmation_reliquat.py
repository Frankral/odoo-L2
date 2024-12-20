from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError

class ConfirmationReliquat(models.TransientModel):
    _inherit = "stock.backorder.confirmation"

    def confirm_reliquat(self):
        for record in self:
            record.process()
            if len(record.pick_ids) > 0: 
                record.pick_ids[0].create_invoice()