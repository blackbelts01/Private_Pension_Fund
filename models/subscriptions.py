# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ppfInvoice(models.Model):
    _inherit = 'account.invoice'

    allocated=fields.Float('Allocated')
    o_s=fields.Float('O/S')
    ref_id = fields.Many2one('account.invoice', string="Invoice")
    totalamount=fields.Float(store=True, readonly=True,string='Total Amount',compute='_onchange_totalamount')

    @api.one
    @api.depends('invoice_line_ids')
    def _onchange_totalamount(self):
        if self.invoice_line_ids:
            self.totalamount=0.0
            for record in self.invoice_line_ids:
                self.totalamount += record.total


    @api.onchange('allocated', 'totalamount')
    def _onchange_sum(self):
        self.o_s = self.totalamount - self.allocated









class invoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    member_id = fields.Char(related='member_name.member_id',string='Member ID',store=True,readonly=True)
    member_name = fields.Many2one('res.partner',string='Member Name')
    salary = fields.Float(string='Salary')
    perc_salary = fields.Integer(' % of Salary')
    own = fields.Float('Own')
    company = fields.Float('Company')
    booster = fields.Float('Booster')
    side = fields.Float('Side')
    total=fields.Float('Total',store=True, readonly=True,compute='_compute_total')

    @api.one
    @api.depends('salary','perc_salary','own','company','booster','side')
    def _compute_total(self):
        self.total = (self.salary * (self.perc_salary/100))+self.own+self.company+self.booster+self.side




