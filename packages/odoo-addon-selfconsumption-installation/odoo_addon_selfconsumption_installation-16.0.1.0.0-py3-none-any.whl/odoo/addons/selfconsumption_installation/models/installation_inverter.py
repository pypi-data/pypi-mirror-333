from odoo import api, fields, models

class InstallationInveter(models.Model):
    _name = 'installation.inverter'
    _description = 'Inverter asociated with an installation'

    installation_id = fields.Many2one(
        string = 'Installation',
        comodel_name='selfconsumption.installation',
        index=True,
        ondelete='cascade'
    )

    inverter_id = fields.Many2one(
        string = 'Model',
        comodel_name='photovoltaic.inverter',
        ondelete='cascade'
    )

    power = fields.Float(
        related='inverter_id.rated_power_ac',
        string='Power (kW)'
    )

    intensity=fields.Float(
        related='inverter_id.maximun_current_ac',
        string='Intensity'
    )

    serial_number=fields.Char(
        string='Serial number'
    )


