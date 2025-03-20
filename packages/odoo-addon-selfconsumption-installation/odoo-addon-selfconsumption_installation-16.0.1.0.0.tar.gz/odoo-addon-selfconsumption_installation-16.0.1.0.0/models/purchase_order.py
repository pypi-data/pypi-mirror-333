from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    installation_id = fields.Many2one(comodel_name='selfconsumption.installation', string='Proyecto')