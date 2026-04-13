import requests
import logging
import re
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class CinemaApiController(http.Controller):
    """
    API controller for providing cinema-related data externally.
    Exposes cinema data as JSON endpoints consumable by external systems.
    """

    @http.route('/api/cinema/customers', type='json', auth='public', methods=['POST'], csrf=False)
    def get_customers_json(self, **kwargs):  # ✅ Đổi tên hàm
        customers = request.env['res.partner'].sudo().search([('is_company', '=', False)])
        result = []
        for customer in customers:
            result.append({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email or '',
                'birth_date': str(customer.birth_date) if customer.birth_date else False,
            })
        return {'status': 'success', 'count': len(result), 'data': result}

    @http.route('/api/cinema/v1/customers', type='http', auth='public', methods=['GET'], csrf=False)
    def get_customers_public(self, **kwargs):  # ✅ Đổi tên hàm
        import json
        from odoo.http import Response

        customers = request.env['res.partner'].sudo().search([('is_company', '=', False)])
        result = []
        for customer in customers:
            result.append({
                'id': customer.id,
                'name': customer.name,
                'email': customer.email or '',
            })

        return Response(
            json.dumps({'status': 'success', 'count': len(result), 'data': result}),
            content_type='application/json',  # ✅ Trả về JSON đúng chuẩn
            status=200
        )

    @http.route('/api/cinema/v1/customers', type='http', auth='public', methods=['POST'], csrf=False, cors='*')
    def create_customer_public(self, **kwargs):
        """
        Creates a new customer (res.partner) via a REST POST request.
        Expects a JSON body with 'name' and optionally 'email'.
        """
        import json
        from odoo.http import Response

        try:
            # Parse JSON body from raw HTTP request
            # We use type='http' to allow standard REST JSON payloads 
            # instead of requiring Odoo's JSON-RPC format.
            body = request.httprequest.data
            if not body:
                return Response(
                    json.dumps({'status': 'error', 'message': 'Empty request body'}),
                    content_type='application/json',
                    status=400
                )
            
            data = json.loads(body.decode('utf-8'))
            name = data.get('name')
            email = data.get('email')

            if not name:
                return Response(
                    json.dumps({'status': 'error', 'message': 'Missing required field: "name"'}),
                    content_type='application/json',
                    status=400
                )

            # Check for existing customer by email (optional, avoids duplicates)
            if email:
                existing_customer = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
                if existing_customer:
                    return Response(
                        json.dumps({'status': 'error', 'message': 'Customer with this email already exists'}),
                        content_type='application/json',
                        status=409
                    )

            # Create the customer record with sudo() since auth='public'
            new_customer = request.env['res.partner'].sudo().create({
                'name': name,
                'email': email,
                'is_company': False,  # Ensure it is created as an individual, not a company
            })

            result = {
                'id': new_customer.id,
                'name': new_customer.name,
                'email': new_customer.email or '',
            }

            return Response(
                json.dumps({'status': 'success', 'data': result}),
                content_type='application/json',
                status=201
            )

        except json.JSONDecodeError:
            return Response(
                json.dumps({'status': 'error', 'message': 'Invalid JSON format'}),
                content_type='application/json',
                status=400
            )
        except Exception as e:
            _logger.error("Error creating customer from API: %s", str(e))
            return Response(
                json.dumps({'status': 'error', 'message': 'Internal Server Error'}),
                content_type='application/json',
                status=500
            )

    @http.route('/api/cinema/v1/customers_json', type='json', auth='public', methods=['POST'], csrf=False, cors='*')
    def create_customer_json(self, **kwargs):
        """
        Creates a new customer via an Odoo JSON-RPC request.
        Arguments are natively extracted directly from kwargs.
        """
        # Because of type='json', Odoo maps the 'params' object to kwargs!
        name = kwargs.get('name')
        email = kwargs.get('email')

        if not name:
            # Odoo wraps this in the JSON-RPC response automatically
            return {'status': 'error', 'message': 'Missing required field: "name"'}

        if email:
            existing_customer = request.env['res.partner'].sudo().search([('email', '=', email)], limit=1)
            if existing_customer:
                return {'status': 'error', 'message': 'Customer with this email already exists'}

        new_customer = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'is_company': False,
        })

        # Whatever dictionary is returned here is automatically embedded into a 'result' key
        return {
            'status': 'success',
            'data': {
                'id': new_customer.id,
                'name': new_customer.name,
                'email': new_customer.email or '',
            }
        }
