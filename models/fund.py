from odoo import models, tools, fields, api

class ppfFund(models.Model):
    _name = 'ppf.fund'

    name = fields.Char('Name', required=True)
    manager = fields.Many2one('res.partner', string='Manager')
    release_date = fields.Date('Release Date')
    employees = fields.Integer('Employees', compute='_compute_total_employees')
    total_value = fields.Float('Total Amount', compute='_compute_total_amount')
    percentage = fields.Float('Percentage')
    company_share = fields.Float('Company Share', compute='_compute_total_company_amount')
    employee_share = fields.Float('Employee Share', compute='_compute_total_own_amount')
    boosters = fields.Float('Boosters', compute='_compute_total_boosters_amount')
    department_ids = fields.One2many('ppf.department','fund')

    @api.one
    @api.depends('department_ids')
    def _compute_total_amount(self):
        self.total_value = 0.0
        for record in self.department_ids:
            self.total_value += record.total_value

    @api.one
    @api.depends('department_ids')
    def _compute_total_company_amount(self):
        self.company_share = 0.0
        for record in self.department_ids:
            self.company_share += record.company_share
            print(self.company_share)

    @api.one
    @api.depends('department_ids')
    def _compute_total_own_amount(self):
        self.employee_share = 0.0
        for record in self.department_ids:
            self.employee_share += record.employee_share

    @api.one
    @api.depends('department_ids')
    def _compute_total_boosters_amount(self):
        self.boosters = 0.0
        for record in self.department_ids:
            self.boosters += record.boosters


    @api.one
    @api.depends('department_ids')
    def _compute_total_employees(self):
        self.employees = 0.0
        for record in self.department_ids:
            self.employees += record.employees


class ppfFundReport(models.Model):
    _name = 'ppf.fund.report'
    _table = 'report'
    _auto = False

    member_name = fields.Many2one('res.partner',string='Employee Name',domain="[('company_type','=','person')]",required=True)
    own = fields.Float('Own')
    company = fields.Float('Company')
    batch_date = fields.Date('Batch Date')

    @api.model_cr
    def init(self):

        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
               CREATE VIEW report AS(
                SELECT ppf_subscription_line.id,member_name,own,ppf_subscription_line.company,batch_date FROM ppf_subscription_line LEFT JOIN 
                ppf_subscription ON ppf_subscription_line.subscription_id=ppf_subscription.id GROUP BY ppf_subscription.batch_date, ppf_subscription_line.member_name
                 , ppf_subscription_line.own,ppf_subscription_line.id,ppf_subscription_line.company)"""
        self.env.cr.execute(query)