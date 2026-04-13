# -*- coding: utf-8 -*-
"""
name: Cinema Movie Model
description: This file defines the 'cinema.movie' model. It now includes user reviews and computes an average score for sorting purposes.
"""

from odoo import models, fields, api

class CinemaMovie(models.Model):
    _name = 'cinema.movie'
    _description = 'Movie'
    
    # Sort movies display based on the average score in descending order
    _order = 'average_score desc, name asc'

    name = fields.Char(string='Name')
    category = fields.Selection([('sci_fi', 'Sci-fi'), ('thriller', 'thriller'),
                                 ('action', 'Action'), ('comedy', 'Comedy')], string='Category')
    rating = fields.Selection([('g_rating', 'G'), ('pg_rating', 'PG'), ('pg12_rating', 'PG-13'),
                               ('r_rating', 'R'), ('nc17_rating', 'NC-17')], string='Rating')

    review_ids = fields.One2many('customer.review', 'movie_id', string='Reviews')
    average_score = fields.Float(string='Average Score', compute='_compute_average_score', store=True)

    @api.depends('review_ids.score')
    def _compute_average_score(self):
        """
        Calculates the average score of the movie based on the attached reviews
        to sort them.
        """
        for movie in self:
            if movie.review_ids:
                total_score = sum(movie.review_ids.mapped('score'))
                movie.average_score = total_score / len(movie.review_ids)
            else:
                movie.average_score = 0.0

