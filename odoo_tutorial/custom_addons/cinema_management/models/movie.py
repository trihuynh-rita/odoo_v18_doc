"""
name: Movie Comparison Wizard
description: Provides a transient interface to compare external API movie data with Odoo's database without persisting external fields like Price.
"""

import requests
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class CinemaMovie(models.Model):
    _inherit = 'cinema.movie'

    # We keep external_api_id to help with comparison/mapping, 
    # but we won't store 'price' here as requested.
    external_api_id = fields.Char(string='External API ID')

class MovieApiComparator(models.TransientModel):
    _name = 'movie.api.comparator'
    _description = 'Movie API Comparator'

    name = fields.Char(string='Catalog session', default='External Movie Catalog')
    line_ids = fields.One2many('movie.api.comparator.line', 'wizard_id', string='Movie Comparisons')

    @api.model
    def action_view_external_catalog(self):
        """
        Creates a new comparator instance, fetches data immediately, 
        and returns an action to view it in full page.
        """
        new_wizard = self.create({})
        new_wizard.action_fetch_from_api()
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'External Movie Catalog',
            'res_model': 'movie.api.comparator',
            'res_id': new_wizard.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_fetch_from_api(self):
        """
        Fetch movies from API and populate transient lines for comparison.
        """
        api_url = "http://0.0.0.0:8000/movies/"
        self.line_ids.unlink() # Clear previous results
        
        try:
            response = requests.get(api_url, timeout=10)
            if response.status_code == 200:
                movies_data = response.json()
                lines = []
                for data in movies_data:
                    movie_name = data.get('name')
                    ext_id = data.get('id') or data.get('_id')
                    
                    # Check if exists in Odoo
                    existing_movie = self.env['cinema.movie'].search([
                        '|', ('name', '=', movie_name), ('external_api_id', '=', ext_id)
                    ], limit=1)

                    lines.append((0, 0, {
                        'name': movie_name,
                        'category': data.get('category'),
                        'rating': data.get('rating'),
                        'remote_price': data.get('price'), # Keep as string for display
                        'average_score': data.get('average_score', 0.0),
                        'odoo_movie_id': existing_movie.id if existing_movie else False,
                        'status': 'exists' if existing_movie else 'new',
                        'external_api_id': ext_id,
                    }))
                
                self.write({'line_ids': lines})
                
                # Return the same wizard view to show results
                return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'movie.api.comparator',
                    'view_mode': 'form',
                    'res_id': self.id,
                    'target': 'new',
                }
            else:
                raise UserError(_("API returned status: %s") % response.status_code)
        except Exception as e:
            raise UserError(_("Error connecting to API: %s") % str(e))

    def action_import_selected(self):
        """
        Optional: Import movies that don't exist yet.
        """
        for line in self.line_ids:
            if line.status == 'new':
                self.env['cinema.movie'].create({
                    'name': line.name,
                    'category': line.category,
                    'rating': line.rating,
                    'external_api_id': line.external_api_id,
                })
        return {'type': 'ir.actions.act_window_close'}

class MovieApiComparatorLine(models.TransientModel):
    _name = 'movie.api.comparator.line'
    _description = 'Movie API Comparison Line'

    wizard_id = fields.Many2one('movie.api.comparator', string='Wizard')
    name = fields.Char(string='Movie Name')
    category = fields.Char(string='Category (External)')
    rating = fields.Char(string='Rating (External)')
    remote_price = fields.Char(string='Price (External ONLY)')
    average_score = fields.Float(string='API Score', readonly=True)
    
    odoo_movie_id = fields.Many2one('cinema.movie', string='Odoo Movie')
    status = fields.Selection([
        ('new', 'New (Not in Odoo)'),
        ('exists', 'Exists in Odoo')
    ], string='Status', default='new')
    
    external_api_id = fields.Char(string='External ID')
