# Project Cafeteria

## Descripción
Sistema de gestión para una cafetería que permite administrar productos, pedidos y usuarios.  
Este proyecto está orientado al desarrollo de una aplicación web con backend en Python.

---

## Guía de instalación paso a paso

1. Clonar el repositorio:
```bash
git clone https://github.com/cristianobeltranjosephsebastia-design/ProjectCafeteria.git
```

2. Entrar al proyecto:
```bash
cd ProjectCafeteria
```

3. Crear entorno virtual:
```bash
python -m venv venv
```

4. Activar entorno virtual:

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

5. Instalar dependencias:
```bash
pip install -r requirements.txt
```

6. Ejecutar el servidor:
```bash
python manage.py runserver
```

---

## Requisitos de instalación

### Versión de Python
* Python 3.10 o superior

### Herramientas específicas
* pip  
* virtualenv  
* Git  
* Firebase  

---

## Stack tecnológico

* Python  
* Django / Django REST Framework  
* Firebase  
* HTML, CSS, JavaScript  

---

## Documentación de la API

La API permite gestionar productos, pedidos y usuarios dentro del sistema de cafetería.

---

### Base URL
```http
http://127.0.0.1:8000/api/
```

---

### Endpoints disponibles

### 1. Obtener productos
```http
GET /api/productos/
```

**Descripción:** Obtiene la lista de productos disponibles.

**Respuesta:**
```json
[
  {
    "id": 1,
    "nombre": "Café",
    "precio": 2500,
    "disponibilidad": true
  }
]
```

---

### 2. Crear pedido
```http
POST /api/pedidos/
```

**Descripción:** Permite crear un nuevo pedido.

**Body (JSON):**
```json
{
  "usuario_id": 1,
  "productos": [
    {
      "producto_id": 1,
      "cantidad": 2
    }
  ]
}
```

**Respuesta:**
```json
{
  "mensaje": "Pedido creado correctamente"
}
```

---

### 3. Autenticación (Firebase)

**Descripción:** Manejo de usuarios mediante Firebase Authentication.

---

### Códigos de respuesta

* 200 → OK (Solicitud exitosa)  
* 201 → Creado correctamente  
* 400 → Error en la solicitud  
* 401 → No autorizado  
* 404 → No encontrado  

---

---

## Nombres y cuentas

* Cristian Beltrán  
* Joseph Sebastián   
* Juan Daza Alcazar

## Email
* cristianobeltranjosephsebastia@gmail.com
* jostynnicolascristianobeltran@gmail.com
* jpablodaza2007@gmail.com

## Usuarios de GitHub
* cristianobeltranjosephsebastia-design
* NicolasC11-design
* jpablodaza2007


Repositorio:  
https://github.com/cristianobeltranjosephsebastia-design/ProjectCafeteria  

