# -*- coding: utf-8 -*-
{
    'name': 'HRM MVP',
    'summary': 'Core HR and employee data management (MVP)',
    'author': 'RitaVo',
    'version': '19.0.0.1',
    'category': 'Human Resources',
    'license': 'LGPL-3',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/history_work_views.xml',
        'views/rita_chatbot_views.xml',
        'views/menu_items.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hrm_mvp/static/lib/marked.min.js',
            'hrm_mvp/static/src/js/rita_chatbot.js',
            'hrm_mvp/static/src/xml/rita_chatbot.xml',
            'hrm_mvp/static/src/scss/rita_chatbot.scss',
        ],
    },
    'installable': True,
    'application': True,
}
