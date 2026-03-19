import requests
import time
import getpass
from google import genai
from google.genai import types

import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# 1. Función de login
def login_usuario():
    print("--- Login De Usuario ---")
    email = input("Email: ")
    password = getpass.getpass("Contraseña: ")
    url_login = "http://127.0.0.1:8000/api/auth/login/" 
    
    try:
        response = requests.post(url_login, json={"email": email, "password": password})
        if response.status_code == 200:
            print("✅ Usuario loggeado exitosamente")
            return response.json().get("token") or response.json().get("idToken")
        print(f"❌ Error: {response.json().get('error')}")
    except Exception as e:
        print(f"⚠️ Error de conexion: {e}")
    return None

# 2. Herramientas (Tools)
def consultar_mis_pedidos():
    """
    Consulta la lista de todos los pedidos del usuario autenticado.
    """
    global token 
    print("\n[SISTEMA]: Consultando la API de pedidos...")
    url = "http://127.0.0.1:8000/api/pedidos/" 
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
    

def eliminar_pedido(id_pedido: str):
    """
    Elimina un pedido del sistema usando su ID numérico.
    """
    global token
    id_limpio = str(id_pedido).strip() 
    
    print(f"\n[SISTEMA]: Intentando eliminar el pedido ID: {id_limpio}...")
    url = f"http://127.0.0.1:8000/api/pedidos/{id_limpio}/" 
    headers = {"Authorization": f"Bearer {token}"}
    # Se agrega manejo de errores específico para el caso de cuota agotada (429) y se implementa una espera antes de reintentar automáticamente, además de un manejo general de excepciones para otros posibles errores.
    
    try:
        response = requests.delete(url, headers=headers)
        if response.status_code in [200, 204]:
            return {"status": "success", "message": f"Pedido {id_limpio} eliminado correctamente."}
        else:
            return {"status": "error", "detalle": response.json()}
    except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                print("⚠️ IA: Cuota agotada temporalmente.")
                # Extraemos o simplemente esperamos el tiempo recomendado
                print("Esperando 16 segundos para reintentar automáticamente...")
                time.sleep(16)
                # Opcional: podrías relanzar la petición aquí
            else:
                print(f"Ups, ocurrió un error: {e}")


def crear_pedido(producto: str, cantidad: int):
    """
    Crea un nuevo pedido en el sistema. 
    Requiere el nombre del 'producto' (string) y la 'cantidad' (int).
    """
    global token
    print(f"\n[SISTEMA]: Enviando a la API -> Producto: {producto}, Cantidad: {cantidad}")
    
    url = "http://127.0.0.1:8000/api/pedidos/"
    headers = {"Authorization": f"Bearer {token}"}
    
    data = {
        "producto": producto, 
        "cantidad": cantidad
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        if response.status_code in [201, 200]:
            return {"status": "success", "data": response.json()}
        else:
            print(f"❌ Error de validación: {response.json()}")
            return {"status": "error", "detalle": response.json()}
    except Exception as e:
        return {"error": str(e)}

def editar_pedido(id_pedido: str, producto: str = None, cantidad: int = None):
    """
    Actualiza un pedido. REQUIERE id_pedido. 
    Opcional: producto (str) o cantidad (int).
    """
    global token
    try:
        id_final = int(float(str(id_pedido).strip()))
        
        if not producto and cantidad is None:
            return "RESULTADO: ERROR_DATOS_VACIOS"

        url = f"http://127.0.0.1:8000/api/pedidos/{id_final}/"
        headers = {"Authorization": f"Bearer {token}"}
        
        payload = {}
        if producto: payload["producto"] = producto
        if cantidad is not None: payload["cantidad"] = int(cantidad)

        print(f"\n[SISTEMA]: PATCH en ID {id_final}...")
        response = requests.patch(url, json=payload, headers=headers, timeout=5)

        if response.status_code == 200:
            return f"RESULTADO: EXITOSO. El pedido {id_final} fue modificado."
        
        return f"RESULTADO: ERROR_API_CODE_{response.status_code}"

    except Exception as e:
        return f"RESULTADO: ERROR_TECNICO_{str(e)[:20]}"
    # Creacion de herramientas para la IA

# 3. Configuración de la IA

API_KEY = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key = API_KEY)
modelo_id = 'gemini-2.5-flash' 

# 4. Flujo de la lógica
token = login_usuario()
if token:
    print("IA: Hola, veo que has iniciado sesion. ¿Quieres Crear, Editar o Eliminar un pedido?")
    
    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ['salir', 'exit', 'chao', 'bye']:
            break
        
        prompt = (
            f"Contexto: El usuario está autenticado.\n"
            f"Usuario pregunta: {user_input}\n\n"
            "INSTRUCCIONES:\n"
            "1. Ver pedidos: usa 'consultar_mis_pedidos'.\n"
            "2. Eliminar: extrae el ID y usa 'eliminar_pedido'.\n"
            "3. Crear: extrae descripción y cantidad, usa 'crear_pedido'.\n"
            "4. Editar: extrae el ID y los campos a cambiar, usa 'editar_pedido'.\n"
            "5. Si faltan datos para crear o editar, pregunta amigablemente al usuario."
        )
        
        try: 
            response = client.models.generate_content(
                model=modelo_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    # Se agrega las funciones 
                    tools=[
                        consultar_mis_pedidos, 
                        eliminar_pedido, 
                        crear_pedido, 
                        editar_pedido
                    ]
                )
            )
            
            if response.text:
                print(f"IA: {response.text}")
            else:
                print("IA: Procesando solicitud... (Acción completada en el sistema)")

        except Exception as e:
            print(f"Ups, ocurrió un error: {e}")