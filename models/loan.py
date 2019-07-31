from odoo import models, tools, fields, api
from datetime import datetime

class ppfLoan(models.Model):
    _name = 'ppf.loan'

    employee_name = fields.Many2one('res.partner', string='Employee Name', required=True)
    subscription_date = fields.Date('Subscription Date', compute='compute_sub_date')
    retirement_date = fields.Date('Pension Date', compute='compute_retirement_date')
    #loan_units_taken = fields.Float('Loan Units Taken', compute='_compute_loan_units_taken')
    # loan_amount = fields.Float('Loan Amount', compute='_compute_loan_amount')
    loan_date = fields.Date('Loan Date', default=datetime.today())
    # total_units_owned = fields.Float('Total Units Owned', compute='_compute_total_units_owned')
    # value_of_units_owned = fields.Float('Units Owned Value', compute='_compute_value_units_owned')
    # total_units_after_loan = fields.Float('Total Units After Loan', compute='_compute_total_units_after_loan')
    # value_of_units_after_loan = fields.Float('Units After Loan Value', compute='_compute_value_units_after_loan')
    state = fields.Selection([('pending', 'Pending'), ('paid', 'Paid'), ('rejected', 'Rejected')],
                             required=True, default='pending')
    prev_unit_balance_ids = fields.One2many('ppf.prev.years.unit.balance', 'loan_id')
    unit_balance_ids = fields.One2many('ppf.year.unit.balance', 'loan_id')
    loans_taken_ids = fields.One2many('ppf.loans.taken.before', 'loan_id')
    loans_entry_items_ids = fields.One2many('ppf.loan.entry.items', 'loan_id')
    fund_price_ids = fields.One2many('ppf.fund.price', 'loan_id')

    @api.onchange('employee_name')
    @api.multi
    def compute_sub_date(self):
        self.subscription_date = self.employee_name.subscription_date

    @api.onchange('employee_name')
    @api.multi
    def compute_retirement_date(self):
        self.retirement_date = self.employee_name.pension_date

    @api.multi
    def approve(self):
        bill = self.env['account.invoice'].create({
            'type': 'in_invoice',
            #'partner_id': ,
            'user_id': self.env.user.id,
            'loan_id': self.id,
            #'origin': self.employee_name,
            'date_due': self.loan_date,
            'invoice_line_ids': [(0, 0, {
                'name': 'Bill For Loan',
                'quantity': 1,
                'price_unit': self.loan_amount,
                #'account_id': self.company.property_account_receivable_id.id,
            })],
        })
        bill.action_invoice_open()
        self.state = 'paid'


    def reject(self):
        self.state = 'rejected'

    #@api.model_cr
    @api.one
    def compute_total_emp_units(self):

        units = self.env['ppf.unit.yearly.balance'].search([('name', '=', self.employee_name.name)])
        date = datetime.now().year
        for rec in units:
            x = datetime.strptime(str(rec.year), '%Y').year
            print(x)
            if x == date:
                self.env.cr.execute("INSERT INTO  ppf_year_unit_balance (year, total_emp_units,"
                                    " total_company_units,total_booster_units, loan_id) VALUES (%s,%s,%s,%s,%s)"
                                    , (datetime.strptime(str(rec.year), '%Y').year, rec.total_emp_units
                                       , rec.total_comp_units, rec.total_booster_units, self.id))
            else:
                self.env.cr.execute("INSERT INTO  ppf_prev_years_unit_balance (year, total_emp_units,"
                                    " total_company_units,total_booster_units, loan_id) VALUES (%s,%s,%s,%s,%s)"
                                    ,(datetime.strptime(str(rec.year),'%Y').year, rec.total_emp_units
                                    ,rec.total_comp_units,rec.total_booster_units, self.id))
                # self.env['ppf.prev.years.unit.balance'].create({
                #     'year': rec.year,
                #     'total_emp_units': rec.total_emp_units,
                #     'total_company_units': rec.total_comp_units,
                #     'total_booster_units': rec.total_booster_units,
                #     'loan_id': self.id,
                #
                # })
        loans = self.env['ppf.loan'].search([('employee_name', '=', self.employee_name.name),('state', '=', 'Approved')])
        for record in loans:
            self.env.cr.execute("INSERT INTO  ppf_loans_taken_before (date, units_taken,"
                                " amount, loan_id) VALUES (%s,%s,%s,%s)"
                                , (record.loan_date, record.total_units_after_loan
                                   , record.value_of_units_after_loan, self.id))





class ppfPrevYearsUnitBalance(models.Model):
    _name = 'ppf.prev.years.unit.balance'

    year = fields.Integer('Year')
    # fund_name = fields.Char('Fund Name')
    total_emp_units = fields.Float('Total Emp.Units')
    total_company_units = fields.Float('Total Comp.Units')
    total_booster_units = fields.Float('Total Booster Units')
    total = fields.Float('Total')
    loan_id = fields.Many2one('ppf.loan', string='Loan')

class ppfYearUnitBalance(models.Model):
    _name = 'ppf.year.unit.balance'

    year = fields.Integer('Year')
    # fund_name = fields.Char('Fund Name')
    total_emp_units = fields.Float('Total Emp.Units')
    total_company_units = fields.Float('Total Comp.Units')
    total_booster_units = fields.Float('Total Booster Units')
    total = fields.Float('Total')
    loan_id = fields.Many2one('ppf.loan', string='Loan')

class ppfLoansTakenBefore(models.Model):
    _name = 'ppf.loans.taken.before'

    date = fields.Date('Date')
    # fund_name = fields.Char('Fund Name')
    units_taken = fields.Float('Units Taken')
    amount = fields.Float('Amount')
    loan_id = fields.Many2one('ppf.loan', string='Loan')


class ppfLoanEntryItems(models.Model):
    _name = 'ppf.loan.entry.items'

    date = fields.Date('Date', default=datetime.today())
    fund_name = fields.Many2one('product.template', string='Fund Name', required=True)
    units_taken = fields.Float('Units Taken')
    amount = fields.Float('Amount')
    loan_id = fields.Many2one('ppf.loan', string='Loan')

class ppfFundPrice(models.Model):
    _name = 'ppf.fund.price'

    fund_name = fields.Many2one('product.template', string='Fund Name', required=True)
    current_price = fields.Float('Current Price', compute='compute_current_price')
    loan_id = fields.Many2one('ppf.loan', string='Loan')

    @api.onchange('fund_name')
    @api.multi
    def compute_current_price(self):
        self.current_price = self.fund_name.product_pricing.price



class AccountInvoiceRelate(models.Model):
    _inherit = 'account.invoice'

    loan_id = fields.Many2one('ppf.loan', string='Loan')
