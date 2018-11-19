from odoo import models, fields, api
class cashPool(models.Model):
    _name='ppf.cash.pool'
    _rec_name = 'name'


    name=fields.Char('ID')
    cash_date=fields.Date('Date')
    percentage=fields.Float('Percentage',default=100)
    type = fields.Many2one('product.category',string='Type')
    amount=fields.Float('Amount',compute='_compute_amount',store=True)
    perv_amount=fields.Float('Previous Invested')
    os_amount=fields.Float('Outstanding',compute='_compute_os_amount')
    subscription_id = fields.Many2one('ppf.subscription',string='Sub')
    # allocation_line_invest = fields.One2many('account.invoice','allocation_id')

    @api.one
    @api.depends('percentage')
    def _compute_amount(self):
        if self.subscription_id.total_amount >= self.subscription_id.o_s:
            self.amount = (self.percentage * (self.subscription_id.total_amount)) / 100

    # @api.one
    # @api.depends('allocation_line_invest')
    # def _compute_perv_amount(self):
    #     self.perv_amount =0.0
    #     for record in self.allocation_line_invest:
    #         self.perv_amount += record.totalamount

    @api.one
    @api.depends('perv_amount')
    def _compute_os_amount(self):
        self.os_amount = self.amount - self.perv_amount

