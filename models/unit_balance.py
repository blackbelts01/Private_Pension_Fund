from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta

class ppfUnitYearly(models.Model):
    _name = 'ppf.unit.yearly.balance'

    year = fields.Selection([(num, str(num)) for num in range(2000, (datetime.now().year)+1 )], 'Year')
    department = fields.Many2one('ppf.department', string='Subsidiary')
    name = fields.Char('Name')

    jan_employee_units = fields.Float('Jan Employee Units', digits=(16, 4))

    jan_company_units = fields.Float('Jan Company Units', digits=(16, 4))

    jan_booster_units = fields.Float('Jan Booster Units', digits=(16, 4))

    feb_employee_units = fields.Float('Feb Employee Units', digits=(16, 4))

    feb_company_units = fields.Float('Feb Company Units', digits=(16, 4))

    feb_booster_units = fields.Float('Feb Booster Units', digits=(16, 4))

    mar_employee_units = fields.Float('Mar Employee Units', digits=(16, 4))

    mar_company_units = fields.Float('Mar Company Units', digits=(16, 4))

    mar_booster_units = fields.Float('Mar Booster Units', digits=(16, 4))

    apr_employee_units = fields.Float('Apr Employee Units', digits=(16, 4))

    apr_company_units = fields.Float('Apr Company Units', digits=(16, 4))

    apr_booster_units = fields.Float('Apr Booster Units', digits=(16, 4))

    may_employee_units = fields.Float('May Employee Units', digits=(16, 4))

    may_company_units = fields.Float('May Company Units', digits=(16, 4))

    may_booster_units = fields.Float('May Booster Units', digits=(16, 4))

    jun_employee_units = fields.Float('Jun Employee Units', digits=(16, 4))

    jun_company_units = fields.Float('Jun Company Units', digits=(16, 4))

    jun_booster_units = fields.Float('Jun Booster Units', digits=(16, 4))

    jul_employee_units = fields.Float('Jul Employee Units', digits=(16, 4))

    jul_company_units = fields.Float('Jul Company Units', digits=(16, 4))

    jul_booster_units = fields.Float('Jul Booster Units', digits=(16, 4))

    aug_employee_units = fields.Float('Aug Employee Units', digits=(16, 4))

    aug_company_units = fields.Float('Aug Company Units', digits=(16, 4))

    aug_booster_units = fields.Float('Aug Booster Units', digits=(16, 4))

    sep_employee_units = fields.Float('Sep Employee Units', digits=(16, 4))

    sep_company_units = fields.Float('Sep Company Units', digits=(16, 4))

    sep_booster_units = fields.Float('Sep Booster Units', digits=(16, 4))

    oct_employee_units = fields.Float('Oct Employee Units', digits=(16, 4))

    oct_company_units = fields.Float('Oct Company Units', digits=(16, 4))

    oct_booster_units = fields.Float('Oct Booster Units', digits=(16, 4))

    nov_employee_units = fields.Float('Nov Employee Units', digits=(16, 4))

    nov_company_units = fields.Float('Nov Company Units', digits=(16, 4))

    nov_booster_units = fields.Float('Nov Booster Units', digits=(16, 4))

    dec_employee_units = fields.Float('Dec Employee Units', digits=(16, 4))

    dec_company_units = fields.Float('Dec Company Units', digits=(16, 4))

    dec_booster_units = fields.Float('Dec Booster Units', digits=(16, 4))
    unit_yearly_balance_id = fields.Many2one('ppf.unit.yearly.balance')

    total_emp_units = fields.Float('Total Employee Units', store=True, readonly=True, compute='compute_total_emp_units')

    total_comp_units = fields.Float('Total Company Units', store=True, readonly=True,
                                    compute='compute_total_comp_units')

    total_booster_units = fields.Float('Total Booster Units', store=True, readonly=True,
                                       compute='compute_total_booster_units')

    unit_yearly_balance_created = fields.Boolean('is unit yearly balance created ?', default=False)

    @api.one
    @api.depends('jan_employee_units', 'feb_employee_units', 'mar_employee_units', 'apr_employee_units',
                 'may_employee_units', 'jun_employee_units', 'jul_employee_units', 'aug_employee_units',
                 'sep_employee_units', 'oct_employee_units', 'nov_employee_units', 'dec_employee_units')
    def compute_total_emp_units(self):
        self.total_emp_units = self.jan_employee_units + self.feb_employee_units + self.mar_employee_units + \
                               self.apr_employee_units + self.may_employee_units + self.jun_employee_units + \
                               self.jul_employee_units + self.aug_employee_units + self.sep_employee_units + \
                               self.oct_employee_units + self.nov_employee_units + self.dec_employee_units

    @api.one
    @api.depends('jan_company_units', 'feb_company_units', 'mar_company_units', 'apr_company_units',
                 'may_company_units', 'jun_company_units', 'jul_company_units', 'aug_company_units',
                 'sep_company_units', 'oct_company_units', 'nov_company_units', 'dec_company_units')
    def compute_total_comp_units(self):
        self.total_comp_units = self.jan_company_units + self.feb_company_units + self.mar_company_units + \
                                self.apr_company_units + self.may_company_units + self.jun_company_units + \
                                self.jul_company_units + self.aug_company_units + self.sep_company_units + \
                                self.oct_company_units + self.nov_company_units + self.dec_company_units

    @api.one
    @api.depends('jan_booster_units', 'feb_booster_units', 'mar_booster_units', 'apr_booster_units',
                 'may_booster_units', 'jun_booster_units', 'jul_booster_units', 'aug_booster_units',
                 'sep_booster_units', 'oct_booster_units', 'nov_booster_units', 'dec_booster_units')
    def compute_total_booster_units(self):
        self.total_booster_units = self.jan_booster_units + self.feb_booster_units + self.mar_booster_units + \
                                   self.apr_booster_units + self.may_booster_units + self.jun_booster_units + \
                                   self.jul_booster_units + self.aug_booster_units + self.sep_booster_units + \
                                   self.oct_booster_units + self.nov_booster_units + self.dec_booster_units




    @api.model_cr
    @api.one
    def compute_total_units(self):
        emp = self.env['res.partner'].search([('department', '=', self.department.id)])
        res = []
        seen = []
        product = 0
        year = datetime.strptime(str(self.year), '%Y').year
        from_date = datetime.strptime('01/01/' + str(year), '%m/%d/%Y').date()
        to_date = datetime.strptime('01/31/' + str(year), '%m/%d/%Y').date()
        # units_list=[]
        # units_per_month=[]
        # for month in range(0, 12):
        #     add_mon = relativedelta(months=month)
        #     From = from_date + add_mon
        #     to = to_date + add_mon
        #     for x in emp:
        #         units = self.env['ppf.unit'].search([('name', '=', x.name), ('date', '>=', From),('date', '<=', to)])
        #         for n in units:
        #             units_per_month.append(n)
        #     # units_list.append(units)
        #     i=0
        #     print(units_per_month)
        #     for elem in units_per_month:
        #         # print(elem)
        #         employees=[]
        #         unit = self.env['ppf.unit'].search(['id','=',elem.id])
        #         employees.append(unit.name)

                # if unit.
                # self.env['ppf.unit.yearly.balance'].create({
                #     'name': unit.name,
                #     'department': self.department.id,
                #     'year': self.year,
                #     'jan_employee_units': elem['own_units'][0],
                #
                #     'jan_company_units': elem['company_units'][0],
                #
                #     'jan_booster_units': elem['booster_units'][0],
                #
                #     'feb_employee_units': elem['own_units'][1],
                #
                #     'feb_company_units': elem['company_units'][1],
                #
                #     'feb_booster_units': elem['booster_units'][1],
                #
                #     'mar_employee_units': elem['own_units'][2],
                #
                #     'mar_company_units': elem['company_units'][2],
                #
                #     'mar_booster_units': elem['booster_units'][2],
                #
                #     'apr_employee_units': elem['own_units'][3],
                #
                #     'apr_company_units': elem['company_units'][3],
                #
                #     'apr_booster_units': elem['booster_units'][3],
                #
                #     'may_employee_units': elem['own_units'][4],
                #
                #     'may_company_units': elem['company_units'][4],
                #
                #     'may_booster_units': elem['booster_units'][4],
                #
                #     'jun_employee_units': elem['own_units'][5],
                #
                #     'jun_company_units': elem['company_units'][5],
                #
                #     'jun_booster_units': elem['booster_units'][5],
                #
                #     'jul_employee_units': elem['own_units'][6],
                #
                #     'jul_company_units': elem['company_units'][6],
                #
                #     'jul_booster_units': elem['booster_units'][6],
                #
                #     'aug_employee_units': elem['own_units'][7],
                #
                #     'aug_company_units': elem['company_units'][7],
                #
                #     'aug_booster_units': elem['booster_units'][7],
                #
                #     'sep_employee_units': elem['own_units'][8],
                #
                #     'sep_company_units': elem['company_units'][8],
                #
                #     'sep_booster_units': elem['booster_units'][8],
                #
                #     'oct_employee_units': elem['own_units'][9],
                #
                #     'oct_company_units': elem['company_units'][9],
                #
                #     'oct_booster_units': elem['booster_units'][9],
                #
                #     'nov_employee_units': elem['own_units'][10],
                #
                #     'nov_company_units': elem['company_units'][10],
                #
                #     'nov_booster_units': elem['booster_units'][10],
                #
                #     'dec_employee_units': elem['own_units'][11],
                #
                #     'dec_company_units': elem['company_units'][11],
                #
                #     'dec_booster_units': elem['booster_units'][11],
                #
                # })
                # i+=1
        # ahmed
        for rec in emp:
            name = rec.name

            res7 = []
            res8 = []
            funds = self.env['product.template'].search([])


            for fund in funds:
                res1 = []
                res2 = []
                res3 = []
                res4 = []
                res5 = []
                res6 = []
                for month in range(0, 12):
                    add_mon = relativedelta(months=month)
                    From = from_date + add_mon
                    to = to_date + add_mon
                    # print(From)
                    # print(to)



                    units = self.env['ppf.unit'].search([('name', '=', rec.name), ('date', '>=', From),
                                                       ('date', '<=', to),('product', '=', fund.id)])

                    own = 0.0
                    company = 0.0
                    booster = 0.0
                    own_units = 0.0
                    company_units = 0.0
                    booster_units = 0.0

                    for record in units:


                        own += record.own
                        company += record.company
                        booster += record.booster
                        own_units += record.own_units
                        company_units += record.company_units
                        booster_units += record.booster_units
                        product = record.product.name
                        name = record.name

                    res1.append(own)
                    res2.append(company)
                    res3.append(booster)
                    res4.append(own_units)
                    res5.append(company_units)
                    res6.append(booster_units)

                res.append({"name": name, 'product': product,"own": res1, "own_units": res4, "company": res2, "company_units": res5,
                        "booster": res3, "booster_units": res6})
            print(res)
        #
        # for elem in res:
        #     self.env['ppf.unit.yearly.balance'].create({
        #             'name': elem['name'],
        #             'department': self.department.id,
        #             'year': self.year,
        #             'jan_employee_units': elem['own_units'][0],
        #
        #             'jan_company_units': elem['company_units'][0],
        #
        #             'jan_booster_units': elem['booster_units'][0],
        #
        #             'feb_employee_units': elem['own_units'][1],
        #
        #             'feb_company_units': elem['company_units'][1],
        #
        #             'feb_booster_units': elem['booster_units'][1],
        #
        #             'mar_employee_units': elem['own_units'][2],
        #
        #             'mar_company_units': elem['company_units'][2],
        #
        #             'mar_booster_units': elem['booster_units'][2],
        #
        #             'apr_employee_units': elem['own_units'][3],
        #
        #             'apr_company_units': elem['company_units'][3],
        #
        #             'apr_booster_units': elem['booster_units'][3],
        #
        #             'may_employee_units': elem['own_units'][4],
        #
        #             'may_company_units': elem['company_units'][4],
        #
        #             'may_booster_units': elem['booster_units'][4],
        #
        #             'jun_employee_units': elem['own_units'][5],
        #
        #             'jun_company_units': elem['company_units'][5],
        #
        #             'jun_booster_units': elem['booster_units'][5],
        #
        #             'jul_employee_units': elem['own_units'][6],
        #
        #             'jul_company_units': elem['company_units'][6],
        #
        #             'jul_booster_units': elem['booster_units'][6],
        #
        #             'aug_employee_units': elem['own_units'][7],
        #
        #             'aug_company_units': elem['company_units'][7],
        #
        #             'aug_booster_units': elem['booster_units'][7],
        #
        #             'sep_employee_units': elem['own_units'][8],
        #
        #             'sep_company_units': elem['company_units'][8],
        #
        #             'sep_booster_units': elem['booster_units'][8],
        #
        #             'oct_employee_units': elem['own_units'][9],
        #
        #             'oct_company_units': elem['company_units'][9],
        #
        #             'oct_booster_units': elem['booster_units'][9],
        #
        #             'nov_employee_units': elem['own_units'][10],
        #
        #             'nov_company_units': elem['company_units'][10],
        #
        #             'nov_booster_units': elem['booster_units'][10],
        #
        #             'dec_employee_units': elem['own_units'][11],
        #
        #             'dec_company_units': elem['company_units'][11],
        #
        #             'dec_booster_units': elem['booster_units'][11],
        #
        #         })


        self.unit_yearly_balance_created = True
        # self.env.cr.execute("DELETE FROM ppf_unit WHERE subscription_id.department = %s"
        #                     , [self.department.id])




