from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class policy(models.Model):
    _name = 'ppf.policy'
    _rec_name='policy_id'


    policy_id=fields.Char('Name')
    date_from = fields.Date()
    date_to = fields.Date()
    description = fields.Text(string='Investment Policy Description')
    cash_type = fields.One2many('ppf.lines', 'fund_name', string='Fund')
    # fund_from_one2many_field = fields.Many2one(related='fund_ids.fund')
    # allocation_from_one2many_field = fields.Float(related='fund_ids.allocation')

    # @api.constrains('date_from')
    # def _check_valid(self):
    #
    #     for record in self:
    #
    #             if record.date_to < record.date_from:
    #                 raise ValidationError('date conflict')
    #
    # @api.constrains('fund_ids')
    # def _check_valid(self):
    #     self.total = 0.0
    #     for record in self.fund_ids:
    #         self.total += record.allocation
    #         print('hi this is test' + str(self.total))
    #         if self.total > 100:
    #             raise ValidationError('Allocation conflict total of allocation must not be greater than 100%')


class policyfund(models.Model):
    _name = 'ppf.lines'
    # _rec_name = 'fund'

    fund_name = fields.Many2one('ppf.policy')
    # description = fields.Char(related="type.disc", string="Description")
    allocation = fields.Float()
    type = fields.Many2one('product.category',string='Type',domain="[('parent_id.name','=','Investment')]")




