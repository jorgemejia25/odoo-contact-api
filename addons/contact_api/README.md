# API REST para Gestión de Contactos en Odoo

Esta API REST permite gestionar contactos en Odoo. Proporciona métodos para obtener, crear, actualizar y agregar comentarios a los contactos.

## Endpoints

### Obtener Contactos

- **URL:** `/api/contacts`
- **Método:** `GET`
- **Descripción:** Obtiene una lista de contactos que no son compañías.
- **Respuesta:**
  - `200 OK`: JSON con la lista de contactos.

### Agregar Comentario a un Contacto

- **URL:** `/api/contacts/add_comment`
- **Método:** `POST`
- **Descripción:** Agrega un comentario a un contacto existente.
- **Datos esperados en el cuerpo de la solicitud:**
  - `phone` (str): Número de teléfono del contacto (obligatorio).
  - `comment` (str): Comentario a agregar (opcional, por defecto 'No comment provided').
- **Respuesta:**
  - `200 OK`: JSON con el resultado de la operación.
  - `400 Bad Request`: JSON con un mensaje de error si falta el número de teléfono.
  - `404 Not Found`: JSON con un mensaje de error si no se encuentra el contacto.

### Crear Contacto

- **URL:** `/api/contacts`
- **Método:** `POST`
- **Descripción:** Crea un nuevo contacto.
- **Propiedades esperadas en `kwargs`:**
  - `phone` (str): Número de teléfono del contacto (obligatorio).
  - `comment` (str): Comentario a agregar (opcional, por defecto 'No comment provided').
- **Respuesta:**
  - `200 OK`: JSON con el resultado de la operación.
  - `400 Bad Request`: JSON con un mensaje de error si falta el número de teléfono.

### Actualizar Contacto

- **URL:** `/api/contact/update`
- **Método:** `POST`
- **Descripción:** Actualiza los detalles de un contacto existente o crea uno nuevo si no se encuentra.
- **Propiedades esperadas en `kwargs`:**
  - `phone` (str): Número de teléfono del contacto (obligatorio).
  - `name` (str): Nombre del contacto (opcional).
  - `email` (str): Correo electrónico del contacto (opcional).
  - `company_id` (int): ID de la compañía asociada al contacto (opcional).
- **Respuesta:**
  - `200 OK`: JSON con el resultado de la operación.
  - `400 Bad Request`: JSON con un mensaje de error si falta el número de teléfono.
  - `404 Not Found`: JSON con un mensaje de error si no se encuentra el contacto y no se puede crear uno nuevo.

## Ejemplos de Uso

### Obtener Contactos

```bash
curl -X GET http://localhost:8069/api/contacts
```

### Agregar Comentario a un Contacto

```bash
curl -X POST http://localhost:8069/api/contacts/add_comment \
    -H "Content-Type: application/json" \
    -d '{"phone": "123456789", "comment": "Este es un comentario"}'
```

### Crear Contacto

```bash
curl -X POST http://localhost:8069/api/contacts \
    -H "Content-Type: application/json" \
    -d '{"phone": "123456789", "comment": "Nuevo contacto"}'
```

### Actualizar Contacto

```bash
curl -X POST http://localhost:8069/api/contact/update \
    -H "Content-Type: application/json" \
    -d '{"phone": "123456789", "name": "Nuevo Nombre", "email": "nuevo@correo.com", "company_id": 1}'
```