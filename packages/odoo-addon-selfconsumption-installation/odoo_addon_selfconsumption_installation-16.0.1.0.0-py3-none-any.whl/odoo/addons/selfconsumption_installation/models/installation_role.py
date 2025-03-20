from odoo import api, fields, models, _
from odoo.exceptions import UserError


class InstallationRole(models.Model):
    _name = 'installation.role'
    _description = 'Roles y coordinadores'

    name = fields.Char(
        string='Rol')

    responsible_ids = fields.Many2many(
        comodel_name='res.users',
        string='Coordinadores')
