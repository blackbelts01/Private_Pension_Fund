from odoo import models, fields, api
from odoo.exceptions import ValidationError


# class ppfInvestment(models.Model):
#     _inherit = 'account.invoice'
#
#     totalamount = fields.Float(store=True, readonly=True,string='Total Invested',compute='_onchange_sum_amount')
#     allocation_id = fields.Many2one('cash.pool', string="Cash Pool")
#     cashpool_amount = fields.Float(related='allocation_id.amount',string='Cash P Amount')
#     perv_amount = fields.Float(related='allocation_id.perv_amount',string='Previous Invested')
#     os_amount = fields.Float(related='allocation_id.os_amount',string='Outstanding')
#     type_categ =fields.Many2one(related='allocation_id.type',store=True)
#
#
#     # @api.onchange('invoice_line_ids')
#     # def _onchange_prduct(self):
#     #   if self.allocation_id:
#     #       self.invoice_line_ids.type_categ = '1'
#
#
#     @api.one
#     @api.depends('amount_total')
#     def _onchange_sum_amount(self):
#         self.totalamount = self.amount_untaxed

