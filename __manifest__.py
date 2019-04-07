# -*- coding: utf-8 -*-
{
    'name': "Exit Reenter",

    'summary': """ this module for request exit entry for saudi hr systems 
        """,

    'author': "Raed Technology",
    'website': "http://www.raedtechnology.com",

    'category': 'hr',
    'version': '0.1',
    'depends': ['base','common_base','hr_contract_allded','hr'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/views.xml',
        'security/ir.model.access.csv',

    ],
    # only loaded in demonstration mode
}