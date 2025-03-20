from odoo import fields, models


class InstallationElectricLine(models.Model):
    _name = 'installation.electric.line'
    _description = 'An electric line for a selfconsumption installation'

    type=fields.Selection(
        [
            ('ac', 'AC'),
            ('cc', 'CC')
        ],
        string='Line type'
    )
    
    lenght=fields.Float(
    string='Length'
    )
    channeling=fields.Char(
        string='Channeling'
    )
    permisible_intensity=fields.Float(
        string='Permisible intensity'
    )
    section=fields.Char(
        string='Section'
    )
    voltage_drop_percentage=fields.Float(
        string='Voltage drop (%)'
    )
    voltage_drop=fields.Float(
        string='Voltage drop (V)'
    )
    voltage=fields.Float(
        string='Voltage (V)'
    )
    wire_type=fields.Char(
        string='Wire type'
    )
    installation_id = fields.Many2one(
        comodel_name='selfconsumption.installation',
        string='Installation',
        ondelete='cascade')