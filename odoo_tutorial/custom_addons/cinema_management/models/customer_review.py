# -*- coding: utf-8 -*-
"""
name: Customer Review Model
description: This model tracks user reviews and scores which are used to sort movies.
"""

from odoo import models, fields, api

class CustomerReview(models.Model):
    _name = 'customer.review'
    _description = 'Customer Review'

    movie_id = fields.Many2one('cinema.movie', string='Movie', required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    score = fields.Float(string='Score (1-5)', default=5.0)
    review = fields.Text(string='Review')