# name: Cinema Management Manifest
# description: Manifest file for the cinema management module, declaring metadata, dependencies, and data paths.
# -*- coding: utf-8 -*-
{
    'name': "Cinema Management",
    'summary': "Manages the logistic and sales of a multiple movie theaters",
    'author': "Alex Esteves",
    'version': '19.0.0.1',
    "category": "Movies",
    "license": "AGPL-3",
    'depends': ['base', 'sale_management', 'mail_bot'],
    'data': [
        'security/ir.model.access.csv',
        'security/cinema_manager_record_rule.xml',
        'views/movie_theater_views.xml',
        'views/theater_room_views.xml',
        'views/movie_showing_views.xml',
        'views/cinema_movie_views.xml',
        'views/customer_views.xml',
        'views/customer_review_views.xml',
        'views/res_config_setting.xml',
        'views/movie_showing_line_views.xml',
        'views/movie_comparator_views.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": True,
}