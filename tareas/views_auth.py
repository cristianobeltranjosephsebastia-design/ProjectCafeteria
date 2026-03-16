import os
import requests
from rest_framework.permissions import AllowAny
from dotenv import load_dotenv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from firebase_admin import auth, firestore
from Cafeteria.firebase_config import firestore
# Inicializamos la base de datos para consultar el perfil
db = firestore.client()
load_dotenv()

class RegistroApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        rol = request.data.get('rol', 'Cliente') # Toma el rol del JSON

        try:
            # creacion del usuario en firebase auth
            user = auth.create_user(email=email, password=password)
            uid = user.uid

            # 2. CREAMOS EL PERFIL EN FIRESTORE (Esto es lo que falta)
            db.collection('perfiles').document(uid).set({
                'email': email,
                'rol': rol,
                'fecha_registro': firestore.SERVER_TIMESTAMP
            })

            return Response({"mensaje": "Usuario y perfil creados ✅"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class LoginApiView(APIView):
    """
    ENDPOINT publico que valida las credenciales y obtiene el JSON web Token de firebase
    """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        api_key = os.getenv('FIREBASE_WEB_API_KEYS')

        if not email or not password:
            return Response({"Error": "Faltan credenciales"}, status = status.HTTP_400_BAD_REQUEST)

        #Endpoint oficial de google

        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"

        payload = {
            "email" : email,
            "password" : password,
            "returnSecureToken" : True
        }

        try:
            response = requests.post(url, json= payload)
            data = response.json()  

            if response.status_code == 200:
                return Response ({
                "Mensaje": "Login Exitoso✅",
                "token" : data['idToken'],
                "uid" : data['localId']
                }, status = status.HTTP_200_OK)
            else:
                error_msg = data.get('error', {}).get('message', 'error desconocido')
                return Response (
                    {'error':{error_msg}}, status = status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'error de conexion'}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)