from odoo import api, fields, models


class InstallationTypeCover(models.Model):
    _name = 'installation.type.cover'
    _description = 'Tipo cubierta'

    name = fields.Char(
        string='Nombre')


class InstallationTypeAnchorage(models.Model):
    _name = 'installation.type.anchorage'
    _description = 'Tipo anclaje'

    name = fields.Char(
        string='Nombre')


class InstallationTypeStructure(models.Model):
    _name = 'installation.type.structure'
    _description = 'Tipo estructura'

    name = fields.Char(
        string='Nombre')
