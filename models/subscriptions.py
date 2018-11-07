# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ppfInvoice(models.Model):
    _inherit = 'account.invoice'

    o_s = fields.Float('Outstanding',compute='_compute_os')
    ref_id = fields.Many2one('account.invoice', string="Invoice")
    total_amount = fields.Float(string='Batch Amount',compute='_compute_total_amount')
    cash_pool_ids = fields.One2many('cash.pool','subscription_id', string="Cash Pool Lines")
    total_cash = fields.Float('Total Cash Pool',compute='_compute_total_cashpool',store=True)

    @api.one
    @api.depends('amount_total_signed')
    def _compute_total_amount(self):
        self.total_amount = self.amount_total_signed

    @api.one
    @api.depends('cash_pool_ids')
    def _compute_total_cashpool(self):
        self.total_cash = 0.0
        for record in self.cash_pool_ids:
            self.total_cash += record.amount

    @api.one
    @api.depends('total_cash')
    def _compute_os(self):
        self.o_s = self.amount_total_signed - self.total_cash
    @api.multi
    def sub_print(self):
        return self.env.ref('Private_Pension_Fund.subs').report_action(self)

    @api.multi
    def send_mail_sub(self):
        # Find the e-mail template
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.env.ref('Private_Pension_Fund.sub_email_template')
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'account.invoice',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id.id),
            'default_template_id': template_id.id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            # 'custom_layout': "sale.mail_template_data_notification_email_sale_order",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True
        }

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    # @api.constrains('total_cash')
    # def _constrain_total_cashpool(self):
    #     if self.total_cash > self.total_amount:
    #         raise ValidationError(('Error! Total Cash Pool invalid'))

class invoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    @api.onchange('member_name')
    def get_account(self):
        account=self.env['account.account'].search([('id', '=', '1')])
        self.account_id=account.id
        self.name="aya 7aga"

    # account_id = fields.Many2one('account.account', string='Account',
    #                              required=True, readonly=True, states={'draft': [('readonly', False)]},
    #                              domain=[('deprecated', '=', False)], help="The partner account used for this invoice.",default=get_account)


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




    member_id = fields.Char(related='member_name.member_id',string='Member ID',store=True)
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






