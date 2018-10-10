from odoo import models, fields, api
from odoo.exceptions import  ValidationError
class product_fund(models.Model):
    _inherit='product.template'

    product_id=fields.Char('Product id')
    Assest_manger=fields.Many2one('res.partner','Assest Manger')
    issuer=fields.Many2one('res.partner','Issuer')
    product_unit=fields.Char('Product_unit')
    face_value=fields.Many2one('res.currency','Face Value')


    product_compos=fields.One2many('product.composition','product')
    product_pricing=fields.One2many('product.pricing','product_price')

class Product_Composition(models.Model):
    _name='product.composition'
    item=fields.Char('Item')
    perc=fields.Integer('Percentage')
    cat=fields.Many2one('product.category')
    product=fields.Many2one('product.template')


class Product_Price(models.Model):
    _name='product.pricing'
    date_from=fields.Date('Date From')
    date_to = fields.Date('Date To')
    price=fields.Float('Price')
    product_price=fields.Many2one('product.template')



class Partners(models.Model):
    _inherit='res.partner'

    DOB = fields.Date('Date of Birth')
    hiring_date = fields.Date('Hiring Date')
    member_id=fields.Char('Membership_ID')
    job_title=fields.Char('Job Tilte')
    grade = fields.Char('Grade')
    benef = fields.Char('Beneficiary')


    martiual_status = fields.Selection([('Single', 'Single'),
                                        ('Married', 'Married'), ],
                                       'Marital Status', track_visibility='onchange')

    @api.multi
    def search_sub(self):
        sub=self.env['account.invoice.line'].search([('member_name', '=', self.id)])
        inv=self.env['account.invoice'].search([('invoice_line_ids','in',sub.ids)])
        return inv


    @api.multi
    def search_cash_pool(self):
        sub = self.env['account.invoice.line'].search([('member_name', '=', self.id)])
        inv = self.env['account.invoice'].search([('invoice_line_ids', 'in', sub.ids)])
        all_lines = self.env['allocation.lines'].search([('sub', 'in', inv.ids)])
        allocation = self.env['allocation'].search([('allocation_line', 'in', all_lines.ids)])
        # investment = self.env['account.invoice'].search([('allocation_id', 'in', allocation.ids)])

        return allocation
    @api.multi
    def search_invest(self):
        sub = self.env['account.invoice.line'].search([('member_name', '=', self.id)])
        inv = self.env['account.invoice'].search([('invoice_line_ids', 'in', sub.ids)])
        all_lines=self.env['allocation.lines'].search([('sub', 'in', inv.ids)])
        allocation = self.env['allocation'].search([('allocation_line', 'in', all_lines.ids)])
        investment = self.env['account.invoice'].search([('allocation_id', 'in', allocation.ids)])



        return investment







