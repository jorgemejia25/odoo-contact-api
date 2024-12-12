from odoo import http
from odoo.http import request, Response
import json

class ContactsRestApi(http.Controller):

    @http.route('/api/contacts', type='http', auth='public', methods=['GET'], csrf=False)
    def get_example(self):
        contacts = request.env['res.partner'].sudo().search([('is_company', '=', False)])
        
        # Formatear los datos para devolverlos como JSON
        contacts_data = []
        for contact in contacts:
            contacts_data.append({
                'id': contact.id,
                'name': contact.name,
                'email': contact.email,
                'phone': contact.phone,
                'company': contact.company_id.name if contact.company_id else None
            })
        
        # Devolver la respuesta en formato JSON
        return Response(
            json.dumps(contacts_data),
            content_type='application/json',
            status=200
        )
        

    @http.route('/api/contacts/add_comment', type='http', auth='public', methods=['POST'], csrf=False)
    def add_comment(self):
        data = json.loads(request.httprequest.data)

        contact_phone = data.get('phone')
        comment = data.get('comment', 'No comment provided')

        print(contact_phone)
        print(comment)

        if not contact_phone:
            return http.Response(
                json.dumps({'error': 'Phone number is required'}),
                content_type='application/json',
                status=400
            )

        # Normalizar el número de teléfono
        contact_phone = contact_phone.strip().replace(' ', '').replace('+', '').replace('-', '')

        # Buscar el contacto por número de teléfono
        contact = request.env['res.partner'].sudo().search([('phone', '=', contact_phone)], limit=1)

        if not contact:
            return http.Response(
                json.dumps({'error': 'Contact not found'}),
                content_type='application/json',
                status=404
            )

        # Agregar el comentario en el Chatter del contacto
        contact.message_post(body=comment)

        return http.Response(
            json.dumps({'success': 'Comment added successfully'}),
            content_type='application/json'
        )
        
    @http.route('/api/contacts', type='http', auth='public', methods=['POST'], csrf=False)
    def create_contact(self, **kwargs):
        contact_phone = kwargs.get('phone')
        comment = kwargs.get('comment', 'No comment provided')
        
        print (contact_phone)
        print (comment)
        
        if not contact_phone:
            return http.Response(
                json.dumps({'error': 'Phone number is required'}),
                content_type='application/json',
                status=400
            )
            
            
        # trim the phone number
        contact_phone = contact_phone.strip()
        
        # Eliminar espacios en blanco del número de teléfono
        contact_phone = contact_phone.replace(' ', '')
        
        # Eliminar signo de más del número de teléfono
        contact_phone = contact_phone.replace('+', '')
        
        # Eliminar guiones del número de teléfono
        contact_phone = contact_phone.replace('-', '')