from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ppfInvestment(models.Model):
    _inherit = 'account.invoice'

    allocation_id = fields.Many2many('cash.pool', string="Cash Pool")
    totalamount=fields.Float(store=True, readonly=True,string='Total Invested',compute='_onchange_sum_amount')
    total_cashpool=fields.Float(string='Total Cash Pool',compute='_compute_cash_pool',readonly=True)

    @api.one
    @api.depends('amount_total')
    def _onchange_sum_amount(self):
        self.totalamount = self.amount_total


    @api.one
    @api.depends('allocation_id')
    def _compute_cash_pool(self):
        self.total_cashpool = 0.0
        for record in self.allocation_id:
            self.total_cashpool += record.amount

    @api.constrains('total_cashpool')
    def _constrain_total_cashpool(self):
        if self.total_cashpool < self.amount_total:
            raise ValidationError(_('Error! Total invested invalid'))

