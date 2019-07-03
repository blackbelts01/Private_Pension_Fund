from odoo import models, fields, api

class ppfDepartment(models.Model):
    _name = 'ppf.department'

    name = fields.Char('Name', required=True)
    department_number = fields.Integer('Sub Company Number')
    employees = fields.Integer('Employees', compute='_compute_total_employees')
    total_value = fields.Float('Total Amount', compute='_compute_total_amount')
    percentage = fields.Float('Percentage')
    company_share = fields.Float('Company Share', compute='_compute_total_company_amount')
    employee_share = fields.Float('Employee Share', compute='_compute_total_own_amount')
    boosters = fields.Float('Boosters', compute='_compute_total_boosters_amount')
    fund = fields.Many2one('ppf.fund', string='Fund', default=lambda self: self._default_fund())
    subscription_ids = fields.One2many('ppf.subscription','department')
    account_payable = fields.Many2one('account.account', string='Payable Account', domain="[('user_type_id','=','Payable')]")
    account_receivable = fields.Many2one('account.account', string='Receivable Account', domain="[('user_type_id','=','Receivable')]")

    _sql_constraints = [
        ('department_number_uniq',
         'UNIQUE (department_number)',
         'Department Number must be unique.')
    ]

    @api.one
    @api.depends('subscription_ids')
    def _compute_total_amount(self):
        for record in self.subscription_ids:
            self.total_value += record.total_amount

    @api.one
    @api.depends('subscription_ids')
    def _compute_total_own_amount(self):
        for record in self.subscription_ids:
            self.employee_share += record.total_own_amount

    @api.one
    @api.depends('subscription_ids')
    def _compute_total_company_amount(self):
        for record in self.subscription_ids:
            self.company_share += record.total_company_amount

    @api.one
    @api.depends('subscription_ids')
    def _compute_total_boosters_amount(self):
        for record in self.subscription_ids:
            self.boosters += record.total_boosters_amount

    @api.one
    @api.model
    def _compute_total_employees(self):
         employees = len(self.env['res.partner'].search([('department', '=', self.id)]))
         self.employees = employees

    @api.model
    def _default_fund(self):
        return self.env['ppf.fund'].search([],limit=1)