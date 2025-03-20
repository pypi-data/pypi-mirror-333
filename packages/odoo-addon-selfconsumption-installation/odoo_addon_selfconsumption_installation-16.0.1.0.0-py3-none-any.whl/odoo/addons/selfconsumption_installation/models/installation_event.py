from odoo import fields, models, api

class InstallationEvent(models.Model):
    _name = 'installation.event'
    _description = 'A calendar event of a selfconsumption installation'

    name = fields.Char(
        string='name',
        compute='_compute_name',
        store=False
    )
    installation_id = fields.Many2one(
        comodel_name='selfconsumption.installation',
        string='Installation',
        ondelete='cascade')
    start_date = fields.Datetime(
        string='Start date')
    end_date = fields.Datetime(
        string='End date')
    type = fields.Selection(
        [
            ('replanteo', 'Replanteo'),
            ('obra', 'Obra'),
            ('requerimiento', 'Requerimiento'),
            ('irve', 'IRVE')
        ],
        string='Type')

    requierement_ids = fields.One2many(
        comodel_name='installation.legal.requirement',
        inverse_name='installation_event_id',
        invisible=True
    )

    def write(self, vals):
        res = super().write(vals)
        if self.installation_id:
            installation = self.env['selfconsumption.installation'].browse([self.installation_id.id])
            if not self._installation_synced(installation):
                installation.update_installation_by_event(self)
            for requirement in self.requierement_ids:
                if not requirement.event_synced():
                    requirement.update_by_event(self)
        return res

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        if res.installation_id:
            installation = self.env['selfconsumption.installation'].browse([res.installation_id.id])
            if not res._installation_synced(installation):
                installation.update_installation_by_event(res)
        return res

    def _installation_synced(self, installation):
        if self.type == 'obra':
            return installation.construction_dates_synced(self)
        elif self.type == 'irve':
            return installation.irve_dates_synced(self)
        elif self.type == 'replanteo':
            return installation.stakeout_dates_synced(self)
        return True

    def unlink(self):
        for event in self:
            events = self.env['installation.event'].search([
                ('installation_id', '=', event.installation_id.id),
                ('type', '=', event.type), ('id', '!=', event.id)
            ])
            event_type = event.type
            installation = event.installation_id
            super(InstallationEvent, event).unlink()
            if not events:
                if event_type == 'obra':
                    installation.write({'construction_start_date': None, 'construction_end_date': None})
                elif event_type == 'replanteo':
                    installation.write({'stake_out_date': None})
                elif event_type == 'irve':
                    installation.write({
                        'irve_execution_date': None,
                        'irve_execution_end_date': None
                    })
            else:
                installation.update_installation_by_event(events[0])

    def update_event_by_installation(self, installation):
        if self.type == 'obra':
            self.update_construction_event_by_installation(installation)
        elif self.type == 'replanteo':
            self.update_stakeout_event_by_installation(installation)
        elif self.type == 'irve':
            self.update_irve_event_by_installation(installation)

    def update_construction_event_by_installation(self, installation):
        start_date, end_date = installation.get_construction_dates()
        self.write({
            'start_date': fields.Datetime.to_datetime(start_date),
            'end_date': fields.Datetime.to_datetime(end_date)
        })

    def update_stakeout_event_by_installation(self, installation):
        self.write({
            'start_date': installation.stake_out_date,
            'end_date': fields.Datetime.add(installation.stake_out_date, hours=1)
        })

    def update_irve_event_by_installation(self, installation):
        start_date, end_date = installation.get_irve_dates()
        self.write({
            'start_date': fields.Datetime.to_datetime(start_date),
            'end_date': fields.Datetime.to_datetime(end_date)
         })

    def _compute_name(self):
        for record in self:
            if record.type == 'obra':
                record.name = record._compute_construction_name()
            elif record.type == 'irve':
                record.name = record._compute_irve_name()
            elif record.type == 'replanteo':
                record.name = record._compute_stakeout_name()
            elif record.type == 'requerimiento':
                record.name = record._compute_requirement_name()

    def _compute_construction_name(self):
        return f'{self.installation_id.name} - Obra'

    def _compute_stakeout_name(self):
        return f'{self.installation_id.name} - Replanteo'

    def _compute_irve_name(self):
        return f'{self.installation_id.name} - IRVE - {self.installation_id.irve_installer_id.name}'

    def _compute_requirement_name(self):
        if self.requierement_ids:
            requirement = self.requierement_ids[0]
            return f'{requirement.installation_id.name} - Requerimiento - {requirement.type}{" (Hecho)" if requirement.done else ""}'
        return f'{self.installation_id.name} - Requerimiento'

    def get_dates(self):
        start_date = fields.Date.to_date(self.start_date)
        end_date = fields.Date.to_date(self.end_date)
        return start_date, end_date
