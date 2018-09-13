# -*- coding: utf-8 -*-

from odoo import models, fields, api

class invoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    _name='ppf.subscription.line'

    member_id = fields.Char(related='member_name.member_id',string='Member ID',store=True,readonly=True)
    member_name = fields.Many2one('res.partner',string='Member Name')
    salary = fields.Float(string='Salary')
    perc_salary = fields.Float(' % of Salary')
    own = fields.Float('Own')
    company = fields.Float('Company')
    booster = fields.Float('Booster')
    side = fields.Float('Side')
    invoice_id = fields.Many2one('ppf.subscription', string='Invoice Reference',
        ondelete='cascade', index=True)



class ppfInvoice(models.Model):
    _inherit = 'account.invoice'
    _name='ppf.subscription'

    allocated=fields.Float('Allocated')
    o_s=fields.Float('O/S')
    totalamount=fields.Float('Total Amount')
    invoice_line_ids = fields.One2many('ppf.subscription.line', 'invoice_id', string='Subscription Lines', oldname='invoice_line',
        readonly=True, states={'draft': [('readonly', False)]}, copy=True)


    @api.onchange('allocated', 'totalamount')
    def _onchange_sum(self):
        self.o_s = self.totalamount - self.allocated




