from odoo import models, fields, api


class fundraise(models.Model):
    _name = 'ppf.types'
    _rec_name = 'type'

    type=fields.Selection([('Fund', 'Fund'),
                                        ('Money', 'Money'), ],
                                       'Type', track_visibility='onchange')
    disc = fields.Char('Describtion')


# class unit(models.Model):
#     _name = 'ppf.new_unit'
#
#     name = fields.Many2one('ppf.fundraise')
#     unit_date_from = fields.Date()
#     unit_date_to = fields.Date()
#     unit_value = fields.Float()
#     fund_allocation_id = fields.Many2one('ppf.fundallocation')








