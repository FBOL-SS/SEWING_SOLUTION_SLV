# -*- coding: utf-8 -*-

{
    'name': 'Account Custom',
    'version' : '14.0.1.0.0',
    'summary': 'Account Custom',
    'author': 'Heliconia Solutions Pvt. Ltd.',
    'website': 'https://heliconia.io',
    'description': """
        Account Customization
    """,
    'category': 'Accounting/Accounting',
    'depends': [
        'account'
    ],
    'data': [
        'views/account_move_inherit_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
