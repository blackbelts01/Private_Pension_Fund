# -*- coding: utf-8 -*-

# from odoo import models, fields,  api, _
from odoo.exceptions import ValidationError

from openerp import models, fields, api, _
from odoo import xlrd
from xlrd import open_workbook
from tempfile import TemporaryFile
import base64
from psycopg2.extensions import AsIs






class ppfSubscription(models.Model):
    _name = 'ppf.subscription'


    @api.model
    def _default_currency(self):
        return self.env.user.company_id.currency_id

    name = fields.Char(string='Id', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid')],
                             required=True, default='draft')

    batch_date = fields.Date('Batch Date')
    invoice_ids = fields.One2many('account.invoice', 'subscription_id', string='Invoices', readonly=True)
    total_amount = fields.Float(string='Batch Amount', compute='_compute_total_amount')
    total_own_amount = fields.Float('Total Own Amount', compute='_compute_total_own_amount')
    total_company_amount = fields.Float('Total Company Amount', compute='_compute_total_company_amount')
    total_boosters_amount = fields.Float('Total Boosters Amount', compute='_compute_total_boosters_amount')
    total_cash = fields.Float('Total Cash Pool',compute='_compute_total_cashpool',store=True)
    o_s = fields.Float('Outstanding',compute='_compute_os')
    subscription_line = fields.One2many('ppf.subscription.line','subscription_id', ondelete='cascade', string='Subscription Line')
    cash_pool_ids = fields.One2many('ppf.cash.pool','subscription_id', string="Cash Pool Lines")
    currency_id = fields.Many2one('res.currency', string='Currency',
        required=True, readonly=True,
        default=_default_currency, track_visibility='always')
    data= fields.Binary('File')
    policy=fields.Many2one('ppf.policy')
    department = fields.Many2one('ppf.department', string='Subsidiary')
    invoice_created = fields.Boolean('is invoice created ?', default=False)
    number_of_subscriptions = fields.Integer('Num.Subscription', compute='_compute_total_subscriptions')




    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('ppf.subscription') or 'New'
        return super(ppfSubscription, self).create(vals)

    @api.multi
    def validate(self):
        if self.subscription_line:
            for rec in self.policy.cash_type:
                self.env['ppf.cash.pool'].create({
                    'name': self.env['ir.sequence'].next_by_code('ppf.cash.pool')+'/'+ str(self.name),
                    'cash_date': self.batch_date,
                    'type':rec.type.id,
                    'percentage':rec.allocation,
                    'amount': (rec.allocation*self.total_amount)/100,
                    'subscription_id': self.id,
                })
            self.state = 'open'
        else:
            raise ValidationError(_('Please create some Subscription Lines'))


    @api.multi
    def create_invoice(self):
        inv = self.env['account.invoice'].create({
            #'type': 'out_invoice',
            'partner_id': self.department.id,
            #'account_id': self.
            #'user_id': self.env.user.id,
            'subscription_id': self.id,
            #'origin': self.name,
            'date_due': self.batch_date,
            'invoice_line_ids': [(0, 0, {
                'name': 'Invoice For Subscription',
                'quantity': 1,
                'price_unit': self.total_amount,
                'account_id': self.department.account_payable.id,
            })],
        })
        inv.action_invoice_open()
        #self.state = 'paid'
        self.invoice_created = True

    @api.one
    @api.depends('invoice_ids')
    def _compute_state(self):
        for record in self.invoice_ids:
            if record.id == self.id:
                self.state = record.state
            else:
                return ('false')

    @api.one
    @api.depends('subscription_line')
    def _compute_total_amount(self):
        self.total_amount = 0.0
        for record in self.subscription_line:
            self.total_amount += record.total

    @api.one
    @api.depends('subscription_line')
    def _compute_total_own_amount(self):
        self.total_own_amount = 0.0
        for record in self.subscription_line:
            self.total_own_amount += record.own

    @api.one
    @api.depends('subscription_line')
    def _compute_total_company_amount(self):
        self.total_company_amount = 0.0
        for record in self.subscription_line:
            self.total_company_amount += record.company

    @api.one
    @api.depends('subscription_line')
    def _compute_total_boosters_amount(self):
        self.total_boosters_amount = 0.0
        for record in self.subscription_line:
            self.total_company_amount += record.booster

    @api.one
    @api.depends('cash_pool_ids')
    def _compute_total_cashpool(self):
        self.total_cash = 0.0
        for record in self.cash_pool_ids:
            self.total_cash += record.amount

    @api.one
    @api.depends('subscription_line')
    def _compute_total_subscriptions(self):
        self.number_of_subscriptions = len(self.subscription_line)


    @api.one
    @api.depends('total_cash')
    def _compute_os(self):
        self.o_s = self.total_amount - self.total_cash

    @api.model_cr
    @api.multi
    def import_file(self):
        wb = open_workbook(file_contents=base64.decodestring(self.data))
        sheet = wb.sheets()[0]

        for s in wb.sheets():

            values = []

            for row in range(1,s.nrows):

                col_value = []

                for col in range(s.ncols):

                    value = (s.cell(row, col).value)

                    # try:
                    #     value = str(int(value))
                    #     value=float(value)
                    # except:
                    #     pass

                    col_value.append(value)
                print('20202020202020')
                print(col_value)
                #name = self.env['res.partner'].search([('name', '=',col_value[0])]).id
                #total = (col_value[1] *(col_value[2]/100))+col_value[3]+col_value[4]+col_value[5]
                self.env.cr.execute("INSERT INTO  ppf_subscription_line (member_name, salary, perc_salary,"
                                    " own, company, " \
                                        "booster, total, subscription_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                                    ,(self.env['res.partner'].search([('name', '=',col_value[0])]).id, col_value[1], col_value[2], col_value[3],
                                     col_value[4], col_value[5], (col_value[1] * (col_value[2]/100))+col_value[3]+col_value[4]+col_value[5], self.id))
                # self.update({
                # 'subscription_line': [(0, 0, {'member_name':(self.env['res.partner'].search([('name', '=',col_value[0])]).id), 'salary': col_value[1],'perc_salary': col_value[2],
                #                               'own':col_value[3],'company':col_value[4],'booster':col_value[5]})],
                # })


            values.append(col_value)
        print(values)

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
            'default_model': 'ppf.subscription',
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




class subscriptionLine(models.Model):
    _name = 'ppf.subscription.line'

    @api.multi
    @api.onchange('member_name')
    def get_account(self):
        account=self.env['account.account'].search([('id', '=', '1')])
        self.account_id=account.id
        self.name="aya 7aga"


    member_name = fields.Many2one('res.partner',string='Employee Name',domain="[('company_type','=','person')]",required=True)
    member_id = fields.Char(related='member_name.member_id',string='Employee ID',readonly=True,store=True)

    salary = fields.Float(string='Salary',required=True)
    perc_salary = fields.Integer(' % of Salary',required=True)
    own = fields.Float('Own')
    company = fields.Float('Company')
    booster = fields.Float('Booster')
    total = fields.Float('Total',store=True, readonly=True,compute='_compute_total')
    subscription_id = fields.Many2one('ppf.subscription')

    @api.one
    @api.depends('salary','perc_salary','own','company','booster')
    def _compute_total(self):
        self.total = (self.salary * (self.perc_salary/100))+self.own+self.company+self.booster





class AccountInvoiceRelate(models.Model):
    _inherit = 'account.invoice'

    subscription_id = fields.Many2one('ppf.subscription', string='Subscription')

