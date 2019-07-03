from odoo import models, fields, api

class ppfYearly(models.Model):
    _name = 'ppf.yearly.balance'

    from_date = fields.Date('From')
    to = fields.Date('To')
    department = fields.Many2one('ppf.department', string='Sub Company')
    yearly_balance = fields.One2many('ppf.yearly.balance.line', 'yearly_balance_id', string='Yearly Balance')
    yearly_balance_created = fields.Boolean('is yearly balance created ?', default=False)

    @api.model_cr
    @api.one
    def compute_total_amount(self):
        emp = self.env['res.partner'].search([('department', '=', self.department.id)])
        res = []
        seen = []
        for rec in emp:
            sub = self.env['ppf.subscription.line'].search([('member_name', '=', rec.id),
                                                            ('subscription_id.batch_date', '>=', self.from_date),
                                                            ('subscription_id.batch_date', '<=', self.to)])
            own = 0.0
            company = 0.0
            booster = 0.0
            for record in sub:
                own += record.own
                company += record.company
                booster += record.booster
            name = rec.name
            res.append({"name": name, "own": own, "company": company, "booster": booster})
        print(res)
        for elem in res:
            if elem in seen:
                return('Duplicated')
            else:
                self.env['ppf.yearly.balance.line'].create({
                    'name': elem['name'],
                    'employee_share': elem['own'],
                    'company_share': elem['company'],
                    'booster': elem['booster'],
                    'yearly_balance_id': self.id,
                })
                seen.append(elem)

        self.yearly_balance_created = True

        self.env.cr.execute("DELETE FROM ppf_subscription WHERE ppf_subscription.department = %s" \
                "And batch_date >= %s And batch_date <= %s;",(self.department.id,self.from_date,self.to))



class ppfYearlyLine(models.Model):
    _name = 'ppf.yearly.balance.line'

    name = fields.Char('Name')
    employee_share = fields.Float('Employee Share')
    company_share = fields.Float('Company Share')
    booster = fields.Float('Booster')
    yearly_balance_id = fields.Many2one('ppf.yearly.balance')





