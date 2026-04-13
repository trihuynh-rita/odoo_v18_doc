# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MovieTheater(models.Model):
    _name = 'movie.theater'
    _description = 'Movie Theater'

    name = fields.Char(string='Name')
    address = fields.Char(string='Address')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help='The company that owns and manages this theater.',
    )
    is_vip = fields.Boolean(string='Is VIP', compute='_is_vip', store=True)
    customer_ids = fields.Many2many('res.partner', string='Customers', compute='_compute_customer_ids', store=True)
    available_movie_ids = fields.Many2many('cinema.movie', string='Available movies')
    theater_room_ids = fields.One2many('theater.room', 'movie_theater_id',string='Theater rooms')
    movie_showing_ids = fields.One2many('movie.showing', 'movie_theater_id', string='Movie showings')

    @api.depends('movie_showing_ids', 'movie_showing_ids.attendee_ids')
    def _compute_customer_ids(self):
        for theater in self:
            theater.customer_ids = theater.mapped('movie_showing_ids.attendee_ids')

    @api.depends('theater_room_ids', 'theater_room_ids.has_vip_seats')
    def _is_vip(self):
        for theater in self:
            if theater.theater_room_ids.filtered(lambda room: room.has_vip_seats):
                theater.is_vip = True
            else:
                theater.is_vip = False
