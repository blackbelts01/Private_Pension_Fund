from odoo import models, fields, api
class Allocation(models.Model):
    _name='cash.pool'




    allocation_id=fields.Char('ID')
    desc=fields.Text('Description')
    allocation_date=fields.Date('Date')
    currency=fields.Many2one('res.currency')
    amount=fields.Float('Amount')
    subscription_id = fields.Many2one()
    allocation_O_S = fields.Float('Cash Pool Outstanding')
    allocation_line_invest = fields.Many2many('account.invoice')


    # @api.onchange('allocation_line')
    # def _onchange_subscription(self):
    #     if self.allocation_line:
    #         sum=0.0
    #         for record in self.allocation_line:
    #             inv = self.env['account.invoice'].search([('id', '=', record.sub.id)])
    #             sum=inv.allocated+record.allocated
    #             inv.write({'allocated': sum})
    #
    #
    #
    #
    #
    #
    #
    # def _get_investment(self):
    #     investmentlines = self.env['account.invoice'].search([('allocation_id','in', self.ids),('state','=','paid'),('type','=','in_invoice')])
    #
    #     if investmentlines:
    #         self.allocation_line_invest = [(6,0, investmentlines.ids)]
    #
    # @api.one
    # @api.depends('allocation_line')
    # def _compute_allocation_total(self):
    #     total=0
    #     if self.allocation_line:
    #         for rec in self.allocation_line:
    #             total+=rec.allocated
    #         self.allocation_total=total
    # # @api.one
    # # @api.depends('allocation_line_invest.totalamount')
    # # def compute_allocation_invested(self):
    # #     print('***************')
    # #     for rec in self.allocation_line_invest.allocation_id:
    # #             rec.allocation_invested = 50
    #
    # @api.multi
    # @api.one
    # @api.depends('allocation_line','allocation_line_invest.allocation_id.allocation_invested')
    # def compute_allocation_O_S(self):
    #     # if self.allocation_line_invest.allocation_id.allocation_invested:
    #         # self.allocation_O_S = 0.0
    #         self.allocation_O_S = self.allocation_total-self.allocation_invested


# class Allocation_lines(models.Model):
#     _name='allocation.lines'
#
#     sub=fields.Many2one('account.invoice',domain="[('state','=','paid'),('type','=','out_invoice')]",string='Subscription')
#     sub_date = fields.Date(related='sub.date_invoice',string='Subscription Date')
#     sub_total_ammount=fields.Float(related='sub.o_s',string='Total Amount',readonly=True,force_save=True)
#     allocated=fields.Float('Allocated')
#     out_standing=fields.Float('O/S',compute='compute_O_S',store=True)
#     allocation_id=fields.Many2one('allocation')
#
#     @api.one
#     @api.depends('allocated')
#     def compute_O_S(self):
#         if self.allocated:
#            self.out_standing += self.sub_total_ammount - self.allocated
#         else:
#             self.out_standing += self.sub_total_ammount
#
#
#
#
# class Investment_lines(models.Model):
#     _name='investment.lines'
#     # invest=fields.Many2one('account.invoice',domain="[('state','=','paid'),('type','=','in_invoice')]",string='investment')
#     # bill_lines=fields.One2many(related='invest.invoice_line_ids')
#     # amount=fields.Float(related='invest.totalamount')
#     # date_invest=fields.Date(related='invest.date_invoice',string='Date')
#     # allocation_id_invest = fields.Many2one('allocation')
#
#
#
#     # sub_date = fields.Date(related='sub.date_inv
#     # sub_total_ammount=fields.Float(related='sub.
#     # allocated=fields.Float('Allocated')
#     # out_standing=fields.Float('O/S')
#     # allocation_id=fields.Many2one('allocation')
