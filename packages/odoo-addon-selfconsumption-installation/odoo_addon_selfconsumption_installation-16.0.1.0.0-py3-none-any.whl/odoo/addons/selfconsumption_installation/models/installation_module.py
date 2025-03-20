from odoo import api, fields, models

class InstallationModule(models.Model):
    _name = 'installation.module'
    _description = 'Module asociated with an installation'

    installation_id = fields.Many2one(
        string = 'Installation',
        comodel_name='selfconsumption.installation',
        index=True,
        ondelete='cascade'
    )

    module_id = fields.Many2one(
        string='Model',
        comodel_name='photovoltaic.module',
        ondelete='cascade'
    )

    power = fields.Float(
        string='Power (W)',
        related='module_id.power'
    )

    intensisty = fields.Float(
        string='Intensity',
        related='module_id.max_current'
    )

    number_of_modules = fields.Integer(
        string='Nº of modules'
    )

