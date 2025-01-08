from odoo import http
from odoo.http import request, Response
import json

class ContactsRestApi(http.Controller):
    """
    API REST para gestionar contactos en Odoo.
    
    Métodos:
    - get_example: Obtiene una lista de contactos.
    - add_comment: Agrega un comentario a un contacto.
    - create_contact: Crea un nuevo contacto.
    - update_contact: Actualiza los detalles de un contacto existente o crea uno nuevo si no se encuentra.
    """

    @http.route('/api/contacts', type='http', auth='public', methods=['GET'], csrf=False)
    def get_example(self):
        """
        Obtiene una lista de contactos que no son compañías.
        
        Retorna:
        - JSON con la lista de contactos.
        """
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
        print("adding comment")
        """
        Agrega un comentario a un contacto existente.
        
        Datos esperados en el cuerpo de la solicitud:
        - phone (str): Número de teléfono del contacto (obligatorio).
        - comment (str): Comentario a agregar (opcional, por defecto 'No comment provided').
        
        Retorna:
        - JSON con el resultado de la operación.
        """
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
        print("creating contact")
        """
        Crea un nuevo contacto.
        
        Propiedades esperadas en kwargs:
        - phone (str): Número de teléfono del contacto (obligatorio).
        - comment (str): Comentario a agregar (opcional, por defecto 'No comment provided').
        
        Retorna:
        - JSON con el resultado de la operación.
        """
        contact_phone = kwargs.get('phone')
        comment = kwargs.get('comment', 'No comment provided')
        
        print(contact_phone)
        print(comment)
        
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
        
    @http.route('/api/contact/update', type='http', auth='public', methods=['POST'], csrf=False)
    def update_contact(self, **kwargs):
        print("updating contact")
        """
        Actualiza los detalles de un contacto existente o crea uno nuevo si no se encuentra.
        
        Propiedades esperadas en kwargs:
        - phone (str): Número de teléfono del contacto (obligatorio).
        - name (str): Nombre del contacto (opcional).
        - email (str): Correo electrónico del contacto (opcional).
        - company_id (int): ID de la compañía asociada al contacto (opcional).
        
        Retorna:
        - JSON con el resultado de la operación.
        """
        # search for the contact by phone number, if not found, create a new contact
        contact_phone = kwargs.get('phone')
        
        if not contact_phone:
            return http.Response(
                json.dumps({'error': 'Phone number is required'}),
                content_type='application/json',
                status=400
            )
            
        contact_phone = contact_phone.strip()
        
        # Eliminar espacios en blanco del número de teléfono
        contact_phone = contact_phone.replace(' ', '')
        
        # Eliminar signo de más del número de teléfono
        contact_phone = contact_phone.replace('+', '')
        contact_phone = contact_phone.replace('-', '')

        contact = request.env['res.partner'].sudo().search([('phone', '=', contact_phone)], limit=1)

        if not contact:
            # Crear un nuevo contacto si no se encuentra
            contact = request.env['res.partner'].sudo().create({
                'name': kwargs.get('name', 'Unknown'),
                'email': kwargs.get('email', ''),
                'phone': contact_phone,
                'company_id': kwargs.get('company_id', False)
            })

            return http.Response(
                json.dumps({'success': 'Contact created successfully'}),
                content_type='application/json'
            )

        # Actualizar los detalles del contacto
        contact.write({
            'name': kwargs.get('name', contact.name),
            'email': kwargs.get('email', contact.email),
            'phone': contact_phone,
            'company_id': kwargs.get('company_id', contact.company_id.id)
        })

        return http.Response(
            json.dumps({'success': 'Contact updated successfully'}),
            content_type='application/json'
        )
