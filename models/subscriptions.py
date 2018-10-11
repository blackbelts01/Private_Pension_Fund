# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ppfInvoice(models.Model):
    _inherit = 'account.invoice'

    allocated=fields.Float('Cash Pool')
    o_s=fields.Float('O/S',compute='_compute_os')
    ref_id = fields.Many2one('account.invoice', string="Invoice")
    total_amount = fields.Float(string='Total Amount',compute='_compute_total_amount')

    @api.one
    def _compute_total_amount(self):
        self.total_amount = self.amount_total_signed


    @api.one
    def _compute_os(self):
        self.o_s = self.total_amount - self.allocated

class invoiceLine(models.Model):
    _inherit = 'account.invoice.line'


    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        currency = self.invoice_id and self.invoice_id.currency_id or None
        price = 0.0
        if self.total:
            price = self.total
        else:
            price = self.price_unit * (1 - (self.discount or 0.0) / 100.0)
        taxes = False
        if self.invoice_line_tax_ids:
            taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
        self.price_subtotal = price_subtotal_signed = taxes['total_excluded'] if taxes else self.quantity * price
        self.price_total = taxes['total_included'] if taxes else self.price_subtotal
        if self.invoice_id.currency_id and self.invoice_id.currency_id != self.invoice_id.company_id.currency_id:
            price_subtotal_signed = self.invoice_id.currency_id.with_context(date=self.invoice_id._get_currency_rate_date()).compute(price_subtotal_signed, self.invoice_id.company_id.currency_id)
        sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
        self.price_subtotal_signed = price_subtotal_signed * sign




    member_id = fields.Char(related='member_name.member_id',string='Member ID',store=True,readonly=True)
    member_name = fields.Many2one('res.partner',string='Member Name')
    salary = fields.Float(string='Salary')
    perc_salary = fields.Integer(' % of Salary')
    own = fields.Float('Own')
    company = fields.Float('Company')
    booster = fields.Float('Booster')
    side = fields.Float('Side')
    total=fields.Float('Total',store=True, readonly=True,compute='_compute_total')


    @api.one
    @api.depends('salary','perc_salary','own','company','booster','side')
    def _compute_total(self):
        self.total = (self.salary * (self.perc_salary/100))+self.own+self.company+self.booster+self.side





