# -*- coding: utf-8 -*-
from odoo import models, fields,  api, _
from odoo.exceptions import ValidationError


class ppfSubscription(models.Model):
    _name = 'ppf.subscription'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid')],
                             required=True, default='draft')
    company = fields.Many2one('res.partner',string='Company')
    batch_date = fields.Date('Batch Date')
    invoice_id = fields.Many2one('account.invoice', string="Invoice")
    total_amount = fields.Float(string='Batch Amount',compute='_compute_total_amount')
    total_cash = fields.Float('Total Cash Pool',compute='_compute_total_cashpool',store=True)
    o_s = fields.Float('Outstanding',compute='_compute_os')
    subscription_line = fields.One2many('ppf.subscription.line','subscription_id',string='Subscription Line')
    cash_pool_ids = fields.One2many('ppf.cash.pool','subscription_id', string="Cash Pool Lines")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('ppf.subscription') or 'New'
        return super(ppfSubscription, self).create(vals)

    @api.multi
    def validate(self):
        if self.subscription_line:
            self.state = 'open'
        else:
            raise ValidationError(_('Please create some Subscription Lines'))


    @api.one
    @api.depends('subscription_line')
    def _compute_total_amount(self):
        self.total_amount = 0.0
        for record in self.subscription_line:
            self.total_amount += record.total

    @api.one
    @api.depends('cash_pool_ids')
    def _compute_total_cashpool(self):
        self.total_cash = 0.0
        for record in self.cash_pool_ids:
            self.total_cash += record.amount

    @api.one
    @api.depends('total_cash')
    def _compute_os(self):
        self.o_s = self.total_amount - self.total_cash


class invoiceLine(models.Model):
    _name = 'ppf.subscription.line'

    @api.multi
    @api.onchange('member_name')
    def get_account(self):
        account=self.env['account.account'].search([('id', '=', '1')])
        self.account_id=account.id
        self.name="aya 7aga"

    member_name = fields.Many2one('res.partner',string='Member Name',domain="[('company_type','=','person')]")
    member_id = fields.Char(related='member_name.member_id',string='Member ID',store=True)
    salary = fields.Float(string='Salary')
    perc_salary = fields.Integer(' % of Salary')
    own = fields.Float('Own')
    company = fields.Float('Company')
    booster = fields.Float('Booster')
    side = fields.Float('Side')
    total=fields.Float('Total',store=True, readonly=True,compute='_compute_total')
    subscription_id = fields.Many2one('ppf.subscription')


    @api.one
    @api.depends('salary','perc_salary','own','company','booster','side')
    def _compute_total(self):
        self.total = (self.salary * (self.perc_salary/100))+self.own+self.company+self.booster+self.side






