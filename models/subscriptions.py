# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ppfInvoice(models.Model):
    _inherit = 'account.invoice'

    allocated=fields.Float('Allocated')
    o_s=fields.Float('O/S')
    ref_id = fields.Many2one('account.invoice', string="Invoice")
    totalamount=fields.Float(store=True, readonly=True,string='Total Amount',compute='_onchange_sum_amount')

    @api.one
    @api.depends('amount_total')
    def _onchange_sum_amount(self):
        self.totalamount = self.amount_total

    @api.onchange('allocated', 'totalamount')
    def _onchange_sum(self):
        self.o_s = self.totalamount - self.allocated







class invoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    member_id = fields.Char(related='member_name.member_id',string='Member ID',store=True,readonly=True)
    member_name = fields.Many2one('res.partner',string='Member Name')
    salary = fields.Float(string='Salary')
    perc_salary = fields.Float(' % of Salary')
    own = fields.Float('Own')
    company = fields.Float('Company')
    booster = fields.Float('Booster')
    side = fields.Float('Side')




