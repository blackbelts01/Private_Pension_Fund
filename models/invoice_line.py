# -*- coding: utf-8 -*-

from odoo import models, fields, api

class invoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    member=fields.Char(string='Member')

