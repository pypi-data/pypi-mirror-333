from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    installation_ids = fields.One2many(
        comodel_name='selfconsumption.installation',
        inverse_name='partner_id',
        string='Proyectos')

    installation_partner_count = fields.Integer(
        compute='_compute_installation_partner_count',
        string='Contador proyectos')

    installation_id = fields.Many2one(
        comodel_name='selfconsumption.installation',
        compute='_compute_active_installation',
        string='Proyecto activo',
        store=True,
        readonly=False)

    # Suministro

    supplier_id = fields.Many2one(
        comodel_name='res.partner',
        string='Distribuidor')
    partner_id2 = fields.Many2one(
        comodel_name='res.partner',
        string='Titular factura')
    partner_id2_name = fields.Char(
        string='Nombre titular')
    partner_id2_surname = fields.Char(
        string='Apellidos titular')
    partner_id2_vat = fields.Char(
        string='DNI titular')
    partner_id2_street = fields.Char(
        string='Dirección suministro')
    partner_id2_zip = fields.Char(
        string='CP suministro')
    partner_id2_comercial = fields.Char(
        string='Comercializadora')
    cups = fields.Char(
        string='CUPS')
    contract_power = fields.Float(
        string='Potencia contratada')
    energy_cost = fields.Float(
        string='Coste energia medio €/kWh')
    energy_cost_first_period = fields.Float(
        string='Coste de la energia - Periodo 1')
    energy_cost_second_period = fields.Float(
        string='Coste de la energia - Periodo 2')
    energy_cost_third_period = fields.Float(
        string='Coste de la energia - Periodo 3')
    annual_energy_consumed = fields.Integer(
        string='Energia consumida anual kWh/año')
    phase = fields.Selection([
        ('monophase', 'Monofásico'),
        ('threefase', 'Trifásico')],
        string='Fase')
    access_pricelist = fields.Char(
        string='Tarifa acceso')
    supply_autoproject = fields.Boolean(
        string='Suministro autoconsumo',
        compute='_compute_supply_selfconsumption')

    def _compute_supply_selfconsumption(self):
        for record in self:
            if record.parent_id.installation_id:
                record.supply_autoproject = True
            else:
                record.supply_autoproject = False

    @api.depends('installation_ids')
    def _compute_active_installation(self):
        for record in self:
            if record.installation_ids:
                record.installation_id = record.installation_ids[0]

    def _compute_installation_partner_count(self):
        for record in self:
            record.installation_partner_count = len(record.installation_ids)

    def action_view_installation_partner(self):
        return {
            'name': self.name,
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'selfconsumption.installation',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.installation_ids.ids)],
            'context': {'default_partner_id': self.id}
        }
    
    def action_view_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Partner Form',
            'res_model': 'res.partner',
            'view_mode': 'form',
            'view_id': self.env.ref('base.view_partner_form').id,
            'res_id': self.id,
            'target': 'current',
        }
