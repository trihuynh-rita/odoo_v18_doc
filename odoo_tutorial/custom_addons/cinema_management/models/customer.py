# -*- coding: utf-8 -*-
"""
name: Customer Model
description: Inherits res.partner to hold customer specific details including reviews they submitted.
"""

from odoo import models, fields, api

class Customer(models.Model):
    _inherit = 'res.partner'

    birth_date = fields.Date(string='Birth date')
    review_ids = fields.One2many('customer.review', 'customer_id', string='Reviews')
