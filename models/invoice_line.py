# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class ppfInvoice(models.Model):
    _inherit = 'account.invoice'

    allocated=fields.Float('Allocated')
    o_s=fields.Float('O/S')
    totalamount=fields.Float('Total Amount')
    number2=fields.Char(string='Number', copy=False, readonly=True, index=True,default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('number2', 'New') == 'New':
            vals['number2'] = self.env['ir.sequence'].next_by_code('account.invoice') or 'New'
        return super(ppfInvoice, self).create(vals)

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




