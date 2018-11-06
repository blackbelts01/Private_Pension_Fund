from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ppfInvestment(models.Model):
    _inherit = 'account.invoice'

    totalamount=fields.Float(store=True, readonly=True,string='Total Invested',compute='_onchange_sum_amount')
    allocation_id = fields.Many2one('cash.pool', string="Cash Pool")
    cashpool_amount = fields.Float(related='allocation_id.amount',string='Cash P Amount')
    perv_amount=fields.Float(related='allocation_id.perv_amount',string='Previous Invested')
    os_amount=fields.Float(related='allocation_id.os_amount',string='Outstanding')

    @api.one
    @api.depends('amount_total')
    def _onchange_sum_amount(self):
        self.totalamount = self.amount_untaxed


    # @api.one
    # @api.depends('allocation_id')
    # def _compute_cash_pool(self):
    #     self.total_cashpool = 0.0
    #     for record in self.allocation_id:
    #         self.total_cashpool += record.amount
    #
    # @api.constrains('total_cashpool')
    # def _constrain_total_cashpool(self):
    #     if self.total_cashpool < self.amount_total:
    #         raise ValidationError(_('Error! Total invested invalid'))

