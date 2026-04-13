# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MovieShowing(models.Model):
    _name = 'movie.showing'
    _description = 'Movie Showing'

    movie_id = fields.Many2one('cinema.movie', string='Movie')
    movie_theater_id = fields.Many2one('movie.theater', string='Movie theater')
    theater_room_id = fields.Many2one('theater.room', string='Theater room')
    seats_number = fields.Integer(related='theater_room_id.seats_number', store=True)
    attendee_ids = fields.Many2many('res.partner', string='Attendees')
    ticket_line_ids = fields.One2many('movie.showing.line', 'showing_id', string='Tickets')
    total_attendees = fields.Integer(string='Total audience', compute='_compute_total_attendees', store=True)
    date_start = fields.Datetime(string='Date start')
    date_end = fields.Datetime(string='Date end')
    is_past = fields.Boolean(string="Is Past", compute="_compute_is_past", store="True")
    price = fields.Integer(string="Price", default=lambda self: self.env['ir.config_parameter'].sudo().get_param('cinema_management.ticket_price', default=0))

    status = fields.Selection([
        ('open', 'Open'),
        ('ended', 'Ended'),
        ('Playing', 'Playing'),
    ], default='open', string='Status')

    def write(self, vals):
        if vals and 'status' in vals:
            if not self.env.user.has_group('cinema_management.cinema_manager_group'):
                raise ValidationError(_('Only Managers can change the status.'))
        return super().write(vals)


    def _compute_is_past(self):
        for showing in self:
            if showing.date_start and showing.date_start < fields.Datetime.now().replace(hour=0, minute=0, second=0):
                showing.is_past = True
            else: 
                showing.is_past = False

    @api.depends('attendee_ids')
    def _compute_total_attendees(self):
        for showing in self:
            showing.total_attendees = len(showing.attendee_ids)
