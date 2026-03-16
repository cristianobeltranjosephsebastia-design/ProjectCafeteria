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

# 3. Configuración de la IA

API_KEY = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key = API_KEY)
modelo_id = 'gemini-2.5-flash' 

# 4. Flujo de la lógica
token = login_usuario()
if token:
    print("IA: Hola, veo que has iniciado sesion. ¿Quieres que te muestre tus pedidos o necesitas eliminar alguno?")
    
    while True:
        user_input = input("\nTu: ")
        if user_input.lower() in ['salir', 'exit', 'chao', 'bye']:
            break
        
        # PROMPT OPTIMIZADO: Ahora incluye instrucciones para ambas herramientas
        prompt = (
            f"Contexto: El usuario está autenticado.\n"
            f"Usuario pregunta: {user_input}\n\n"
            "INSTRUCCIONES:\n"
            "1. Si pide ver pedidos, usa 'consultar_mis_pedidos'.\n"
            "2. Si pide eliminar un pedido, extrae el ID numérico y usa 'eliminar_pedido'.\n"
            "3. Si el resultado es exitoso, confírmalo amigablemente."
        )
        
        try: 
            response = client.models.generate_content(
                model=modelo_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    
                    tools=[consultar_mis_pedidos, eliminar_pedido]
                )
            )
            
            if response.text:
                print(f"IA: {response.text}")
            else:
                print("IA: Procesando solicitud... (Acción completada en el sistema)")

        except Exception as e:
            print(f"Ups, ocurrió un error: {e}")