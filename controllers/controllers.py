# -*- coding: utf-8 -*-
from odoo import http

# class FundMang(http.Controller):
#     @http.route('/fund_mang/fund_mang/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fund_mang/fund_mang/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fund_mang.listing', {
#             'root': '/fund_mang/fund_mang',
#             'objects': http.request.env['fund_mang.fund_mang'].search([]),
#         })

#     @http.route('/fund_mang/fund_mang/objects/<model("fund_mang.fund_mang"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fund_mang.object', {
#             'object': obj
#         })