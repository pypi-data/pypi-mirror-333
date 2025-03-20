from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    installation_id = fields.Many2one(comodel_name='selfconsumption.installation', string='Proyecto')