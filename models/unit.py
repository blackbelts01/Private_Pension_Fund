from odoo import models, tools, fields, api
from datetime import datetime

class ppfUnit(models.Model):
    _name = 'ppf.unit'

    name = fields.Char('Member Name')
    product = fields.Many2one('product.template', string='Product')
    own = fields.Float('Emp.Share')
    company = fields.Float('Comp.Share')
    booster = fields.Float('Booster')
    own_units = fields.Float('Emp Units', digits=(16, 4))
    company_units = fields.Float('Company Units', digits=(16, 4))
    booster_units = fields.Float('Booster Units', digits=(16, 4))
    date = fields.Date('Allocation Date', default=datetime.today())
    department = fields.Many2one('ppf.department', string='Subsidiary')
    subscription_id = fields.Many2one('ppf.subscription', string='Subscription ID')
    investment_id = fields.Many2one('ppf.investment')



