from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from firebase_admin import auth
import firebase_admin
from Cafeteria.firebase_config import initialize_firebase

# Base de datos
db = initialize_firebase()

class FirebaseAuthentication(BaseAuthentication):
    """
    Lee el token JWT del encabezado, lo valida en Firebase y extrae el rol 
    desde la colección 'perfiles' de Firestore.
    """

    def authenticate(self, request):

        auth_header = request.META.get('HTTP_AUTHORIZATION') or request.headers.get('Authorization')
        if not auth_header:
            return None

        partes = auth_header.split()
        # Validación del formato "Bearer <token>"
        if len(partes) != 2 or partes[0].lower() != 'bearer':
            return None
            
        token = partes[1]

        try:
            
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token.get('uid')
            email = decoded_token.get('email')
            user_profile = db.collection('perfiles').document(uid).get()
            
            if user_profile.exists:
                rol = user_profile.to_dict().get('rol', 'Cliente')
            else:
                rol = 'Cliente'

            class FirebaseUser:
                def __init__(self, uid, rol, email):
                    self.uid = uid
                    self.rol = rol
                    self.email = email
                    self.is_authenticated = True

            
            return (FirebaseUser(uid, rol, email), decoded_token)

        except Exception as e:
            
            raise AuthenticationFailed(f"Token no es válido o está expirado: {str(e)}")