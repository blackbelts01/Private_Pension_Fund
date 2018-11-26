from odoo import models, fields, api
class cashPool(models.Model):
    _name='ppf.cash.pool'
    _rec_name = 'name'

    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    name = fields.Char('ID',required=True)
    cash_date = fields.Date('Date')
    percentage = fields.Float('Percentage',default=100,required=True)
    type = fields.Many2one('product.category',string='Type')
    amount = fields.Float('Amount',compute='_compute_amount',store=True)
    perv_amount = fields.Float('Previous Invested',compute='_compute_perv_amount')
    os_amount = fields.Float('Outstanding',compute='_compute_os_amount')
    subscription_id = fields.Many2one('ppf.subscription',string='Sub')
    allocation_line_invest = fields.One2many('ppf.investment','cash_pool_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True,default=_default_currency, track_visibility='always')


    @api.one
    @api.depends('percentage')
    def _compute_amount(self):
        self.amount = (self.percentage * (self.subscription_id.total_amount)) / 100



    @api.one
    @api.depends('allocation_line_invest')
    def _compute_perv_amount(self):
        self.perv_amount =0.0
        for record in self.allocation_line_invest:
            self.perv_amount += record.total_amount



    @api.one
    @api.depends('perv_amount')
    def _compute_os_amount(self):
        self.os_amount = self.amount - self.perv_amount



