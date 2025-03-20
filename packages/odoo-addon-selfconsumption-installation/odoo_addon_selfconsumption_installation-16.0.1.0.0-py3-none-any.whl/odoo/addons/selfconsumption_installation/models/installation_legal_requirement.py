from odoo import fields, models


class InstallationLegalRequirement(models.Model):
    _name = 'installation.legal.requirement'
    _description = 'Legal requirement asociated with an installation'

    installation_id = fields.Many2one(
        string='Installation',
        comodel_name='selfconsumption.installation',
        index=True,
        ondelete='cascade'
    )

    type = fields.Char(
        string='Type'
    )

    limit_date = fields.Date(
        string='Limit date'
    )

    response_date = fields.Date(
        string='Response date'
    )

    done = fields.Boolean(
        string='Done'
    )

    manager_id = fields.Many2one(
        string='Manager',
        comodel_name='hr.employee',
        index=True,
        ondelete='restrict'
    )

    notes = fields.Char(
        string='Notes'
    )

    installation_event_id = fields.Many2one(
        comodel_name='installation.event',
        ondelete='cascade'
    )

    def create(self, vals):
        res = super().create(vals)
        self.__create_or_update_requirement_event(res)
        return res

    def write(self, vals):
        res = super().write(vals)
        relevant_vals = {
            'limit_date',
            'done'
        }
        set_vals = set(vals)
        has_relevant_vals = relevant_vals.intersection(set_vals)
        if has_relevant_vals:
            self.__create_or_update_requirement_event(self)
        return res

    def unlink(self):
        for requierement in self:
            if requierement.installation_event_id and requierement.installation_event_id.exists():
                self.env['installation.event'].browse([requierement.installation_event_id.id]).unlink()
        super().unlink()

    def __create_or_update_requirement_event(self, requirement):
        if requirement.installation_event_id and not requirement.event_synced():
            requirement.installation_event_id.write({
                'start_date': requirement.limit_date,
                'end_date': requirement.limit_date
            })
        elif not requirement.installation_event_id:
            event = self.env['installation.event'].create({
                'installation_id': requirement.installation_id.id,
                'start_date': requirement.limit_date,
                'end_date': requirement.limit_date,
                'type': 'requerimiento'
            })
            requirement.installation_event_id = event.id

    def event_synced(self):
        if self.installation_event_id:
            start_date, end_date = self.installation_event_id.get_dates()
            return self.limit_date == start_date and self.limit_date == end_date
        return True

    def update_by_event(self, event):
        start_date, _ = event.get_dates()
        self.write({
            'limit_date': start_date
        })
