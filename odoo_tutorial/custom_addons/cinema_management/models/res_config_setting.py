from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ticket_price = fields.Integer(string="Ticket Price", config_parameter="cinema_management.ticket_price")