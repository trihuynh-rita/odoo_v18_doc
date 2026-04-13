# -*- coding: utf-8 -*-
"""
name: Sale Order Override
description: Inherits sale.order to intercept the ticket_price passed via ORM
             context. When a Sale Order is created with ticket_price in context,
             this override automatically generates a Sale Order Line with the
             movie ticket details and correct price.
"""

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to catch ticket_price from context and auto-generate
        a Sale Order Line.

        Parameters:
            vals_list (list[dict]): List of value dictionaries for new records.

        Returns:
            recordset: The newly created sale.order records.

        Context keys consumed:
            - ticket_price (int): The price of the movie ticket.
            - movie_name (str): The name of the movie for the order line label.
        """
        # Step 1: Run the original create logic first
        orders = super().create(vals_list)

        # Step 2: Unpack the "backpack" — read ticket data from context
        ticket_price = self.env.context.get('ticket_price')
        movie_name = self.env.context.get('movie_name', 'Movie Ticket')

        # Step 3: If ticket_price exists, create a Sale Order Line automatically
        if ticket_price:
            for order in orders:
                self.env['sale.order.line'].create({
                    'order_id': order.id,
                    'name': f'Movie Ticket: {movie_name}',
                    'product_uom_qty': 1,
                    'price_unit': ticket_price,
                })

        return orders
