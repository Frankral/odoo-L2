from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


class ConfirmationSms(models.TransientModel):
    _inherit = "confirm.stock.sms"

    def confirm_sms(self):
        for record in self:
            record.send_sms()
            if len(record.pick_ids) > 0:
                record.pick_ids[0].create_invoice()

    def not_confirm_sms(self):
        for record in self:
            record.dont_send_sms()
            if len(record.pick_ids) > 0:
                record.pick_ids[0].create_invoice()