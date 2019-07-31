from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

class ppfYearly(models.Model):
    _name = 'ppf.yearly.balance'

    year = fields.Selection([(num, str(num)) for num in range(2000, (datetime.now().year)+1 )], 'Year')
    department = fields.Many2one('ppf.department', string='Subsidiary')
    yearly_balance_created = fields.Boolean('is yearly balance created ?', default=False)
    name = fields.Char('Name')
    jan_employee_share = fields.Float('Jan Employee Share')
    jan_company_share = fields.Float('Jan Company Share')
    jan_booster = fields.Float('Jan Booster')
    feb_employee_share = fields.Float('Feb Employee Share')
    feb_company_share = fields.Float('Feb Company Share')
    feb_booster = fields.Float('Feb Booster')
    mar_employee_share = fields.Float('Mar Employee Share')
    mar_company_share = fields.Float('Mar Company Share')
    mar_booster = fields.Float('Mar Booster')
    apr_employee_share = fields.Float('Apr Employee Share')
    apr_company_share = fields.Float('Apr Company Share')
    apr_booster = fields.Float('Apr Booster')
    may_employee_share = fields.Float('May Employee Share')
    may_company_share = fields.Float('May Company Share')
    may_booster = fields.Float('May Booster')
    jun_employee_share = fields.Float('Jun Employee Share')
    jun_company_share = fields.Float('Jun Company Share')
    jun_booster = fields.Float('Jun Booster')
    jul_employee_share = fields.Float('Jul Employee Share')
    jul_company_share = fields.Float('Jul Company Share')
    jul_booster = fields.Float('Jul Booster')
    aug_employee_share = fields.Float('Aug Employee Share')
    aug_company_share = fields.Float('Aug Company Share')
    aug_booster = fields.Float('Aug Booster')
    sep_employee_share = fields.Float('Sep Employee Share')
    sep_company_share = fields.Float('Sep Company Share')
    sep_booster = fields.Float('Sep Booster')
    oct_employee_share = fields.Float('Oct Employee Share')
    oct_company_share = fields.Float('Oct Company Share')
    oct_booster = fields.Float('Oct Booster')
    nov_employee_share = fields.Float('Nov Employee Share')
    nov_company_share = fields.Float('Nov Company Share')
    nov_booster = fields.Float('Nov Booster')
    dec_employee_share = fields.Float('Dec Employee Share')
    dec_company_share = fields.Float('Dec Company Share')
    dec_booster = fields.Float('Dec Booster')
    total_emp = fields.Float('Total Employee', store=True, readonly=True, compute='compute_total_emp')
    total_comp = fields.Float('Total Company', store=True, readonly=True, compute='compute_total_comp')
    total_booster = fields.Float('Total Booster', store=True, readonly=True, compute='compute_total_booster')

    @api.one
    @api.depends('jan_employee_share', 'feb_employee_share', 'mar_employee_share', 'apr_employee_share',
                 'may_employee_share', 'jun_employee_share', 'jul_employee_share', 'aug_employee_share',
                 'sep_employee_share', 'oct_employee_share', 'nov_employee_share', 'dec_employee_share')
    def compute_total_emp(self):
        self.total_emp = self.jan_employee_share + self.feb_employee_share + self.mar_employee_share + \
                         self.apr_employee_share + self.may_employee_share + self.jun_employee_share + \
                         self.jul_employee_share + self.aug_employee_share + self.sep_employee_share + \
                         self.oct_employee_share + self.nov_employee_share + self.dec_employee_share

    @api.one
    @api.depends('jan_company_share', 'feb_company_share', 'mar_company_share', 'apr_company_share',
                 'may_company_share', 'jun_company_share', 'jul_company_share', 'aug_company_share',
                 'sep_company_share', 'oct_company_share', 'nov_company_share', 'dec_company_share')
    def compute_total_comp(self):
        self.total_comp = self.jan_company_share + self.feb_company_share + self.mar_company_share + \
                          self.apr_company_share + self.may_company_share + self.jun_company_share + \
                          self.jul_company_share + self.aug_company_share + self.sep_company_share + \
                          self.oct_company_share + self.nov_company_share + self.dec_company_share

    @api.one
    @api.depends('jan_booster', 'feb_booster', 'mar_booster', 'apr_booster', 'may_booster', 'jun_booster',
                 'jul_booster', 'aug_booster', 'sep_booster', 'oct_booster', 'nov_booster', 'dec_booster')
    def compute_total_booster(self):
        self.total_booster = self.jan_booster + self.feb_booster + self.mar_booster + self.apr_booster + \
                             self.may_booster + self.jun_booster + self.jul_booster + self.aug_booster + \
                             self.sep_booster + self.oct_booster + self.nov_booster + self.dec_booster

    # @api.model_cr
    # @api.one
    # def compute_total_amount(self):
    #     emp = self.env['res.partner'].search([('department', '=', self.department.id)])
    #     res = []
    #     seen = []
    #     for rec in emp:
    #         sub = self.env['ppf.subscription.line'].search([('member_name', '=', rec.id),
    #                                                         ('subscription_id.batch_date', '>=', self.from_date),
    #                                                         ('subscription_id.batch_date', '<=', self.to)])
    #         own = 0.0
    #         company = 0.0
    #         booster = 0.0
    #         for record in sub:
    #             own += record.own
    #             company += record.company
    #             booster += record.booster
    #         name = rec.name
    #         res.append({"name": name, "own": own, "company": company, "booster": booster})
    #     print(res)
    #     for elem in res:
    #         if elem in seen:
    #             return('Duplicated')
    #         else:
    #             self.env['ppf.yearly.balance.line'].create({
    #                 'name': elem['name'],
    #                 'employee_share': elem['own'],
    #                 'company_share': elem['company'],
    #                 'booster': elem['booster'],
    #                 'yearly_balance_id': self.id,
    #             })
    #             seen.append(elem)
    #
    #     self.yearly_balance_created = True
    #
    #     self.env.cr.execute("DELETE FROM ppf_subscription WHERE ppf_subscription.department = %s" \
    #             "And batch_date >= %s And batch_date <= %s;",(self.department.id,self.from_date,self.to))

    @api.model_cr
    @api.one
    def compute_total_amount(self):
        emp = self.env['res.partner'].search([('department', '=', self.department.id)])
        res = []
        seen = []

        year = datetime.strptime(str(self.year), '%Y').year
        from_date = datetime.strptime('01/01/' + str(year), '%m/%d/%Y').date()
        to_date = datetime.strptime('01/31/' + str(year), '%m/%d/%Y').date()
        print(year)
        for rec in emp:
            res1 = []
            res2 = []
            res3 = []
            for month in range(0, 12):
                add_mon = relativedelta(months=month)
                From = from_date + add_mon
                to = to_date + add_mon
                # print(From)
                # print(to)

                sub = self.env['ppf.subscription.line'].search([('member_name', '=', rec.id),
                                                           ('subscription_id.batch_date', '>=', From),
                                                ('subscription_id.batch_date', '<=', to)])
                res1.append(sub.own)
                res2.append(sub.company)
                res3.append(sub.booster)

            name = rec.name
            res.append({"name": name, "own": res1, "company": res2, "booster": res3})
        print(res[0]['own'][11])

        for elem in res:
            if elem in seen:
                return ('Duplicated')
            else:
                self.env['ppf.yearly.balance'].create({
                    'name': elem['name'],
                    'department': self.department.id,
                    'year': self.year,
                    'jan_employee_share': elem['own'][0],
                    'jan_company_share': elem['company'][0],
                    'jan_booster': elem['booster'][0],
                    'feb_employee_share': elem['own'][1],
                    'feb_company_share': elem['company'][1],
                    'feb_booster': elem['booster'][1],
                    'mar_employee_share': elem['own'][2],
                    'mar_company_share': elem['company'][2],
                    'mar_booster': elem['booster'][2],
                    'apr_employee_share': elem['own'][3],
                    'apr_company_share': elem['company'][3],
                    'apr_booster': elem['booster'][3],
                    'may_employee_share': elem['own'][4],
                    'may_company_share': elem['company'][4],
                    'may_booster': elem['booster'][4],
                    'jun_employee_share': elem['own'][5],
                    'jun_company_share': elem['company'][5],
                    'jun_booster': elem['booster'][5],
                    'jul_employee_share': elem['own'][6],
                    'jul_company_share': elem['company'][6],
                    'jul_booster': elem['booster'][6],
                    'aug_employee_share': elem['own'][7],
                    'aug_company_share': elem['company'][7],
                    'aug_booster': elem['booster'][7],
                    'sep_employee_share': elem['own'][8],
                    'sep_company_share': elem['company'][8],
                    'sep_booster': elem['booster'][8],
                    'oct_employee_share': elem['own'][9],
                    'oct_company_share': elem['company'][9],
                    'oct_booster': elem['booster'][9],
                    'nov_employee_share': elem['own'][10],
                    'nov_company_share': elem['company'][10],
                    'nov_booster': elem['booster'][10],
                    'dec_employee_share': elem['own'][11],
                    'dec_company_share': elem['company'][11],
                    'dec_booster': elem['booster'][11],
                    'yearly_balance_id': self.id,
                })
                seen.append(elem)

        self.yearly_balance_created = True
        # self.env["ppf.subscription"].search_read([])
        #
        # self.env["ppf.subscription"].search([('department', '=', self.department.id),
        #                                      (datetime.strptime('batch_date', '%m/%d/%Y').year, '=', year)]).unlink()
        self.env.cr.execute("DELETE FROM ppf_subscription WHERE ppf_subscription.department  = %s "
                            ,[self.department.id])

        # self.env.cr.execute("DELETE FROM ppf_subscription_line WHERE"
        #                     "ppf_subscription_line.subscription_id.department  = %s "
        #                     ,[self.department.id])



class ppfYearlyLine(models.Model):
    _name = 'ppf.yearly.balance.line'








