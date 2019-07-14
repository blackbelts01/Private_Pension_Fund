from odoo import models, tools, fields, api

class ppfUnit(models.Model):
    _name = 'ppf.unit'

    name = fields.Char('Member Name')
    own = fields.Float('Own')
    company = fields.Float('Company')
    booster = fields.Float('Booster')
    own_units = fields.Float('Own Units')
    company_units = fields.Float('Company Units')
    booster_units = fields.Float('Booster Units')
    date = fields.Date('Allocation Date')

    investment_id = fields.Many2one('ppf.investment')

