from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'
    installation_id = fields.Many2one(comodel_name='selfconsumption.installation', string='Instalación')