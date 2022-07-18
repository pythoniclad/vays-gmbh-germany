# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CRMLead(models.Model):
    _inherit = "crm.lead"

    expected_revenue = fields.Monetary('Expected Revenue', currency_field='company_currency', tracking=True,
                                       compute='_get_expected_revenue', readonly=False, store=True)

    @api.depends('partner_id')
    def _get_expected_revenue(self):
        """
            To compute revenue according to last sale order
            created for partner.
        """
        for rec in self:
            if rec.partner_id:
                last_order = self.env['sale.order'].sudo().search([('partner_id', '=', rec.partner_id.id),
                                                                   ('state', '=', 'sale')],
                                                                  order='date_order DESC, id DESC', limit=1)

                if last_order:
                    rec.expected_revenue = last_order.amount_total

    def _set_expected_revenue(self):
        """
            Hook that fires after a user manually sets the order count themselves. For
            this field.
        """
        pass
