from odoo import models, fields, api
class Allocation(models.Model):
    _name='allocation'




    allocation_id=fields.Char('Alloction Number')
    desc=fields.Text('Describtion')
    allocation_date=fields.Date('Allocation Date')
    currency=fields.Many2one('res.currency')
    allocation_total=fields.Float('Allocation Total')
    allocation_invested = fields.Float('Allocation Invested')
    allocation_O_S = fields.Float('Allocation O/S')
    allocation_line=fields.One2many('allocation.lines','allocation_id')



class Allocation_lines(models.Model):
    _name='allocation.lines'

    sub=fields.Many2one('ppf.subscription',domain="[('state','=','paid')]",string='Subscribtion')
    sub_date = fields.Date(related='sub.date_invoice',string='Subscribtion Date')
    sub_total_ammount=fields.Float(related='sub.totalamount',readonly=True,force_save=True)
    allocated=fields.Float('Allocated')
    out_standing=fields.Float('O/S')
    allocation_id=fields.Many2one('allocation')
