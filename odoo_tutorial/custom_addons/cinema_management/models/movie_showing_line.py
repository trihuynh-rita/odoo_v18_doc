# -*- coding: utf-8 -*-
"""
name: Movie Showing Line Model
description: Represents an individual attendee/ticket for a movie showing.
             When confirmed, it creates a Sale Order and passes the ticket price
             via the ORM context so the overridden sale.order.create can
             automatically generate a Sale Order Line with the correct price.
"""

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class MovieShowingLine(models.Model):
    _name = 'movie.showing.line'
    _description = 'Movie Showing Line (Ticket)'

    # --- Core Fields ---
    showing_id = fields.Many2one(
        'movie.showing',
        string='Showing',
        required=True,
        ondelete='cascade',
    )
    customer_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
    )

    # --- Related Fields (from the showing) ---
    ticket_price = fields.Integer(
        related='showing_id.price',
        string='Ticket Price',
        store=True,
        readonly=True,
    )
    movie_name = fields.Char(
        related='showing_id.movie_id.name',
        string='Movie',
        store=True,
        readonly=True,
    )
    date_start = fields.Datetime(
        related='showing_id.date_start',
        string='Date',
        store=True,
        readonly=True,
    )

    # --- Sale Order Link ---
    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        readonly=True,
        copy=False,
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='draft', string='Status', tracking=True)

    def action_confirm_ticket(self):
        """
        Confirm the ticket and create a Sale Order for the customer.
        The ticket_price is passed via the ORM context so that the
        overridden sale.order.create() can automatically generate an
        order line with the correct price.

        Flow:
            1. Pack ticket_price and movie_name into context.
            2. Call sale.order.create() with the enriched context.
            3. The overridden create() in sale_order.py reads context
               and adds a Sale Order Line automatically.
        """
        for record in self:
            if record.state != 'draft':
                raise ValidationError(
                    _('Only draft tickets can be confirmed.')
                )

            # --- Step 1: Pack data into the context ("backpack") ---
            sale_order = self.env['sale.order'].with_context(
                ticket_price=record.ticket_price,
                movie_name=record.movie_name,
            ).create({
                'partner_id': record.customer_id.id,
            })

            # --- Step 2: Link sale order back to the ticket line ---
            record.write({
                'sale_order_id': sale_order.id,
                'state': 'confirmed',
            })

            # --- Step 3: Also register the customer as an attendee ---
            record.showing_id.write({
                'attendee_ids': [(4, record.customer_id.id)],
            })

    def action_cancel_ticket(self):
        """Cancel the ticket and revert the attendee registration."""
        for record in self:
            if record.state != 'confirmed':
                raise ValidationError(
                    _('Only confirmed tickets can be cancelled.')
                )
            record.write({'state': 'cancelled'})
            # Remove the customer from the showing attendees
            record.showing_id.write({
                'attendee_ids': [(3, record.customer_id.id)],
            })
