from odoo import models, fields, api

class ppfJoin(models.Model):
    _name = 'ppf.join'

    name = fields.Char('Name', required=True)
    birth_date = fields.Date('Date of Birth')
    job_position = fields.Char('Job Position')
    subscription_fees = fields.Float('Subscription Fees', default=100)
    department = fields.Many2one('ppf.department', string='Subsidiary')
    invoice_ids = fields.One2many('account.invoice', 'join_id', string='Invoices', readonly=True)
    state = fields.Selection([('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
                             required=True, default='pending')


    @api.multi
    def approve(self):
        self.env['res.partner'].create({
            'name': self.name,
            'DOP': self.birth_date,
            'function': self.job_position,
            'department': self.department.id,
            })

        self.env['account.invoice'].create({
            'partner_id': self.env['res.partner'].search([('display_name','=',self.name)]).id,
            'join_id': self.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Invoice For Joining Fund',
                'quantity': 1,
                'price_unit': self.subscription_fees,
                'account_id': self.env['res.partner'].search([('display_name','=',self.name)]).property_account_payable_id.id,
            })],
        })

        self.state = 'approved'

    def reject(self):
        self.state = 'rejected'





class AccountInvoiceRelate(models.Model):
    _inherit = 'account.invoice'

    join_id = fields.Many2one('ppf.join', string='Joining')