# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class invoiceLine(models.Model):
#     _inherit = 'account.invoice.line'
#     _name='ppf.invoice.line'
# mem_id = fields.Char('Member ID')
# mem_name = fields.Char('Member Name')
# salary = fields.Char('Salary')
# perc_salary = fields.Char(' % salary')
# own = fields.Char('Own')
# company = fields.Char('Company')
# booster = fields.Char('Booster')
# side = fields.Char('Side')
# sub_total = fields.Char('Total')
# sub_line_subscribtion = fields.Many2one('subcribtion.bb')



class ppfInvoice(models.Model):
    _inherit = 'account.invoice'
    _name='ppf.subscription'

    allocated=fields.Float('Allocated')
    o_s=fields.Float('O/S')






