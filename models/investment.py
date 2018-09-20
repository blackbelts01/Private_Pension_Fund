from odoo import models, fields, api


class ppfInvestment(models.Model):
    _inherit = 'account.invoice'

    allocation_id = fields.Many2many('allocation', string="Allocation")
    totalamount=fields.Float(store=True, readonly=True,string='Total Amount',compute='_onchange_sum_amount')

    @api.one
    @api.depends('amount_total')
    def _onchange_sum_amount(self):
        self.totalamount = self.amount_total