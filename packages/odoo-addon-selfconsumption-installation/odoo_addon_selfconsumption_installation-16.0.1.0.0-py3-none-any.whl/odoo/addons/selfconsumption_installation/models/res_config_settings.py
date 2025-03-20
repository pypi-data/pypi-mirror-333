from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    file_manager_tag = fields.Many2one(
        string='File manager Category',
        comodel_name='res.partner.category',
        ondelete='set null'
    )

    supplier_tag = fields.Many2one(
        string='Supplier Category',
        comodel_name='res.partner.category',
        ondelete='set null'
    )

    installer_tag = fields.Many2one(
        string='Installer Category',
        comodel_name='res.partner.category',
        ondelete='set null'
    )


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()

        params = self.env['ir.config_parameter'].sudo()
        file_manager_tag = params.get_param('file_manager_tag', default=False)
        supplier_tag = params.get_param('supplier_tag', default=False)
        installer_tag = params.get_param('installer_tag', default=False)
        res.update(
            file_manager_tag=int(file_manager_tag),
            supplier_tag=int(supplier_tag),
            installer_tag=int(installer_tag)
        )
        return res

    @api.model
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("file_manager_tag", self.file_manager_tag.id)
        self.env['ir.config_parameter'].sudo().set_param("supplier_tag", self.supplier_tag.id)
        self.env['ir.config_parameter'].sudo().set_param("installer_tag", self.installer_tag.id)
