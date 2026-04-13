# -*- coding: utf-8 -*-

from odoo import models, fields


class TheaterRoom(models.Model):
    _name = 'theater.room'
    _description = 'Theater room'

    name = fields.Char(string='Name')
    movie_theater_id = fields.Many2one('movie.theater', string='Movie theater')
    seats_number = fields.Integer(string='Seats number')
    has_vip_seats = fields.Boolean(string='Has VIP Sheet')
