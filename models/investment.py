from odoo import models, fields,  api, _
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

class ppfInvestment(models.Model):
    _name = 'ppf.investment'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid')],
                             required=True, default='draft')
    company = fields.Many2one('res.partner', string='Partner', required=True)
    invested_date = fields.Date('Invested Date')
    total_amount = fields.Float(store=True, readonly=True,string='Total Invested',compute='_compute_amount')
    cash_pool_id = fields.Many2one('ppf.cash.pool', string="Cash Pool")
    cash_pool_amount = fields.Float(related='cash_pool_id.amount',string='Cash Pool Amount')
    cash_poo_perv_amount = fields.Float(related='cash_pool_id.perv_amount',string='Previous Invested')
    cash_pool_os_amount = fields.Float(related='cash_pool_id.os_amount',string='Outstanding')
    type_categ =fields.Many2one(related='cash_pool_id.type',store=True)
    investment_line_ids= fields.One2many('ppf.investment.line','investment_id')
    invoice_ids = fields.One2many('account.invoice', 'investment_id', string='Invoices', readonly=True)



    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('ppf.investment') or 'New'
        return super(ppfInvestment, self).create(vals)

    @api.multi
    def validate(self):
        if self.investment_line_ids:
            self.state = 'open'
        else:
            raise ValidationError(_('Please create some Investment Lines'))

    @api.one
    @api.depends('investment_line_ids')
    def _compute_amount(self):
        self.total_amount = 0.0
        for record in self.investment_line_ids:
            self.total_amount += record.amount

    @api.multi
    def create_bill(self):
        bill = self.env['account.invoice'].create({
            'type': 'in_invoice',
            'partner_id': self.company.id,
            'user_id': self.env.user.id,
            'investment_id': self.id,
            'origin': self.name,
            'date_due': self.invested_date,
            'invoice_line_ids': [(0, 0, {
                'name': 'Bill For Investment',
                'quantity': 1,
                'price_unit': self.total_amount,
                'account_id': 1,
            })],
        })
        bill.action_invoice_open()
        self.state = 'paid'


class investmentLine(models.Model):
    _name = 'ppf.investment.line'


    product = fields.Many2one('product.product',string='Product')
    quantity = fields.Integer('Quantity')
    unit_price = fields.Float('Unit Price')
    amount = fields.Float('Amount',compute='_compute_amount')
    investment_id = fields.Many2one('ppf.investment')

    @api.one
    @api.depends('unit_price')
    def _compute_amount(self):
        self.amount = self.quantity * self.unit_price


class AccountInvoiceRelate(models.Model):
    _inherit = 'account.invoice'

    investment_id = fields.Many2one('ppf.investment', string='Investment')