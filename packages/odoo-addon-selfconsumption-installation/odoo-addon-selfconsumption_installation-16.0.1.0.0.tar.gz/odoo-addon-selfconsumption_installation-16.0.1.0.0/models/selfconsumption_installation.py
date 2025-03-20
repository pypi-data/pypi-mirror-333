from odoo import api, fields, models


class SelfconsumptionInstallation(models.Model):
    _name = "selfconsumption.installation"
    _description = 'Selfconsumption Installation'
    _inherit = ['mail.thread']

    name = fields.Char(string="Name")

    status = fields.Selection(
        [
            ("active", "Active"),
            ("deactivated", "Deactivated"),
            ("executed", "executed"),
            ("in-service", "In service"),
        ],
        string="Status",
        tracking=True,
    )

    project = fields.Many2one(comodel_name="project.project", string="Project")

    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        auto_join=True,
        tracking=True,
        domain="[\
            '|',\
            ('company_id', '=', False),\
            ('company_id', '=', company_id)\
        ]",
    )

    # Proyecto
    code = fields.Char(string="Código")

    installer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Instalador",
        domain="[('supplier_rank','>', 1)]",
    )

    # Recuired computed field to allow filtering by config value in domain
    installer_tag = fields.Many2one(
        comodel_name="res.partner.category",
        compute="_compute_installer_tag",
        store=False,
    )

    surge = fields.Selection(
        [
            ("o3", "O3"),
            ("lre", "LRE"),
            ("ims", "IMS"),
            ("org", "ORG"),
            ("eru", "ERU"),
            ("col", "COL"),
        ],
        string="Oleada",
    )
    activation_date = fields.Date(string="Fecha activación")
    lead_code = fields.Char(string="Código lead")

    project_phase = fields.Char(string="Fase proyecto")

    typology = fields.Selection(
        [("individual", "Individual"), ("collective", "Collective")],
        string="Typology"
    )

    subgroup = fields.Char(string="Subgroup")

    model_shortlisted = fields.Char(string="Modelo preelegido")

    power_shortlisted = fields.Integer(string="Potencia preelegida (kW)")

    notes_shortlisted = fields.Text(string="Notas proyecto")

    maintenance_contact = fields.Many2one(
        comodel_name="res.partner", string="Maintenance contact"
    )

    # suministro
    supplier_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier"
    )

    # Recuired computed field to allow filtering by config value in domain
    supplier_tag = fields.Many2one(
        comodel_name="res.partner.category",
        compute="_compute_supplier_tag",
        store=False,
    )
    partner_id2 = fields.Many2one(
        comodel_name="res.partner",
        string="Titular factura"
    )
    partner_id2_name = fields.Char(string="Nombre titular")
    partner_id2_surname = fields.Char(string="Apellidos titular")
    partner_id2_vat = fields.Char(string="DNI titular")
    supply_street = fields.Char(string="Dirección suministro")
    supply_zip = fields.Char(string="CP suministro")
    supply_state = fields.Char(string="Supply state")
    supply_region = fields.Char(string="Supply region")
    supply_municipality = fields.Char(string="Supply municipality")
    supply_comercial = fields.Char(string="Comercializadora")
    cups = fields.Char(string="CUPS")
    contract_power = fields.Float(string="Potencia contratada")
    energy_cost = fields.Float(string="Average energy cost €/kWh")
    fixed_toll_cost = fields.Float(string="Fixed toll cost €/Kw.day")
    annual_energy_consumed = fields.Integer(
        string="Energia consumida anual kWh/año"
    )
    phase = fields.Selection(
        [("monophase", "Monofásico"), ("threefase", "Trifásico")],
        string="Fase"
    )
    access_pricelist = fields.Char(string="Tarifa acceso")
    bill_recieved = fields.Boolean(string="Electric Bill Recieved")

    # ubicación
    stake_out_date = fields.Datetime("Fecha de replanteo")
    installation_address = fields.Char(string="Dirección instalación")
    installation_zip = fields.Char(string="CP instalación")
    installation_city = fields.Char(string="Municipio instalación")
    estimated_inclination = fields.Integer("Inclinación estimada")
    cover_type_id = fields.Many2one(
        comodel_name="installation.type.cover", string="Tipo cubierta"
    )
    gmaps_address = fields.Char("Dirección Gmaps")
    gmaps_link = fields.Char("Google maps link")
    catastral = fields.Char(string="Catastro")
    utm_coords = fields.Char(string="Coordenadas UTM")
    location_notes = fields.Text(string="Notas ubicación")
    roof_height = fields.Char(string="Roof height")
    stake_out_completed = fields.Boolean(string="Stakeout completed")
    heritage_protection = fields.Boolean(string="Heritage protection")

    # Simulacion
    project_simulation_ids = fields.One2many(
        comodel_name="selfconsumption.installation.simulator",
        inverse_name="installation_id",
        string="Simulaciones",
    )

    # Ejecución
    blueprint_chosen = fields.Many2one(
        comodel_name="selfconsumption.installation.simulator",
        string="Anteproyecto elegido",
    )
    rated_power_execution = fields.Float(
        string="Potencia nominal (W)",
        compute="_compute_rated_power",
        store=True
    )
    peak_power_execution = fields.Float(
        string="Potencia pico (W)", compute="_compute_peak_power", store=True
    )
    cover_type_execution_id = fields.Many2one(
        comodel_name="installation.type.cover", string="Tipo cubierta"
    )
    anchorage_type = fields.Many2one(
        comodel_name="installation.type.anchorage", string="Tipo anclaje"
    )
    structure_type = fields.Many2one(
        comodel_name="installation.type.structure", string="Tipo estructura"
    )
    structure_inclination = fields.Char(string="Structure inclination")
    structure_orientation = fields.Char(string="Structure orientation")
    cover_extra_info = fields.Char(string="Others")
    structure = fields.Char(string="Structure model")
    civil_construction = fields.Char(string="Obra civil")
    media_aux = fields.Char(string="Medios auxiliares")
    extra_element_1 = fields.Char(string="Elemento extra 1")
    extra_element_2 = fields.Char(string="Elemento extra 2")
    extra_element_3 = fields.Char(string="Elemento extra 3")
    design_notes = fields.Text(string="Notas diseño")
    construction_start_date = fields.Date(string="Fecha inicio obra")
    construction_end_date = fields.Date(string="Fecha fin obra")
    construction_address = fields.Char(string="Construction address")
    mains_voltage = fields.Char(string="Mains voltage")
    gcp_location = fields.Char(string="GCP Location")
    gcp_fuse_rated_current = fields.Float(string="Fuse rated current")
    gcp_lga_section = fields.Float(string="LGA section")
    gcp_fuseholder_type = fields.Char(string="Fuseholder type")
    gcp_general_switch = fields.Char(string="General Switch")
    dc_safety_fuse = fields.Char(string="DC Safety fuse")
    dc_fuseholder_type = fields.Char(string="DC fuseholder type")
    pv_line_meter_type = fields.Char(string="Meter type")
    pv_line_meter_sn = fields.Char(string="Meter serial number")
    pv_safety_fuse = fields.Char(string="PV Safety fuse")
    pv_disconectors = fields.Char(string="PV disconectors")
    pv_registrar_number = fields.Char(string="Registrar number")

    nature_of_supply = fields.Char(string="Nature of supply")
    new_or_expansion = fields.Selection(
        [("new", "New"), ("expansion", "Expansion")], string="New or expansion"
    )
    line_ids = fields.One2many(
        comodel_name="installation.electric.line",
        inverse_name="installation_id",
        string="Electric lines",
    )

    inverter_ids = fields.One2many(
        comodel_name="installation.inverter",
        inverse_name="installation_id",
        string="Inverters",
    )

    module_ids = fields.One2many(
        comodel_name="installation.module",
        inverse_name="installation_id",
        string="Modules",
    )
    cnmc_connection_type = fields.Char(string="CNMC Connection type")
    installation_typology_execution = fields.Char(
        string="Installation typology"
    )
    monitorization_email = fields.Char(string="Email")
    monitorization_password = fields.Char(string="Password")
    monitorization_public_link = fields.Char(string="Public link")
    zero_injection = fields.Boolean(string="0 Injection")
    supply_connection = fields.Selection(
        [("BT", "BT"), ("AT", "AT")], string="Supply connection"
    )

    week_construction = fields.Integer(
        string="Semana de obra",
        compute="_compute_construction_week",
        store=True
    )
    investor_serial_number = fields.Char(string="Número de serie del inversor")

    # Licencia/Ayuntamiento
    license_type = fields.Char(string="Tipo permiso")
    requested_by = fields.Char(string="Licencia solicitada por")
    presented_date = fields.Date(string="Fecha presentación")
    file_number = fields.Char(string="Número expediente")
    license_concession = fields.Date(string="Fecha concesión")
    bonification = fields.Selection(
        [("no", "No"), ("yes", "Yes"), ("yes-presented", "Yes, presented")],
        string="Bonification (ICIO)",
    )
    icio_bonification_requested_by = fields.Selection(
        [
            ("ecooo", "Ecooo"),
            ("client", "Client"),
            ("not-needed", "Not needed")
        ],
        string="ICIO requested by",
    )
    pay_taxes = fields.Selection(
        [
            ("ecooo", "Ecooo"),
            ("participant", "Participante"),
            ("other", "Otro")
        ],
        string="Quien paga tasas",
    )
    license_notes = fields.Text(string="Notas licencia")
    ovp_request = fields.Selection(
        [("yes", "Yes"), ("no", "No"), ("not-needed", "Not needed")],
        string="Request OVP",
    )
    ovp_request_date = fields.Date(string="OVP request date")
    ovp_approval_date = fields.Date(string="OVP approval date")
    ovp_ammount = fields.Monetary(string="OVP ammount")
    end_of_work_notified = fields.Boolean(string="End of work notified")
    customer_shipments = fields.Char(string="Customer shipment")
    ibi_bonification_requested_by = fields.Selection(
        [
            ("ecooo", "Ecooo"),
            ("client", "Client"),
            ("not-needed", "Not needed")
        ],
        string="IBI requested by",
    )
    ibi_bonification_request_date = fields.Date(string="Request date")
    ibi_bonification = fields.Boolean(string="Concession")
    legal_requirements_ids = fields.One2many(
        comodel_name="installation.legal.requirement",
        inverse_name="installation_id",
        string="Legal requirement",
    )

    # Needed for monetary fields
    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="company_id.currency_id",
        string="Currency",
        readonly=True,
    )

    # Subvención
    subvention_selection = fields.Selection(
        [("yes", "Si"), ("no", "No")], string="Solicita subvención"
    )
    subvention_type = fields.Char(string="Tipo subvención")
    subvention_request_date = fields.Date(string="Fecha solicitud")
    file_number_subvention = fields.Char(string="Número expediente")
    subvention_requirement_date = fields.Date(string="Fecha requerimientos")
    subvention_response_date = fields.Date(string="Respuesta requerimiento s")
    subvention_concession = fields.Date(string="Fecha concesión subv")
    subvention_funds_approval_date = fields.Date(string="Funds approval date")
    subvention_justification_deadline = fields.Date(
        string="Justification deadline"
    )
    subvention_justification_submission_date = fields.Date(
        string="Justification submission date"
    )
    subvention_notes = fields.Text(string="Notas subvención")

    # Tramitación
    cau = fields.Char(string="CAU")
    file_number_processing = fields.Char(string="File number processing")
    aditional_files = fields.Char(string="Old, closed or additional files")
    management_contact = fields.Many2one(
        comodel_name="res.partner", string="Management Contact"
    )

    management_contact_tag = fields.Many2one(
        comodel_name="res.partner.category",
        compute="_compute_management_contact_tag",
        store=False,
    )

    technical_conditions = fields.Selection(
        [("yes", "Yes"), ("no", "No"), ("not-needed", "No, not needed")],
        string="Technical and economic conditions",
    )
    cta = fields.Selection(
        [("yes", "Yes"), ("no", "No"), ("not-needed", "No, not needed")],
        string="CTA and close",
    )
    approval_number = fields.Char(string="Nº of approval")
    approval_date = fields.Date(string="Date of approval")
    periodic_inspection = fields.Boolean(string="Periodic inspection")
    installer_send_date = fields.Date(string="Installer send date")
    registry_send_date = fields.Date(string="Registry send date")
    cie_resgistry_date = fields.Date(string="CIE registry date")
    inspection_date = fields.Date(string="Inspection date")
    cie_registry_state = fields.Selection(
        [
            ("awaintin_customer", "Awaiting customer"),
            ("awaiting_installer", "Awaiting installer"),
            ("in_process", "In process"),
            ("completed", "Completed"),
        ],
        string="CIE registry state",
    )
    documentation_sent = fields.Boolean(string="Documentation sent")
    meter_verification = fields.Date(string="Meter verified")

    transaction_notes = fields.Text(string="Notas tramitación")

    # IRVE
    irve_execution_date = fields.Date(string="IRVE execution date")
    irve_execution_end_date = fields.Date(string="IRVE execution end date")
    irve_installer_id = fields.Many2one(
        comodel_name="res.partner",
        string="IRVE installer",
        domain="[('supplier_rank','>', 1)]",
    )
    irve_line_ids = fields.One2many(
        comodel_name="installation.electric.line",
        inverse_name="installation_id",
        string="Electric lines",
    )

    # Associated supplies

    representative_id = fields.Many2one(
        comodel_name="res.partner",
        string="Representative"
    )

    distribution_coefficient_sum = fields.Float(
        string="Total distribution coefficient",
        compute="_compute_distribution_coefficient_sum"
    )

    total_associated_supplies = fields.Integer(
        string='Total associated supplies',
        compute='_compute_total_associated_supplies'
    )

    associated_supply_ids = fields.One2many(
        comodel_name="installation.associated.supply",
        inverse_name="installation_id",
        string="Associated supplies"
    )

    # Hitos
    first_milestone_payed = fields.Boolean(string="First milestone payed")
    personalized_studies = fields.Boolean(string="Personalized studies")
    documentation_delivered = fields.Boolean(string="Documentation delivered")
    draft_ready_for_submission = fields.Boolean(
        string="Draft ready for submission"
    )
    draft_sent = fields.Boolean(string="Draft sent")
    draft_sent_date = fields.Date(string="Draft sent date")
    contract_signed = fields.Boolean(string="Contract signed")
    payment_method_chosen = fields.Boolean(string="Payment method chosen")
    distribution_agreement_signed = fields.Boolean(
        string="Distribution agreement signed"
    )
    second_milestone_payed = fields.Boolean(string="Second milestone payed")
    third_milestone_payed = fields.Boolean(string="Third milestone payed")
    fourth_milestone_payed = fields.Boolean(string="Fourth milestone payed")
    payment_date = fields.Date(string="Payment date")
    representation_letter_received = fields.Boolean(
        string="Representation letter recieved"
    )
    construction_scheduled = fields.Boolean(
        string="Scheduled", compute="_compute_construction_scheduled"
    )
    installation_date_confirmed = fields.Boolean(
        string="Installation date confirmed"
    )
    responsible_statement_presented = fields.Boolean(
        string="Responsible statement presented",
        compute="_compute_responsible_statement_presented",
    )
    installation_date_reminder = fields.Boolean(
        string="Installation date reminder"
    )
    end_of_work_completed = fields.Boolean(string="End of work completed")
    client_documentation_sent = fields.Boolean(
        string="Client documentation sent"
    )
    payment_pending = fields.Boolean(string="Payment pending")
    notification_one_month_after_execution = fields.Boolean(
        string="Notifaction one month after execution"
    )
    notification_one_year_after_execution = fields.Boolean(
        string="Notifaction one year after execution"
    )
    notification_warranty_expired = fields.Boolean(
        string="Notifaction warranty expired"
    )
    irve_restated = fields.Boolean(string="IRVE restated")
    irve_scheduled = fields.Boolean(
        string="IRVE scheduled",
        compute="_compute_irve_scheduled"
    )
    irve_executed = fields.Boolean(string="IRVE executed")
    irve_billed = fields.Boolean(string="IRVE billed")
    irve_processing_status = fields.Selection(
        [
            ("awaintin_customer", "Awaiting customer"),
            ("awaiting_installer", "Awaiting installer"),
            ("in_process", "In process"),
            ("completed", "Completed"),
        ],
        string="IRVE processing status",
    )

    sale_order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="installation_id",
        string="Pedidos de venta",
    )
    purchase_order_ids = fields.One2many(
        comodel_name="purchase.order",
        inverse_name="installation_id",
        string="Pedidos de compra",
    )

    invoice_ids = fields.One2many(
        comodel_name="account.move",
        inverse_name="installation_id",
        string="Facturas"
    )

    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account", string="Analytic account"
    )

    sale_orders_count = fields.Integer(
        string="Pedidos de venta", compute="_compute_sale_orders"
    )
    purchase_orders_count = fields.Integer(
        string="Pedidos de compra", compute="_compute_purchase_orders"
    )
    invoices_count = fields.Integer(
        string="Facturas",
        compute="_compute_invoices"
    )

    role_ids = fields.One2many(
        comodel_name="installation.role.line",
        inverse_name="installation_id",
        string="Roles",
    )

    def _compute_sale_orders(self):
        for record in self:
            record.sale_orders_count = len(record.sale_order_ids)

    def _compute_purchase_orders(self):
        for record in self:
            record.purchase_orders_count = len(record.purchase_order_ids)

    def _compute_invoices(self):
        for record in self:
            record.invoices_count = len(record.invoice_ids)

    @api.depends("construction_start_date")
    def _compute_construction_scheduled(self):
        for record in self:
            record.construction_scheduled = (
                True if record.construction_start_date else False
            )

    @api.depends("construction_start_date")
    def _compute_construction_week(self):
        for record in self:
            record.week_construction = (
                record.construction_start_date.isocalendar()[1]
                if record.construction_start_date
                else False
            )

    @api.onchange("partner_id2")
    def _onchange_partner_id2(self):
        if self.partner_id2:
            self.partner_id2_name = self.partner_id2.firstname or self.partner_id2.name
            self.partner_id2_surname = self.partner_id2.lastname
            self.partner_id2_vat = self.partner_id2.vat
            self.supply_street = self.partner_id2.street
            self.supply_zip = self.partner_id2.zip

    @api.depends("presented_date")
    def _compute_responsible_statement_presented(self):
        for record in self:
            record.responsible_statement_presented = (
                True if record.presented_date else False
            )

    @api.depends("inverter_ids")
    def _compute_rated_power(self):
        self.rated_power_execution = sum(
            inverter.power for inverter in self.inverter_ids
        )

    @api.depends("module_ids")
    def _compute_peak_power(self):
        self.peak_power_execution = (
            sum(module.power * module.number_of_modules for module in self.module_ids)
            / 1000
        )

    def _compute_management_contact_tag(self):
        self.management_contact_tag = int(
            self.env["ir.config_parameter"].sudo().get_param("file_manager_tag")
        )

    def _compute_supplier_tag(self):
        self.supplier_tag = int(
            self.env["ir.config_parameter"].sudo().get_param("supplier_tag")
        )

    def _compute_installer_tag(self):
        self.installer_tag = int(
            self.env["ir.config_parameter"].sudo().get_param("installer_tag")
        )

    @api.depends("irve_execution_date", "irve_execution_end_date")
    def _compute_irve_scheduled(self):
        for record in self:
            record.irve_scheduled = record.irve_execution_date and record.irve_execution_end_date

    @api.depends('associated_supply_ids.distribution_coefficient')
    def _compute_distribution_coefficient_sum(self):
        for record in self:
            distribution_coefficient_sum = 0
            for associated_supply in record.associated_supply_ids:
                distribution_coefficient_sum += associated_supply.distribution_coefficient
            record.distribution_coefficient_sum = distribution_coefficient_sum

    @api.depends('associated_supply_ids')
    def _compute_total_associated_supplies(self):
        for record in self:
            record.total_associated_supplies = len(record.associated_supply_ids)

    def write(self, vals):
        res = super().write(vals)
        event_fields = {
            "construction_start_date",
            "construction_end_date",
            "irve_execution_date",
            "irve_execution_end_date",
            "construction_end_date",
            "stake_out_date",
        }
        set_vals = set(vals)
        event_fields_modified = event_fields.intersection(set_vals)
        if event_fields_modified:
            self._create_or_update_installation_event()
        if 'partner_id' in vals:
            for associated_supply in self.associated_supply_ids:
                associated_supply.compute_partner_parent_id()
        return res

    def action_view_sale_orders(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Pedidos de venta",
            "view_mode": "tree,form",
            "res_model": "sale.order",
            "domain": [("id", "in", self.sale_order_ids.ids)],
            "context": "{'create': False}",
        }

    def action_view_purchase_orders(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Pedidos de compra",
            "view_mode": "tree,form",
            "res_model": "purchase.order",
            "domain": [("id", "in", self.purchase_order_ids.ids)],
            "context": "{'create': False}",
        }

    def action_view_invoices(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Facturas",
            "view_mode": "tree,form",
            "res_model": "account.move",
            "domain": [("id", "in", self.invoice_ids.ids)],
            "context": "{'create': False}",
        }

    def action_view_customer(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Customer",
            "view_mode": "form",
            "res_model": "res.partner",
            "res_id": self.partner_id.id,
        }

    def action_view_analytic_account(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Analytic account",
            "view_mode": "tree",
            "res_model": "account.analytic.line",
            "domain": [("account_id", "=", self.analytic_account_id.id)],
            "context": {
                "search_default_group_date": 1,
                "default_account_id": self.analytic_account_id.id,
            },
            "view_id": self.env.ref("analytic.view_account_analytic_line_tree").id,
        }

    def _create_or_update_installation_event(self):
        self._create_or_update_construction_event()
        self._create_or_update_stakeout_event()
        self._create_or_update_irve_event()

    def _create_or_update_construction_event(self):
        construction_event = self._find_construction_event()

        if self._execution_scheduled():
            if construction_event and not self.construction_dates_synced(
                construction_event
            ):
                construction_event.update_event_by_installation(self)
            elif not construction_event:
                self._create_construction_event()
        elif construction_event:
            construction_event.unlink()

    def _create_or_update_stakeout_event(self):
        stake_out_event = self._find_stake_out_event()

        if self.stake_out_date:
            if stake_out_event and not self.stakeout_dates_synced(stake_out_event):
                stake_out_event.update_event_by_installation(self)
            elif not stake_out_event:
                self._create_stake_out_event()
        elif stake_out_event:
            stake_out_event.unlink()

    def _create_or_update_irve_event(self):
        irve_event = self._find_irve_event()
        if self._irve_scheduled():
            if irve_event and not self.irve_dates_synced(irve_event):
                irve_event.update_event_by_installation(self)
            elif not irve_event:
                self._create_irve_event()
        elif irve_event:
            irve_event.unlink()

    def _get_installation_events(self, type):
        events = self.env["installation.event"].search(
            [("installation_id", "=", self.id), ("type", "=", type)]
        )
        if events:
            return events[-1]
        return None

    def _find_construction_event(self):
        return self._get_installation_events("obra")

    def _find_stake_out_event(self):
        return self._get_installation_events("replanteo")

    def _find_irve_event(self):
        return self._get_installation_events("irve")

    def _execution_scheduled(self):
        return self.construction_start_date or self.construction_end_date

    def get_construction_dates(self):
        construction_start_date = None
        construction_end_date = None

        if self.construction_start_date and self.construction_end_date:
            construction_start_date = self.construction_start_date
            construction_end_date = self.construction_end_date
        elif self.construction_start_date:
            construction_start_date = self.construction_start_date
            construction_end_date = self.construction_start_date
        elif self.construction_end_date:
            construction_start_date = self.construction_end_date
            construction_end_date = self.construction_end_date

        return construction_start_date, construction_end_date

    def _create_construction_event(self):
        vals = {
            "name": f"{self.name} - Obra",
            "installation_id": self.id,
        }
        start_date, end_date = self.get_construction_dates()
        vals.update(type="obra", start_date=start_date, end_date=end_date)
        self.env["installation.event"].create(vals)

    def construction_dates_synced(self, event):
        start_date, end_date = self.get_construction_dates()
        return (
            fields.Date.to_date(event.start_date) == start_date
            and fields.Date.to_date(event.end_date) == end_date
        )

    def stakeout_dates_synced(self, event):
        return (
            event.start_date == self.stake_out_date
            and event.end_date == fields.Datetime.add(self.stake_out_date, hours=1)
        )

    def _create_stake_out_event(self):
        vals = {
            "name": f"{self.name} - Replanteo",
            "installation_id": self.id,
        }
        vals.update(
            start_date=self.stake_out_date,
            end_date=fields.Datetime.add(self.stake_out_date, hours=1),
            type="replanteo",
        )
        self.env["installation.event"].create(vals)

    def _irve_scheduled(self):
        return self.irve_execution_date or self.irve_execution_end_date

    def get_irve_dates(self):
        if self.irve_execution_date and self.irve_execution_end_date:
            return self.irve_execution_date, self.irve_execution_end_date
        elif self.irve_execution_date:
            return self.irve_execution_date, self.irve_execution_date
        elif self.irve_execution_end_date:
            return self.irve_execution_end_date, self.irve_execution_end_date
        return None, None

    def irve_dates_synced(self, event):
        start_date, end_date = self.get_irve_dates()
        return (
            fields.Date.to_date(event.start_date) == start_date
            and fields.Date.to_date(event.end_date) == end_date
        )

    def _create_irve_event(self):
        star_date, end_date = self.get_irve_dates()
        vals = {
            "name": f"{self.name} - IRVE - {self.irve_installer_id.name}",
            "installation_id": self.id,
        }
        vals.update(type="irve", start_date=star_date, end_date=end_date)
        self.env["installation.event"].create(vals)

    def update_installation_by_event(self, event):
        if event.type == "obra" and not self.construction_dates_synced(event):
            self._update_construction_dates_by_event(event)
        elif event.type == "irve" and not self.irve_dates_synced(event):
            self._update_irve_dates_by_event(event)
        elif event.type == "replanteo" and not self.stakeout_dates_synced(event):
            self._update_stakeout_dates_by_event(event)

    def _update_construction_dates_by_event(self, event):
        self.write(
            {
                "construction_start_date": fields.Date.to_date(event.start_date),
                "construction_end_date": fields.Date.to_date(event.end_date),
            }
        )

    def _update_irve_dates_by_event(self, event):
        self.write(
            {
                "irve_execution_date": fields.Date.to_date(event.start_date),
                "irve_execution_end_date": fields.Date.to_date(event.end_date),
            }
        )

    def _update_stakeout_dates_by_event(self, event):
        self.write({"stake_out_date": event.start_date})
