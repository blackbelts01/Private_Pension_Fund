from odoo import models, fields, api
from odoo.exceptions import  ValidationError
class Subscribiton(models.Model):
    _inherit = 'account.invoice'
    _name='subcribtion.bb'

    currency=fields.Many2one('res.currency','Currency')
    Alloctaed=fields.Float('Allocated')
    o_s=fields.Float('O/S')
    sub_lines=fields.One2many('subsribtion.line','sub_line_subscribtion')


class Subscribiton_line(models.Model):
    _name='subsribtion.line'

    mem_id=fields.Char('Member ID')
    mem_name=fields.Char('Member Name')
    salary=fields.Char('Salary')
    perc_salary=fields.Char(' % salary')
    own = fields.Char('Own')
    company = fields.Char('Company')
    booster = fields.Char('Booster')
    side=fields.Char('Side')
    sub_total=fields.Char('Total')
    sub_line_subscribtion=fields.Many2one('subcribtion.bb')


