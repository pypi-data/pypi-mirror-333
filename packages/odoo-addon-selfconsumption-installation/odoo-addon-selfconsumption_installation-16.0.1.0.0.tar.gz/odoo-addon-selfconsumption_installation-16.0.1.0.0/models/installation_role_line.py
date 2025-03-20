from odoo import fields, models

class InstallationRoleLine(models.Model):
    _name = 'installation.role.line'
    _description = 'Installation Role Line'

    role_id = fields.Many2one(
        comodel_name='installation.role',
        string='Rol')

    responsible_candidates_ids = fields.Many2many(related='role_id.responsible_ids')

    responsible_ids = fields.Many2many(
        comodel_name='res.users',
        string='Coordinadores')

    installation_id = fields.Many2one(
        comodel_name='selfconsumption.installation',
        string='Instalación')


