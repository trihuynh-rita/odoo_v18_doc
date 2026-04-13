# -*- coding: utf-8 -*-
"""
Employee profile model for HRM MVP.
"""

from odoo import models, fields


class HrmEmployee(models.Model):
    _name = 'hrm.employee'
    _description = 'HRM Employee'

    name = fields.Char(string='Employee Name', required=True)
    employee_code = fields.Char(string='Employee Code')
    major = fields.Char(string='Major')
    department = fields.Char(string='Department')
    job_title = fields.Char(string='Job Title')
    hire_date = fields.Date(string='Hire Date')

    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    address = fields.Char(string='Address')
    birth_date = fields.Date(string='Birth Date')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender')

    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        required=True,
    )
    salary = fields.Monetary(string='Salary', currency_field='currency_id')

    history_work_ids = fields.One2many(
        'hrm.history.work',
        'employee_id',
        string='Work History',
    )
