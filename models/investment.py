from odoo import models, fields, api


class ppfInvestment(models.Model):
    _inherit = 'account.invoice'

    allocation_id = fields.Many2many('allocation', string="Allocation")
    totalamount=fields.Float(store=True, readonly=True,string='Total Amount',compute='_onchange_sum_amount')

    @api.one
    @api.depends('amount_total')
    def _onchange_sum_amount(self):
        self.totalamount = self.amount_total


    # @api.onchange('allocation_id')
    # def _onchange_allocation_id(self):
    #     for record in self.allocation_id:
    #         if self.allocation_id:
    #             sum = 0.0
    #             cashpool = self.env['allocation'].search([('id', '=', record.allocation_id.id)])
    #             sum = cashpool.allocation_O_S
    #             inv.write({'allocated': sum})