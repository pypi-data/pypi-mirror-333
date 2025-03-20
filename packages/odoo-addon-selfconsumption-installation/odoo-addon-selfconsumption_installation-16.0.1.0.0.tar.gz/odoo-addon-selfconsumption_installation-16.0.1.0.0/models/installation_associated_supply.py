from odoo import api, fields, models


class InstallationAssociatedSupply(models.Model):
    _name = "installation.associated.supply"
    _description = 'Installation Associated Supply'

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Contact"
    )

    installation_id = fields.Many2one(
        comodel_name="selfconsumption.installation",
        string="Installation"
    )

    firstname = fields.Char(string="Name", related='partner_id.firstname')
    lastname = fields.Char(string="Last name", related='partner_id.lastname')
    vat = fields.Char(string="vat", related='partner_id.vat')
    cups = fields.Char(string="CUPS")
    distribution_coefficient = fields.Float(string="Distribution coefficient")
    cadastral_reference = fields.Char(string="Cadastral reference")
    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier"
    )
    contracted_power = fields.Float(string="Contracted power (kW)")
    email = fields.Char(string="Email", related='partner_id.email')
    phone = fields.Char(string="Phone", related='partner_id.phone')
    personal_data_policy = fields.Boolean(
        string='Personal data policy',
        related='partner_id.personal_data_policy'
    )
    promotions = fields.Boolean(
        string="Promotions",
        related='partner_id.promotions'
    )

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        for record in res:
            record.compute_partner_parent_id()
        return res

    def write(self, vals):
        if 'partner_id' in vals:
            old_partner = self.partner_id
            res = super().write(vals)
            if old_partner:
                old_partner.write({'parent_id': None})
            self.compute_partner_parent_id
            return res
        return super().write(vals)

    def compute_partner_parent_id(self):
        if self.partner_id and self.installation_id and self.installation_id.partner_id:
            self.partner_id.write({'parent_id': self.installation_id.partner_id.id})
