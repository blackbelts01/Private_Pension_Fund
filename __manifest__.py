# -*- coding: utf-8 -*-
{
    'name': "PPF Private Pension Fund",

    'summary': """Private Pension Fund Management
        """,

    'description': """Private Pension Fund

    """,

    'author': "Black Belts Egypt",
    'website': "www.blackbelts-egypt.com",
    'category': 'Industries',
    'version': '0.1',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base','sale','crm','purchase','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/fund.xml',
        'views/fund_report.xml',
        'views/departments.xml',
        'views/join_to_fund.xml',
        'views/yearly_balance.xml',
        'views/views.xml',
        'views/customer.xml',
        'views/cash_pool.xml',
        'views/subscriptions.xml',
        'views/PPf_menu.xml',
        'views/fundraise.xml',
        'views/investment_policy.xml',
        'views/investment.xml',
        'views/cash_account_trans.xml',
        'views/investment_fund.xml',
        'reports/subs.xml',
        'reports/invest.xml',
        'reports/member_subscription_report.xml',
        'reports/member_investment_report.xml',
        'data/mail_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}