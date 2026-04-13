# -*- coding: utf-8 -*-
"""
Work history log model for HRM MVP.
"""

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrmHistoryWork(models.Model):
    _name = 'hrm.history.work'
    _description = 'HRM Work History'
    _order = 'date_start desc, id desc'

    name = fields.Char(string='Work Title', required=True)
    employee_id = fields.Many2one('hrm.employee', string='Employee', required=True, ondelete='cascade')

    status = fields.Selection([
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    ], string='Status', default='pending', required=True)

    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='employee_id.currency_id',
        store=True,
        readonly=True,
    )
    award_amount = fields.Monetary(
        string='Award (Salary Bonus)',
        currency_field='currency_id',
        help='Salary award if the work is done well.',
    )
    note = fields.Text(string='Note')

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError('End Date must be greater than or equal to Start Date.')
