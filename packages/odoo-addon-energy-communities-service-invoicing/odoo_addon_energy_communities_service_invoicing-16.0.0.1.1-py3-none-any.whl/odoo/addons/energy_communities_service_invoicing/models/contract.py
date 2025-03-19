from collections import namedtuple
from datetime import datetime

from odoo import _, api, fields, models

from ..utils import (
    _CONTRACT_STATUS_VALUES,
    _SALE_ORDER_SERVICE_INVOICING_ACTION_VALUES,
    get_existing_open_pack_contract,
    raise_existing_same_open_platform_pack_contract_error,
)

_CLOSING_ACTION_VALUES = _SALE_ORDER_SERVICE_INVOICING_ACTION_VALUES + [
    ("close", _("Close"))
]


class ContractContract(models.Model):
    _inherit = "contract.contract"
    _order = "id desc"

    community_company_id = fields.Many2one(
        "res.company",
        string="Related community",
        domain="[('hierarchy_level','=','community')]",
    )
    predecessor_contract_id = fields.Many2one(
        "contract.contract", string="Predecessor contract"
    )
    successor_contract_id = fields.Many2one(
        "contract.contract", string="Successor contract"
    )
    status = fields.Selection(
        selection=_CONTRACT_STATUS_VALUES,
        required=True,
        string="Status",
        default="in_progress",
    )
    discount = fields.Float(
        string="Discount (%)",
        digits="Discount",
        compute="_compute_discount",
        store=False,
    )
    last_date_invoiced = fields.Date(
        string="Last Date Invoiced", compute="_compute_last_date_invoiced", store=False
    )
    pack_type = fields.Selection(related="contract_template_id.pack_type")
    is_free_pack = fields.Boolean(related="contract_template_id.is_free_pack")
    closing_action = fields.Selection(
        selection=_CLOSING_ACTION_VALUES,
        compute="_compute_closing_action",
        string="Closing reason",
        default="none",
        store=True,
    )
    closing_action_description = fields.Char(
        string="Closing reason description",
        compute="_compute_closing_action_description",
        store=True,
    )
    related_contract_product_ids = fields.One2many(
        "product.product",
        string="Related services",
        compute="_compute_related_contract_product_ids",
        store=False,
    )
    pack_id = fields.Many2one(
        "product.product",
        string="Service Pack",
        compute="_compute_pack_id",
        store=False,
    )
    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order (activation)",
    )
    received_invoices_count = fields.Integer(compute="_compute_received_invoices_count")
    # On energy_communities all contracts have skip_zero_qty marked by default
    skip_zero_qty = fields.Boolean(default=True)
    # On energy communities all contracts have company_id
    company_id = fields.Many2one(required=True)

    @api.depends("status", "successor_contract_id")
    def _compute_closing_action(self):
        for record in self:
            record.closing_action = "none"
            if record.status in ["closed", "closed_planned"]:
                if record.successor_contract_id:
                    record.closing_action = (
                        record.successor_contract_id.sale_order_id.service_invoicing_action
                    )
                else:
                    record.closing_action = "close"

    @api.depends("status", "successor_contract_id")
    def _compute_closing_action_description(self):
        for record in self:
            record.closing_action_description = ""
            if record.status in ["closed", "closed_planned"]:
                if record.successor_contract_id:
                    record.closing_action_description = (
                        record.successor_contract_id.sale_order_id.service_invoicing_action_description
                    )

    @api.constrains("partner_id", "community_company_id")
    def _constrain_unique_contract(self):
        for record in self:
            if record.community_company_id:
                existing_contract = (
                    record._get_existing_same_open_platform_pack_contract()
                )
                if existing_contract:
                    raise_existing_same_open_platform_pack_contract_error(
                        existing_contract
                    )

    def _compute_received_invoices_count(self):
        for record in self:
            record.received_invoices_count = len(record._get_received_invoices_ids())

    @api.depends("contract_template_id")
    def _compute_related_contract_product_ids(self):
        for record in self:
            rel_products = [(5, 0, 0)]
            record.related_contract_product_ids = rel_products
            if record.contract_template_id:
                for line in record.contract_template_id.contract_line_ids:
                    rel_products.append((4, line.product_id.id))
                record.related_contract_product_ids = rel_products

    @api.depends("contract_line_ids")
    def _compute_discount(self):
        for record in self:
            record.discount = 0
            if record.contract_line_ids:
                record.discount = record.contract_line_ids[0].discount

    @api.depends("contract_line_ids")
    def _compute_last_date_invoiced(self):
        for record in self:
            record.last_date_invoiced = None
            if record.contract_line_ids:
                record.last_date_invoiced = record.contract_line_ids[
                    0
                ].last_date_invoiced

    @api.depends("contract_template_id")
    def _compute_pack_id(self):
        for record in self:
            record.pack_id = False
            if record.contract_template_id:
                rel_product = self.env["product.product"].search(
                    [
                        (
                            "property_contract_template_id",
                            "=",
                            record.contract_template_id.id,
                        )
                    ],
                    limit=1,
                )
                if rel_product:
                    record.pack_id = rel_product.id

    def _recurring_create_invoice(self, date_ref=False):
        moves = super()._recurring_create_invoice(date_ref)
        for move in moves:
            if not move.line_ids:
                move.unlink()
        return moves

    def action_activate_contract(self):
        return self._action_contract("activate", {"execution_date": self.date_start})

    def action_close_contract(self):
        return self._action_contract(
            "close",
            {
                "execution_date": self.last_date_invoiced
                if self.last_date_invoiced
                else self.date_start
            },
        )

    def action_modify_contract(self):
        return self._action_contract(
            "modification",
            {
                "execution_date": self.last_date_invoiced
                if self.last_date_invoiced
                else self.date_start
            },
        )

    def action_reopen_contract(self):
        return self._action_contract(
            "reopen",
            {
                "execution_date": self.date_end,
                "pack_id": self.pack_id.id if self.pack_id else False,
                "pricelist_id": self.pricelist_id.id if self.pricelist_id else False,
                "payment_mode_id": self.payment_mode_id.id
                if self.payment_mode_id
                else False,
            },
        )

    def _action_contract(self, action, wizard_defaults_extra):
        self.ensure_one()
        # wizard params
        wizard_defaults = {
            "service_invoicing_id": self.id,
            "executed_action": action,
            "discount": self.discount,
        } | wizard_defaults_extra
        # wizard creation and display
        wizard = self.env["service.invoicing.action.wizard"].create(wizard_defaults)
        return {
            "type": "ir.actions.act_window",
            "name": _("Executing: {}").format(action),
            "res_model": "service.invoicing.action.wizard",
            "view_type": "form",
            "view_mode": "form",
            "target": "new",
            "res_id": wizard.id,
        }

    def action_show_received_invoices(self):
        self.ensure_one()
        tree_view = self.env.ref("account.view_invoice_tree", raise_if_not_found=False)
        form_view = self.env.ref("account.view_move_form", raise_if_not_found=False)
        ctx = dict(self.env.context)
        ctx["default_move_type"] = "in_invoice"
        action = {
            "type": "ir.actions.act_window",
            "name": "Invoices",
            "res_model": "account.move",
            "view_mode": "tree,form",
            "domain": [("id", "in", self._get_received_invoices_ids())],
            "context": ctx,
        }
        if tree_view and form_view:
            action["views"] = [(tree_view.id, "tree"), (form_view.id, "form")]
        return action

    @api.model
    def cron_close_todays_closed_planned_contacts(self):
        impacted_contracts = self.env["contract.contract"].search(
            [("status", "=", "closed_planned")]
        )
        for contract in impacted_contracts:
            contract.set_close_status_type_by_date()
        return True

    # TODO: It would be very cool being able to use this methods on service_invoicing xml act_window definition
    @api.model
    def get_service_invoicing_views_domain(self):
        return [("community_company_id", "!=", False)]

    @api.model
    def get_service_invoicing_views_context(self):
        return {"search_default_not_finished": 1, "search_default_paused": 1}

    # TODO: Not working. Lack of access rules
    def _get_received_invoices_ids(self):
        received_invoices = []
        issued_invoices = self.sudo()._get_related_invoices().ids
        # related_partner = self.env["res.partner"].sudo.
        all_received_invoices = self.env["account.move"].search(
            [
                ("partner_id", "=", self.sudo().company_id.partner_id.id),
                ("move_type", "=", "in_invoice"),
            ]
        )
        for invoice in all_received_invoices:
            if invoice.sudo().ref_invoice_id:
                if invoice.sudo().ref_invoice_id.id in issued_invoices:
                    received_invoices.append(invoice.id)
        return received_invoices

    def _get_existing_same_open_platform_pack_contract(self):
        return get_existing_open_pack_contract(
            self.env,
            self.partner_id,
            "platform_pack",
            contract_id=self,
            custom_query=[("community_company_id", "=", self.community_company_id.id)],
        )

    def get_active_monitoring_members(self):
        QueryResult = namedtuple("QueryResult", ["total"])
        QUERY = """
            select count(energy_selfconsumption_supply_point.code) from energy_project_project
            inner join energy_selfconsumption_selfconsumption on
                energy_selfconsumption_selfconsumption.project_id = energy_project_project.id
            inner join energy_selfconsumption_distribution_table on
                energy_selfconsumption_distribution_table.selfconsumption_project_id = energy_selfconsumption_selfconsumption.id
            inner join energy_selfconsumption_supply_point_assignation on
                energy_selfconsumption_supply_point_assignation.distribution_table_id = energy_selfconsumption_distribution_table.id
            inner join energy_selfconsumption_supply_point on
                energy_selfconsumption_supply_point.id = energy_selfconsumption_supply_point_assignation.supply_point_id
            inner join energy_project_service_contract on
                energy_project_service_contract.project_id= energy_project_project.id
            inner join energy_project_provider on energy_project_service_contract.provider_id=energy_project_provider.id
            where
                energy_project_project.company_id={current_company_id} and
                energy_selfconsumption_distribution_table.state = 'active' and
                energy_project_provider.name LIKE '{arkenova_like}';
        """.format(
            current_company_id=int(self.community_company_id.id),
            arkenova_like="%Arkenova%",
        )
        self.env.cr.execute(QUERY)
        members = QueryResult._make(self.env.cr.fetchone())
        return members.total

    def set_close_status_type_by_date(self):
        if self.date_end.strftime("%Y-%m-%d") <= datetime.now().strftime("%Y-%m-%d"):
            self.write({"status": "closed"})
        else:
            self.write({"status": "closed_planned"})
