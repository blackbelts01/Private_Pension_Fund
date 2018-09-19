from odoo import models, fields, api
class Allocation(models.Model):
    _name='allocation'




    allocation_id=fields.Char('Alloction Number')
    desc=fields.Text('Describtion')
    allocation_date=fields.Date('Allocation Date')
    currency=fields.Many2one('res.currency')
    allocation_total=fields.Float('Allocation Total',compute='compute_allocation_invested',store=True)
    allocation_invested = fields.Float('Allocation Invested',compute='compute_allocation_invested',store=True)
    allocation_O_S = fields.Float('Allocation O/S')
    allocation_line=fields.One2many('allocation.lines','allocation_id')
    allocation_line_invest = fields.One2many('investment.lines', 'allocation_id_invest')



    @api.onchange('allocation_line')
    def compute_allocation_total(self):
        if self.allocation_line:
            self.allocation_total=0.0
            for rec in self.allocation_line:
                self.allocation_total+=rec.allocated

    @api.onchange('allocation_line_invest')
    def compute_allocation_invested(self):
        if self.allocation_line_invest:
            self.allocation_invested=0.0
            for rec in self.allocation_line_invest:
                self.allocation_invested += rec.amount


class Allocation_lines(models.Model):
    _name='allocation.lines'

    sub=fields.Many2one('account.invoice',domain="[('state','=','paid'),('type','=','out_invoice')]",string='Subscribtion')
    sub_date = fields.Date(related='sub.date_invoice',string='Subscribtion Date')
    sub_total_ammount=fields.Float(related='sub.totalamount',readonly=True,force_save=True)
    allocated=fields.Float('Allocated')
    out_standing=fields.Float('O/S')
    allocation_id=fields.Many2one('allocation')

class Investment_lines(models.Model):
    _name='investment.lines'
    invest=fields.Many2one('account.invoice',domain="[('state','=','paid'),('type','=','in_invoice')]",string='investment')
    bill_lines=fields.One2many(related='invest.invoice_line_ids')
    amount=fields.Float(related='invest.totalamount')
    date_invest=fields.Date(related='invest.date_invoice',string='Date')
    allocation_id_invest = fields.Many2one('allocation')



    # sub_date = fields.Date(related='sub.date_inv
    # sub_total_ammount=fields.Float(related='sub.
    # allocated=fields.Float('Allocated')
    # out_standing=fields.Float('O/S')
    # allocation_id=fields.Many2one('allocation')
