# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Export Sale Order in Excel',
    'version': '14.0.1.0',
    'sequence': 1,
    'category': 'Generic Modules/Sales Management',
    'description':
        """
odoo apps will Export Sale Order into Excel sheet

Export Sale Order in Excel
Odoo Export Sale Order in Excel
Sale order 
Odoo sale order 
Export sale order 
Odoo export sale order 
Sale order in excel 
Odoo sale order in excel 
Apps will Export Sale Order into Excel sheet
Odoo Apps will Export Sale Order into Excel sheet
Manage sale order 
Odoo manage sale order 
Manage sale order in excel 
Odoo manage sale order in excel 
Print sale order in excel 
Odoo print sale order in excel 
Print sale order in csv 
Odoo print sale order in csv 
Sale order
Odoo sale order

    """,
    'summary': 'Export Sale Order into Excel sheet, expoer sale order, export sale excel, export sale int excel sheet,excel export for sale order , export excel sle order line, export sale excel, export sale order line excel, export sale order, export customer sales',
    'author': 'Devintelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',
    'images': ['images/main_screenshot.png'],
    'depends': ['sale'],
    'data': [   
            'security/ir.model.access.csv',
            'wizard/sale_history_product.xml',
        ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price':9.0,
    'currency':'EUR', 
    'live_test_url':'https://youtu.be/EMu3PnP_I-A', 
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
