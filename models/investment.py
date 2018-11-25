from odoo import models, fields,  api, _
from odoo.exceptions import ValidationError

class ppfInvestment(models.Model):
    _name = 'ppf.investment'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    state = fields.Selection([('draft', 'Draft'), ('open', 'Open'), ('paid', 'Paid')],
                             required=True, default='draft')
    company = fields.Many2one('res.partner', string='Partner', required=True)
    invested_date = fields.Date('Investment Date')
    total_amount = fields.Float(store=True, readonly=True,string='Total Invested',compute='_compute_amount')
    cash_pool_id = fields.Many2one('ppf.cash.pool', string="Cash Pool")

    cash_pool_amount = fields.Float(related='cash_pool_id.amount',string='Cash Account Amount')
    cash_poo_perv_amount = fields.Float(related='cash_pool_id.perv_amount',string='Previous Invested')
    cash_pool_os_amount = fields.Float(related='cash_pool_id.os_amount',string='Outstanding')
    type_categ =fields.Many2one(related='cash_pool_id.type',store=True)
    investment_line_ids= fields.One2many('ppf.investment.line','investment_id')
    invoice_ids = fields.One2many('account.invoice', 'investment_id', string='Invoices', readonly=True)
    validate_cash_pool=fields.Boolean(default=True)
    validate_invest_lines = fields.Boolean()

    @api.multi
    def validate_cash(self):
        self.validate_cash_pool = True
        self.validate_invest_lines = False
        return True

    @api.multi
    def validate_Lines(self):

            self.validate_cash_pool = False
            self.validate_invest_lines = True
            return True




    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('ppf.investment') or 'New'
        return super(ppfInvestment, self).create(vals)

    @api.multi
    def validate(self):
        if self.investment_line_ids:
            self.env['cash.pool.trans'].create({
                'state': 'buying',
                'investment_id': self.id,
                'date': self.invested_date,
                'amount': self.total_amount,
                'cash_pool_id': self.cash_pool_id.id,
            })
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


    @api.multi
    def invest_print(self):
        return self.env.ref('Private_Pension_Fund.invest').report_action(self)

    @api.multi
    def send_mail_invest(self):
        # Find the e-mail template
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        template_id = self.env.ref('Private_Pension_Fund.invest_email_template')
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'ppf.investment',
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



class investmentLine(models.Model):
    _name = 'ppf.investment.line'


    type_line=fields.Many2one(related='investment_id.type_categ')
    product = fields.Many2one('product.product',string='Product',domain="[('categ_id','=',type_line)]")

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