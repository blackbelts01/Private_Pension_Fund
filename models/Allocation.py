from odoo import models, fields, api
class Allocation(models.Model):
    _name='allocation'




    allocation_id=fields.Char('Alloction Number')
    desc=fields.Text('Describtion')
    allocation_date=fields.Date('Allocation Date')
    currency=fields.Many2one('res.currency')
    allocation_total=fields.Float('Allocation Total',compute='_compute_allocation_total',store=True)
    allocation_invested = fields.Float('Allocation Invested')
    allocation_O_S = fields.Float('Allocation O/S',compute='compute_allocation_O_S',store=True)
    allocation_line=fields.One2many('allocation.lines','allocation_id')
    allocation_line_invest = fields.Many2many('account.invoice',compute='_get_investment')


    @api.onchange('allocation_line')
    def _onchange_subscription(self):
        if self.allocation_line:
            sum=0.0
            for record in self.allocation_line:
                inv = self.env['account.invoice'].search([('id', '=', record.sub.id)])
                sum=inv.allocated+record.allocated
                inv.write({'allocated': sum})







    def _get_investment(self):
        investmentlines = self.env['account.invoice'].search([('allocation_id','in', self.ids),('state','=','paid'),('type','=','in_invoice')])

        if investmentlines:
            self.allocation_line_invest = [(6,0, investmentlines.ids)]

    @api.one
    @api.depends('allocation_line')
    def _compute_allocation_total(self):
        total=0
        if self.allocation_line:
            for rec in self.allocation_line:
                total+=rec.allocated
            self.allocation_total=total
    # @api.multi
    # @api.depends('allocation_line_invest')
    # def compute_allocation_invested(self):
    #     if self.allocation_line_invest:
    #         self.allocation_invested=0.0
    #         for rec in self.allocation_line_invest:
    #             self.allocation_invested += rec.totalamount

    @api.multi
    @api.one
    @api.depends('allocation_line')
    def compute_allocation_O_S(self):
        if self.allocation_line:
            self.allocation_O_S = 0.0
            for rec in self.allocation_line:
                self.allocation_O_S += rec.out_standing


class Allocation_lines(models.Model):
    _name='allocation.lines'

    sub=fields.Many2one('account.invoice',domain="[('state','=','paid'),('type','=','out_invoice')]",string='Subscribtion')
    sub_date = fields.Date(related='sub.date_invoice',string='Subscribtion Date')
    sub_total_ammount=fields.Float(related='sub.o_s',string='Total Amount',readonly=True,force_save=True)
    allocated=fields.Float('Allocated')
    out_standing=fields.Float('O/S',compute='compute_O_S',store=True)
    allocation_id=fields.Many2one('allocation')

    @api.one
    @api.depends('allocated')
    def compute_O_S(self):
        if self.allocated:
           self.out_standing += self.sub_total_ammount - self.allocated
        else:
            self.out_standing += self.sub_total_ammount




class Investment_lines(models.Model):
    _name='investment.lines'
    # invest=fields.Many2one('account.invoice',domain="[('state','=','paid'),('type','=','in_invoice')]",string='investment')
    # bill_lines=fields.One2many(related='invest.invoice_line_ids')
    # amount=fields.Float(related='invest.totalamount')
    # date_invest=fields.Date(related='invest.date_invoice',string='Date')
    # allocation_id_invest = fields.Many2one('allocation')



    # sub_date = fields.Date(related='sub.date_inv
    # sub_total_ammount=fields.Float(related='sub.
    # allocated=fields.Float('Allocated')
    # out_standing=fields.Float('O/S')
    # allocation_id=fields.Many2one('allocation')
