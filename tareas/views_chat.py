from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .authentication import FirebaseAuthentication
from Cafeteria.firebase_config import initialize_firebase

db = initialize_firebase()

class ChatHistorialAPIView(APIView):
    authentication_classes = [FirebaseAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        Devuelve los ultimos 20 mensajes del chat principal
        """
        try:
            mensaje_ref = db.collection('api_chat_mensajes')\
                        .order_by('timestamp',direction='DESCENDING')\
                        .limit(20)\
                        .stream()
            historial = []
            for doc in mensaje_ref:
                data = doc.to_dict()
                historial.append({
                    "id": doc.id,
                    "usuario" : data.get("uid_usuario", "anonimo"),
                    "mensaje": data.get("mensaje", ""),
                    "timestamp": data.get("timestamp")
                })
            historial.reverse() 
            return Response(historial, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

