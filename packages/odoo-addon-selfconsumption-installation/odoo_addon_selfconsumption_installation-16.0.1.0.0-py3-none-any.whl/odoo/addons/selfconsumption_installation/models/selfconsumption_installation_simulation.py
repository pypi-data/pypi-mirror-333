from odoo import api, fields, models
import logging

class SelfconsumptionInstallationSimulator(models.Model):
    _name = 'selfconsumption.installation.simulator'
    _description = 'Simulación proyecto'
    _rec_name = 'blueprint'

    active = fields.Boolean(default=True)
    installation_id = fields.Many2one(
        comodel_name='selfconsumption.installation',
        string='Proyecto',
        index=True,
        ondelete='cascade')
    blueprint = fields.Char(
        string='Anteproyecto',
        required=True)
    rated_power_simulation = fields.Float(
        string='Potencia nominal (W)',
        compute='_compute_rated_power',
        store=True)
    peak_power_simulation = fields.Float(
        string='Potencia pico (W)',
        compute='_compute_peak_power',
        store=True)
    energy_consumed = fields.Float(
        string='Energía consumida kWh/año')
    generator_energy = fields.Float(
        string='Energía generador')
    self_consumption = fields.Float(
        string='Consumo propio %')
    solar_cover = fields.Float(
        string='Cobertura solar')
    annual_perfomance = fields.Float(
        string='Rendimiento anual')
    shading = fields.Float(
        string='Sombreado %')
    co2_avoided = fields.Float(
        string='CO2 evitado')
    pvsol_notes = fields.Text(
        string='Notas pvsol')

    inverter_ids = fields.One2many(
        comodel_name='selfconsumption.installation.simulator.inverter',
        inverse_name='simulation_id',
        string='Inverters')
    
    module_ids = fields.One2many(
        comodel_name='selfconsumption.installation.simulator.module',
        inverse_name='simulation_id',
        string='Modules')

    @api.depends('inverter_ids')
    def _compute_rated_power(self):
        self.rated_power_simulation = sum(inverter.power for inverter in self.inverter_ids)

    @api.depends('module_ids')
    def _compute_peak_power(self):
        self.peak_power_simulation = sum(module.power*module.number_of_modules for module in self.module_ids)/1000


class SelfconsumptionInstallationSimulatorInverter(models.Model):
    _name = 'selfconsumption.installation.simulator.inverter'
    _description = 'Inverter asociated with a simulaiton'

    simulation_id = fields.Many2one(
        string = 'Simulation',
        comodel_name='selfconsumption.installation.simulator',
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

class SelfconsumptionInstallationSimulatorModule(models.Model):
    _name = 'selfconsumption.installation.simulator.module'
    _description = 'Module asociated with a simulaiton'

    simulation_id = fields.Many2one(
        string = 'Simulation',
        comodel_name='selfconsumption.installation.simulator',
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

    number_of_modules = fields.Integer(
        string='Nº of modules'
    )